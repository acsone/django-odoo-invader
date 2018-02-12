# Copyright 2018 ACSONE SA/NV
import urllib.parse

import requests
from django.conf import settings
from django.http import HttpResponse
from django.utils.translation import to_locale
from rest_framework import permissions
from rest_framework.views import APIView

_ODOO_SESSION = None


class OdooApi(APIView):
    """
    Forward restfull calls to Odoo
    """

    @property
    def odoo_session(self):
        global _ODOO_SESSION
        if not _ODOO_SESSION:
            _ODOO_SESSION = requests.Session()
            _ODOO_SESSION.headers['API-KEY'] = settings.ODOO_API_KEY
        return _ODOO_SESSION

    def _get_lang(self, request):
        if 'HTTP_ACCEPT_LANGUAGE' in request.META:
            return to_locale(
                request.META['HTTP_ACCEPT_LANGUAGE'].split(',')[0])
        return None

    def _get_headers(self, request):
        """
        Retrieve the HTTP headers from a WSGI environment dictionary.
        """
        headers = {}
        for key, value in request.META.items():
            if key.startswith('HTTP_') and key != 'HTTP_HOST':
                headers[key[5:].replace('_', '-')] = value
            elif key in ('CONTENT_TYPE', 'CONTENT_LENGTH') and value:
                headers[key.replace('_', '-')] = value

        if request.user:
            headers['PARTNER-EMAIL'] = request.user.email
        lang = self._get_lang(request)
        if lang:
            headers['LANG'] = lang
        return headers

    def _formward_method_to_odoo(self, request, service_path):
        session = self.odoo_session
        odoo_api_url = settings.ODOO_API_URL
        if not odoo_api_url.endswith('/'):
            odoo_api_url = odoo_api_url + '/'

        service_url = urllib.parse.urljoin(odoo_api_url, service_path)
        odoo_response = session.request(
            request.method,
            service_url,
            headers=self._get_headers(request),
            data=request.data,
            params=request.query_params
        )

        response = HttpResponse(
            odoo_response.content,
            status=odoo_response.status_code
        )
        excluded_headers = set([
            # filter message headers to not forward.
            # http://www.w3.org/Protocols/rfc2616/rfc2616-sec13.html#sec13.5.1
            'connection', 'keep-alive', 'proxy-authenticate',
            'proxy-authorization', 'te', 'trailers', 'transfer-encoding',
            'upgrade',
        ])
        for key, value in odoo_response.headers.items():
            if key.lower() in excluded_headers:
                continue
            response[key] = value
        return response

    def get(self, request, service_path, format=None):
        return self._formward_method_to_odoo(request, service_path)

    def post(self, request, service_path, format=None):
        return self._formward_method_to_odoo(request, service_path)

    def put(self, request, service_path, format=None):
        return self._formward_method_to_odoo(request, service_path)

    def delete(self, request, service_path, format=None):
        return self._formward_method_to_odoo(request, service_path)

    def initial(self, request, *args, **kwargs):
        """
        Runs anything that needs to occur prior to calling the method handler.
        """
        super(OdooApi, self).initial(request, *args, **kwargs)
        self.check_service_permission(request, kwargs.get('service_path'))

    def get_service_permissions(self, request, service_path):
        """
        Instantiates and returns the list of permissions that the requested
        odoo service requires.
        """

        service_path_permission_classes = getattr(
            settings,
            'ODOO_API_SERVICE_PATH_PERMISSION_CLASSES',
            {}
        )
        permission_classes = None
        for pattern, perms in service_path_permission_classes.items():
            if pattern.match(service_path):
                permission_classes = perms.get(request.method.upper())
                break
        permission_classes = permission_classes or getattr(
            settings,
            'ODOO_API_PERMISSION_CLASSES',
            (permissions.IsAuthenticated,))
        return [permission() for permission in permission_classes]

    def check_service_permission(self, request, service_path=None):
        """
        Check if the request should be permitted for the requested Odoo
        service.
        Raises an appropriate exception if the request is not permitted.
        """
        for permission in self.get_service_permissions(request, service_path):
            if not permission.has_permission(request, self):
                self.permission_denied(
                    request, message=getattr(permission, 'message', None)
                )
