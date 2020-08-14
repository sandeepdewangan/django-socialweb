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



## Using Authentication Framework

### User Login and Logout

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
		password_change_form.html
		password_change_done.html
		password_reset_form.html
		password_reset_email.html
		password_reset_done.html
		password_reset_confirm.html
		password_reset_complete.html
```

**NOTE:** Make sure the account app should be placed at the top of the `INSTALLED_APPS` settings, so that Django use our templates by default.

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
  



### Change Password Views

`account/urls.py`

```python
path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
```

`password_change_form.html`  - see above directory structure.

```html
{% extends "base.html" %}
{% block title %}Change your password{% endblock %}
{% block content %}
  <h1>Change your password</h1>
  <p>Use the form below to change your password.</p>
  <form method="post">
    {{ form.as_p }}
    <p><input type="submit" value="Change"></p>
    {% csrf_token %}
  </form>
{% endblock %}
```

`password_change_done.html`

```html
{% extends "base.html" %}
{% block title %}Password changed{% endblock %}
{% block content %}
  <h1>Password changed</h1>
  <p>Your password has been successfully changed.</p>
{% endblock %}
```



### Password Reset

`account/urls.py`

```python
# reset password urls
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
```

`password_reset_form.html`

```html
{% extends "base.html" %}
{% block title %}Reset your password{% endblock %}
{% block content %}
  <h1>Forgotten your password?</h1>
  <p>Enter your e-mail address to obtain a new password.</p>
  <form method="post">
    {{ form.as_p }}
    <p><input type="submit" value="Send e-mail"></p>
    {% csrf_token %}
  </form>
{% endblock %}
```

`password_reset_email.html`

The password_reset_email.html template will be used to render the email sent to users to reset their password.

```html
Someone asked for password reset for email {{ email }}. 
Follow the link below:

{{ protocol }}://{{ domain }}{% url "password_reset_confirm" uidb64=uid token=token %}
Your username, in case you've forgotten: {{ user.get_username }}
```

`password_reset_done.html`

```html
{% extends "base.html" %}
{% block title %}Reset your password{% endblock %}
{% block content %}
  <h1>Reset your password</h1>
  <p>We've emailed you instructions for setting your password.</p>
  <p>If you don't receive an email, please make sure you've entered the address you registered with.</p>
{% endblock %}
```

`password_reset_confirm.html`

```html
{% extends "base.html" %}
{% block title %}Reset your password{% endblock %}
{% block content %}
  <h1>Reset your password</h1>
  {% if validlink %}
    <p>Please enter your new password twice:</p>
    <form method="post">
      {{ form.as_p }}
      {% csrf_token %}
      <p><input type="submit" value="Change my password" /></p>
    </form>
  {% else %}
    <p>The password reset link was invalid, possibly because it has already been used. Please request a new password reset.</p>
  {% endif %}
{% endblock %}
```

`password_reset_complete.html`

```html
{% block title %}Password reset{% endblock %}
{% block content %}
  <h1>Password set</h1>
  <p>Your password has been set. You can <a href="{% url "login" %}">log in now</a></p>
{% endblock %}
```

Edit `registration/login.html`

```html
<p><a href="{% url "password_reset" %}">Forgotten your password?</a></p>
```



**For this we need to add a Simple Mail Transfer Protocol (SMTP) configuration to the settings.py file of your project so that Django is able to send emails.** For this reference [Django Book](Chapter 2, Enhancing Your Blog with Advanced Features.) : <mark>TODO</mark>

However, during development, you can configure Django to write emails to the standard output instead of sending them through an SMTP server. Django provides an email backend to write emails to the console. Edit the `settings.py` file of your project, and add the following line:

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

