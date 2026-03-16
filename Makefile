setup:
	bash scripts/setup.sh

backend:
	bash scripts/run_backend.sh

frontend:
	bash scripts/run_frontend.sh

migrate:
	cd backend && python manage.py makemigrations && python manage.py migrate

test:
	cd backend && python manage.py test
	pytest tests/

clean:
	find . -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -delete
