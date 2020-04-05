# PROJET PPC

Ahmed Haouchette & Alem Sabanovic - 3TCA

## Start

Ce dépôt est public ; si vous souhaitez tester le code directement sur votre machine, exécuter la commande suivante (vérifier que l'URL n'a pas changé) :

```
git clone https://github.com/alsab89/projet_ppc.git
```

Un répertoire sera crée sur votre machine. Il faut un compte GitHub au préalable.

## Usage

Il y a 3 fichiers et 1 dossier utiles pour lancer le jeu :
  - server.py
  - player1.py
  - player2.py (=player1)
 -> player3.py est une version du jeu sur terminal

Codé en python3.6
Exécuté de la façon suivante :

```
python3 ./server.py
```

!! Selon vos ressources, il peut arriver que la taille indiquée en argument dans la création de la shared memory ne correspond pas. !!

### Description

Vous avez deux possibilités dans le jeu :
  - Quitter, en appuyant sur Echap
  - Cliquer sur une carte, pour la poser sur le tapis
  
 3 interruptions possibles :
   - Il n'y a plus de cartes dans la pile
   - Vous avez gagné
   - Votre adversaire a gagné
   
  Une carte sera automatiquement piochée toutes les 5 secondes si vous aucune carte de votre main n'est posée.



