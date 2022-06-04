# How to run
To run this assignment, you first need to run the authorization microservice 
made on the last assignment. it is included in this zip file.
* Run "python manage.py runserver 8000" inside /authentication

Now that the auth service is running, you can run the message queues microservice:
* Run api.py inside /message-queues with for example "python api.py"

# How to test
This service was tested using postman. You can import the collection of requests:
* import postman_collection.json from your Postman client

# API Specification
To get a nice overview of the available endpoints:
* go to http://localhost:7500/docs

Just have in mind that you won't be able to do http requests from the openapi
since you need an auth token attached to the request. For this use Postman.

# Configuration
There are 2 variables to configure, which have already defaulted values:
* max_queue_size: sets the maximum number of items in each queue.
* backup_time_seconds: how often should the queues be backed up

You can set those values at config.py. Keep in mind that already created queues cannot
have their max length changed.

# File Structure
* history.log: logs all requests and server errors
* postman_collection.json: you can import this with postman to test the api
* readme.md: this file
* \_\_init__.py: makes the project a python package
* api.py: the main file where the api resides
* backup: contains the function to backup the queues
* config: contains 2 configuration options
* requirements.txt: python packages to be installed
