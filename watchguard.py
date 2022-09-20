#! /usr/bin/python3
from netmiko.watchguard.fireware_ssh import WatchguardFirewareSSH
from netmiko import ConnectHandler
import getpass

username=input("Enter the username: ")
password=getpass.getpass("Enter the password: ")
sshport=input("Enter the SSH port: ")

cfglist = [
	"config",
	"policy",
	"alias Remote_SNMP_Monitoring fqdn outgoing.hsia.sonifi.cloud",
	"alias Remote_Device_Management fqdn outgoing.hsia.sonifi.cloud",
	"apply",
	"rule Watchguard-SNMP",
	"from alias Remote_SNMP_Monitoring",
	"apply",
	"exit",
	"rule SNMP",
	"from alias Remote_SNMP_Monitoring",
	"apply",
	"exit",
	"rule 'WatchGuard Web UI'",
	"from alias Remote_SNMP_Monitoring",
	"from alias Remote_Device_Management",
	"apply",
	"exit",
	"rule WatchGuard",
	"from alias Remote_SNMP_Monitoring",
	"from alias Remote_Device_Management",
	"apply",
	"exit",
	"exit",
]
with open('devices.txt') as firewalls:
	for IP in firewalls:
		firewall = {
			'device_type': 'watchguard_fireware',
			'ip': IP,
			'username': username,
			'password': password,
			'port': sshport,
}

		net_connect = ConnectHandler(**firewall)
		print('Connecting to ' + IP.strip(), str(sshport))
		print('-'*79)
		print(net_connect.find_prompt())
		#hostname = net_connect.send_command('show hostname')
		#print('Backing up ' + IP)
		#filename = '/home/pregan/scripts/backups/' + IP + '.txt'
		#showrun = net_connect.send_command('show run')
		#log_file = open(filename, "a")
		#log_file.write(showrun)

		print('Sending commands to ' + IP)
		net_connect.enable()
		#net_connect.send_config_from_file(config_file='wgconfig.txt')
		configoutput = net_connect.send_config_set(cfglist)
		print(configoutput)
		#configoutput += net_connect.save_config()
		net_connect.disconnect()
