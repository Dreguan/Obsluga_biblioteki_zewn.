import requests, sys, json
from datetime import datetime
from os.path import getmtime

key = input()

class Weather:
    def __init__(self):
        self.response = []
        self.is_it_rain = {}

    def get_response(self, key):
        url = "https://visual-crossing-weather.p.rapidapi.com/forecast"
        querystring = {"location": "Washington,DC,USA", "aggregateHours": "24", "shortColumnNames": "0",
                       "unitGroup": "us", "contentType": "json"}
        headers = {
            'x-rapidapi-key': key,
            'x-rapidapi-host': "visual-crossing-weather.p.rapidapi.com"
        }
        self.response = requests.request("GET", url, headers=headers, params=querystring).json()
        #print(self.response)

    def load_response(self,key, file):
        sec = getmtime(file)
        now = datetime.now().timestamp()
        if now - sec < (60*60*24):
            with open(file, "r") as f:
                self.response = json.load(f)
            print("*Pobrane dane z pliku*")
        else:
            self.get_response(key)
            self.save_response(file)

    def save_response(self, file):
        with open(file, "w") as fp:
            file_content_json = json.dumps(self.response)
            fp.write(file_content_json)
        return True

    def forecast(self):
        for current_value in self.response["locations"]["Washington,DC,USA"]["values"]:
            date = datetime.utcfromtimestamp(current_value["datetime"]/1000).strftime("%Y-%m-%d")
            forecast = current_value["conditions"]
            self.is_it_rain[date] = forecast

    def __getitem__(self, item):
        if item not in self.is_it_rain:
            return "Nie wiem"
        if "Rain" in self.is_it_rain[item]:
            return "Będzie padać"
        else:
            return "Nie będzie padać"


weather = Weather()
outfile = sys.argv[1]
weather.load_response(key, outfile)
weather.forecast()
dict = weather.is_it_rain
print(weather[sys.argv[2]])
