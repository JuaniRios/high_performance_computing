import datetime
import json
import pickle
from mpi4py import MPI
import requests
import re

from timeseries import linear_fit, predict_value

comm = MPI.COMM_WORLD

if comm.rank == 0:
    token = requests.get("http://127.0.0.1:8000/token", data={"username": "admin", "password": "1234"})
    token = token.json()
    print("waiting for next job")
    new_job = requests.get("http://localhost:7500/queues/jobs", headers={"Authorization": f"Bearer {token}"})
    print("new job received, computing...")
    assert new_job.status_code == 200
    new_job = new_job.json()
    new_job = new_job["response"]

    # update master data that job is processing (status 2)
    requests.patch(new_job["url"], data={"status": 2}, headers={"Authorization": f"Bearer {token}"})
    tasks = re.split(r",\s*", new_job["assets"])

    scatter_tasks = [[] for x in range(comm.size)]
    current_proc = 0
    for task in tasks:
        scatter_tasks[current_proc].append(task)
        current_proc = (current_proc + 1) % comm.size

else:
    scatter_tasks = None

asset_list = comm.scatter(scatter_tasks, root=0)

with open("data.pkl", "rb") as f:
    time_data = pickle.load(f)

# get model that we want and discard the rest of the data
series_list = [time_data[int(asset)] for asset in asset_list]
data_length = len(time_data)
del time_data  # save some memory

calcs = []
for series in series_list:
    model = linear_fit(series)
    calc = predict_value(model, len(series) + 1)  # predict at T+1 where T is length of time series data. I created all 100 time series with 300 points
    calcs.append(calc)

result = comm.gather(calcs, root=0)

if comm.rank == 0:
    result = [item for sublist in result for item in sublist]  # flatten list
    final_result = sum(result) / data_length

    # update master data that job is done (status 3)
    requests.patch(new_job["url"], data={"status": 3}, headers={"Authorization": f"Bearer {token}"})

    # put result in queue
    data = {
        "job": new_job["url"],
        "timestamp": str(datetime.datetime.now()),
        "assets": new_job["assets"],
        "weights": str(final_result)
    }
    result = requests.post("http://localhost:7500/queues/results", json=data, headers={"Authorization": f"Bearer {token}"})

    print("final result is: ", final_result)
