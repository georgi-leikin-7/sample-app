DOCKER_COMPOSE_FILES := $(shell find docker-compose -type f -name "*.yaml" | sed -e 's/^/-f /')

$(shell touch .env)
include .env
export

.PHONY: debug
debug:
	@echo ${DOCKER_COMPOSE_FILES}

.PHONY: build
build:
	docker compose ${DOCKER_COMPOSE_FILES} build --parallel=false

.PHONY: start
start:
	docker compose ${DOCKER_COMPOSE_FILES} up -d

.PHONY: clean
clean:
	find . -name ".idea" -exec rm -rf {} +
	find . -name "__pycache__" -exec rm -rf {} +
	rm -rf facade_lib/build
	rm -rf facade_lib/facade_lib.egg-info
	rm -rf frontend/node_modules