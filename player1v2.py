#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import random, sys, os, pygame, sysv_ipc, pickle, multiprocessing, threading, time
from pygame.locals import *

# ----------------------- Constants ------------------------------

COLON = 216  #5 colons => 216 px per colon
LINE = 90  #4 lines => 180 px per line

key = 516
key1 = 527
key2 = 538
key3 = 549
key4 = 551
pid = os.getpid()
state=True

# ----------------------- Functions ------------------------------

class card_board(pygame.sprite.Sprite):   #The card on the board, an object
    def __init__(self,color,number):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("/home/user1/Documents/PPC/repogit/divers/"+color+"_"+str(number)+".JPG")
        self.rect=self.image.get_rect()
        self.rect.centerx=3*COLON #middle of the screen
        self.rect.top=90 #first line
        self.color=color
        self.number=number
    def check_click(self,mouse):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True
        else:
            pass
    def get_card(self):
        return self.color,self.number

class card(pygame.sprite.Sprite):   #Each card will be an object displayed on the screen
    def __init__(self,lin,col,color,number):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("/home/user1/Documents/PPC/repogit/divers/"+color+"_"+str(number)+".JPG")
        self.rect=self.image.get_rect()
        self.rect.centerx=col*COLON #col = col+270
        self.rect.top=lin*LINE #lin = lin+180
        self.color=color
        self.number=number
    def check_click(self,mouse):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True
        else:
            pass
    def get_card(self):
        return self.color,self.number

def distribution(pile):  #The player picks 5 cards to compose his hand
    player = []
    for i in range(5):
        pos = random.randint(0,(len(pile)-1))
        player.append(pile.pop(pos)) #pop return value and delete from the list
    return (player,pile)

def pick(pile):
    pos = random.randint(0,(len(pile)-1))
    board = pile.pop(pos)
    return (board,pile)

# ----------------------- Pygame code ------------------------------

def display():

    for card_fetch in groupe_cards:
        groupe_cards.remove(card_fetch)

    for i in range(len(player)):
        card_color=player[i][0]
        card_number=player[i][1]
        graphic_card=card(3,i+1,card_color,str(card_number))
        groupe_cards.add(graphic_card)
        i+=1

    #Change background
    fond = pygame.image.load("/home/user1/Documents/PPC/repogit/divers/wallpaper.jpg").convert()
    fond = pygame.transform.scale(fond,size)
    screen.blit(fond, (0,0))  #We paste the image in the window
    hello_msg = pygame.image.load("/home/user1/Documents/PPC/repogit/divers/banner.JPG").convert()
    screen.blit(hello_msg, (0,0))

    groupe_cards.update() #Each card is updated and drawn on the screen
    groupe_board.update()
    groupe_cards.draw(screen)
    groupe_board.draw(screen)

    # Screen actualization
    pygame.display.flip()

def display_board():

    for card_fetch in groupe_cards:
        groupe_cards.remove(card_fetch)

    for i in range(len(player)):
        card_color=player[i][0]
        card_number=player[i][1]
        graphic_card=card(3,i+1,card_color,str(card_number))
        groupe_cards.add(graphic_card)
        i+=1

    for board_fetch in groupe_board:
        groupe_board.remove(board_fetch)

    semaphore_board.acquire()
    board_card = pickle.loads(sm_board.read())
    semaphore_board.release()

    board_color=board_card[0][0]
    board_number=board_card[0][1]
    board_card=card_board(board_color,board_number)
    groupe_board.add(board_card)

    #Change background
    fond = pygame.image.load("/home/user1/Documents/PPC/repogit/divers/wallpaper.jpg").convert()
    fond = pygame.transform.scale(fond,size)
    screen.blit(fond, (0,0))  #We paste the image in the window
    hello_msg = pygame.image.load("/home/user1/Documents/PPC/repogit/divers/banner.JPG").convert()
    screen.blit(hello_msg, (0,0))

    groupe_cards.update() #Each card is updated and drawn on the screen
    groupe_board.update()
    groupe_cards.draw(screen)
    groupe_board.draw(screen)

    # Screen actualization
    pygame.display.flip()


