#! /usr/bin/python3
from netmiko import ConnectHandler
from netmiko.ssh_exception import  NetMikoTimeoutException
from paramiko.ssh_exception import SSHException 
from netmiko.ssh_exception import  AuthenticationException
from getpass import getpass
from pprint import pprint

username=input("Enter the username: ")
password=getpass.getpass("Enter the password: ")


with open('devices.txt') as firewalls:
	for IP in firewalls:
		firewall = {
			'device_type': 'fortinet',
			'ip': IP,
			'username': username,
			'password': password,
}

    Timeouts=open("Connection time outs.txt", "a")
    Authfailure=open("Auth failures.txt", "a")
    SSHException=("SSH Failure.txt", 'a')
    EOFError=("EOFerrors.txt",'a')
    UnknownError=("UnknownError.txt",'a')
    
    try:
        net_connect = ConnectHandler(**firewall)
        print('Connecting to ' + IP)
		print('-'*79)
		net_connect.enable()
		print(net_connect.find_prompt())  
        output=net_connect.send_command('get system status')
        print(output)
    except (AuthenticationException):
        print ('Authentication Failure: ' + IP)
        Authfailure.write('\n' + IP)
        continue 
    except (NetMikoTimeoutException):
        print ('\n' + 'Timeout to device: ' + IP)
        Timeouts.write('\n' + IP)
        continue
    except (SSHException):
        print ('SSH might not be enabled: ' + IP)
        SSHException.write('\n' + IP)
        continue 
    except (EOFError):
        print ('\n' + 'End of attempting device: '  IP)
        EOFError.write('\n' + IP)
        continue
    except unknown_error:
        print ('Some other error: ' + str(unknown_error))
        continue
