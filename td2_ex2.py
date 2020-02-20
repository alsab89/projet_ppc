#!/usr/bin/env python3

import sysv_ipc
 
key = 128
 
mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
 
value = 1
while True:
    try:
        value = int(input())
    except:
        print("Input error, try again!")
    message = str(value).encode()
    mq.send(message)
    message_recu, t = mq.receive()
    value = message_recu.decode()
    if message_recu[1]==3:
        print("received:", value)
    else:
        print("exiting.")
        break
 
mq.remove()