def press_key():

    mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)

    pid = os.getpid()
    clock = pygame.time.Clock()

    while True:
        clock.tick(15) # Loop is repeating each 15 seconds
        # Event detection :
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN: # C'est une touche clavier
                if event.key == pygame.K_ESCAPE:
                    #sys.exit()      # Sortie du jeu
                    print("End of the game. Goodbye.")
                    global state
                    state=False
                    break
            elif event.type == pygame.MOUSEBUTTONDOWN: #a mouse click
                if len(player)==1:
                    for card_check in groupe_cards:
                        if card_check.check_click(event.pos):
                            card_color,card_number=card_check.get_card()
                            card_to_lay=(card_color,card_number)
                            info = ["last",pid,[card_to_lay]]    # MQ : ( [action,player,card] , type )
                            msg = pickle.dumps(info)
                            mq.send(msg, type=1)
                else:
                    for card_check in groupe_cards:
                        if card_check.check_click(event.pos):
                            card_color,card_number=card_check.get_card()
                            card_to_lay=(card_color,card_number)
                            info = ["lay",pid,[card_to_lay]]    # MQ : ( [action,player,card] , type )
                            msg = pickle.dumps(info)
                            mq.send(msg, type=1)

def listen_mq(semaphore_pile,semaphore_board):

    try:
        mq = sysv_ipc.MessageQueue(key)
    except:
        print("Can not connect to message queue ", key, ", terminating.")
        sys.exit(1)

    while True:

        msg, t = mq.receive(type=pid)

        #Le premier player qui reçoit le message le supprimer => il faut que le type soit le pid de destination

        semaphore_pile.acquire()
        pile = pickle.loads(sm_pile.read())
        semaphore_pile.release()

        msg_decode = pickle.loads(msg)
        action = msg_decode[0]    # MQ : ( [action,card,issue] , type ) -> ( [str,[(str,str)],str] , pid ) !! number = str here
        issue = msg_decode[2]

        print(action,issue)
        if (action=="lay") and (issue == "OK"):
            card_to_delete = msg_decode[1]  #Server resend the layed card
            card_color = card_to_delete[0][0]
            card_number = int(card_to_delete[0][1]) #!!
            card_to_delete = (card_color,card_number)
            player.remove(card_to_delete)

            print("Good job ! One less card.")
            display_board()

        elif (action=="last") and (issue == "OK"):
            print("!! YOU WIN !! Congratulations.")
            global state
            state=False
            break
            #sys.exit()

        else:
            picked_card, pile_update = pick(pile)
            player.append(picked_card)
            print(player)

            semaphore_pile.acquire()
            sm_pile.write(pickle.dumps(pile_update))
            semaphore_pile.release()

            print("Shit.... One more.")
            display()


if __name__ == '__main__':
    #player1 = [('blue', 10), ('red', 8), ('blue', 3), ('red', 10), ('red', 4)]

    # ----------------------- Client code ------------------------------

    sm_pile = sysv_ipc.SharedMemory(key1)   # SM : [pile]
    sm_board = sysv_ipc.SharedMemory(key2)   # SM : [board]
    semaphore_pile = sysv_ipc.Semaphore(key3)
    semaphore_board = sysv_ipc.Semaphore(key4)

    semaphore_pile.acquire()
    read_data = sm_pile.read() #Read in the shared memory
    semaphore_pile.release()
    pile = pickle.loads(read_data) #Decode bytes

    player, pile_update = distribution(pile)
    semaphore_pile.acquire()
    sm_pile.write(pickle.dumps(pile_update))
    semaphore_pile.release()

    # ----------------------- Pygame code ------------------------------

    # Library initialization and some parameters
    pygame.init()
    size = width, height = 1080, 720 #Screen size
    black = 0, 0, 0   #Default background

    #Window game dimension
    screen = pygame.display.set_mode(size)

	#Window game title
    pygame.display.set_caption("Uno is Bueno - Stay at home")

    groupe_cards = pygame.sprite.Group() #We create and add each object in a group of objects
    for i in range(5):
        card_color=player[i][0]
        card_number=player[i][1]
        graphic_card=card(3,i+1,card_color,str(card_number))
        groupe_cards.add(graphic_card)
        i+=1

    groupe_board = pygame.sprite.Group()

    display_board()

    # ----------------------- Threads to manage the functions ------------------------------

    thread1 = threading.Thread(target=listen_mq,args=(semaphore_pile,semaphore_board,)) #MQ management
    thread2 = threading.Thread(target=press_key) #Keyboard entries management

    thread1.start()
    thread2.start()

    while state:
        pass

    sys.exit()
