from .models import City
from .Weather.weather import Weather
from datetime import datetime

w = Weather()
month_list = ['Yanvar', 'Fevral', 'Mart', 'Aprel', 'May', 'Iyun', 'Iyul', 'Avgust', 'Sentyabr', 'Oktabr', 'Noyabr', 'Dekabr']
weekdays_list = ['Yakshanba', 'Dushanba', 'Seshanba', 'Chorshanba', 'Payshanba', 'Juma', 'Shanba']

def ceil(x):
    n = int(x)
    return n if n-1 < x <= n else n+1

def filter_res(res, city_name):
	now = datetime.now()
	data = {
		'city_name':city_name,
		'day': now.day,
		'month': month_list[now.month-1],
		'weekday': weekdays_list[int(now.strftime("%w"))],
		'icon': res['current']['weather'][0]['icon'],
		'temp': ceil(res['current']['temp']),
		'max': ceil(res['daily'][0]['temp']['max']),
		'min': ceil(res['daily'][0]['temp']['min']),
		'main': res['current']['weather'][0]['main'],
		'pop': ceil(float(res['daily'][0]['pop'])*100),
		'humidity': res['current']['humidity'],
		'dev_point': ceil(res['daily'][0]['dew_point']),
		'sunrise': datetime.fromtimestamp(res['current']['sunrise']).strftime("%H:%M"),
		'sunset': datetime.fromtimestamp(res['current']['sunset']).strftime("%H:%M"),
		'moon_phase': res['daily'][0]['moon'],
		'uvi': ceil(res['daily'][0]['uvi']),
		'wind_side': w.wind_side(res['current']['wind_deg']),
		'wind_speed': ceil(float(res['current']['wind_speed'])*3.6),
		'pressure': ceil(int(res['current']['pressure']) / 1.33),
		'morn_temp': ceil(res['daily'][0]['temp']['morn']),
		'day_temp': ceil(res['daily'][0]['temp']['day']),
		'night_temp': ceil(res['daily'][0]['temp']['night']),
	}
	_list = []
	for i in range(1, 8):
		_list.append({
			'day': datetime.fromtimestamp(res['daily'][i]['dt']).strftime("%d"),
			'month': month_list[int(datetime.fromtimestamp(res['daily'][i]['dt']).strftime("%m"))-1],
			'weekday': weekdays_list[int(datetime.fromtimestamp(res['daily'][i]['dt']).strftime("%w"))],
			'weekend': datetime.fromtimestamp(res['daily'][i]['dt']).strftime("%w"),
			'icon': res['daily'][i]['weather'][0]['icon'],
			'max': ceil(res['daily'][i]['temp']['max']),
			'min': ceil(res['daily'][i]['temp']['min']),
			'main': res['daily'][i]['weather'][0]['main'],
			'description': res['daily'][i]['weather'][0]['description'],
			'pop': ceil(float(res['daily'][i]['pop'])*100)
		})
	data.update({'daily': _list})
	return data

def getDataCity(city:City):
	res = w.onecall(city.lat, city.lon)
	return filter_res(res, city.name)

def search_location(lat, lon):
	res1 = w.current(lat, lon)
	if res1['cod'] == "404":
		return False
	res2 = w.onecall(lat, lon)
	return filter_res(res2, res1['name'])

def search_city(q):
	res1 = w.by_city(q)
	if res1['cod'] == "404":
		return False
	lon, lat = res1['coord'].values()
	res2 = w.onecall(lat, lon)
	return filter_res(res2, res1['name'])
