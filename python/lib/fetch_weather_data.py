import requests
import json
import pandas as pd

def fetch():

    # manually selected cities
    id_list = [2352778, 3451138, 3941584, 3451189, 188714, 587084, 1496153, 1311874, 2643743, 5128638, 1850147, 1275339, 2657896, 5368361, 3369157, 360630, 184745, 1796236, 1880251, 2147714] 

    # get city info
    f = open('./data/cities.json', 'r')
    places = json.load(f)


    # call api from openweathermap
    result_list = []
    for id in id_list:
        # appid must be replaced
        url = 'https://api.openweathermap.org/data/2.5/forecast?id=%d&units=metric&appid=3694ecea1914e82ca6449d5ae9cc5323' % id
        print(url)
        res = requests.get(url)
        data = res.json()

        result_list.append(data)

    # extract weather data
    dic = {
        'loc_index': [],
        'time_index': [],
        'dt': [],
        'temp': [],
        'temp_min': [],
        'temp_max': [],
        'humidity': [],
        'weather_id': [],
        'cloudiness': [],
        'wind_speed': [],
        'wind_deg': [],
        'rain': []
    }

    for i, r in enumerate(result_list):

        for (time_index, d) in enumerate(r['list']):

            dt         = d['dt']
            temp       = d['main']['temp']
            temp_min   = d['main']['temp_min']
            temp_max   = d['main']['temp_max']
            sea_level  = d['main']['sea_level']
            humidity   = d['main']['humidity']
            grnd_level = d['main']['grnd_level']

            weather_id = d['weather'][0]['id']
            cloudiness = d['clouds']['all']
            wind_speed = d['wind']['speed']
            wind_deg   = d['wind']['deg']

            if 'rain' in d and '3h' in d['rain']:
                rain   = d['rain']['3h']
            else:
                rain   = 0

            dic['loc_index'].append(i)
            dic['time_index'].append(time_index)
            dic['dt'].append(dt)
            dic['temp'].append(temp)
            dic['temp_min'].append(temp_min)
            dic['temp_max'].append(temp_max)
            dic['humidity'].append(humidity)
            dic['weather_id'].append(weather_id)
            dic['cloudiness'].append(cloudiness)
            dic['wind_speed'].append(wind_speed)
            dic['wind_deg'].append(wind_deg)
            dic['rain'].append(rain)


    df = pd.DataFrame.from_dict(dic)
    df.to_pickle('./data/weather.pkl')