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

#### Setup

- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `pip install -r requirements.txt`
- `make local-reset-db`

#### Run

- `make local-run`
- access the app at `http://localhost:9000`
- Test routes

#### Test

- `make local-test`
