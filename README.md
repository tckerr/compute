# Setup and installation

## Installation

1. Create a virtualenv `python3 -m venv .venv`
2. Start your virtualenv: `source .venv/bin/activate`
3. Run `pip install -r requirements.txt`

## Running the server

2. Start your virtualenv: `source .venv/bin/activate`
3. Run the server: `uvicorn api:app --port 5000`

## Running the test client

1. Start your virtualenv: `source .venv/bin/activate`. This is required because `requests` is not a built-in module.
2. Run `python3 client.py`

# Contributing

## Adding a new server operation

1. Create a file in the `operations` directory which will hold the code for your operation.
2. Within that file, import and extend the `BaseModule` abstract class, by supplying a list of supported message types and a method for processing messages. Note that any message types which are shared with another module will cause the server to fail to start.
3. Import the module into `api.py`, and add an instance of it to the `modules` list below.
4. Include the Post and Response models to the union type so that our API can properly
   de/serialize the request and response.

Once these steps are completed, any message send to the server which has a `type` supported by your module will be processed by that module. See `operations/compute_max.py` for an implementation example. 
