"""
Check Port configuration: Create a list of port randomly. Then apply the Python script to check the information automatically -> export to a file (txt or CSV…)

User to be asked for the path of the Port list or type All to execute the script follow the requirement (apply script for individual ports on list or all port of device)
*Need Standardizing
"""
#NOTES
#	Name: CheckIPInterface.py
#	Author:  Duc Le
#	Version:  1.0
#	Major Release History:
#DESCRIPTION
#	Create a list of ports. Then apply the Python script to check the information automatically -> export to a file (txt or CSV…)
#   User to be asked for the path of the Port list or type All to execute the script follow the requirement (apply script for individual ports on list or all port of device)
#REQUIREMENT
#	Credentials to access Huawei Network
#INPUTS
#	Path of interface list
#OUTPUTS
#	Information of IP Interface to IPInterface folder
#EXAMPLE
#	python3 CheckIPInterface.py to run the script
#   Type "1" to enter the path file. Type "2" to check all ip interface. Then the script outputs information of IP Interface to IPInterface folder

#SCript done, need standardizing

from netmiko import ConnectHandler, NetMikoAuthenticationException
from datetime import datetime
import getpass

# Function to prompt the user for username and password
def get_credentials():
	username = input("Enter your username: ")
	password = getpass.getpass()
	return username, password

# Function to read a list of ports from a file
def get_ports_from_file():
	while True:
		try:
			file_path = input("Enter your file path: ")
			with open(f'{file_path}','r') as file:
				return file.read().splitlines()
        
		except FileNotFoundError:
			print("File not found. Please try again!")
			continue # Continue if unvalid

# Function to check the port configuration
def check_port_configuration(conn, port):
	out = conn.send_command(f"display interface {port}")
	print(out)

def check_all_port_configuration(conn):
	out = conn.send_command("display current-configuration all")
	print(out)

# Function to check if a port exists
def check_port_exists(conn, port):
    output = conn.send_command(f"display current-configuration interface {port}")
	# Checks for specific error messages in the output
    if "Wrong parameter found at '^' position." in output or "Error: Incomplete command found at '^' position." in output:
        return False
	
    else:
        return True

# main
def main():
	# Loop for user to enter username and password until valid
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
				timestamp = datetime.now().strftime("%d_%m_%y_%H_%M") # Generates a timestamp for the output file
				# Prompt user for "1" or "2" option until valid
				while True:
					confirmation = input("Type '1' to enter your file path. Type '2' to check all Ports: ")
					if confirmation == "1":
						# Prompt user for file path until valid
						ports = get_ports_from_file()
						# Print the output to the console and creates a file to write the output   
						with open(f"./PortConfiguration/CheckPortConfiguration_Output_{timestamp}.txt",'w') as f:
							for port in ports:
								out = check_port_configuration(conn, port)
								print(out, file=f)	
						break

					if confirmation == "2":
						# Print the output to the console and creates a file to write the output   
						with open(f"./PortConfiguration/CheckPortConfiguration_Output_{timestamp}.txt",'w') as f:
							out = check_all_port_configuration(conn)
							print(out, file=f)
						break # Exit the loop after writing the output

					else:
						continue # Continue to the loop until user types "1" or "2"
			break

		except NetMikoAuthenticationException:
			print("Invalid credentials, please try again!")
			continue
		except Exception as e:
			print(f"An error has occured: {e}")

if __name__ == "__main__":
	main()