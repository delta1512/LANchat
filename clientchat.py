import sys
import socket
import time
import multiprocessing
import random
import _tkinter
import tkinter
from tkinter import *

client = Tk()
client.geometry('730x500')

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
def broadhndlr():
        serverlist.delete(0, END)
        servers = []
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        t = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        t.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        port = 14196
        broad = 'ping'
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
def connectf():
        refreshf()
        serverfound = False
        global servaddr
        select = serverselect.get()
        for x in range(0, len(servlist)):
                if str(servlist[x][0]) == str(select):
                        servaddr = servlist[x][1]
                        usrname = namein.get()
                        if usrname == '':
                                y = random.randint(0, len(randomnames))
                                usrname = randomnames[y]
                                comm('Username box empty, using random name: ' + usrname, 'localhost')
                        comm('-c ' + str(usrname) + ':', servlist[x][1])
                        serverfound = True
                        break
        if not serverfound:
                comm('Server not found. Try refreshing or check spelling', 'localhost')
        return
def disconnectf():
        usrname = namein.get()
        if usrname == '':
                y = random.randint(0, len(randomnames))
                usrname = randomnames[y]
                comm('Username box empty, using random name: ' + usrname, 'localhost')
        comm('-d ' + str(usrname), servaddr)
        return
def refreshf():
        global servlist
        servlist = broadhndlr()
        for x in range(0, len(servlist)):
                serverlist.insert(END, str(servlist[x][0]))
        return
def sendf():
        msg = msgbox.get()
        usrname = namein.get()
        if usrname == '':
                y = random.randint(0, len(randomnames))
                usrname = randomnames[y]
                comm('Username box empty, using random name: ' + usrname, 'localhost')
        #do something that limits the amount of characters
        comm(usrname + ': ' + msg, servaddr)
        return
def comm(data, addr):
        a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        a.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        port = 14197
        a.connect((addr, port))
        a.sendall(data.encode())
        a.close()
        return

global serverlist
serverlist = Listbox(client, width=20, height=15)
serverlist.grid(row=0, column=0, sticky=N)
labela = Label(client, text='Select server:').grid(row=1, column=0, sticky=N)
global serverselect
serverselect = Entry(client, width=19)
serverselect.grid(row=2, column=0, sticky=N)
connect = Button(client, text='Connect', width=17, command=lambda: connectf()).grid(row=3, column=0, sticky=N)
disconnect = Button(client, text='Disconnect', width=17, command=lambda: disconnectf()).grid(row=4, column=0, sticky=N)
refresh = Button(client, text='Refresh servers', width=17, command=lambda: refreshf()).grid(row=5, column=0, sticky=N)

global chatbox
chatbox = Listbox(client, width=50, height=25)
chatbox.grid(row=0, column=1, rowspan=5)
global msgbox
msgbox = Entry(client, width=35)
msgbox.grid(row=5, column=1, sticky=W)
send = Button(client, text='Send', width=10, command=lambda: sendf()).grid(row=5, column=1, sticky=SE)

labelb = Label(client, text='Username:').grid(row=0, column=2, sticky=N)
global namein
namein = Entry(client, width=19)
namein.grid(row=0, column=2, sticky=N, pady=20)

global q
q = multiprocessing.Queue()
t = multiprocessing.Process(target=sockthread)
t.start()

global randomnames
randomnames = ['Bob', 'JohnSmith', 'Chad', 'Stacy',
               'Anon', 'Robot#2195', 'RandomName#482',
               'xxHaxorz420xx', 'Doggo', 'Catto']

client.after(100, qhndlr)
client.mainloop()

'''
Cleanup notes:
        - Remove double brackets, test if they are necessary
        - Uneccessary return statements
        - Only use one socket object for broadcast
        - Change socket vars to a, b, c...
        - Global var for UDP and TCP port number
        - t.close() (ln: 29) shouldn't exist but test first
        - sys module may not be required
'''
