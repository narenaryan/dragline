
import thread


from redisds import Queue
from redis import StrictRedis
import os
from subprocess import Popen


re=StrictRedis()
start=Queue(name="start",namespace="dragd")
start.put("1")

stop=Queue(name="stop",namespace="dragd")

global process
def listen_start():
    try:

        while True:


            run_id=start.get()

            global process

            FNULL = open(os.devnull, 'w')
            comm=["python","start.py",run_id]

            print comm
            process=Popen(comm)



            #process.wait()







    except Exception as e:
        print "error in start"



def listen_stop():


    while True:
        try:
            global process


            run_id = stop.get()


            process.terminate()
        except Exception as e:
            print "error"



if __name__ == "__main__":
    thread.start_new_thread(listen_stop,())
    listen_start()







