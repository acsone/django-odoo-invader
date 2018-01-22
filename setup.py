
from setuptools import find_packages, setup

setup(
    name='django-odoo-invader',
    version='1.0.0',
    description='Restfull proxy for Odoo services',
    long_description=open('README.rst').read(),
    author='Laurent Mignon',
    author_email='laurent.mignon@acsone.eu',
    url='https://github.com/acsone/django-odoo-invader',
    download_url='https://pypi.python.org/pypi/django-odoo-invader',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'Django',
        'djangorestframework',
        'requests',
    ],
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
