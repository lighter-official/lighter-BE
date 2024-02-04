IMAGE_NAME := gloo
CONTAINER_NAME := gloo
VERSION := 1.0

run:
	poetry run python backend/main.py

docker.run:
	docker build -t ${IMAGE_NAME} .
	docker run -d -p 8000:8000 \
		--name ${CONTAINER_NAME}-server ${IMAGE_NAME}

docker.remove:
	docker stop ${CONTAINER_NAME}-server
	docker rm ${CONTAINER_NAME}-server

# 수동배포를 위해 이미지를 푸시합니다. ex) make docker.push v=230514-2 혹은 make docker.push v=1.3.2
docker.push:
	docker build --platform linux/amd64 -t lighter0125/gloo:${VERSION} .
	docker push lighter0125/gloo:${VERSION}

docker.rmi: # remove image - 모든 이미지 삭제
	docker rmi $(docker images -q)
