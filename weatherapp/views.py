import json                                                     # module that allows to work with JSON data / data interchange on the web
import requests                                                 # python library that allows to send HTTP requests (weather API) and handle the response and data
from django.shortcuts import render                             # part of the Django web framework to handle shortcuts for rendering views and redirecting users
from datetime import datetime                                   # part of Python standard library to work with date and time values 
import pytz                                                     # module that provide timezone-related functionality
from django.contrib.auth.decorators import login_required       # part of Django framework to handle user authentication and authorization
import pandas as pd                                             # data manipulation library to manipulate the data retrieved from the weather API
import plotly.express as px                                     # module to create interactive visualizations of the weather data
from plotly.offline import plot                                 # module to create interactive visualizations of the weather data

# class created for making requests to air quality API and retrieve data from it 
class AirVisualAPI:
    # initialize an object's state that store my api key           
    def __init__(self):                 
        self.api_key = "1bc7b8c0-9a65-4935-a911-42dffefbe512"                   
    
    # defining a method for getting states available that takes in country argument
    def get_states(self, country):                                      
        states = []                                                            
        state_available_api_request = requests.get("http://api.airvisual.com/v2/states?country=" + country + "&key=" + self.api_key)    # make a GET request to the API
        try: 
            state_api = json.loads(state_available_api_request.content)        # parse the API Call JSON response to a string and returns a Python object
            if state_api['status'] == "success":
                for state in state_api['data']:
                    states.append(state['state'])         # list out all the states available for the given country
        except Exception as e:
            state_api = "Error..."
        return state_api, states            # return two values 'state_api' and 'states'
    
    # defining a method for getting cities available that takes in country and state argument
    def get_cities(self, country, state):
        cities = []
        city_available_api_request = requests.get("http://api.airvisual.com/v2/cities?state=" + state + "&country=" + country + "&key=" + self.api_key)    # make a GET request to the API
        try:
            city_api = json.loads(city_available_api_request.content)          # parse the API Call JSON response to a string and returns a Python dictionary
            if city_api['status'] == "success":
                for city in city_api['data']:
                    cities.append(city['city'])     # list out all the cities available for the given country and state
        except Exception as e:
            city_api = "Error..."
        return city_api, cities      # return two values 'city_api' and 'cities'
    
    # defining a method for retrieving aqi json dictionary for a specific city, state, country 
    def get_aqi(self, country, state, city):
        city_aqi_api_request = requests.get("http://api.airvisual.com/v2/city?city=" + city + "&state=" + state + "&country=" + country + "&key=" + self.api_key)   # make a GET request to the API
        try:
            city_aqi_api = json.loads(city_aqi_api_request.content)       # parse the API Call JSON response to a string and returns a Python dictionary
        except Exception as e:
            city_aqi_api = "Error..."
        return city_aqi_api         # return python dictionary containing aqi data 

