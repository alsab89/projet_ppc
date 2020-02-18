#!/usr/bin/env python3

from multiprocessing import Process, Pipe

def f(conn):
    msg = input("Ecrire message : ")
    conn.send([42, None, msg])
    conn.close()

if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p = Process(target=f, args=(child_conn,))
    p.start()
    print(parent_conn.recv())   # prints "[42, None, 'hello']"
    p.join()
