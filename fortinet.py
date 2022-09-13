#! /usr/bin/python3
from netmiko import ConnectHandler
import getpass

username=input("Enter the username: ")
password=getpass.getpass("Enter the password: ")


cfglist = [
	"config firewall address",
	"edit AMPAWS",
	"set type fqdn",
	"set fqdn outgoing.hsia.sonifi.cloud",
	"end",
	"config firewall addrgrp",
	"edit External\ Management",
	"append member AMPAWS",
	"end",
	"config firewall addrgrp",
	"edit SNMP\ Management",
	"append member AMPAWS",
	"end",
	"config firewall addrgrp",
	"edit SNMP",
	"append member AMPAWS",
	"end",
]
with open('devices.txt') as firewalls:
	for IP in firewalls:
		firewall = {
			'device_type': 'fortinet',
			'ip': IP,
			'username': username,
			'password': password,
}

		net_connect = ConnectHandler(**firewall)
		print('Connecting to ' + IP.strip())
		print('-'*79)
		print(net_connect.find_prompt())
		#hostname = net_connect.send_command('show hostname')
		print('Backing up ' + IP.strip())
		filename = '/home/pregan/scripts/backups/' + IP.strip() + '.txt'
		showrun = net_connect.send_command('show full-configuration')
		log_file = open(filename, "a")
		log_file.write(showrun)

		print('Sending commands to ' + IP)
		configoutput = net_connect.send_config_set(cfglist)
		#configoutput += net_connect.save_config()
		net_connect.disconnect()
