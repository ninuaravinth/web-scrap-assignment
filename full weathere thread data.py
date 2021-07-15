
import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
import datetime
from threading import Thread
import sqlite3

d = datetime.date.today()
d.strftime('%d %B, %Y')
def getCurrentWeather(params):
    weather = 'http://api.openweathermap.org/data/2.5/weather'
    params['APPID'] = '1714486ff1a0070e51d0757147b0eeb0'
    params['units'] = 'metric'
    return requests.get(weather,params)
params = {'q':'Los Angeles'}
response = getCurrentWeather(params)

response.status_code
response.json()

cit = response.json()
tim = cit['dt'] - 60*60*3 + cit['timezone']

datetime.datetime.fromtimestamp(tim).strftime("%Y-%m-%d %H:%M")
world_cities = requests.get('https://worldpopulationreview.com/world-cities/')

cities = BeautifulSoup(world_cities.text,'lxml')

city_names = []
for i in range(42,450):
    if i%2 == 0:
        city_names.append(cities.findAll('a')[i].getText())

city_names[:5]

city_names_pop = pd.DataFrame(data={"city_names":city_names})
city_names_pop.to_csv('city_names.csv',index=False)
city_np = pd.read_csv('city_names.csv')
if city_np is None:
    print(3)

city_np['city_names'].values.tolist()

for i in range(0,5):
    print(city_names_pop['city_names'].values.tolist()[i])

len(city_names)




def get_correct_name(city_name):
    correct_name = city_name
    if city_name == 'St Petersburg':
        correct_name = 'St.Petersburg'
    elif city_name == 'Rome':
        correct_name = 'Rome,IT'
    elif city_name == 'Melbourne':
        correct_name = 'Melbourne,AU'
    return correct_name


world_temperatures = []
for i in range(5):
    params['q'] = get_correct_name(city_names[i])
    response = getCurrentWeather(params)
    if response.status_code != 200:
        continue
    city_information = response.json()
    country = city_information['sys']['country']
    latitude = city_information['coord']['lat']
    longitude = city_information['coord']['lon']
    weather_condition = city_information['weather'][0]['main']
    weather_det = city_information['weather'][0]['description']
    feels_like = city_information['main']['feels_like']
    temp = city_information['main']['temp']
    max_temp = city_information['main']['temp_max']
    min_temp = city_information['main']['temp_min']
    wind_speed = city_information['wind']['speed']
    city_data = {'City': city_names[i],
                     'Country': country,
                     'Date': d.strftime('%d-%m-%Y'),
                     'Latitude': latitude,
                     'Longitude': longitude,
                     'Weather': weather_condition,
                     'Main_Weather': weather_det,
                     'Feels_like': feels_like,
                     'temp': temp,
                     'max_temp': max_temp,
                     'min_temp': min_temp,
                     'Wind_Speed': wind_speed}
    world_temperatures.append(city_data)

world_temps_df = pd.DataFrame(world_temperatures, columns = city_data.keys())


world_temps_df.to_csv('weather4.csv')

conn = sqlite3.connect('TestDB1.db')
c = conn.cursor()

c.execute('CREATE TABLE scrap3 (City,Country,Date,Latitude,Longitude,Weather,Main_Weather,Feels_like,temp,max_temp,min_temp,Wind_Speed)')
conn.commit()
scrap3 = world_temps_df
        

df = pd.DataFrame(scrap3, columns= ['City','Country','Date','Latitude','Longitude','Weather','Main_Weather','Feels_like','temp','max_temp','min_temp','Wind_Speed'])
df.to_sql('scrap3', conn, if_exists='replace', index = False)
 
c.execute('''  
SELECT * FROM scrap3
          ''')

for row in c.fetchall():
    print (row)




