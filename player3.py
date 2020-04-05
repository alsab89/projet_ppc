#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random, os, multiprocessing, sysv_ipc, pickle, pygame, threading, time
import sys, termios, atexit
from select import select

key = 516
key1 = 527
key2 = 538
key3 = 549
key4 = 551
pid = os.getpid()

class KBHit:
    def __init__(self):
        '''Creates a KBHit object that you can call to do various keyboard things.
        '''
        if os.name == 'nt':
            pass
        else:
            # Save the terminal settings
            self.fd = sys.stdin.fileno()
            self.new_term = termios.tcgetattr(self.fd)
            self.old_term = termios.tcgetattr(self.fd)
            # New terminal setting unbuffered
            self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)
            # Support normal-terminal reset at exit
            atexit.register(self.set_normal_term)
    def set_normal_term(self):
        ''' Resets to normal terminal.  On Windows this is a no-op.
        '''
        if os.name == 'nt':
            pass
        else:
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)
    def getch(self):
        ''' Returns a keyboard character after kbhit() has been called.
            Should not be called in the same program as getarrow().
        '''
        s = ''
        if os.name == 'nt':
            return msvcrt.getch().decode('utf-8')
        else:
            return sys.stdin.read(1)
    def getarrow(self):
        ''' Returns an arrow-key code after kbhit() has been called. Codes are
        0 : up
        1 : right
        2 : down
        3 : left
        Should not be called in the same program as getch().
        '''
        if os.name == 'nt':
            msvcrt.getch() # skip 0xE0
            c = msvcrt.getch()
            vals = [72, 77, 80, 75]
        else:
            c = sys.stdin.read(3)[2]
            vals = [65, 67, 66, 68]
        return vals.index(ord(c.decode('utf-8')))
    def kbhit(self):
        ''' Returns True if keyboard character was hit, False otherwise.
        '''
        if os.name == 'nt':
            return msvcrt.kbhit()
        else:
            dr,dw,de = select([sys.stdin], [], [], 0)
            return dr != []


def distribution(pile):  #The player picks 5 cards to compose his hand
    player = []
    for i in range(5):
        pos = random.randint(0,(len(pile)-1))
        player.append(pile.pop(pos)) #pop return value and delete from the list
    return (player,pile)

def pick(pile):
    board = []
    pos = random.randint(0,(len(pile)-1))
    board.append(pile.pop(pos))
    return (board,pile)

def pick_timer(pile):
    picked_card, pile_update = pick(pile)
    player1.append(picked_card[0])
    semaphore_pile.acquire()
    sm_pile.write(pickle.dumps(pile_update))
    semaphore_pile.release()
    print("Shit.... One more. Timer expired")

def display_board(semaphore_board):  #Display value of card_board continuously
    semaphore_board.acquire()
    sm_board = sysv_ipc.SharedMemory(key2)   # SM : [ [pile] , (board_card) ]
    board_card_update = pickle.loads(sm_board.read()) #read -> Read in the shared memory and loads -> Decode bytes
    semaphore_board.release()
    print("****************************")
    print(board_card_update)
    print("***************************")

