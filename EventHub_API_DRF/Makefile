.PHONY: run migrations migrate check test shell superuser showmigrations lint format typecheck collectstatic

run:
	python manage.py runserver

migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

check:
	python manage.py check

test:
	pytest

shell:
	python manage.py shell

superuser:
	python manage.py createsuperuser

showmigrations:
	python manage.py showmigrations

lint:
	flake8 .

format:
	black .

typecheck:
	mypy .

collectstatic:
	python manage.py collectstatic --noinput