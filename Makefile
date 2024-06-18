reset:
	python3 reset_local_db.py
	python3 manage.py makemigrations payment_app
	python3 manage.py migrate
	python3 manage.py createsuperuser

makemigrations:
	python3 manage.py makemigrations payment_app

migrate:
	python3 manage.py migrate

run:
	python3 manage.py runserver

populate:
	python3 populate_local_db.py

tailwind:
	python3 manage.py tailwind start
