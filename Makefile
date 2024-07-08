up:
	docker compose up --build

down:
	docker compose down

model:
	docker exec -it mcadmin-web-1 python manage.py startapp ${MODEL_NAME}

rw:
	docker exec -it mcadmin-web-1 chmod 777 -R ${MODEL_NAME}/

makemigrations:
	docker exec -it mcadmin-web-1 python manage.py makemigrations

migrate:
	docker exec -it mcadmin-web-1 python manage.py migrate

createsuperuser:
	docker exec -it mcadmin-web-1 python manage.py createsuperuser

collectstatic:
	docker exec -it mcadmin-web-1 python manage.py collectstatic