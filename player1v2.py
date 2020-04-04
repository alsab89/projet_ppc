#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import random, sys, os, pygame, sysv_ipc, pickle
from pygame.locals import *

# ----------------------- Constants ------------------------------

COLON = 108  #5 colons => 216 px per colon
LINE = 90  #4 lines => 180 px per line

key = 516
key1 = 527
key2 = 538
key3 = 549
key4 = 551
pid = os.getpid()

# ----------------------- Functions ------------------------------

class card_board(pygame.sprite.Sprite):   #The card on the board, an object
    def __init__(self,color,number):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("./divers/"+color+"_"+number+".jpg")
        self.rect=self.image.get_rect()
        self.rect.centerx=3*COLON #middle of the screen
        self.rect.top=90 #first line

class card(pygame.sprite.Sprite):   #Each card will be an object displayed on the screen
    def __init__(self,lin,col,color,number):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("./divers/"+color+"_"+number+".jpg")
        self.rect=self.image.get_rect()
        self.rect.centerx=col*COLON #col = col+270
        self.rect.top=lin*LINE #lin = lin+180

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

# ----------------------- Pygame code ------------------------------

def display():

    #Change background
    fond = pygame.image.load("./divers/wallpaper.jpg").convert()
    fond = pygame.transform.scale(fond,size)
    screen.blit(fond, (0,0))  #We paste the image in the window
    hello_msg = pygame.image.load("./divers/banner.jpg").convert()
    screen.blit(hello_msg, (0,0))

    print("----------------------")
    print("Your distribution is : ",player)
    print("----------------------")

    semaphore_board.acquire()
    board_card = pickle.loads(sm_board.read())
    semaphore_board.release()

    board_color=board_card[0]
    board_number=board_card[1]
    board_card=card_board(board_color,board_number)
    groupe_board.add(board_card) #We superpose the new object each time, but that's not a problem..

    groupe_cards.update() #Each card is updated and drawn on the screen
    groupe_board.update()
    groupe_cards.draw(screen)
    groupe_board.draw(screen)

    # Screen actualization
    pygame.display.flip()


def press_key():

    clock = pygame.time.Clock()
    while True:
        clock.tick(15) # Loop is repeating each 15 seconds
        # Event detection :
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN: #a mouse click
                print("Mouse detected ...")
                x,y = pygame.mouse.get_pos() #we get the click's position on the screen
                for card_check in groupe_cards:
                    which_card = card_check.get_rect()
                    if which_check.rect.collidepoint(x,y):
                        #groupe_cards.remove(card_check)
                        print("ok")
            elif event.type == pygame.KEYDOWN: # C'est une touche clavier
                if event.key == pygame.K_ESCAPE:
                    print("End of the game. Goodbye.")
                    sys.exit()      # Sortie du jeu
                elif event.key == pygame.K_RIGHT:
                    print("droite")


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

    thread1 = threading.Thread(target=listen_mq,args=(semaphore_pile,semaphore_board,)) #MQ management
    thread2 = threading.Thread(target=press_key,args=(semaphore_board,)) #Keyboard entries management

    thread1.start()
    thread2.start()

    while True:
        pass

    sys.exit()
