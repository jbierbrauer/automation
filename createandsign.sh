#!/bin/bash

if [[ -z $1 ]]; then
  echo no Argument for jarfile given
  path2jarfile=/opt/siebel/siebel811/sweapp/public/deu/21225/applets/SiebelToolbar.jar
  echo "Using ${path2jarfile}"
fi

if [[ $1 == "-h" ]]; then
  echo 'Usage: createandsign.sh [jarfile] [jarsigner]'
  exit 
fi

if [[ -z $2 ]]; then
  echo no Argument for jarsigner given, using:
  if [[ -d /usr/oracle/product/11.2.0.3/client_1/jdk.old/bin ]]; then
     echo "Directorycheck passed successfully"
     path2jarsigner=/usr/oracle/product/11.2.0.3/client_1/jdk.old/bin/jarsigner
     path2keytool=/usr/oracle/product/11.2.0.3/client_1/jdk.old/jre/bin/keytool
     echo ${path2jarsigner}
  else
     path2jarsigner=`dzdo find / -name jarsigner | tail -n 1`
     echo ${path2jarsigner}
  fi
else
  path2jarsigner=$2
  echo "Using Argument ${path2jarsigner}"
fi

echo "Using jarfile ${path2jarfile}"
echo "Using signer ${path2jarsigner}"

firstlastname='siebeluser'
orgunit='Infrastructure'
org='QVC'
city='Liverpool'
state='Merseyside'
countrycode='UK'
pass=lkwpeter

dzdo rm -f /tmp/certdata
dzdo cat <<EOF >/tmp/certdata
${pass}
${firstlastname}
${orgunit}
${org}
${city}
${state}
${countrycode}
yes

EOF

echo "Generated certdata in tmp"

dzdo chown siebel:siebel /tmp/certdata

echo "changed ownership of /tmp/certdata to user siebel"

dzdo mv /root/.keystore /root/.keystore.`date +%s`


dzdo su - root "-c ${path2keytool} -genkey -alias siebel -keyalg RSA -sigalg SHA256withRSA -keystore /root/.keystore -keysize 4096 -validity 3650 </tmp/certdata"

echo "=========created keystore as user siebel==========="


dzdo ${path2keytool} -list -v -storepass ${pass} -keypass ${pass}

echo "===============creating Copy of SiebelToolbar.jar=============="
dzdo rm -rf /root/signing
dzdo mkdir -p /root/signing
dzdo cp ${path2jarfile} /root/signing/SiebelToolbar.jar
echo "===============file was copied to /root/signing/==============="
tempjarfile=/root/signing/SiebelToolbar.jar
dzdo cp ${path2jarfile} /root/SiebelToolbar.bak`date +%s` 

mycommand="${path2jarsigner} -storepass ${pass} -keypass ${pass} ${tempjarfile} siebel"

# echo "executing... command ${mycommand}"

tmpcmd="-c ${mycommand}"
echo $tmpcmd
dzdo su - root "${tmpcmd}"
erg=$?

if [[ ${erg} -eq 0  ]]; then
   dzdo cp ${tempjarfile} ${path2jarfile}
   dzdo chown siebel:users ${path2jarfile}
   echo "Copied signed file to original location"
else
   echo "Signing not successful" 
fi

echo "----------executed command ${mycommand} with RC ${erg}-----------"
