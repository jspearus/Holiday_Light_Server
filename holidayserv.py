import requests
import websockets
import _thread
import asyncio
import time
import os
import sys

connected = set()

sys.stdout.write("test runing \n")


async def server(websocket, path):
    # Register.
    connected.add(websocket)
    try:
        async for message in websocket:
            for conn in connected:
                if conn != websocket:
                    sys.stdout.write(str(type(conn)))
                    await conn.send(f'Got a new MSG FOR YOU: {message}')
                    sys.stdout.write(message + '\n')
    finally:
        # Unregister.
        connected.remove(websocket)


start_server = websockets.serve(server, "192.168.1.114", 5000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
