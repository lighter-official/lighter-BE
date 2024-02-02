
from fastapi import FastAPI, WebSocket
from fastapi.responses import JSONResponse
import uvicorn
import websockets

app = FastAPI()

# WebSocket 연결을 저장할 리스트
websocket_connections = []


@app.get("/api-endpoint")
async def api_endpoint():
    # API 요청을 받았을 때의 로직
    # 여기에서 필요한 처리를 수행하고 WebSocket으로 데이터를 전송할 수 있습니다.

    # 예제: 모든 WebSocket 연결에 데이터를 전송
    for connection in websocket_connections:
        await connection.send_text('Hello from WebSocket!')

    return JSONResponse(content={"message": "API 요청이 처리되었습니다."})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # WebSocket 연결이 성립되었을 때 처리
    await websocket.accept()
    websocket_connections.append(websocket)

    try:
        while True:
            # WebSocket에서 데이터를 수신하거나 필요한 로직 수행
            message = await websocket.receive_text()
            print(f"Received message: {message}")

    except websockets.exceptions.ConnectionClosed:
        # WebSocket 연결이 닫힌 경우
        websocket_connections.remove(websocket)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)