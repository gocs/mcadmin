include .env
export

up:
	docker compose up --build

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
	docker exec -it mcadmin-web-1 ./manage.py collectstatic

clear:
	docker exec -it mcadmin-web-1 cp /dev/null general.log

tw:
	npx tailwindcss -i ./static/src/input.css -o ./static/src/output.css --watch

rcon:
	go run main.go