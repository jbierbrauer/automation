#!/usr/bin/python
import time

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
            time.sleep(5)

app = App()
app.run()
