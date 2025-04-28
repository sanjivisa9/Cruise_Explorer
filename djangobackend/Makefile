.PHONY: setup test lint clean

setup:
	chmod +x setup.sh
	./setup.sh

test:
	python manage.py test

lint:
	flake8 .
	black .

run:
	python manage.py runserver

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name "*.egg" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".tox" -exec rm -r {} +

migrations:
	python manage.py makemigrations
	python manage.py migrate

superuser:
	python manage.py createsuperuser

shell:
	python manage.py shell_plus --ipython

backup:
	python manage.py dumpdata > backup.json