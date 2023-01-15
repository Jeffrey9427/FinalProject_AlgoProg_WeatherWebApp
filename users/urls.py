from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('login', LoginView.as_view(template_name='users/login.html'), name='login'),            # Login page
 
    path('logout', views.logoutUser, name='logout'),                # Log out page

    path('register', views.register, name='register'),                   # Register page
]