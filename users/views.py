from django.shortcuts import render, redirect     # django.shortcuts module's used for rendering templates and redirecting the user to different pages respectively
from django.urls import reverse                   # django.urls module's reverse function for reversing URL pattern for redirection
from django.contrib import messages               # django.contrib module's used for storing messages to be displayed to the user

from django.contrib.auth import authenticate, login, logout     # django.contrib.auth module's used for authenticating a user, logging a user and logging out a user

from .forms import CreateUserForm

# function to handle user login requests
def loginPage(request):
    if request.user.is_authenticated:                   # if user is already authenticated, will be redirected to index page
        return redirect(reverse('weatherapp:index'))
    else: 
        if request.method == "POST": 
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)      # call the authenticate method to check the credentials

            if user is not None: 
                login(request, username)     
                return redirect(reverse('weatherapp:index'))        # an user will be redirected to index page if authenticated
            else: 
                messages.info(request, 'Username OR password is incorect')      # shows message if credentials do not match

        context = {}
        return render(request, 'users/login.html', context)

# function to handle user logout requests
def logoutUser(request): 
    logout(request)
    return redirect(reverse('index'))

# function to handle user registration requests 
def register(request):
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    else: 
        form = CreateUserForm()       # create a form object of CreateUserForm
        if request.method == 'POST':
            form = CreateUserForm(request.POST)    
            if form.is_valid():       # check if the data is valid 
                form.save()           # saves the new user to the database
                user = form.cleaned_data.get('username')
                # show a success message and redirect the user to login page
                messages.success(request, 'Account was created for ' + user)    
                return redirect(reverse('users:login'))

    context = {'form': form}
    return render(request, 'users/register.html', context)