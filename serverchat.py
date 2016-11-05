import sys
import socket
import time
import multiprocessing
import _tkinter
import tkinter
from tkinter import *

server = Tk()
server.geometry('600x500')

def qhndlr():
        if not q.empty():
                msg = q.get()
                addr = q.get()
                servcore(msg, addr)
        server.after(100, qhndlr)
def sockthread():
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        c.bind(('', tcp))
        while True:
                c.listen(5)
                d, addr = c.accept()
                data = str(d.recv(2048).decode())
                q.put(data)
                q.put(addr[0])
def broadhndlr():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.bind(('', udp))
        while True:
                data, addr = s.recvfrom(1024)
                time.sleep(0.1)
                #name = str(servname.get())
                name = 'test'
                s.sendto(name.encode(), (addr[0], udp))
def servcore(data, host):
        if data[0:2] == '-c':
                usrtable.append(host)
                sender(data[3:] + ' Has connected to the server')
        if data[0:2] == '-d':
                y = 0
                for x in usrtable:
                        if x == host:
                                usrtable.delete[y]
                                break
                        y = y + 1
                sender(data[3:] + 'Has disconnected')
        if data[0:1] != '-':
                for x in usrtable:
                        if x == host:
                                sender(data)
def sender(msg):
        a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        a.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        for x in usrtable:
                if x == 'localhost':
                        chatbox.insert(END, msg)
                else:
                        a.connect((x, tcp))
                        a.sendall(msg.encode())
                        a.close
global udp
udp = 14196
global tcp
tcp = 14197
global tcpcli
tcpcli = 14198
global usrtable
usrtable = ['localhost']

global servname
servname = Entry(server, width=19)
servname.grid(row=0, column=1, sticky=N)

global chatbox
chatbox = Listbox(server, width=50, height=25)
chatbox.grid(row=0, column=0, rowspan=4)

global q
q = multiprocessing.Queue()
t0 = multiprocessing.Process(target=sockthread)
t1 = multiprocessing.Process(target=broadhndlr)
t0.start()
t1.start()

server.after(100, qhndlr)
server.mainloop()

'''
Cleanup notes:
        - sys module may not be required
        - Uneccessary return statements
        - Remove double brackets, test if they are necessary
'''
