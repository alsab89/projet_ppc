#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import random, sys, os, pygame, sysv_ipc, pickle
from pygame.locals import *

COLON = 170
LINE = 385

key = 111


class card(pygame.sprite.Sprite):
    def __init__(self,lin,col,color,number):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("/mnt/c/Users/alem-/Desktop/Dossiers d'école/TCA/PPC/Projet/divers/"+color+"_"+number+".jpg")
        self.rect=self.image.get_rect()
        self.rect.centerx=(col*COLON)+120
        self.rect.top=lin*LINE


def distribution(pile):  #The player picks 5 card to compose his hand
    player = []
    for i in range(5):
        pos = random.randint(0,(len(pile)-1))
        player.append(pile[pos])
        del pile[pos]
    return (player,pile)

def main():
    # Initialisation de la librairie et de quelques paramètres
    pygame.init()
    size = width, height = 800, 600
    black = 0, 0, 0

    screen = pygame.display.set_mode(size)

	#Titre
    pygame.display.set_caption("Uno is Bueno - Stay at home")

	#Chargement et collage du fond
    fond = pygame.image.load("/mnt/c/Users/alem-/Desktop/Dossiers d'école/TCA/PPC/Projet/divers/wallpaper.jpg").convert()
    fond = pygame.transform.scale(fond,size)
    screen.blit(fond, (0,0))
    hello_msg = pygame.image.load("/mnt/c/Users/alem-/Desktop/Dossiers d'école/TCA/PPC/Projet/divers/banner.jpg").convert()
    screen.blit(hello_msg, (0,0))

    print("----------------------")
    print("Your distribution is : ",player1)
    print("----------------------")
    
    groupe_cards = pygame.sprite.Group()
    for i in range(5):
        x=player1[i][0]
        y=player1[i][1]
        graphic_card=card(1,i,x,str(y))
        groupe_cards.add(graphic_card)
        i+=1
    
    #Boucle principale 
    clock = pygame.time.Clock()
    while 1:
        clock.tick(15) # La boucle se répète 15 fois par sec
		# Détection d'un événement (clic souris ou appui touche clavier) :
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN: #c'est un clic souris
                print("Mouse detected ...")
            elif event.type == pygame.KEYDOWN: # C'est une touche clavier
                if event.key == pygame.K_ESCAPE:
                    print("End of the game. Goodbye.")
                    sys.exit()      # Sortie du jeu
                elif event.key == pygame.K_RIGHT:
                    print("droite")
    
        #Effacement de l'ancienne image
        screen.blit(fond,(0,0))
        screen.blit(hello_msg, (0,0))
     
        groupe_cards.update()
        groupe_cards.draw(screen)

        # Actualisation de l'écran
        pygame.display.flip()

if __name__ == '__main__':
    #player1 = [('blue', 10), ('red', 8), ('blue', 3), ('red', 10), ('red', 4)]
    
    sm = sysv_ipc.SharedMemory(key)

    rec = sm.read() #Read in the shared memory 
    pile = pickle.loads(rec) #Decode bytes
    print(pile)
    print("----------------------")
    
    player1, pile = distribution(pile)
    # print(player1)
    # print("----------------------")
    print(pile)
    
    main()
 