# class created for processing all the aqi data retrieved from airvisual API
class AQIProcessor:
    # initializes an attribute that is assigned the response from the AirVisual API
    def __init__(self, city_aqi_api):
        self.city_aqi_api = city_aqi_api

    # defining a method for determining the category, color, and description of the AQI based on the AQI value.
    def process_aqi(self):
        aqi_categories = {          # create a dictionary that maps AQI ranges to AQI categories, category colors, and descriptions. 
        (0, 50): ("Good", "good", "(0-50) Air quality is considered satisfactory, and air pollution poses little or no risk."),
        (51, 100): ("Moderate", "moderate", "(51-100) Air quality is acceptable. However, there may be a risk for some people, particularly those who are unusually sensitive to air pollution."),
        (101, 150): ("Unhealthy for Sensitive Group", "usg", "(101-150) Members of sensitive groups may experience health effects. The general public is less likely to be affected."),
        (151, 200): ("Unhealthy", "unhealthy", "(151-200) Some members of the general public may experience health effects; members of sensitive groups may experience more serious health effects."),
        (201, 300): ("Very Unhealthy", "veryunhealthy", "(201-300) Health alert: The risk of health effects is increased for everyone."),
        (301, 500): ("Hazardous", "hazardous", "(301-500) Health warning of emergency conditions: everyone is more likely to be affected."),
        }

        if self.city_aqi_api['status'] == 'success':
            aqi = self.city_aqi_api['data']['current']['pollution']['aqius']
            for aqi_range, (category, category_color, category_description) in aqi_categories.items():
                if aqi_range[0] <= aqi <= aqi_range[1]:
                    return category, category_color, category_description, aqi
        return "", "", "", ""      # returns an empty tuple if the API request is not successful or aqi value is not found in any of the range
    
    # defining a method for retrieving the weather conditions for the specific city 
    def weather_condition(self):
        if self.city_aqi_api['status'] == 'success':
            temperature = self.city_aqi_api['data']['current']['weather']['tp']
            pressure = self.city_aqi_api['data']['current']['weather']['pr']
            humidity = self.city_aqi_api['data']['current']['weather']['hu']
            wind_speed = self.city_aqi_api['data']['current']['weather']['ws']
            climate_icons = self.city_aqi_api['data']['current']['weather']['ic']
            climate_dict = {         # create a dictionary that stores the description of climate_icons and the icon path
                "01d" : ("Clear Sky", "images/01d.png"),
                "01n" : ("Clear Sky", "images/01n.png"),
                "02d" : ("Few Clouds", "images/02d.png"),
                "02n" : ("Few Clouds", 'images/02n.png'),
                "03d" : ("Scattered Clouds", "images/03d.png"),
                "03n" : ("Scattered Clouds", "images/03d.png"),
                "04d" : ("Broken Clouds", "images/04d.png"),
                "04n" : ("Broken Clouds", "images/04d.png"),
                "09d" : ("Shower Rain", "images/09d.png"),
                "09n" : ("Shower Rain", "images/09d.png"),
                "10d" : ("Rain", "images/10d.png"),
                "10n" : ("Rain", "images/10n.png"),
                "11d" : ("Thunderstorm", "images/11d.png"),
                "11n" : ("Thunderstorm", "images/11d.png"),
                "13d" : ("Snow", "images/13d.png"),
                "13n" : ("Snow", "images/13d.png"),
                "50d" : ("Mist", "images/50d.png"),
                "50n" : ("Mist", "images/50d.png"),
            }
            for icons, (climate, icon_link) in climate_dict.items():
                if climate_icons == icons:
                    return temperature, pressure, humidity, wind_speed, climate, icon_link
        return "", "", "", "", "", ""      # returns an empty tuple if the API request is not successful or icon is not found in any of the dictionary

# function to handle requests made and returns index.html template to the client to be rendered
def index(request):
    return render(request, 'weatherapp/index.html', {})

# decorator to check whether the user is logged in, and if not, redirects the user to login_url
@login_required(login_url='users/login')
# function to handle requests made and returns about.html template to the client to be rendered
def about(request):
    airvisual = AirVisualAPI()     # create an instance of AirVisualAPI class
    if request.method == "POST":
        if 'find-state' in request.POST:     # if find-state button is pressed, return the states and state_api
            country = request.POST['country-for-state']
            state_api, states = airvisual.get_states(country)       
            return render(request, 'weatherapp/about.html', {'state_api': state_api, 'states': states})
        elif 'find-city' in request.POST:   # if find-city button is pressed, return the cities and city_api
            country = request.POST['country-for-city']
            state = request.POST['state']   
            city_api, cities = airvisual.get_cities(country, state)
            return render(request, 'weatherapp/about.html', {'city_api': city_api, 'cities': cities})
    return render(request, 'weatherapp/about.html', {})     # returns an empty context data if request method is not POST

# decorator to check whether the user is logged in, and if not, redirects the user to login_url
@login_required(login_url='users/login')
# function to handle requests made and returns about.html template to the client to be rendered
def aqi(request):
    airvisual = AirVisualAPI()      # create an instance of AirVisualAPI class
    if request.method == "POST":    
        country = request.POST['country-aqi']
        state = request.POST['state-aqi']
        city = request.POST['city-aqi']
        city_aqi_api = airvisual.get_aqi(country, state, city)    # get AQI data by passing all the parameters to get_aqi method 
    else:       # default value if the request method is not post
        city_aqi_api = airvisual.get_aqi("Indonesia", "Jakarta", "Jakarta")

    # create an instance of AQIProcessor class 
    aqi_processor = AQIProcessor(city_aqi_api)     

    # assign returned values of process_aqi method to the corresponding variables
    category, category_color, category_description, aqi = aqi_processor.process_aqi()  

    # assign returned values of weather_condition method to the corresponding variables     
    temperature, pressure, humidity, wind_speed, climate, icon_link = aqi_processor.weather_condition()
    jakartaTz = pytz.timezone("Asia/Jakarta") 
    current_datetime = datetime.now(jakartaTz).strftime("%b %d, %Y at %H:%M %p %Z")     # set the timezone to Jakarta timezone
    return render(request, 'weatherapp/aqi.html', {      # render all the returned values as context data
        'city_aqi_api': city_aqi_api,
        'category': category,
        'category_color': category_color,
        'category_description': category_description,
        'aqi': aqi,
        'temperature': temperature,
        'pressure': pressure,
        'humidity': humidity,
        'wind_speed': wind_speed,
        'climate': climate,
        'icon_link': icon_link,
        'current_datetime': current_datetime
    })       

