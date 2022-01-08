.PHONY: local-reset-db
local-reset-db:
	PYTHONPATH=src FLASK_APP=stravastats FLASK_ENV=development flask dev create-db --drop-existing

.PHONY: local-run
local-run:
	PYTHONPATH=src FLASK_APP=stravastats FLASK_ENV=development flask run --host 0.0.0.0 --port 9000

.PHONY: local-test
local-test:
	PYTHONPATH=src pytest