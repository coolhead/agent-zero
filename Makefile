.PHONY: venv install run-api run-ui embed fmt lint test up down

PY := python3
VENV := .venv
ACT := $(VENV)/bin/activate

venv:
	@test -d $(VENV) || $(PY) -m venv $(VENV)

install: venv
	. $(ACT) && pip install -U pip && pip install -r requirements.txt

run-api:
	. $(ACT) && uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload

run-ui:
	. $(ACT) && streamlit run src/ui/app.py --server.port 8501 --server.address 0.0.0.0

embed:
	. $(ACT) && python -m src.retrieval.embed

fmt:
	. $(ACT) && black .
	. $(ACT) && ruff check --fix .

lint:
	. $(ACT) && ruff check . && black --check .

test:
	. $(ACT) && pytest -q

up:
	docker compose up --build

down:
	docker compose down -v
