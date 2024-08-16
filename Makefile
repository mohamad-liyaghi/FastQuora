.PHONY: help build run deploy stop test

help:
	@echo "Available targets:"
	@echo "  help    - Show this help message."
	@echo "  build   - Build the docker image."
	@echo "  run     - Run the docker container."
	@echo "  stop    - Stop the docker container."
	@echo "  test    - Run the tests."


build:
	docker compose build

run:
ifeq ($(DETACHED),true)
	docker compose up -d
else
	docker compose up
endif

deploy:
	docker compose -f docker-compose.prod.yaml up -d

stop:
	docker compose down

test:
	docker exec fast-quora-backend pytest
