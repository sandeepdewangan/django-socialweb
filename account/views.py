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