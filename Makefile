.PHONY: help build run deploy stop test local_confmap prod_confmap k8s

help:
	@echo "Available targets:"
	@echo "  help    - Show this help message."
	@echo "  build   - Build the docker image."
	@echo "  run     - Run the docker container."
	@echo "  stop    - Stop the docker container."
	@echo "  test    - Run the tests."
	@echo "  local_confmap - Make Kubernetes config maps for local stage"
	@echo "  prod_confmap - Make Kubernetes config maps for production stage"
	@echo "  k8s - Deploy to Kubernetes"


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

local_confmap:
	kubectl create configmap fast-quora-env --from-env-file=envs/.env.local \
	&& kubectl create configmap fast-quora-env-file --from-file=.env=envs/.env.local

prod_confmap:
	kubectl create configmap fast-quora-env --from-env-file=.envs/.env.prod \
	&& kubectl create configmap fast-quora-env-file --from-file=.env=envs/.env.prod

k8s:
	kubectl apply -f kubernetes/
