import thread
from redisds import Queue
from redis import StrictRedis
import os
from subprocess import Popen


process = None
run_id = None

start = Queue(name="start", namespace="dragd", db=1)
redisclient = StrictRedis(db=1)



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
        print "error in start"


def listen_stop():
    global process, run_id

    pubsub = redisclient.pubsub()
    pubsub.subscribe("dragd:stop")
    while True:
        try:
            for i in pubsub.listen():
                if i['data'] == run_id:
                    process.terminate()
                    print run_id, "stopped"
        except Exception as e:
            print "error"
            print traceback.format_exc()


if __name__ == "__main__":
    thread.start_new_thread(listen_stop, ())
    listen_start()
