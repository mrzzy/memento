#
# Memento
# Project Makefile
#

## config vars
CONTAINERS_DIR:=containers
# docker image build confg 
IMG_PREFIX:=mrzzy/memento-
IMAGES:=$(foreach IMG,$(wildcard $(CONTAINERS_DIR)/*),$(IMG_PREFIX)$(notdir $(IMG)) )

# test config 
API_HOST:=localhost:5000

## targets
.DEFAULT: 
.PHONY: test api-test images

images: $(IMAGES)

$(IMG_PREFIX)%: $(CONTAINERS_DIR)/%/Dockerfile
	docker build -t $@ -f $< .

# test targets
test: test-api

# run tests for api
test-api:
	newman run --global-var api_host=$(API_HOST) \
		tests/api/momento-api.postman_collection.json
