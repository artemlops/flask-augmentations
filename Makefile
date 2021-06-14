FLASK_APP ?= flask_augmentations.app:app

COMMIT ?=

IMAGE_REMOTE_PREFIX ?= artemlops
IMAGE_NAME ?= flask_augmentations
IMAGE_TAG ?= $(COMMIT)

IMAGE_LOCAL_FULL = $(IMAGE_NAME):$(IMAGE_TAG)
IMAGE_REMOTE_FULL = $(IMAGE_REMOTE_PREFIX)/$(IMAGE_LOCAL_FULL)


setup:
	python -m pip install -U pip setuptools wheel
	python -m pip install -r requirements-dev.txt

format:
	black mymodel/ flask_augmentations
	isort mymodel/ flask_augmentations


serve:
	FLASK_APP=$(FLASK_APP) flask run -p 8080


test: test_model test_flask
	@echo "OK"

test_model:
	python -m pytest mymodel

test_flask:
	python -m pytest flask_augmentations


docker_build:
	docker build -f Dockerfile -t $(IMAGE_LOCAL_FULL) .

docker_push:
	docker tag $(IMAGE_LOCAL_FULL) $(IMAGE_REMOTE_FULL)
	docker push $(IMAGE_REMOTE_FULL)

docker_serve: require.COMMIT
	docker run --rm -d --name flask_augmentations -p 8080:8080 $(IMAGE_REMOTE_FULL)


.PHONY: \
	setup \
	serve \
	test \
	test_model \
	test_flask \
	docker_build \
	docker_push \
	docker_serve

# utils
##

# This target prints provided variable value,
# for example: 'make print.IMAGE_NAME'
.SILENT: print.%
print.%:
	@echo $($*)


# This target allows us to explicitly require some env var to be set.
.SILENT: require.%
require.%:
	$(if $(value $(*)),,$(error Missing required argument $(*)))