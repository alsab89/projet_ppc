# PROJET PPC

Ahmed Haouchette & Alem Sabanovic - 3TCA

## Start

Si vous souhaitez tester le code directement sur votre machine, exécuter la commande suivante (vérifier que l'URL n'a pas changé) :

```
git clone https://github.com/alsab89/projet_ppc.git
```

Un répertoire sera crée sur votre machine. Il faut un compte GitHub au préalable.

## Usage

Il y a 3 fichiers et 1 dossier utiles pour lancer le jeu :
  - server.py
  - player1.py
  - player3.py est une version du jeu sur terminal

Codé en python3.6
Exécuté de la façon suivante :

```
python3 ./server.py
```

!! Selon vos ressources, il peut arriver que la taille indiquée en argument dans la création de la shared memory ne correspond pas. !!

### Description

Vous avez deux possibilités dans le jeu graphique (player.py):
  - Quitter, en appuyant sur Echap
  - Cliquer sur une carte, pour la poser sur le tapis
  
Pour l'implémentation en terminal (player3.py) :
  - La touche Echap pour quitter
  - La touche D pour afficher le board
  - La touche S pour afficher sa main
 Pour choisir une carte à poser, il suffit d'entrer la position de la carte dans la main.
  
 2 interruptions possibles :
   - Il n'y a plus de cartes dans la pile
   - Vous avez gagné
   
  Une carte sera automatiquement piochée toutes les 5 secondes si aucune carte de votre main n'est posée ; attention au timer !
  
  ### Mécanisme
  
  Il y a 2 threads :
    - Un qui gère les entrées clavier
    - Un qui gère la message queue (qui communique avec le process serveur)
    
## Notes
 
Quelquefois, pygame rame un peu ; ne pas hésiter à cliquer plus fort sur une carte (oui c'est un code soviétique) !
 
Nous n'avons pas testé ce que ça donne avec deux joueurs en même temps ; il nous reste à implémenter un MQ pour communiquer quand un des deux joueurs pose une carte bonne, ou gagne. A vous de voir.
    
   


