"""
Check Port configuration: Create a list of port randomly. Then apply the Python script to check the information automatically -> export to a file (txt or CSV…)

User to be asked for the path of the Port list or type All to execute the script follow the requirement (apply script for individual ports on list or all port of device)
*Need Standardizing
"""

#DONE Create a list of port randomly. Then apply the Python script to check the information automatically -> export to a file (txt or CSV…)

from netmiko import ConnectHandler, NetMikoAuthenticationException
from datetime import datetime
import getpass

# Prompting for username and password
def get_credentials():
	username = input("Enter your username: ")
	password = getpass.getpass()
	return username, password

def get_ports(filepath): # Open PortList.txt and read its contents
	with open(f'{filepath}', 'r') as file:
	    return file.read().splitlines()

def check_port_configuration(conn, port):
	out = conn.send_command(f"display interface {port}")
	return out

def check_port_exists(conn, port):
    output = conn.send_command(f"display current-configuration interface {port}")
    if "Wrong parameter found at '^' position." in output or "Error: Incomplete command found at '^' position." in output:
        return False
    else:
        return True
	
def main():
	while True:
		username, password = get_credentials()
		
		connection_info = {
		'device_type': 'huawei',
        'host': '10.224.130.1',
        'port': 22,
        'username': username,
        'password': password
        }
		
		try:
			with ConnectHandler(**connection_info) as conn:
				print("Connected Successfully")
				timestamp = datetime.now().strftime("%d_%m_%y_%H_%M")
				while True:
					confirmation = input("Type '1' to enter your file path. Type '2' to check all Ports: ")
					if confirmation == "1":
						while True:
							try:
								filepath = input("Enter your file path: ")
								Ports = get_ports(filepath)
								break #exit when file is found
							except FileNotFoundError:
								print("File not found. Please try again!")
								continue 		
						with open(f"./PortConfiguration/CheckPortConfiguration_Output_{timestamp}.txt",'w') as f:
							for Port in Ports:
								out = check_port_configuration(conn, Port)
								print(out)
								print(out, file=f)	
						break
					if confirmation == "2":
						with open(f"./PortConfiguration/CheckPortConfiguration_Output_{timestamp}.txt",'w') as f:
								out = conn.send_command(f"display current-configuration all")
								print(out)
								print(out, file=f)
						break
					else:
						continue
				break

		except NetMikoAuthenticationException:
			print("Invalid credentials, please try again!")
			continue
		except Exception as e:
			print(f"An error has occured: {e}")
			break

if __name__ == "__main__":
	main()