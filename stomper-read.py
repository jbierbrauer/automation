#!/usr/bin/python3
import time
import sys
import socket
import datetime
#from javax.jms import Session
#from org.apache.activemq import ActiveMQConnectionFactory
import stomp
from stomp.listener import TestListener

def timestamp2date(timestamp_in_ms):
	# in Python3 wird // anstatt / fuer die Division benoetigt
	timestamp_in_s=int(timestamp_in_ms)//1000.0
	datum=datetime.datetime.fromtimestamp(timestamp_in_s)
	if debug_on==True: print(datum)
	return datum
 
def readoutloud(targethost='localhost'):
	targetip=str(socket.gethostbyname(targethost))
#	conn = stomp.Connection12()
	conn = stomp.Connection12([(targetip,61613)])
	listener = TestListener()
	conn.set_listener('', listener)
#	conn.set_listener('message', ConnectionListener(conn))
#	conn.set_listener('print', PrintingListener())
#	conn.set_listener('stats', StatsListener())
	conn.start()
	conn.connect()
#	conn.connect(username, password, wait=True)
	conn.subscribe(destination='mytestqueue', id=1, ack='auto')
# Es muss nur auf neue Nachrichten gewartet werden, wenn noch keine Nachrichten in der Queue sind	
	if len(listener.message_list)==0: listener.wait_for_message()
	listener.message_list #This can read all the messages from the queue
#	print(listener.message_list)
	print('Anzahl Elemente:'+str(len(listener.message_list)))
	print('Betrete For-Schleife')
	elementanzahl=len(listener.message_list)
	for i in range(elementanzahl):
	   aktuellenachricht=listener.message_list[i]
	   if debug_on==True: print(aktuellenachricht)
	   zeitstempel=timestamp2date(aktuellenachricht[0]['timestamp'])
	   print('Zeitstempel:'+str(zeitstempel)+' Nachricht:'+aktuellenachricht[1])
#	   print('Zeitstempel:'+aktuellenachricht[0]['timestamp']+' Nachricht:'+aktuellenachricht[1])


#	i=0
#	while True:
#	   try:
#	      headers, message = listener.get_latest_message() #This can read the last message from the queue
#	      print(message)
#	      time.sleep(1)
#	   except:
#	      print('Fehler bei get_latest_message()')
#	      break

	conn.unsubscribe('mytestqueue')
	conn.disconnect()   
#	conn.close()

class App():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/tmp/smalldaemin.pid'
        self.pidfile_timeout = 5
        global debug_on, zielhost
        debug_on=False
        if len(sys.argv)==2: 
          zielhost=str(sys.argv[1])
        print(sys.argv)
    def run(self):
        while True:
            print("Frage weitere Nachrichten in 2 Sekunden ab...")
            readoutloud(zielhost)
            time.sleep(1)

app = App()
app.run()
