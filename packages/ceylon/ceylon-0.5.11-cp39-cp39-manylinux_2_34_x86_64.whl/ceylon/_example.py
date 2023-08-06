import asyncio
import logging
import time

import ceylon


async def _start():
    async def python_callback(message):
        logging.info(f"---------------------------------------Python callback received: {message}")

    logging.info("-----------------------------------------Starting Python client")
    pubsub = ceylon.PubSub()
    id = pubsub.get_node_id()
    logging.info(f"---------------------------------------Python client id: {id}")
    await pubsub.subscribe("agent_topic", python_callback)

    async def pass_message():
        # await asyncio.sleep(10)
        # pubsub.publish("agent_topic", rk_python.python_string_to_vec_u8(f"Hello from Python! {id}"))
        while True:
            await asyncio.sleep(5)
            current_time_ns = time.time_ns()
            pubsub.publish("agent_topic",
                           ceylon.python_string_to_vec_u8(f"Hello from Python! {id} {current_time_ns}"))

    async def start_subscriber():
        await pubsub.start()

    tx = asyncio.create_task(pass_message())
    tx1 = asyncio.create_task(start_subscriber())

    await asyncio.gather(tx, tx1)
