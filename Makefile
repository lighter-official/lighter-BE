IMAGE_NAME := lighter
CONTAINER_NAME := lighter

run:
	poetry run python backend/main.py

docker.run:
	docker build -t ${IMAGE_NAME} .
	docker run -d -p 8000:8000 \
		--name ${CONTAINER_NAME}-server ${IMAGE_NAME}

docker.remove:
	docker stop ${CONTAINER_NAME}-server
	docker rm ${CONTAINER_NAME}-server