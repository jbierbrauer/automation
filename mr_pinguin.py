#!/usr/bin/python

import subprocess
import sys
import socket
import re 
import time
import imp

try:
    imp.find_module('multiping')
    found = True
    use_mping=True
    from multiping import MultiPing
except ImportError:
    found = False
    use_mping=False

global debug_me
global names
debug_me=False
names={'127.0.0.1':'localhost'}

ipadresse=re.compile('^[1-9][0-9][0-9]?.[1-2]?[0-9]?[0-9].[1-2]?[0-9]?[0-9]?.[1-2]?[0-9]?[0-9]$')

def fancyoutput(ipliste,nogolist):
#  huebschere Ausgabe der IP-Adressen (anstatt jede einzeln auszugeben)
   ipcount=len(ipliste) 
   if (debug_me): print "Im DNS vermerkte Adressen:"+str(nogolist)
   print 'Anzahl freie Adressen:'+str(ipcount)
   for i in range(0,ipcount):
       if ipliste[i] in nogolist:
                 print "Nr."+str((i+1))+" => "+ipliste[i]+" (im DNS jedoch vergeben )"

       else:
                 print "Nr."+str((i+1))+" => "+ipliste[i]





def pingclassc(subnet):
   print "Nutze alte langsamere Methode fuer Pings, da multiping-Modul nicht installiert ist"
   tmp=subnet.split('.')
   print "tmp ist gleich :"+str(tmp)
   subnetaddress=tmp[0]+'.'+tmp[1]+'.'+tmp[2]+'.0'
   subnet_ohne_hostadresse=tmp[0]+'.'+tmp[1]+'.'+tmp[2]+'.'

#  names={(subnetaddress):'Subnetz'}

   for ping in range(1,254):
       currentaddress=subnet_ohne_hostadresse+str(ping)
       print 'IP: '+currentaddress
       fqdn='not resolved'
       try: 
          fqdn, alias, addresslist=socket.gethostbyaddr(currentaddress)
          names.update({currentaddress:fqdn})
       except socket.herror:
          # print "Error resolving Name for Address"
          fqdn='Error resolving Name for address '+str(currentaddress)
       print 'FQDN: '+str(fqdn)
       res = subprocess.call(['ping', '-c', '1', str(currentaddress)])
       if res == 0:
           print "\033[91mping to", currentaddress, "OK. Address not available\033[0m"
       elif res == 2:
           print "no response from", currentaddress
       else:
           print "\033[92m ping to", currentaddress, "failed! Address available\033[0m"


#   print names

# pingclassc ends here

def mpingclassc(subnet):
   print "Nutze mping-Modul fuer schnellere Verarbeitung der Pings "
   tmp=subnet.split('.')
#  print "tmp ist gleich :"+str(tmp)
   subnetaddress=tmp[0]+'.'+tmp[1]+'.'+tmp[2]+'.0'
   subnet_ohne_hostadresse=tmp[0]+'.'+tmp[1]+'.'+tmp[2]+'.'
   targetaddresses=['127.0.0.1',]
   dnstaken=['',]
   names={(subnetaddress):'Subnetz'}

   for ping in range(1,254):
       currentaddress=subnet_ohne_hostadresse+str(ping)
       fqdn='not resolved'
       try: 
          fqdn, alias, addresslist=socket.gethostbyaddr(currentaddress)
          names.update({currentaddress:fqdn})
          dnstaken.append(currentaddress)
       except socket.herror:
          # print "Error resolving Name for Address"
          if (debug_me): 
             fqdn='Error resolving Name for address '+str(currentaddress)
       if fqdn!='not resolved' and (debug_me):
          print 'FQDN: '+str(fqdn)+"("+currentaddress+")"
       
       targetaddresses.append(currentaddress)
       
   if (debug_me):
       print "Inhalt von targetaddresses:"
       print targetaddresses    
   pings=MultiPing(targetaddresses)
   pings.send()
   time.sleep(2)   
   responses, no_responses = pings.receive(2) 
   if debug_me==True:
       for addr, rtt in responses.items():
          print "%s antwortete in %f sekunden" % (addr,rtt)
   if no_responses:
          fancyoutput(no_responses,dnstaken)
          if (debug_me):
             print "Diese Adressen antworten nicht auf Ping: %s" % ", ".join(no_responses)

#  print names

if len(sys.argv) < 1:
       print "keine Argumente angegeben"
       exit()
if len(sys.argv) < 2 :
       print 'kein Argument angegeben, verwende lokales Subnetz'
       print 'moegliche Argumente sind <IP-Adresse>, z.B. 192.168.3.1 und der Schalter -s zum erzwingen der langsameren Pingmethode'
#      print sys.argv[0]
       # finde lokale IP-Adresse, um diese fuer das zu durchsuchende Subnetz zu verwenden
       localip=socket.gethostbyname(socket.gethostname())          
       print "lokale Adresse: "+localip

       if ipadresse.match(localip) and use_mping==True:
           mpingclassc(str(localip))
       else:
          pingclassc(str(localip))
       exit()

if len(sys.argv) == 2:
       if ipadresse.match(str(sys.argv[1])) and use_mping==True:
          mpingclassc(str(sys.argv[1]))
       else:
          pingclassc(str(sys.argv[1]))
          exit()
#      print 'Argument ist keine IP-Adresse!'
       exit() 

if len(sys.argv) > 3:
       print 'zu viele Argumente. Eines reicht ;)'
       exit()

if len(sys.argv) > 2:
       print 'Nur ein Argument (IP-Adresse) benoetigt' 
       
       if sys.argv[1]=='-s' and ipadresse.match(str(sys.argv[2])):
          pingclassc(str(sys.argv[2]))
          exit() 
        
       if sys.argv[2]=='-s' and ipadresse.match(str(sys.argv[1])):
          pingclassc(str(sys.argv[1]))
          exit()
       else:    
          exit()

