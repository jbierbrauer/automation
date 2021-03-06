#!/usr/bin/python

# funktioniert auch in Python3 (da Tabs und Space Indents angepasst wurden. Python2 meckert dort nicht)

import time
import stomp
import sys
import socket
import random

# stomp.Connection10() besagt, dass eine Verbindung mit Stomp Protokollversion 1.0 auf Localhost aufgebaut werden soll
# stomp.Connection12() steht somit fuer Version 1.2 des Protokolls. 
# stomp.Connection12([('127.0.0.1',61613)]) ist also identisch mit stomp.Connection12()

def send2queue( targethost='localhost', targetqueue='mytestqueue'  ):   
# gethostbyname funktioniert nur mit fqdn-notation. ein einfacher hostnam zu fehlern
	targetip=str(socket.gethostbyname(targethost))
	print('Zielbroker:' + targetip)
	nachricht=str(random.random())
	conn=stomp.Connection10([(targetip,61613)])
#	conn=stomp.Connection12([('127.0.0.1',61613)])
	conn.start()
	conn.connect()
#	conn.send(str(targetqueue),'Hello World... ehrm Queue')
	conn.send(str(targetqueue),nachricht)
	print ('Nachricht gesendet:'+nachricht)
	conn.disconnect()
	return


class App():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/tmp/smalldaemin.pid'
        self.pidfile_timeout = 5
        # Aaengig von der Anzahl von Argu wird entweder nur der Zielhost oder der Zielhost und die Zielqueue oder der Zielhost, die Zielqueue und die Anzahl der Nachrichten angegeben
        global runs, zielhost,zielqueue
        runs=5  
        print(sys.argv)
        if len(sys.argv)==1: 
            runs=5
            zielqueue='mytestqueue'
            zielhost='localhost'
            print("No guments given")
            exit()

        if len(sys.argv)==4:
            runs=int(sys.argv[3])
            zielqueue=str(sys.argv[2])
            zielhost= str(sys.argv[1])
        elif len(sys.argv)==3:
            zielqueue=str(sys.argv[2])
            zielhost=str(sys.argv[1])
            runs=5
        else:
            zielhost=str(sys.argv[1])
            zielqueue='mytestqueue'
            runs=5
        


    def run(self):
        i=1
        durchlauf=runs
        while durchlauf>0:
            print("Sende zufaellige Nachricht. Iteration:"+str(i))
            send2queue(targethost=zielhost,targetqueue=zielqueue)
            time.sleep(0.3)
            durchlauf=durchlauf-1
            i=i+1
        print('Game Over')
        exit()       
 
app = App()
app.run()
