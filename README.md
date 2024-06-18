# Unit, Integration and Mutation Testing Project


## Steps for this exercice

### 1. Execute and test the app

- a. Run the App:

First install runtime dependencies and development too:

pip install -r requirements-dev.txt

python run.py

- b. See the results with Postman, access localhost:8000/courses with GET, and create a Course with POST, with something as:

{
    "name": "Workshop de Kubernetes",
    "description": "Cursos con practicas"
}


### 2. Run the Unit Tests with coverage

- a. Run the tests:

pytest

-b. See the Coverage:

coverage run -m pytest

See here:

htmlcov/index.hmtl


### 3. Execute Mutation Tests

- a. Execute mutation tests:

mutmut run --paths-to-mutate app --tests-dir tests

mutmut results

mutmut html

- b. Result of the Mutation:

In html/index.html

