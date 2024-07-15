include .env
export

.PHONY: setup up down startapp makemigrations migrate createsuperuser collectstatic clear inittw tw getpayment

# this is most likely to be run as sudo
setup:
	docker compose up --build -d
	docker compose exec -it web ./manage.py makemigrations
	docker compose exec -it web ./manage.py migrate
	docker compose exec -it web ./manage.py createsuperuser
	docker compose exec -it web ./manage.py collectstatic --no-input

up:
	docker compose up --build -d

down:
	docker compose down

startapp:
	docker compose exec -it web ./manage.py startapp ${APP_NAME}
	docker compose exec -it web chmod 777 -R ${APP_NAME}/

makemigrations:
	docker compose exec -it web ./manage.py makemigrations

migrate:
	docker compose exec -it web ./manage.py migrate

createsuperuser:
	docker compose exec -it web ./manage.py createsuperuser

collectstatic:
	docker compose exec -it web ./manage.py collectstatic --no-input

clear:
	docker compose exec -it web cp /dev/null general.log

twi:
	npm i && npm run build

tw:
	npx tailwindcss -i ./static/src/input.css -o ./static/src/output.css --watch

getpayment:
	curl -u ${ADMIN} -H 'Accept: application/json; indent=4' http://localhost/api/payment/