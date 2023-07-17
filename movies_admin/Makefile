up:
	docker-compose up -d

migrate:
	docker-compose exec movies_admin python manage.py migrate --no-input

superuser:
	docker-compose exec movies_admin python manage.py createsuperuser --username admin --email admin@email.com --no-input

static:
	docker-compose exec movies_admin python manage.py collectstatic --no-input --clear

load-data:
	docker-compose exec movies_admin sh -c "python sqlite_to_postgres/load_data.py"

full-up:
	make up
	make migrate
	make static
	make superuser
	make load-data

stop:
	docker-compose stop

remove:
	docker-compose down

remove-all:
	docker-compose down -v
