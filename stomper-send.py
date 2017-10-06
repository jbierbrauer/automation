#!/usr/bin/python
import time
import stomp

# stomp.Connection10() besagt, dass eine Verbindung mit Stomp Protokollversion 1.0 auf Localhost aufgebaut werden soll
# stomp.Connection12() steht somit fuer Version 1.2 des Protokolls. 
# stomp.Connection12([('127.0.0.1',62613)]) ist also identisch mit stomp.Connection12()
def send2queue():
	conn=stomp.Connection10()
	conn.start()
	conn.connect()
	conn.send('mytestqueue','Hello World... ehrm Queue')
	conn.disconnect()
	return

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
            send2queue()
            time.sleep(5)

app = App()
app.run()
