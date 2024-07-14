include .env
export

.PHONY: setup up down startapp makemigrations migrate createsuperuser collectstatic clear inittw tw getpayment

# this is most likely to be run as sudo
setup:
	docker compose up --build -d
	docker exec -it mcadmin-web-1 ./manage.py makemigrations
	docker exec -it mcadmin-web-1 ./manage.py migrate
	docker exec -it mcadmin-web-1 ./manage.py createsuperuser
	docker exec -it mcadmin-web-1 ./manage.py collectstatic --no-input

up:
	docker compose up --build -d

down:
	docker compose down

startapp:
	docker exec -it mcadmin-web-1 ./manage.py startapp ${APP_NAME}
	docker exec -it mcadmin-web-1 chmod 777 -R ${APP_NAME}/

makemigrations:
	docker exec -it mcadmin-web-1 ./manage.py makemigrations

migrate:
	docker exec -it mcadmin-web-1 ./manage.py migrate

createsuperuser:
	docker exec -it mcadmin-web-1 ./manage.py createsuperuser

collectstatic:
	docker exec -it mcadmin-web-1 ./manage.py collectstatic --no-input

clear:
	docker exec -it mcadmin-web-1 cp /dev/null general.log

twi:
	npm i && npm run build

tw:
	npx tailwindcss -i ./static/src/input.css -o ./static/src/output.css --watch

getpayment:
	curl -u ${ADMIN} -H 'Accept: application/json; indent=4' http://localhost/api/payment/