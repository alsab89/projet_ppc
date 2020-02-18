#!/usr/bin/env python3

#Dans un CLI, on entre ps ax et on relève le numéro du process ex2.py
#Ensuite, on exécute kill -s SIGKILL 12236(=PID)

# while True:
#     pass

# import signal
#
# def handler(sig, frame):
#     if sig == signal.SIGINT:
#         print("}:-)")
#
# signal.signal(signal.SIGINT, handler)
#
# while True:
#     pass

#On peut aussi ignorer les signaux (voir doc) ; alors on crée un virus


from multiprocessing import Process
import time, signal, os

def handler(sig, frame):
    if sig == signal.SIGUSR1:
        os.kill(childPID,signal.SIGKILL)
        print("Process enfant tué")

signal.signal(signal.SIGUSR1, handler)

def func():
    time.sleep(5)
    while True:
        os.kill(os.getppid(),signal.SIGUSR1) #os.kill permet d'envoyer des signaux entre process
        #print("hello")

if __name__ == "__main__":
    p = Process(target=func)
    p.start()
    global childPID
    childPID = p.pid
    p.join()
