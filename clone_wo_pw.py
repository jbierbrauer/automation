
# coding: utf8
import os, sys, paramiko
quellvmid=001
zielvmidstart=7000
anzahl=10
zielhost="192.168.0.9" # Standardmäßig verbinden wir uns auf Universum9, kann in Zukunft noch geändert werden
benutzer="root"
passwort="NoneOfUrBusiness"
ssh=paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
befehl="qm clone"

def verifyparameters(a,b,c):
	if a.isdigit & b.isdigit & c.isdigit:
			return True;
	else:
			return False;

print("Hallo zum VM-Klon-Skript:")
print("Ausführung mit Python Version: "+sys.version)
print("Es werden gleich Angaben zur zu klonenenden VM (als VM-ID) und den Ziel-IDs erforderlich. Stelle sicher, dass die Ziel-IDs noch nicht vergeben sind!")

parameterok=False

while parameterok!= True:

	quellvmideingabe=input("Wie ist die ID der zu klonenden VM? (z.B. 102) ")
	zielvmideingabe=input("Mit welcher ID sollen die geklonte VMs beginnen? ")
	anzahleingabe=input("Wie viele Klone werden benötigt ?")
	vmname=raw_input("Wie sollen die neuen VMs heißen? (Zahl wird angehängt)")
	print("Die VM mit der ID %i soll also %i mal geklont werden. Die erstellten Klone fangen mit der ID %i an."%(quellvmideingabe,anzahleingabe,zielvmideingabe)) 
	
	allesokeingabe= raw_input( 'Sind diese Angaben richtig ?(J/N)')
	if allesokeingabe=="J" or allesokeingabe=="j":
		parameterok=True
		break
	else:
		parameterok=False


# zielvmideingabe.isdigit() = true, wenn nur Zahlen enthalten sind
# vlen(zielvmideingabe)   # sollte kleiner als 6 Zeichen sein

# aufruf der Parametervalidierung
# parameter-ok=verifyparameters()



if (parameterok):
	print ("Eingegebene Parameter haben die Pruefung bestanden")
	zielvmidstart=zielvmideingabe
	anzahl=anzahleingabe
	quellvmid=quellvmideingabe
	print("Klone VM mit ID %i auf Proxmox %i mal mit Startziel-ID %i"%(quellvmid,anzahl,zielvmidstart))
	print("Baue SSH-Verbindung auf...")
	


	try:
		ssh.connect(zielhost,username=benutzer,password=passwort)
	except ValueError as e:
		print(e)	
	finally:
		print("SSH-Verbindungsphase abgeschlossen")	




# Durchführen der Operation mit For-Schleife

# der wichtigste Befehl ist hier "qm clone <quellid> <zielid> [Optionen]"
# -name "VMName" -storage "storagename"
# anschließend kann die MAC-Adresse mit dem qm config <vmid> [Optionen] Befehl noch moduliert werden, sodass ein etwaiges Gast-OS-Skript die IP-Adresse automatisch vergibt


	for i in range(1,(anzahl+1)):
	#hier wird überprüft ob die Ziel-VM-ID vorhanden ist, falls ja wird gestoppt, falls nein wird weitergemacht
		try:
			print("Iteration:"+str(i))
			zielid=(int(zielvmidstart) - 1) + i
			quellid=quellvmid
			befehl="/usr/sbin/qm clone "+str(quellid)+" "+str(zielid)+" -name "+vmname+str(i)+" -storage ZFS -full >/tmp/clone"+str(zielid)+".log"
			print("Führe Befehl aus: "+befehl)
			stdin, stdout, stderr = ssh.exec_command(befehl)
			print("Abgesetzter Befehl:"+ str(stdin))
			channel=stdout.channel
			returncode=channel.recv_exit_status()
			ausgabe=str(stdout)
			fehler=str(stderr)
			print("Rückgabe:" + ausgabe)
			print("Fehler:" + fehler)

		except ValueError as e:
			print(e)
		finally:
			print("Mit Iteration %i abgeschlossen."%i)

else:
	print("Die eingegebenen Parameter waren nicht korrekt.")



