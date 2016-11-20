import sys
import socket
import time
import multiprocessing
import random
import _tkinter
import tkinter
from tkinter import *

client = Tk()
client.geometry('820x500')

def qhndlr():
        if not q.empty():
                msg = q.get()
                chatbox.insert(END, msg)
        client.after(100, qhndlr)
def sockthread():
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        port = 14197
        c.bind(('', port))
        while True:
                c.listen(5)
                d, addr = c.accept()
                data = str(d.recv(2048).decode())
                q.put(data)
                d.close()
def broadhndlr():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udp = 14196
        s.bind(('', udp))
        while True:
                data, addr = s.recvfrom(1024)
                print(data)
                if data.decode() == socket.gethostname():
                        pass
                else:
                        time.sleep(0.1)
                        name = 'test'
                        s.sendto(name.encode(), (addr[0], udp))
def broadacc():
        serverlist.delete(0, END)
        servers = []
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        t = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        t.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        port = 14196
        broad = socket.gethostname()
        s.sendto(broad.encode(), ('224.0.0.1', port))
        s.close()
        t.bind(('', port))
        t.settimeout(3)
        while True:
                try:
                        data, addr = t.recvfrom(1024)
                except:
                        break
                servinfo = [data.decode(), addr[0]]
                servers.append(servinfo)
        return servers
def refreshf():
        global servlist #may be unnecessary if defined outside of function
        servlist = broadacc()
        for x in range(0, len(servlist)):
                serverlist.insert(END, str(servlist[x][0]))
        return
def sendf():
        msg = msgbox.get()
        usrname = namein.get()
        if usrname == '':
                comm('Username box empty, set username to chat with other users', 'localhost')
                #clear function
                return
        #do something that limits the amount of characters
        comm(usrname + ': ' + msg, servaddr)
        #clear function
        return
def comm(data, addr):
        a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        a.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        port = 14197
        a.connect((addr, port))
        a.sendall(data.encode())
        a.close()
        return
def clear(option):
        #basic clear
		#clears based on options
        return

peerlistlb = Label(client, text='Peer list\n(double click)').grid(row=0, column=0)
global serverlist
serverlist = Listbox(client, width=20, height=20) #change to peerlist
serverlist.grid(row=1, column=0, sticky=N)
refresh = Button(client, text='Refresh peers', width=17, command=lambda: refreshf()).grid(row=2, column=0, sticky=N)

global chatbox
chatbox = Listbox(client, width=61, height=26)
chatbox.grid(row=0, column=1, rowspan=3)
tolb = Label(client, text='To:').grid(row=3, column=1, sticky=W)
global peersel
peersel = Listbox(client, width=10, height=1)
peersel.grid(row=3, column=1, sticky=W, padx=25)
global msgbox
msgbox = Entry(client, width=33)
msgbox.grid(row=3, column=1, sticky=W, padx=110)
send = Button(client, text='Send', width=10, command=lambda: sendf()).grid(row=3, column=1, sticky=SE)

labelb = Label(client, text='Username:').grid(row=0, column=2, sticky=N)
global namein
namein = Entry(client, width=19)
namein.grid(row=0, column=2, sticky=N, pady=20)

global q
q = multiprocessing.Queue()
t = multiprocessing.Process(target=sockthread)
t0 = multiprocessing.Process(target=broadhndlr)
t.start()
t0.start()

global randomnames
randomnames = ['Bob', 'JohnSmith', 'Chad', 'Stacy',
               'Anon', 'Robot#2195', 'RandomName#482',
               'xxHaxorz420xx', 'Doggo', 'Catto']

client.after(100, qhndlr)
client.mainloop()
