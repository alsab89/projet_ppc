#!/usr/bin/env python3

#Notes :
# -> () est une expression sous python, (,) est un tuple : d'où args=("Kitty",) = tuple d'ordre 1
# -> __name__ = __main__ seulement si on appelle le script en ligne de commande
# -> join() fait en sorte que le process attend la fin de ses process fils

# print("ok")

from multiprocessing import Process
import time

def fibo(n):
    if n==0:
        return 0
    elif n==1:
        return 1
    else :
        return (fibo(n-1)+fibo(n-2))

def fibo_process(n):
    for i in range (n):
        print(fibo(i))
        time.sleep(3)


# print(fibo(7))
# print(fibo_process(7))

if __name__ == "__main__":
    p = Process(target=fibo_process, args=(7,))
    #q = Process(target=fibo_process, args=(7,))  -> On voit un process en plus avec ps ax
    p.start()
    #q.start()
    p.join()
    #q.join()
