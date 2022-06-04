import datetime
import pickle

import requests

from hpc.timeseries import create_time_series


def push_job(assets: str):
    token = requests.get("http://127.0.0.1:8000/token", data={"username": "admin", "password": "1234"})
    token = token.json()
    body = {
        "assets": assets,
        "date_range": str(datetime.date.today() + datetime.timedelta(days=10)),
        "status": 1,
    }

    master_data_request = requests.post("http://localhost:9000/jobs", data=body, headers={"Authorization": f"Bearer {token}"})
    assert master_data_request.status_code == 201


time_series_storage = []

# have new data to work with
new_series_arr = create_time_series(100, 300)
time_series_storage += new_series_arr
indexes = list(range(len(time_series_storage)))
push_job(str(indexes)[1:-1])  # list of indexes for time_series_storage

with open("data.pkl", "wb+") as f:
    pickle.dump(time_series_storage, f)
