#!/usr/bin/python

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("host_or_address",help="Hostname or IPv4 address of the AMQ-Server")
args = parser.parse_args()


if args.host_or_address=='':
	print args.echo
	exit()

print "Zieladresse:", args.host_or_address





