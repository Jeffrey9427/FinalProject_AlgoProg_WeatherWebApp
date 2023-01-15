from django.urls import path
from .views import index, about, aqi, forecast

urlpatterns = [
    path('', index, name='index'),                 # Home page        
    path('about', about, name='about'),            # Page showing details of the web app         
    path('aqi', aqi, name='aqi'),                  # Page showing AQI and Weather of a city 
    path('forecast', forecast, name='forecast')    # Page showing weather forecast of a city          
]