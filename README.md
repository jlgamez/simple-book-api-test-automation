# Simple Book API test automation
## General description
This Python project uses the pipenv tool and the Pytest framework to automate API testing for the simple book API 
(https://simple-books-api.glitch.me)
# Project structure
- The code acts on the API over the internet using the requests library. Therefore, no API code is hosted in this project.
- The **tests/**  folder contains the python scripts with the code necessary to test the API.
- The **tests/conftest.py** is a script with fixtures following the pytest nomenclature. Pytest will run this code whenever a test needs a specific pre-condition.
- The **tests/config/test_data.json** is a file containing test data that will be loaded and re-utilised by the tests. Therefore, most of the test data can be changed from this file without having to refactor the code.
- The **test/support/load_file.py** is a simple helper that loads the test data for the tests . 
- All scripts within **tests/** folder that start with *test_* contain all the tests to be run by the test runner.
## Pre-requisites
- Install Pipenv: `$ pip install pipenv`
- Install dependencies: In the project directory run `$ pipenv install`
- Activate virtual env: In the project directory run `$ pipenv shell`
## Execute tests
- Run `$ pytest` to execute all tests.
- Run `$ pytest -k "test_name"` to execute a specific test
- Run `$ pytest --maxfail={number_failures_allowed}` to indicate Pytest to stop after a specific number of failures.

**Note**: As off the day of the writing of this README file, one failure is expected to occurr at **tests/test_books_retrieval.py** in *test_get_all_books_limit_with_invalid_partition*. The API fails when testing the *"limit"* query parameter with the invalid value of 0. To avoid this fail, open  **tests/config/test_data.json**, locate the *"invalidLimitValues"* array, and remove the number 0.  
