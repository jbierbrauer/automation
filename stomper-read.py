#!/usr/bin/python
import time
#from javax.jms import Session
#from org.apache.activemq import ActiveMQConnectionFactory
import stomp




def readoutloud():
	conn = stomp.Connection10()
	listener = stomp.TestListener()
	conn.set_listener('', listener)
	conn.start()
#	conn.connect(username, password, wait=True)
	conn.subscribe(destination=queue_name, id=1, ack='auto')
	listener.message_list #This can read all the messages from the queue
	headers, message = listener.get_latest_message() #This can read the last message from the queue
	print(message)
	conn.unsubscribe(queue_name)
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
