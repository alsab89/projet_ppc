#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sysv_ipc, pickle, random, sys, os, signal


pile = [("blue",i+1) for i in range(10)] + [("red",i+1) for i in range(10)]
pid = os.getpid()

state = True
key = 516
key1 = 527
key2 = 538
key3 = 549
key4 = 551


def handler(sig, frame):
    global state
    if sig == signal.SIGINT:  #SINGINT = CTRL+C
        state = False #Set state to false when we do ctrl+c => we go out from the loop

def pick(pile):
    board = []
    pos = random.randint(0,(len(pile)-1))
    board.append(pile.pop(pos))
    return (board,pile)

signal.signal(signal.SIGINT, handler)


if __name__ == '__main__':

    print("***** Server PID : "+str(pid)+" *****")
    print("----------------------------")

    mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
    sm_pile = sysv_ipc.SharedMemory(key1, sysv_ipc.IPC_CREAT, size=4096)
    sm_board = sysv_ipc.SharedMemory(key2, sysv_ipc.IPC_CREAT, size=4096)
    semaphore_pile = sysv_ipc.Semaphore(key3, sysv_ipc.IPC_CREAT, initial_value=1)
    semaphore_board = sysv_ipc.Semaphore(key4, sysv_ipc.IPC_CREAT, initial_value=1)

    board_card, pile_update = pick(pile)

    semaphore_board.acquire()
    sm_board.write(pickle.dumps(board_card))
    semaphore_board.release()
    semaphore_pile.acquire()
    sm_pile.write(pickle.dumps(pile_update))
    semaphore_pile.release()

    while state:

        msg, t = mq.receive(type=1)

        #Le premier player qui reçoit le message le supprimer => il faut que le type soit le pid de destination
        if t == 1:

            semaphore_board.acquire()
            board_card = pickle.loads(sm_board.read())
            semaphore_board.release()
            msg_decode = pickle.loads(msg)

            action = msg_decode[0]    # MQ : ( [action,player,card] , type )
            player = msg_decode[1]


            if action == "lay": #Player lay a card

                card = msg_decode[2]

                if (card[0][0]==board_card[0][0]) or (card[0][1]==board_card[0][1]):  #Check
                    semaphore_board.acquire()
                    sm_board.write(pickle.dumps(card)) # Board update
                    semaphore_board.release()
                    msg = pickle.dumps(["lay",card,"OK"])
                    mq.send(msg, type = player)
                else:
                    msg = pickle.dumps(["lay",card,"NOK"])
                    mq.send(msg, type = player)

            elif action == "last":   #It is the last card of the player

                card = msg_decode[2]

                if (card[0][0]==board_card[0][0]) or (card[0][1]==board_card[0][1]):  #Check
                    msg = pickle.dumps(["last",card,"OK"])
                    mq.send(msg, type = player)
                    break
                else:
                    msg = pickle.dumps(["last",card,"NOK"])
                    mq.send(msg, type = player)




    sm_pile.detach()
    sm_board.detach()
    sm_pile.remove()
    sm_board.remove()
    #sysv_ipc.remove_shared_memory(sm[1])
    #print(sm) -> print key, objectID
    #sysv_ipc.remove_shared_memory(ID)

    mq.remove()

    print("End of the game. "+str(player)+" won.")
    sys.exit()
