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
global slow
global targetip

slow=False
debug_me=False
targetip='0.0.0.0'
names={'127.0.0.1':'localhost'}

ipadresse=re.compile('^[1-9][0-9][0-9]?.[1-2]?[0-9]?[0-9].[1-2]?[0-9]?[0-9]?.[1-2]?[0-9]?[0-9]$')

def arg2globals(slow,debug_me):
   # umwandeln von den befehlszeilenargumenten in globale variablen
   # Anzahl der uebergebenen Argumente wird in argcount gespeichert
   argcount=len(sys.argv)
   targetip='0.0.0.0'
   for i in range(1,argcount):
       if debug_me:
          print "Ueberpruefe Argument Nr.%s = %s"%(i,sys.argv[i])
       if (sys.argv[i]=='-d'): 
          debug_me=True
          print "Debug on (-d)"
       if (sys.argv[i]=='-s'): 
          slow=True
          print "Slow on (-s)"
       if (ipadresse.match(sys.argv[i])): 
          targetip=sys.argv[i]
          print "Zieladresse gesetzt auf: "+sys.argv[i]
   if (targetip=='0.0.0.0'):
       targetip=socket.gethostbyname(socket.gethostname())          
   if debug_me:
      print "Targetip: %s, lahm: %s debug? %s"% (targetip, str(slow), str(debug_me))
   return targetip, slow, debug_me 



def fancyoutput(ipliste,nogolist,namensliste, debug_me):
#  huebschere Ausgabe der IP-Adressen (anstatt jede einzeln auszugeben)
   ipcount=len(ipliste) 
   if (debug_me): print "Im DNS vermerkte Adressen:"+str(nogolist)
   print 'Anzahl nicht auf Ping antwortende Adressen:'+str(ipcount)
   for i in range(0,ipcount):
       if ipliste[i] in nogolist:
                 print "Nr."+str((i+1))+" => "+ipliste[i]+" (im DNS jedoch an "+str(namensliste[ipliste[i]])+" vergeben )"

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

def mpingclassc(subnet, debug_me):
   print "Nutze mping-Modul fuer schnellere Verarbeitung der Pings "
   if (debug_me==True):
      print "angegebene Adresse: "+subnet
   tmp=subnet.split('.')

   subnetaddress=tmp[0]+'.'+tmp[1]+'.'+tmp[2]+'.0'
   subnet_ohne_hostadresse=tmp[0]+'.'+tmp[1]+'.'+tmp[2]+'.'
   targetaddresses=['127.0.0.1',]
   dnstaken=['',]
   names={(subnetaddress):'Subnetz'}
   if (debug_me==True):
       print "Betrete for-Schleife"
   for ping in range(1,254):
       currentaddress=subnet_ohne_hostadresse+str(ping)
       fqdn='not resolved'
       try: 
          if (debug_me==True):
             print "Versuche Aufloesung von ..."+str(currentaddress)
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
       print "DNS-Tabelle names: "+str(names)    
   pings=MultiPing(targetaddresses)
   pings.send()
   time.sleep(2)   
   responses, no_responses = pings.receive(2) 
   if debug_me==True:
       for addr, rtt in responses.items():
          print "%s antwortete in %f sekunden" % (addr,rtt)
   if no_responses:
          fancyoutput(no_responses,dnstaken,names,debug_me)
          if (debug_me):
             print "Diese Adressen antworten nicht auf Ping: %s" % ", ".join(no_responses)

#  print names

names={'127.0.0.1':'localhost'}
targetip='0.0.0.0'
slow=False
debug_me=False

targetip, slow, debug_me = arg2globals(slow,debug_me)

if debug_me:
   print "Debug_mode:"+str(debug_me)

if len(sys.argv) < 2 :
       print 'kein Argument angegeben, verwende lokales Subnetz'
       print 'moegliche Argumente sind <IP-Adresse>, z.B. 192.168.3.1 und der Schalter -s zum erzwingen der langsameren Pingmethode'
#      print sys.argv[0]
       if debug_me:
          print "targetip: "+targetip
       if slow==False and use_mping==True:
          mpingclassc(str(targetip), debug_,e)
       else:
          pingclassc(str(targetip))
       exit()

if len(sys.argv) > 1:
       if debug_me: print "Mehr als ein Argument"
       if slow==False and use_mping==True:
          if debug_me: print "Weder Slow, noch use_mping=False"
          mpingclassc(str(targetip), debug_me)
       else:
          pingclassc(str(targetip))
          exit()
#      print 'Argument ist keine IP-Adresse!'
       exit() 

