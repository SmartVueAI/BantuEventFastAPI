.PHONY: up down build logs test clean

up:
	docker-compose up --build

down:
	docker-compose down

build:
	docker-compose build --no-cache

logs:
	docker-compose logs -f

test:
	curl http://localhost:8000/docs

clean:
	docker-compose down -v
	docker system prune -f

#Now you can use:
# make up      # Start containers
# make down    # Stop containers
# make logs    # View logs
# make test    # Quick API test
# make clean   # Clean everything