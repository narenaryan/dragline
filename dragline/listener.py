import thread
from redisds import Queue
from redis import StrictRedis
import os
from subprocess import Popen
import logging
import logging.config
from defaultsettings import LOGCONFIG


process = None
run_id = None

start = Queue(name="start", namespace="dragd", db=1)
redisclient = StrictRedis(db=1)
logging.config.dictConfig(LOGCONFIG)
logger = logging.getLogger("dragd")


def listen_start():
    global run_id, process
    try:
        while True:
            run_id = start.get()
            FNULL = open(os.devnull, 'w')
            comm = ["python", "start.py", run_id]
            process = Popen(comm)
            process.wait()
            run_id = None
    except Exception as e:
        logger.exception("failed to execute %s", run_id)


def listen_stop():
    global process, run_id
    pubsub = redisclient.pubsub()
    pubsub.subscribe("dragd:stop")
    while True:
        try:
            for i in pubsub.listen():
                if i['data'] == run_id:
                    process.terminate()
                    logger.info("stopped %s run", run_id)
        except Exception as e:
            logger.exception("Failed to stop %s", run_id)


if __name__ == "__main__":
    thread.start_new_thread(listen_stop, ())
    listen_start()
