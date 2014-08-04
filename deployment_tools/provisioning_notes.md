Provisioning a new site
=======================

## Required packages:

* nginx
* Python 3
* Git
* pip
* pyvenv-3

on Ubuntu:
    sudo apt-get install nginx git python3 python3-pip

## Nginx Virtual Host config

* see nginx.template.conf
* replace SITENAME with eg. staging.my-domain.com
* replace other placeholders with descriptive names.

## Upstart Job

* see gunicorn-upstart.template.conf
* replace SITENAME with eg. staging.my-domain.com
* replace other placeholders with descriptive names.

## Folder structure:

    /srv
    └── SITENAME
        ├── database
        ├── source
        │   ├── deployment_tools
        │   ├── functional_tests
        │   ├── lists
        │   │   ├── migrations
        │   │   ├── static
        │   │   └── templates
        │   └── superlists
        ├── static
        │   └── bootstrap
        │       ├── css
        │       ├── fonts
        │       └── js
        └── venv
            └── SITENAME
                ├── bin
                ├── include
                ├── lib
                └── share
