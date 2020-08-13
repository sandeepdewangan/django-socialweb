# Social Web Site

Table of Contents

[TOC]

## Project Setup

Start Project

`django-admin startproject bookmarks`

Start App

`django-admin startapp account`

Place it in the INSTALLED_APPS in `settings.py`

```python
INSTALLED_APPS = [
    'bookmarks.apps.AccountConfig', # bookmark application
	....
]
```

Migrate

`python manage.py makemigrations app_name`

`python manage.py migrate`



## Authentication Framework

Django comes with a built-in authentication framework that can handle user authentication, sessions, permissions, and user groups. The authentication framework is located at `django.contrib.auth` and is used by other Django `contrib` packages.

It consists of the `django.contrib.auth`application and the following two middleware classes found in the MIDDLEWARE setting of your project: 

* AuthenticationMiddleware: Associates users with requests using sessions 
* SessionMiddleware: Handles the current session across requests

Middleware are classes with methods that are globally executed during the request or response phase.



## Login View

