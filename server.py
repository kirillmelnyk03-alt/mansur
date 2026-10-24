
import asyncio
import json
import websockets


clients = set()


async def handler(websocket):
    clients.add(websocket)
    print("Клиент ушел")

    try:
        async for message in websocket:
            try:
                data = json.loads(message)
            except json.JSONDecodeError:
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": "Некоректний JSON"
                }))
                continue


            response = {
                "type": "message",
                "data": data
            }


            results = await asyncio.gather(
                *[
                    client.send(json.dumps(response))
                    for client in clients
                ],
                return_exceptions=True
            )


            for client, result in zip(list(clients), results):
                if isinstance(result, Exception):
                    clients.discard(client)

    except websockets.exceptions.ConnectionClosed:
        pass

    finally:
        clients.discard(websocket)
        print("Клиент ушел")


async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("WebSocket-сервер запущено на порту 8765")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
