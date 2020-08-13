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



## User Login

`account/forms.py`

```python
from django import forms

class LoginView(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
```

`account/views.py`

```python
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

# Import from project
from .forms import LoginForm


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user) # Set the user in the session by calling the login() method.
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Account is disabled, contact to administrator')
            else:
                return HttpResponse('Invalid Login, No User Exist')
    else:
        form = LoginForm()
    
    return render(request, 'account/login.html', {'form': form})
```

`account/urls.py`

```python
from django.urls import path

# Import from project
from .import views

urlpatterns = [
    path('login/', views.user_login, name='login'), 
]
```

`bookmarks/urls.py`

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
]
```

**Templates and Static Files**

Create a tree structure like below under `account` directory.

```htm
templates/
	static/
		css/
		js/
    account/
        login.html
    base.html
```

`account ---> login.html`

```html
{% extends "base.html" %}
{% block title %}Log-in{% endblock %}
{% block content %}
  <h1>Log-in</h1>
  <p>Please, use the following form to log-in:</p>
  <form method="post">
    {{ form.as_p }}
    {% csrf_token %}
    <p><input type="submit" value="Log in"></p>
  </form>
{% endblock %}
```



