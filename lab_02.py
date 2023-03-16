from requests import get
s_city = 'Vladikavkaz,RU'
appid = 'fc24e7a0c1e23411267d6497f5a1b3d0'
res = get("http://api.openweathermap.org/data/2.5/weather",
                   params={'q': s_city, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
data = res.json()
print("Город:", s_city)
'''print("Погодные условия:", data['weather'][0]['description'])
print("Температура:", data['main']['temp'])
print("Минимальная температура:", data['main']['temp_min'])
print("Максимальная температура:", data['main']['temp_max'])'''
print("Скорость ветра:", data['wind']['speed'])
print('Видимость:', data['visibility'])
res = get("http://api.openweathermap.org/data/2.5/forecast",
                   params={'q': s_city, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
data = res.json()
print("Прогноз погоды на неделю:")
for i in data['list']:
    #print("Дата <", i['dt_txt'], "> \r\nТемпература <", '{0:+3.0f}'.format(i['main']['temp']), "> \r\nПогодные условия <", i['weather'][0]['description'], ">")
    print(f"Дата <{i['dt_txt']}>")
    print(f"Cкорость ветра <{i['wind']['speed']}>")
    print(f"Видимость <{i['visibility']}>")
    print("-------------------------------")



