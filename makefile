#
# Memento
# Project Makefile
#

.PHONY: test api-test

API_HOST:=localhost:5000

## test targets
test: api-test

# run tests for api
test-api:
	newman run --global-var api_host=$(API_HOST) \
		tests/api/momento-api.postman_collection.json
