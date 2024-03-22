#NOTES
#	Name: CheckIPInterface.py
#	Author:  Duc Le
#	Version:  1.0
#	Major Release History:
#DESCRIPTION
#	Create a list of interfaces. Then apply the Python script to check the information automatically -> export to a file (txt or CSV…)
#   User to be asked for the path of the interface list or type All to execute the script follow the requirement (apply script for individual ports on list or all port of device)
#REQUIREMENT
#	Credentials to access Huawei Network
#INPUTS
#	Path of interface list
#OUTPUTS
#	Information of IP Interface to IPInterface folder
#EXAMPLE
#	python3 CheckIPInterface.py to run the script
#   Type "1" to enter the path file. Type "2" to check all ip interface. Then the script outputs information of IP Interface to IPInterface folder

#Script done, need standardizing

from netmiko import ConnectHandler, NetMikoAuthenticationException
from datetime import datetime
import getpass

# Function to prompt user for username and password
def get_credentials():
    username = input("Enter your username: ")
    password = getpass.getpass() # Securely prompts for password
    return username, password

# Function to read a list of interfaces from a file
def get_interfaces(file_path):
    with open(f'{file_path}','r') as file:
        return file.read().splitlines()

# Function to check the IP interface details
def check_ip_interface(conn, interface):
    out = conn.send_command(f"display ip interface {interface}")
    return out

# Function to check if an interface exists
def check_interface_exists(conn, interface):
    output = conn.send_command(f"display ip interface {interface}")
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
                # Prompt user for "1" or "2" option until valid
                while True:
                    confirmation = input("Type '1' to enter your file path. Type '2' to check all IP Interaces: ")
                    if confirmation == "1":
                        # Prompt user for file path until valid
                        while True:
                            try:
                                file_path = input("Enter your file path: ")
                                interfaces = get_interfaces(file_path)
                                # Print the output to the console and creates a file to write the output
                                timestampt = datetime.now().strftime("%d_%m_%y_%H_%M") # Generates a timestamp for the output file                        
                                with open(f'./IPInterface/CheckIPInterface_Output_{timestampt}.txt','w') as f:
                                    for interface in interfaces:
                                        out = check_ip_interface(conn, interface)
                                        print(out)
                                        print(out, file=f)
                                break
                            
                            except FileNotFoundError:
                                print("File not found. Please try again!")
                                continue # Continue if unvalid
                        break
            
                    if confirmation == "2":
                        # Print the output to the console and creates a file to write the output
                        timestampt = datetime.now().strftime("%d_%m_%y_%H_%M") # Generates a timestamp for the output file
                        with open(f'./IPInterface/CheckIPInterface_Output_{timestampt}.txt','w') as f:
                            out = check_ip_interface(conn, "brief")
                            print(out)
                            print(out, file=f)
                        break # Exit the loop after writing the output

                    else:
                        continue # Continue to the loop until user types "1" or "2"

            break
                    
        except NetMikoAuthenticationException:
            print("Invalid credentials, please try again!")
            continue
    
        except Exception as e:
            print(f"An error has occured {e}")

if __name__ == "__main__":
    main()