App with basic JWT-based authentication, includes the following routes:

- /auth/register
- /auth/login
- /auth/logout
- /athlete/add
- /athlete/[id] (Get athlete)
- /activity/add
- /activities/[strava id] (Get activity)
- /gear/add
- /gears (Get gears)

### Setup (local install)

```
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ make local-reset-db
```

#### Run

- `make local-run`
- access the app at `http://localhost:9000`
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
- Start containers (rebuild app if any code changes)
- VSCode - select remote attach Python debugger, start debugging. Ref~: https://code.visualstudio.com/docs/python/debugging#_example
- Validate homepage message in browser - http://localhost:5000/
- Test API Endpoints

