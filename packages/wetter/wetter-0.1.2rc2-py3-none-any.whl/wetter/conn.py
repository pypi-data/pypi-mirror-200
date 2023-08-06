import pandas as pd
from datetime import datetime as dt
from os import path

DATA_LOCATION = path.join(path.dirname(path.abspath(__file__)), "..", "data")
DB = path.join(DATA_LOCATION, "OpenMeteo.json")


def get_db():
    _data = pd.read_json(DB)
    df = pd.DataFrame(
        {
            "time": [dt.strptime(x, "%Y-%m-%dT%H:%M") for x in _data.hourly["time"]],
            "temperature": _data.hourly["temperature_2m"],
            "wind": _data.hourly["windspeed_10m"],
            "wmo": _data.hourly["weathercode"],
        }
    )
    df = df.set_index("time")
    return df
