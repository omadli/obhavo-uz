import requests, random, json
from .api_keys import API_KEYS
from .dicts import *
class Weather:
    UNITS = "metric"
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    URL = "https://api.openweathermap.org/data/2.5/"

    def gen_key(self):
        return random.choice(API_KEYS)

    def req(self, url, payload):
        r = requests.get(url, params=payload, headers=self.HEADERS)
        res = json.loads(r.text)
        if res['cod'] == 200:
            return self.tr(res)
        else:
            return None

    def current(self, lat, lon):
        """https://openweathermap.org/current"""
        url = self.URL+"weather"
        payload = {
            'lat': lat,
            'lon': lon,
            'appid': self.gen_key(),
            'units': self.UNITS
        }
        return self.req(url, payload)

    def by_city(self, q):
        url = self.URL+"weather"
        payload = {
            'q': q,
            'appid': self.gen_key(),
            'units': self.UNITS
        }
        return self.req(url, payload)

    def onecall(self, lat, lon):
        """https://openweathermap.org/api/one-call-api"""
        url = self.URL + "onecall"
        payload = {
            'lat' : lat,
            'lon' : lon,
            'appid' : self.gen_key(),
            'units' : self.UNITS
        }
        r = requests.get(url, params=payload, headers=self.HEADERS)
        res = json.loads(r.text)
        res2 = res
        res2['current'] = self.tr(res['current'])
        for i in range(len(res['daily'])):
            res2['daily'][i] = self.tr(res['daily'][i])
            res2['daily'][i].update({'moon': self.moon_phase(float(res2['daily'][i]['moon_phase']))})
        return res2

    def moon_phase(self, phase:float):
        if phase == 0 or phase == 1:
            return "Yangi oy"
        elif phase > 0 and phase < 0.25:
            return "O'sayotgan hilol oy"
        elif phase == 0.25 or phase == 0.75:
            return "Yarim oy"
        elif phase > 0.25 and phase < 0.5:
            return "O'sayotgan yarim oy"
        elif phase == 0.5:
            return "To'lin oy"
        elif phase > 0.5 and phase < 0.75:
            return "Qisqarayotgan yarim oy"
        elif phase > 0.75 and phase < 1:
            return "Qisqarayotgan hilol oy"

    def wind_side(self, deg):
        a = deg//22.5
        if a%2: a+=1
        b = 22.5*a
        return DEGS[str(int(b))]

    def tr(self, res):
        res2 = res
        m = res['weather'][0]['main']
        res2['weather'][0]['main'] = MAINS.get(m, m)
        d = res['weather'][0]['description']
        res2['weather'][0]['description'] = DESCRIPTIONS.get(d, d)
        i = res['weather'][0]['icon']
        res2['weather'][0]['emoji'] = ICONS.get(i, "🌏")
        if res.get('wind_deg', False):
            deg = res['wind_deg']
            res2.update({'wind_side' : self.wind_side(deg)})
        elif res.get('wind', False):
            deg = res['wind']['deg']
            res2['wind'].update({'side' : self.wind_side(deg)})
        return res2