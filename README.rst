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

In your settings add:

 * ODOO_API_KEY: The value must be the same as the one configured in Odoo on the
   base_invader backend.
 * ODOO_API_URL: The url if the service endpoint provided by base_invader

The django proxy is available at /odoo_api

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
