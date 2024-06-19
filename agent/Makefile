define HELP_BODY
Available commands:

	make help       			- this thing.

	make init				- install python dependancies
	mage dev				- run the agent
	make build_docker_image			- build the docker image

endef

export HELP_BODY
help:
	@echo "$$HELP_BODY"

init:
	pip install -r requirements.txt > /dev/null
	@echo "Init complete"

dev:
	python3 -m main

build_docker_image:
	docker build -t agent/agent -f Dockerfile ..