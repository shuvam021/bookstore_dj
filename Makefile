dj=python manage.py

run:
	$(dj) runserver

static:
	$(dj) collectstatic

migration:
	$(dj) makemigrations
	$(dj) migrate

superuser:
	$(dj) createsuperuser --username admin --email admin@email.com
