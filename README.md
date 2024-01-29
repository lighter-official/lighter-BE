## Run 

for FE 

```bash
make docker.run # 서버 실행 
make docker.remove # 서버 삭제 
```

for BE 

```bash
poetry shell # 가상환경 시작 
poetry install # 라이브러리 설치
pip install -r requirements.txt # 라이브러리 설치
make run # 서버 실행 
```

## Version

- Mongo DB: 6.0.13 
- pymongo: 3.6.1