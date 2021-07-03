import requests, sys, json
from datetime import datetime
from os.path import getmtime

key = input()

class Weather:
    def __init__(self):
        self.response = []

    def get_response(self, key):
        url = "https://visual-crossing-weather.p.rapidapi.com/forecast"
        querystring = {"location": "Washington,DC,USA", "aggregateHours": "24", "shortColumnNames": "0",
                       "unitGroup": "us", "contentType": "json"}
        headers = {
            'x-rapidapi-key': key,
            'x-rapidapi-host': "visual-crossing-weather.p.rapidapi.com"
        }
        self.response = requests.request("GET", url, headers=headers, params=querystring).json()
        print(self.response)

    def load_response(self,key, file):
        sec = getmtime(file)
        now = datetime.now().timestamp()
        if now - sec < (60*60*24):
            with open(file, "r") as f:
                self.response = json.load(f)
            print("Dane z pliku")
        else:
            self.get_response(key)
            self.save_response(file)
        return True

    def save_response(self, file):
        with open(file, "w") as fp:
            file_content_json = json.dumps(self.response)
            fp.write(file_content_json)

weather = Weather()
outfile = sys.argv[1]
weather.load_response(key, outfile)
#weather.get_response(key)
#weather.save_response(outfile)