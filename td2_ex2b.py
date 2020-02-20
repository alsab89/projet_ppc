# ---- And that of the client program. ----

import sysv_ipc, time
 
key = 128
 
mq = sysv_ipc.MessageQueue(key)
 
while True:
    message, t = mq.receive()
    if message[1]==1:
	message_retour = time.asctime()
        message = str(value).encode()
        mq.send(message_retour)
    elif message[1]==2:
        mq.remove()
    else:
        print("exiting.")
        break

mq.remove()
