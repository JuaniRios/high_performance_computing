import asyncio
import logging
import time
import pickle

logging.basicConfig(level=logging.INFO, filename="history.log", encoding="utf-8")


async def backup_to_pickle(queues: dict):
    while True:
        await asyncio.sleep(10)
        with open("queue_backup.pkl", "wb") as f:
            pickle.dump(queues, f)
        logging.info("queue backed up as pickled dict!")
