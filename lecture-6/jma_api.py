import requests
from datetime import datetime
from db import insert_forecast

FORECAST_URL = "https://www.jma.go.jp/bosai/forecast/data/forecast/{}.json"


def fetch_and_save_forecast(area_code):
    res = requests.get(FORECAST_URL.format(area_code), timeout=5).json()

    short = res[0]["timeSeries"][0]
    temps = res[0]["timeSeries"][2]["areas"][0]["temps"]

    dates = short["timeDefines"]
    weathers = short["areas"][0]["weathers"]

    for i in range(min(5, len(dates))):
        date = datetime.fromisoformat(dates[i]).date().isoformat()
        weather = weathers[i]

        low = temps[i * 2] if i * 2 < len(temps) else None
        high = temps[i * 2 + 1] if i * 2 + 1 < len(temps) else None

        insert_forecast(area_code, date, weather, low, high)
