#!/usr/bin/env python3

#Notes :
# -> () est une expression sous python, (,) est un tuple : d'où args=("Kitty",) = tuple d'ordre 1
# -> __name__ = __main__ seulement si on appelle le script en ligne de commande
# -> join() fait en sorte que le process attend la fin de ses process fils

# print("ok")

from multiprocessing import Process, Value, Array

def fibo(n):
    if n==0:
        return 0
    elif n==1:
        return 1
    else :
        return (fibo(n-1)+fibo(n-2))

def fibo_process(n):
    lst=[]
    while i < n :
        lst.append(fibo(i))

if __name__ == "__main__":
    number = 
    p = Process(target=fibo_process, args=(number,))
    p.start()
    p.join()
