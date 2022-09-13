#! /usr/bin/python3
from netmiko import ConnectHandler
import getpass

username=input("Enter the username: ")
password=getpass.getpass("Enter the password: ")
secret=password

cfglist = [
	"object network Sonifi-AWS",
	"fqdn outgoing.hsia.sonifi.cloud",
	"object-group network Allowed_Public",
	"network-object object Sonifi-AWS",
	"write mem",
]
with open('devices.txt') as firewalls:
	for IP in firewalls:
		firewall = {
			'device_type': 'cisco_asa',
			'ip': IP,
			'username': username,
			'password': password,
			'secret': secret,
}


		net_connect = ConnectHandler(**firewall)
		print('Connecting to ' + IP)
		print('-'*79)
		net_connect.enable()
		print(net_connect.find_prompt())
		hostname = net_connect.send_command('show hostname')
		print('Backing up ' + hostname)
		filename = '/home/pregan/scripts/backups/' + hostname + '.txt'
		showrun = net_connect.send_command('show run')
		log_file = open(filename, "a")
		log_file.write(showrun)

		print('Sending commands to ' + hostname)
		configoutput = net_connect.send_config_set(cfglist)
		print(configoutput)
		configoutput += net_connect.save_config()
		net_connect.disconnect()
