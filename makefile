#
# Memento
# Project Makefile
#

## config vars
# test config 
API_HOST:=localhost:5000

## targets
.DEFAULT:  images
.PHONY: test api-test images push run

## docker image targets
images:
	docker-compose build

push:
	docker-compose push

run: images
	docker-compose up

# test targets
test: test-api

# run tests for api
test-api:
	newman run --global-var api_host=$(API_HOST) \
		tests/api/momento-api.postman_collection.json
