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
	headers, message = listener.get_latest_message() #This can read the last message from the queue
	print(message)
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
            print("Ich lebe!")
            readoutloud()
            time.sleep(5)

app = App()
app.run()