# class created for making requests to forecasted temperature and sky condition API and retrieve data from it 
class ForecastAPI: 
    # initialize an object's state that store my api key
    def __init__(self):
        self.api_key = "141710af2113bab9f55ef73e1bcd33d5"

    # defining a method for retrieving forecast data dictionary for a specific place
    def get_forecast_api(self, place):
        forecast_api_request = requests.get("http://api.openweathermap.org/data/2.5/forecast?q=" + place + "&appid=" + self.api_key) # make a GET request to the API
        try: 
            forecast_api = json.loads(forecast_api_request.content)      # parse the API Call JSON response to a string and returns a Python dictionary
        except Exception as e:
            forecast_api = "Error..."
        return forecast_api      # return python dictionary containing forecasted data

# class created for processing the forecasted data retrieved from api openweathermap
class ForecastProcessor: 
    # initializes an attribute that is assigned the response from the Forecast API
    def __init__(self, forecast_api):
        self.forecast_api = forecast_api
    
    # defining a method for filtering the data retrieved from the API
    def get_data(self, forecast_days):
        filtered_data = self.forecast_api['list']    
        nr_values = 8 * int(forecast_days)
        return filtered_data[:nr_values]

# decorator to check whether the user is logged in, and if not, redirects the user to login_url
@login_required(login_url='users/login')
# function to handle requests made and returns forecast.html template to the client to be rendered
def forecast(request):
    forecast = ForecastAPI()       # create an instance of ForecastAPI class
    if request.method == "POST":
        place = request.POST['place']
        days = request.POST['days']
        option = request.POST['option']
    else:        # default value if the request method is not post
        place = "Jakarta"
        days = "1"
        option = "Temperature"

    if days == "1":
        tostring = f"{option} for the next {days} day in {place}"
    else:
        tostring = f"{option} for the next {days} days in {place}"
    
    # get forecasted data by passing all the parameters to get_forecast_api method 
    forecast_api = forecast.get_forecast_api(place)

    # create an instance of ForecastProcessor class 
    forecast_data = ForecastProcessor(forecast_api)

    # assign returned values of get_data method to the filtered_data variable
    filtered_data = forecast_data.get_data(days)

    if option == "Temperature":
        # list and extracts the temperature and date values, converts the temperature values from Kelvin to Celsius
        temperatures = [data['main']['temp'] for data in filtered_data]
        dates = [data['dt_txt'] for data in filtered_data]
        new_temperatures = [temp-273 for temp in temperatures]

        # Create a dataframe with the dates and temperatures lists as columns
        df = pd.DataFrame()
        df['Dates'] = dates
        df['Temperatures (C)'] = new_temperatures

        # Pass the dataframe to the px.line() function to create a line plot
        figure = px.line(df, x='Dates', y='Temperatures (C)', labels={"x": "Date", "y":"Temperature (C)"})
        # assigns the generated plot to the temperature_plot variable
        temperature_plot = plot(figure, output_type="div")

        return render(request, 'weatherapp/forecast.html', {'place': place, 'option': option, 'tostring': tostring, 'plot_div': temperature_plot})

    elif option == "Sky":
        images = {
            "Clear": "images/clear.png",
            "Clouds": "images/cloud.png",
            "Rain": "images/rain.png",
            "Snow": "images/snow.png"
        }
        # extracts the sky condition and date values, and creates a dictionary with date as key and sky condition as value.
        sky_conditions = [data['weather'][0]['main'] for data in filtered_data]
        image_paths = []
        for condition in sky_conditions: 
            image_paths.append(images[condition])

        dates = [data['dt_txt'] for data in filtered_data]
        sky = {}
        for i in range(len(sky_conditions)):
            sky[dates[i]] = image_paths[i]
        
        return render(request, 'weatherapp/forecast.html', {'forecast_api': forecast_api, 'place': place, 'option': option, 'tostring': tostring, 'image_paths': image_paths, 'sky': sky})

    return render(request, 'weatherapp/forecast.html', {})