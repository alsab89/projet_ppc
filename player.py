#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import random, sys, os, pygame, sysv_ipc, pickle, multiprocessing, threading, time
from pygame.locals import *

# ----------------------- Constants ------------------------------

COLON = 196 #216  #5 colons => 216 px per colon
LINE = 155 #180  #4 lines => 180 px per line

key = 516
key1 = 527
key2 = 538
key3 = 549
key4 = 551
pid = os.getpid()
state=True
timer_state=True

# ----------------------- Functions ------------------------------

class card_board(pygame.sprite.Sprite):   #The card on the board, an object
    def __init__(self,color,number):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("/home/user1/Documents/PPC/repogit/divers/"+color+"_"+str(number)+".JPG")
        self.rect=self.image.get_rect()
        self.rect.centerx=(3*COLON)-(COLON/2) #middle of the screen
        self.rect.top=(1*LINE)-LINE+50  #second line
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
        self.image=pygame.image.load("./divers/"+color+"_"+str(number)+".JPG")
        self.rect=self.image.get_rect()
        self.rect.centerx=(col*COLON)-(COLON/2)
        self.rect.top=(lin*LINE)-LINE-20
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

    semaphore_pile.acquire()
    pile_check = pickle.loads(sm_pile.read())
    semaphore_pile.release()
    if len(pile_check)==1:
        fond = pygame.image.load("./divers/lose.png").convert()
        fond = pygame.transform.scale(fond,size)
        screen.blit(fond, (0,0))  #We paste the image in the window
        print("End of the game. No more cards in the pile.")
        global state
        state=False
    else:
        pos = random.randint(0,(len(pile)-1))
        board = pile.pop(pos)
        semaphore_pile.acquire()
        sm_pile.write(pickle.dumps(pile)) #pile update
        semaphore_pile.release()
        return board


def display():

    for card_fetch in groupe_cards:
        groupe_cards.remove(card_fetch)

    for i in range(len(player)):
        if i<=4:
            card_color=player[i][0]
            card_number=player[i][1]
            graphic_card=card(3,i+1,card_color,str(card_number))
            groupe_cards.add(graphic_card)
        else:
            card_color=player[i][0]
            card_number=player[i][1]
            graphic_card=card(4.2,i-4,card_color,str(card_number))
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
    fond = pygame.image.load("./divers/wallpaper.jpg").convert()
    fond = pygame.transform.scale(fond,size)
    screen.blit(fond, (0,0))  #We paste the image in the window
    hello_msg = pygame.image.load("./divers/banner.JPG").convert()
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

    time_var = 0
    font = pygame.font.SysFont('Consolas', 30)

    global state
    while state:
        clock.tick(15) # Loop is repeating 15 times per second
        # Event detection :
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT: #Each second
                time_var+=1
                text = ">>>> TIMER :"+str(time_var).rjust(10)+" <<<<"
                display()
                screen.blit(font.render(text, True, (255,255,255)), (32,148))
                pygame.display.flip()
                if time_var>=5:
                    picked_card = pick(pile)
                    player.append(picked_card)
                    display()
                    time_var=0
                else:
                    pass
            elif event.type == pygame.KEYDOWN: # C'est une touche clavier
                if event.key == pygame.K_ESCAPE:
                    print("End of the game. Goodbye.")
                    state=False
                    pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN: #a mouse click
                time_var=0
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

def listen_mq():

    try:
        mq = sysv_ipc.MessageQueue(key)
    except:
        print("Can not connect to message queue ", key, ", terminating.")
        sys.exit(1)

    global state
    while state:

        msg, t = mq.receive(type=pid)

        #Le premier player qui reçoit le message le supprimer => il faut que le type soit le pid de destination

        semaphore_pile.acquire()
        pile = pickle.loads(sm_pile.read())
        semaphore_pile.release()

        msg_decode = pickle.loads(msg)
        action = msg_decode[0]    # MQ : ( [action,card,issue] , type ) -> ( [str,[(str,str)],str] , pid ) !! number = str here
        issue = msg_decode[2]

        if (action=="lay") and (issue == "OK"):
            card_to_delete = msg_decode[1]  #Server resend the layed card
            card_color = card_to_delete[0][0]
            card_number = int(card_to_delete[0][1]) #!!
            card_to_delete = (card_color,card_number)
            player.remove(card_to_delete)

            print("Good job ! One less card.")

        elif (action=="last") and (issue == "OK"):
            fond = pygame.image.load("./divers/win.jpg").convert()
            fond = pygame.transform.scale(fond,size)
            screen.blit(fond, (0,0))  #We paste the image in the window
            pygame.display.flip()
            print("!! YOU WIN !! Congratulations.")
            break

        else:
            picked_card = pick(pile)
            player.append(picked_card)

            print("Shit.... One more.")
        display()

    sys.exit()


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

    display()

    # ----------------------- Threads to manage the functions ------------------------------

    thread1 = threading.Thread(target=listen_mq) #MQ management
    thread2 = threading.Thread(target=press_key) #Keyboard entries management

    thread1.start()
    thread2.start()

    pygame.time.set_timer(pygame.USEREVENT, 1000) #We create an event which takes place every seconds

    while state:
        pass

    sys.exit()
