# Social Website
# 

Table of Contents

[TOC]

# Bookmark Module

## Left Overs

1. Adding social authentication to your site


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



## User Registration and User Profiles

### User Registration

Initially, we will create a form to let the user enter a username, their real name, and a password.

`account/forms.py`

```python
from django.contrib.auth.models import User
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
        
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
```

`account/views.py`

```python
from .forms import LoginForm, UserRegistrationForm
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})
```

Instead of saving the raw password entered by the user, you use the `set_password()` method of the user model that handles hashing.

`account/urls.py`

```python
path('register/', views.register, name='register'),
```

`account/register.html`

```html
{% extends "base.html" %}
{% block title %}Create an account{% endblock %}
{% block content %}
  <h1>Create an account</h1>
  <p>Please, sign up using the following form:</p>
  <form method="post">
    {{ user_form.as_p }}
    {% csrf_token %}
    <p><input type="submit" value="Create my account"></p>
  </form>
{% endblock %}
```

`account/register_done.html`

```python
{% extends "base.html" %}
{% block title %}Welcome{% endblock %}
{% block content %}
  <h1>Welcome {{ new_user.first_name }}!</h1>
  <p>Your account has been successfully created. Now you can <a href="{% url "login" %}">log in</a>.</p>
{% endblock %}
```



### Extending User Model  (Profiles)

The best way to extend user is by creating a profile model that contains all additional fields and a one-to-one relationship with the Django User model.

`account/models.py`

```python
from django.conf import settings
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    
    def __str__(self):
        return f'Profile for user {self.user.username}'
```

The `get_user_model()` method to retrieve the user model and the `AUTH_USER_MODEL` setting to refer to it when defining a model's relationship with the user model, instead of referring to the auth user model directly.

The photo field is an ImageField field. You will need to install the Pillow library to handle images. Install Pillow by running the following command in your shell:

`pip install Pillow==7.0.`

To enable Django to serve media files uploaded by users with the development server, add the following settings to the settings.py file of your project:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
```

`MEDIA_URL` is the base URL used to serve the media files uploaded by users, and `MEDIA_ROOT` is the local path where they reside. You build the path dynamically relative to your project path to make your code more generic.

`bookmarks/urls.py`

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
```

**NOTE**: The `static()` helper function is suitable for development, but not for production use. Django is very inefficient at serving static files. Never serve your static files with Django in a production environment. <mark> You will learn how to serve static files in a production environment in Chapter 14, Going Live. TODO </mark>

`account/admin.py`

```python
from .models import Profile
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']
```

### User Profile Edit

`account/forms.py`

```python
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')
```

When users register on your site, you will create an empty profile associated with them.

```python
Profile.objects.create(user=new_user)
```

`account/views.py`

```python
@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm( instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
									
	return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})
```

`account/urls.py`

```python
path('edit/', views.edit, name='edit'),
```

`templates/account/edit.html`

```html
{% extends "base.html" %}
{% block title %}Edit your account{% endblock %}
{% block content %}
  <h1>Edit your account</h1>
  <p>You can edit your account using the following form:</p>
  <form method="post" enctype="multipart/form-data">
    {{ user_form.as_p }}
    {{ profile_form.as_p }}
    {% csrf_token %}
    <p><input type="submit" value="Save changes"></p>
  </form>
{% endblock %}
```

## Messages Framework

When allowing users to interact with your platform, there are many cases where you might want to inform them about the result of their actions. Django has a built-in messages framework that allows you to display one-time notifications to your users.

The messages framework is located at `django.contrib.messages` and is included in the default `INSTALLED_APPS`
Messages are stored in a cookie by default (falling back to session storage), and they are displayed in the next request from the user.

**Usage**

```python
from django.contrib import messages
messages.error(request, 'Something went wrong')
```

* success()
* info()
* warning()
* error()
* debug()

The messages framework includes the context processor `django.contrib.messages.context_processors.messages`, which adds a messages variable to the request context. You can find it in the `context_processors` list of the TEMPLATES setting of your project. You can use the messages variable in your templates to display all existing messages to the user.

`base.html`

```python
{# Message Framework #}
{% if messages %}
  <ul class="messages">
    {% for message in messages %}
      <li class="{{ message.tags }}">
        {{ message|safe }}
        <a href="#" class="close">x</a>
      </li>
    {% endfor %}
  </ul>
{% endif %}
```

**NOTE**: A context processor is a Python function that takes the request object as an argument and returns a dictionary that gets added to the request context.

 <mark> You will learn how to create your own context processors in Chapter 7, Building an Online Shop. TODO </mark>

`account/views.py`

```python
from django.contrib import messages
@login_required
def edit(request):
    if request.method == 'POST':
        # ....
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully') # <---- NEW
        else:
            messages.error(request, 'Error updating your profile') # <---- NEW
	# ...
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})
```



## Custom Authentication Backend

Django allows you to authenticate against different sources. The `AUTHENTICATION_BACKENDS` setting includes the list of authentication backends for your project. By default, this setting is set as follows: `['django.contrib.auth.backends.ModelBackend']`
The default `ModelBackend` authenticates users against the database using the user model of `django.contrib.auth`. This will suit most of your projects. However, you can create custom backends to authenticate your user against other sources, such as a Lightweight Directory Access Protocol (LDAP) directory or any other system.

Django provides a simple way to define your own authentication backends. An authentication backend is a class that provides the following two methods: 

* `authenticate()`: It takes the request object and user credentials as parameters. It has to return a user object that matches those credentials if the credentials are valid, or None otherwise. The request parameter is an HttpRequest object, or None if it's not provided to authenticate(). 

* `get_user()`: This takes a user ID parameter and has to return a user object.

Example

```python
from django.contrib.auth.models import User
class EmailAuthBackend(object):
    """
    Authenticate using an e-mail address.
    """
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
```

`settings.py`

```python
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'account.authentication.EmailAuthBackend', # <-- CUSTOM Backend
]
```

Remember that Django will try to authenticate the user against each of the backends, so now you should be able to log in seamlessly using your username or email account. User credentials will be checked using the `ModelBackend` authentication backend, and if no user is returned, the credentials will be checked using your custom `EmailAuthBackend` backend.

## Social Authentication

Install package

`pip install social-auth-app-django==3.1.0`

Then add `social_django` to the INSTALLED_APPS setting in the settings.py file of your project:

```python
INSTALLED_APPS = [
    #...
    'social_django',
]
```

Then migrate

`python manage.py migrate`

`bookmark/urls.py`

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('social-auth/', include('social_django.urls', namespace='social')), # New
]
```

Several social services will not allow redirecting users to 127.0.0.1 or localhost after a successful authentication; they expect a domain name.
In order to make social authentication work, you will need a domain. To fix this on Linux or macOS, edit your /etc/hosts file and add the following line to it: 

```ini
127.0.0.1 mysite.com
```

This will tell your computer to point the mysite.com hostname to your own machine. If you are using Windows, your hosts file is located at C:\Windows\System32\Drivers\etc\hosts.

Edit the settings.py file of your project and edit the `ALLOWED_HOSTS` setting as follows:

```python
ALLOWED_HOSTS = ['mysite.com', 'localhost', '127.0.0.1']
```

<mark>TODO</mark>

# Images Modules



