## Development

Use either of the following local or docker instructions

### Local

#### Setup

- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `pip install -r requirements.txt`
- `make local-reset-db`

#### Run

- `make local-run`
- access the app at `http://localhost:9000`

#### Test

- `make local-test`
