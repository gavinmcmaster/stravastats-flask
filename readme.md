App with basic JWT-based authentication, includes the following routes:

- /api/auth/register
- /api/auth/login
- /api/auth/logout
- /api/athlete/add
- /api/athlete/[id] (Get athlete)
- /api/activity/add
- /api/activities/[strava id] (Get activity)
- /api/gear/add
- /api/gears (Get gears)

### Setup (local install)

```
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ make local-reset-db
```

#### Run

- `make local-run`
- Access the app at `http://localhost:9000/api/`
- API docs: http://localhost:9000/apidocs/#/
- Test API Endpoints

#### Test
Run all unit tests with following command:
- `make local-test`

### Docker Set-up (debug mode)
```
$ docker build --target debug -t gavmcmaster/stravastats:debug .
$ docker compose pull
$ docker compose up -d
```
#### Debugging in container with VS Code
- Start containers (rebuild 'app' if any code changes)
- VSCode - select remote attach Python debugger, start debugging. Ref~: https://code.visualstudio.com/docs/python/debugging#_example
- Validate homepage message in browser - http://localhost:5000/api/
- API docs: http://localhost:5000/apidocs/#/
- Test API Endpoints

#### Unit Tests in Docker
In 'postgres' container create tests DB then run tests:

```
$ create database stravastats_unit_tests;
# Run all tests in 'app' container
$ make local-test
# Single file
$ py.test tests/test_activity.py
# Test pattern
$ py.test tests/test_activity.py -k "get_no_activities"
```



