#! /usr/bin/python3
from netmiko import ConnectHandler
import getpass

username=input("Enter the username: ")
password=getpass.getpass("Enter the password: ")
secret=password

with open('devices.txt') as firewalls:
	for IP in firewalls:
		firewall = {
			'device_type': 'cisco_asa',
			'ip': IP,
			'username': username,
			'password': password,
			'secret': secret,
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
        output=net_connect.send_command('show version')
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