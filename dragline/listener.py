
from gevent import monkey, spawn, joinall
monkey.patch_all()
from redisds import Queue
import os
from subprocess import Popen



start=Queue(name="start",namespace="dragd")
start.put("1")

stop=Queue(name="stop",namespace="dragd")

global process
def listen_start():
    try:

        while True:

            print "hai"
            run_id=start.get()
            print run_id
            global process
            print os.getcwd()
            comm=["python","start.py",run_id]

            print comm
            process=Popen(comm)
            process.wait()git 

            print "pid there is ",pid
            print "iam hre again"


        print "iam breaking from the while loop some problem"
    except Exception as e:
        pass



def listen_stop():

    while True:
        print "hellllllllllllllllooooooooooooooooooooooooooooo every bodyyyyyyyyyyyyyyyyyy"
        run_id = stop.get()
        global process
        print process
        print run_id
        process.terminate()



if __name__ == "__main__":
    joinall([spawn(listen_start),spawn(listen_stop)])







