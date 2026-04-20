db:
	docker-compose up -d db

tools:
	ruff format
	ruff check --output-format concise --fix

requirements:
	uv export --frozen --output-file=requirements.txt --no-dev

migrations:
	uv run python manage.py makemigrations

migrate:
	uv run python manage.py migrate

su:
	uv run python manage.py createsuperuser --noinput || true

audit: requirements
	uv run pip-audit -r requirements.txt

for_up: tools requirements migrations migrate su

init_from_files: for_up
	uv run python manage.py init_from_files

upl: for_up
	uv run python manage.py runserver 0.0.0.0:8000

upd: for_up
	docker-compose -f docker-compose.yml -f docker-compose.local.yml up --build web

upp: for_up
	TAG=latest docker-compose -f docker-compose.yml up --build web

test: for_up
	uv run pytest

down:
	docker-compose down
