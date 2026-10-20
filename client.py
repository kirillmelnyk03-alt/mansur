
import asyncio
import json
import websockets


async def main():
    async with websockets.connect(
        "ws://127.0.0.1:8765"
    ) as ws:
        await ws.send(json.dumps({
            "type": "message",
            "user": "Kirill",
            "text": "5риBeT, CерVeR!"
        }))

        response = await ws.recv()
        print(json.loads(response))


asyncio.run(main())
