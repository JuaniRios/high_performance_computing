# How to run
#### To run this assignment, you need to first start the 3 microservices created in the previous assignments.

1) Create a Virtual Environment and install the packages from requirements.txt


2) Apply database migrations to master_data
   1) cd ./master_data
   2) python manage.py migrate


3) Run the auth microservice
   1) cd ./authentication
   2) python manage.py runserver 8000


4) Run the master_data microservice
   1) cd ./master_data
   2) python manage.py runserver 9000


5) Run the queues microservice
   1) cd ./message-queues
   2) python ./api.py


#### You can now run the computing service.
* First we need to create some time series data that will be stored as a pickle file:
   1) cd ./hpc
   2) python ./create_data

After creating the data, this file will also post the job to the master_data service. The master_data service will
in turn add this job to the queue with status 1

* Now we can run the computing loop. This is a simple loop that calls compute.py using the mpiexec command
  1) cd ./hpc
  2) python ./main.py


We should see in the console of main.py an output for "waiting job", then a "job found, computing" and finally the 
result of the computation.

We can check the complete result data by pulling from the queue microservice. For this check the postman collection
included inside ./hpc

* We should now see that main.py is stuck at "waiting job". If we want it to compute again, we can run create_data again

# File Structure
The first level contains the 4 services, a documentation file, and a requirements.txt for creating the venv.<br>
I had to do some changes to the microservices to fit the requirements of the computing calculations, like for example
having the master_data push to job queue after receiving a job.<br><br>

### ./HPC
* HPC.postman_collection.json: this is a file to be imported with postman to make the token request, and result queue pull
* compute.py: where the mpi is being executed.
* create_data: creates time series data to be pushed to queue and master_data
* main.py: file to be run to await jobs and execute them
* timeseries.py: file already given. Contains functions to create time series data, make a model from data, and make a prediction
