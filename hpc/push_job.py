import datetime
import pickle

import requests

token = requests.get("http://127.0.0.1:8000/token", data={"username": "admin", "password": "1234"})
token = token.json()


def push_queue_job(assets: str):
    body = {
        "owner": "admin",
        "url": "http://localhost:9000/jobs/13",
        "timestamp": "2022-06-03T20:24:03.442424+00:00",
        "status": 1,
        "date_range": "2022-06-13",
        "assets": assets
    }

    master_data_request = requests.post("http://localhost:7500/queues/jobs", json=body, headers={"Authorization": f"Bearer {token}"})
    assert master_data_request.status_code == 200


if __name__ == "__main__":
    # with open("data.pkl", "rb") as f:
    #     pickled_time_series = pickle.load(f)
    #
    # indexes = list(range(len(pickled_time_series)))
    # push_queue_job((str(indexes)[1:-1]))  # list of indexes for time_series_storage

    data = {
        "job": "http://localhost:9000/jobs/21",
        "timestamp": str(datetime.datetime.now()),
        "assets": "0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99",
        "weights": str(-0.00474)
    }
    result = requests.post("http://localhost:7500/queues/results", json=data, headers={"Authorization": f"Bearer {token}"})
    print(result)
