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



## User Login Using Custom Forms

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



## Authentication Views

Django includes several forms and views in the authentication framework that you can use right away.

It provide class based views to deal with authentication. All of them are located in `django.contrib.auth.views`.

* LoginView
* LogoutView
* PasswordChangeView
* PasswordChangeDoneView
* PasswordResetView
* PasswordResetDoneView
* PasswordResetConfirmView
* PasswordResetCompleteView



## User Login and Logout Using Authentication Framework

`account/urls.py`

```python
from django.urls import path
from django.contrib.auth import views as auth_views
# Import from project
from .import views

urlpatterns = [
    # login view - handling forms by us
    #path('login/', views.user_login, name='login'),
     # login view - handling forms by django auth framework
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LoginView.as_view(), name='logout'),
]
```

Default path where Django views expect templates to be is

```html
templates/
	registration/
		login.html
		logged_out.html
```

<mark>**NOTE:** </mark>Make sure the account app should be placed at the top of the `INSTALLED_APPS` settings, so that Django use our templates by default.

`login.html`

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

`logged_out.html`

```html
{% extends 'base.html' %}
{% block content %}
    <h1>Logged Out </h1>
    You have been successfully logged out.
    You can <a href="{% url 'login' %}">login</a>again.
{% endblock content %}

```

`account/views.py`

```python
from django.contrib.auth.decorators import login_required
@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html')
```

`templates/account/dashboard.html`

```html
{% extends 'base.html' %}
{% block content %}
    <h1>Dashboard</h1>
{% endblock content %}
```

`account/urls.py`

```python
urlpatterns = [
	#.....
    path('', views.dashboard, name='dashboard'),
]
```

`settings.py`

```python
LOGIN_REDIRECT_URL = 'dashboard'
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
```



### HttpRequest

* The current user information is set in the `HttpRequest` object by the authentication middleware. 

* We can access it by `request.user` 

* The non authenticated user object is `AnonymousUser` 

* Best way to check the current user is authentication is by accessing the read only attribute `is_authenticated```

  
  
  `base.html`
  
  ```html
  <div id="header">
    <span class="logo">Bookmarks</span>
    {% if request.user.is_authenticated %}
      <ul class="menu">
        <li {% if section == "dashboard" %}class="selected"{% endif %}>
          <a href="{% url "dashboard" %}">My dashboard</a>
        </li>
        <li {% if section == "images" %}class="selected"{% endif %}>
          <a href="#">Images</a>
        </li>
        <li {% if section == "people" %}class="selected"{% endif %}>
          <a href="#">People</a>
        </li>
      </ul>
    {% endif %}
    <span class="user">
      {% if request.user.is_authenticated %}
        Hello {{ request.user.first_name }},
        <a href="{% url "logout" %}">Logout</a>
      {% else %}
        <a href="{% url "login" %}">Log-in</a>
  	  {% endif %}
    </span>
  </div>
  ```
  
  
  
  
  
  



