# Check Port configuration: Create a list of port randomly. Then apply the Python script to check the information automatically.

from netmiko import ConnectHandler
import getpass

# Prompting for username and password
username = input("Enter your username: ")
password = getpass.getpass()

connection_info = {
    'device_type': 'huawei',
    'host': '10.224.130.1',
    'port': 22,
    'username': username,
    'password': password
}

# Open PortList.txt and read its contents
with open('PortList.txt', 'r') as file:
	ports = file.read().splitlines()

# Assign values to variable port
with ConnectHandler(**connection_info) as conn:
		for port in ports:
			out = conn.send_command(f"display interface {port}")
			print(out) # Print the output for each Port