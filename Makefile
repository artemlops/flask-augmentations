FLASK_APP ?= flask_augmentations.app:app
IMAGE_NAME ?= flask_augmentations
IMAGE_TAG ?= 0.0.1

setup:
	pip install -e .

serve:
	FLASK_APP=$(FLASK_APP) flask run -p 8080

docker_build:
	docker build -f Dockerfile -t $(IMAGE_NAME):$(IMAGE_TAG) .

.PHONY: \
	setup \
	serve