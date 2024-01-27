IMAGE_NAME := lighter
CONTAINER_NAME := lighter

run:
	poetry run python backend/main.py

docker.run:
	docker build -t ${IMAGE_NAME} .
	docker run --rm -d -p 8000:8000 \
		--name ${CONTAINER_NAME}-server ${IMAGE_NAME}

docker.stop:
	docker stop ${CONTAINER_NAME}-server