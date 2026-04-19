db:
	docker-compose up -d db redis

tools:
	ruff format
	ruff check --output-format concise --fix

requirements:
	uv export --frozen --output-file=project/requirements.txt --no-dev

migrations:
	cd project && uv run python manage.py makemigrations

migrate:
	cd project && uv run python manage.py migrate

su:
	cd project && uv run python manage.py createsuperuser --noinput || true

audit: requirements
	uv run pip-audit -r project/requirements.txt

for_up: tools requirements migrations migrate su

init_from_files: for_up
	cd project && uv run python manage.py init_from_files

upl: for_up
	cd project && uv run python manage.py runserver 0.0.0.0:8000

upd: for_up
	docker-compose -f docker-compose.yml -f docker-compose.local.yml up --build web

upp: for_up
	TAG=latest docker-compose -f docker-compose.yml up --build web

test: for_up
	cd project && uv run pytest

down:
	docker-compose down
