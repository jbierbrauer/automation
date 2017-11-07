#!/usr/bin/python

import subprocess
import sys
import socket
import re

ipadresse=re.compile('^[1-9][1-9][1-9]?.[1-2]?[1-9]?[1-9].[1-2]?[1-9]?[1-9]?.[1-2]?[1-9]?[0-9]$')

def pingclassc(subnet):
   for ping in range(1,254):
#       address = "127.0.0." + str(ping)
       tmp=subnet.split('.')
       address=tmp[0]+'.'+tmp[1]+'.'+tmp[3]+'.0'
       print 'IP: '+address
       fqdn=socket.gethostbyaddr(address)
       print 'FQDN: '+str(fqdn)
       res = subprocess.call(['ping', '-c', '2', address,'>>/dev/null'])
       if res == 0:
           print "ping to", address, "OK"
       elif res == 2:
           print "no response from", address
       else:
           print "ping to", address, "failed!"

if len(sys.argv) < 2:
       print 'kein Argument angegeben, verwende lokales Subnetz'
       
       pingclassc('192.168.3.1')
       exit()

if len(sys.argv) == 2:
       if ipadresse.match(str(sys.argv[1])):
          pingclassc(str(sys.argv[1]))
          exit()
       
       print 'Argument ist keine IP-Adresse!'
       exit() 

if len(sys.argv) > 2:
       print 'Nur ein Argument (IP-Adresse) benoetigt' 

       exit()

