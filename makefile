#
# Memento
# Project Makefile
#

## config vars
# test config 
API_HOST:=localhost:5000

## targets
.DEFAULT:  images
.PHONY: test api-test images push run clean

## docker image targets
images:
	docker-compose build

push:
	docker-compose push

run: images
	docker-compose up

clean:
	docker-compose down -v -t 1


# test targets
test: test-backend

test-backend: test-backend-unit test-backend-api

test-backend-unit:
	docker-compose down -t 1
	docker-compose up -d && sleep 4 # wait for stack to start up
	docker-compose exec backend ash -c "python test.py"
	docker-compose down -t 1

test-backend-api:
	docker-compose down -t 1
	docker-compose up -d && sleep 4 # wait for stack to start up
	newman run --global-var api_host=$(API_HOST) \
		tests/api/momento-api.postman_collection.json
	docker-compose down -t 1
