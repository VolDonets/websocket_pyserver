#!/usr/bin/env python

# WS server example that synchronizes state across clients

import asyncio
import json
import logging
import time
import websockets

import data_processing
import my_thread

logging.basicConfig()
USERS = set()
msg_gen = data_processing.MessageProcessing()


async def register(websocket):
    USERS.add(websocket)


async def unregister(websocket):
    USERS.remove(websocket)


async def counter(websocket, path):
    # register(websocket) sends user_event() to websocket
    await register(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
    finally:
        await unregister(websocket)


def get_msg():
    return msg_gen.get_message()


def process_messaging():
    while True:
        if len(USERS) > 0:
            try:
                msg = get_msg()
                asyncio.run(asyncio.wait([user.send(msg) for user in USERS]))
            except websockets.WebSocketException:
                print("Unavailable websocket")
            except ValueError:
                print("Set of websockets is empty")
        else:
            time.sleep(1)


def run_web_socket_server():
    messaging_thread = my_thread.MyThread(name="messaging", func_to_run=process_messaging)
    messaging_thread.start()
    start_server = websockets.serve(counter, "", 6789)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
    return


if __name__ == "__main__":
    run_web_socket_server()
