import json

from django.conf import settings
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView


class OdooApi(APIView):
    """
    List all code snippets, or create a new snippet.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, service_path, format=None):
        return Response(
            json.dumps({'service_path': service_path}))

    def post(self, request, service_path, format=None):
        user = request.user
        data = request.data
        res = {
            'path': service_path,
            'request': data,
            'user': user.get_username(),
            'email': user.email,
            'odoo_api_key': settings.ODOO_API_KEY,
        }
        return Response(res)
