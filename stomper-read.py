#!/usr/bin/python3
import time
#from javax.jms import Session
#from org.apache.activemq import ActiveMQConnectionFactory
import stomp
from stomp.listener import TestListener



def readoutloud():
	conn = stomp.Connection12()
	listener = TestListener()
	conn.set_listener('', listener)
#	conn.set_listener('message', ConnectionListener(conn))
#	conn.set_listener('print', PrintingListener())
#	conn.set_listener('stats', StatsListener())
	conn.start()
	conn.connect()
#	conn.connect(username, password, wait=True)
	conn.subscribe(destination='mytestqueue', id=1, ack='auto')
	listener.wait_for_message()
	listener.message_list #This can read all the messages from the queue
#	print(listener.message_list)
	print('Anzahl Elemente:'+str(len(listener.message_list)))
	print('Betrete For-Schleife')
	elementanzahl=len(listener.message_list)
	for i in range(elementanzahl):
	   aktuellenachricht=listener.message_list[i]
	   print(aktuellenachricht)
	   print('Zeitstempel:'+aktuellenachricht[0]['timestamp']+' Nachricht:'+aktuellenachricht[1])


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
    def run(self):
        while True:
            print("warte auf Nachricht...")
            readoutloud()
            time.sleep(2)

app = App()
app.run()
