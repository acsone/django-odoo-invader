.. image:: https://img.shields.io/badge/licence-MIT-blue.svg
   :target: http://opensource.org/licenses/MIT
   :alt: MIT

==================================
Django Odoo Invader Services Proxy
==================================

Add a new generic restfull view to be used as proxy to call resfull services
on Odoo provided by the base_invader service gateway addon.

Installation
============

At this stage, the module is only available from source. You can use ``pip``
to install ``django-odoo-invader`` and its dependencies:

.. code-block:: console

    $ pip install -e 'git+https://github.com/django-odoo-invader.git@master#egg=django-odoo-invader

Once released, you all be able to nstall from PyPI_ using ``pip`` to install
``django-odoo-invader`` and its dependencies:

.. code-block:: console

    $ pip install django-odoo-invader

Setup
-----

Add the following apps to the ``INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'odoo_invader.apps.OdooInvaderConfig',
    )


Add the routes to your project url configuration:

.. code-block:: python

    from django.urls import path
    urlpatterns = [
       # the proxy will be available at /odoo_api/<path:service_path>
       path('', include('odoo_invader.urls')),
        ...
    ]

Point to the odoo base_invader service url in your ``settings.py`` and specify
the api key:

.. code-block:: python

    # this one must be the same as the value configured into Odoo
    ODOO_API_KEY = 'a_secured_api_key'

    # this one is optional
    ODOO_API_URL = 'http://localhost:8069/invader'


Configuration
=============

Permission Settings
--------------------

  .. warning::
     If you need to adapt the permissions, you must put these settings at the
     end of the  ``settings.py`` file since the import `from rest_framework
     import permissions` will fails if the ``SECRET_KEY`` is not yet defined.


``ODOO_API_PERMISSION_CLASSES`` (default: (permissions.IsAuthenticated,))
  By default only authenticated users are allowed to access to the proxy.

``ODOO_API_SERVICE_PATH_PERMISSION_CLASSES`` (default: [])
  This setting allows you to define custom permission_classes by service_path.
  Each entry must be a two values tuple. The first one must be an instance of
  `django.urls.resolvers.RegexPattern` or `django.urls.resolvers.RoutePattern`
  The second value must be a dict where key is the name of the HTTP method to
  which the permission applies (POST, GET, ...) and the value the list of
  permissions to check. When checking for the permission, we first look into
  ``ODOO_API_SERVICE_PATH_PERMISSION_CLASSES`` if a pattern match with the
  `service_path` arg of the odoo_api service. If no match if found, the
  permission is checked against ``ODOO_API_PERMISSION_CLASSES`` If an entry is
  found we get the permissions from the dict for the HTTP method. If a value
  is found the permission is checked against the given list of permission
  otherwise against ``ODOO_API_PERMISSION_CLASSES``.

.. code-block:: python

    ...
    from django.urls.resolvers import RoutePattern
    from rest_framework import permissions
    ODOO_API_SERVICE_PATH_PERMISSION_CLASSES = [
      RoutePattern('partner/<int:id>'), {
        'GET': (permissions.AllowAny,),
        'POST': (permissions.IsAuthenticated,),
        'DEL': (permissions.IsAdminUser,),
      }
    ]

Credits
=======

Contributors
------------

* Laurent Mignon <laurent.mignon@acsone.eu>

Maintainer
----------

.. image:: https://www.acsone.eu/logo.png
   :alt: ACSONE SA/NV
   :target: http://www.acsone.eu

This module is maintained by ACSONE SA/NV.

.. _PyPI: https://pypi.python.org/pypi/django-odoo-invader