.PHONY: help install run-backend run-frontend test clean docker-up docker-down

help:
	@echo "Available commands:"
	@echo "  make install        Install backend dependencies"
	@echo "  make run-backend    Start FastAPI backend on :8000"
	@echo "  make run-frontend   Start Frontend server on :3001"
	@echo "  make test           Run automated pytest test suite"
	@echo "  make docker-up      Start PostgreSQL and Backend in Docker"
	@echo "  make docker-down    Stop Docker containers"

install:
	pip install -r requirements.txt

run-backend:
	uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

run-frontend:
	python -m http.server 3001 --directory frontend

test:
	pytest backend/tests -v

docker-up:
	docker compose up -d --build

docker-down:
	docker compose down