def press_key(semaphore_board):
    mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
    pid = os.getpid()

    semaphore_pile.acquire()
    pile = pickle.loads(sm_pile.read())
    semaphore_pile.release()

    #timer = threading.Timer(10.0, pick_timer(pile))
    #timer.start()

    while True:

        print("----------------------")
        print("Choose a card to lay (enter position) : ")
        print("----------------------")

        done = False

        # SI LE TIMER EXPIRE (AUCUNE TOUCHE SAISIE), LE JOUEUR PIOCHE UNE CARTE
        kb = KBHit()

        if len(player1)<10:
            if len(player1)==1:  #It is the last card of the player
                while not done:
                    if kb.kbhit():
                        choice = kb.getch()
                        if choice == "q": #quit game
                            print("End of the game. Goodbye.")
                            mq.remove()
                            break
                        elif choice == "s": #show hand
                            print("----------------------")
                            print(player1)
                            print("----------------------")
                        elif choice == "d": #display board
                            print("----------------------")
                            display_board(semaphore_board)
                            print("----------------------")
                        else :  #chose a card to lay
                            card_to_lay = player1[int(choice)-1]
                            info = ["last",pid,[card_to_lay]]    # MQ : ( [action,player_pid,card,card_pos] , type )
                            msg = pickle.dumps(info)
                            mq.send(msg, type=1)
                        done = True
            else:
                while not done:
                    if kb.kbhit():
                        choice = kb.getch()
                        if choice == "q": #quit game
                            print("End of the game. Goodbye.")
                            mq.remove()
                            break
                        elif choice == "s": #show hand
                            print("----------------------")
                            print(player1)
                            print("----------------------")
                        elif choice == "d": #display board
                            print("----------------------")
                            display_board(semaphore_board)
                            print("----------------------")
                        else :  #chose a card to lay
                            card_to_lay = player1[int(choice)-1]
                            info = ["lay",pid,[card_to_lay]]    # MQ : ( [action,player,card] , type )
                            msg = pickle.dumps(info)
                            mq.send(msg, type=1)
                        done = True
        else:
            while not done:
                if kb.kbhit():
                    cho1 = kb.getch()
                    if cho1 == "q": #quit game
                        print("End of the game. Goodbye.")
                        mq.remove()
                        break
                    elif cho1 == "s": #show hand
                        print("----------------------")
                        print(player1)
                        print("----------------------")
                    elif cho1 == "d": #display board
                        print("----------------------")
                        display_board(semaphore_board)
                        print("----------------------")
                    elif not msvcrt.kbhit():
                        cho2 = msvcrt.getch()
                        choice = cho1 + cho2
                        card_to_lay = player1[int(choice)-1]
                        info = ["lay",pid,[card_to_lay]]    # MQ : ( [action,player,card] , type )
                        msg = pickle.dumps(info)
                        mq.send(msg, type=1)
                    done = True

def listen_mq(semaphore_pile,semaphore_board):

    try:
        mq = sysv_ipc.MessageQueue(key)
    except:
        print("Can not connect to message queue ", key, ", terminating.")
        sys.exit(1)

    while True:

        msg, t = mq.receive(type=pid)

        #Le premier player qui reçoit le message le supprimer => il faut que le type soit le pid de destination
        if t == pid: #pid of server

            semaphore_pile.acquire()
            pile = pickle.loads(sm_pile.read())
            semaphore_pile.release()
            semaphore_board.acquire()
            board = pickle.loads(sm_board.read())
            semaphore_board.release()

            msg_decode = pickle.loads(msg)
            action = msg_decode[0]    # MQ : ( [action,card,issue] , type )
            issue = msg_decode[2]

            if (action=="lay") and (issue == "OK"):
                card_to_delete = msg_decode[1]  #Server resend the layed card
                player1.remove(card_to_delete)
                print("Good job ! One less card.")
            elif (action=="last") and (issue == "OK"):
                print("!! YOU WIN !! Congratulations.")
                break
            else:
                picked_card, pile_update = pick(pile)
                player1.append(picked_card[0])
                semaphore_pile.acquire()
                sm_pile.write(pickle.dumps(pile_update))
                semaphore_pile.release()
                print("Shit.... One more.")


if __name__ == '__main__':

    sm_pile = sysv_ipc.SharedMemory(key1)   # SM : [pile]
    sm_board = sysv_ipc.SharedMemory(key2)   # SM : [board]
    semaphore_pile = sysv_ipc.Semaphore(key3)
    semaphore_board = sysv_ipc.Semaphore(key4)
    # try:
    #     sm_pile = sysv_ipc.SharedMemory(key1)   # SM : [pile]
    # except:
    #     print("Can not access to shared memory ", key1, ", terminating.")
    #     sys.exit(1)
    # try:
    #     sm_board = sysv_ipc.SharedMemory(key2)   # SM : [board]
    # except ExistentialError:
    #     print("Can not access to shared memory ", key2, ", terminating.")
    #     sys.exit(1)

    semaphore_pile.acquire()
    read_data = sm_pile.read() #Read in the shared memory
    semaphore_pile.release()
    pile = pickle.loads(read_data) #Decode bytes

    player1, pile_update = distribution(pile)
    semaphore_pile.acquire()
    sm_pile.write(pickle.dumps(pile_update))
    semaphore_pile.release()

    print("----------------------")
    print("Your distribution is : ",player1)
    print("----------------------")

    thread1 = threading.Thread(target=listen_mq,args=(semaphore_pile,semaphore_board,))
    thread2 = threading.Thread(target=press_key,args=(semaphore_board,))

    thread1.start()
    thread2.start()

    while True:
        pass

    sys.exit()





    # x[0] = ('green',99)
    #
    # y = pickle.dumps(x)
    # sm.write(y)



#Le premier player qui reçoit le message le supprimer => il faut que le type soit le pid de destination
#if t == pid:

#    action = msg[0]

#    if action == 1: #Player lay a card
