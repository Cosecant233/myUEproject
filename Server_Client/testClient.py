import asyncio
import websockets

# 向服务器端发送认证后的消息
async def recv_msg(websocket):
    while True:
        recv_text = await websocket.recv()
        print(f"{recv_text}")

# 客户端主逻辑
async def main_logic():
    async with websockets.connect('ws://127.0.0.1:8282') as websocketClient:
        await recv_msg(websocketClient)

asyncio.get_event_loop().run_until_complete(main_logic())