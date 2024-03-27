#NOTES
# Name: AddPortDescription.py
# Author:  Duc Le
# Version:  1.0
# Major Release History:

#DESCRIPTION
# The script prompts the user for their username and password to connect to Huawei Core Switch
# It then provides the user with two options:
# 1. Reading a file containing a list of port and VLAN pairs, and apply the specified VLANs to the corresponding ports.
# 2. Reading a file containing a list of ports, and assign a specified VLAN to all listed ports.

#REQUIREMENT
# Credentials to access to the Huawei network device.

#INPUTS
# 1. User's username and password for the Huawei network device.
# 2. File path containing a list of port and vlan pairs (if option 1 is chosen).
# 3. File path containing a list of ports (if option 2 is chosen).
# 4. VLAN ID to be assigned, if option 2 is chosen (prompted during script execution).

#OUTPUTS
# Backup is saved in ./backup_files/
# The current VLAN and port information is displayed on the console.
# The output of the VLAN assignment is printed to the console.

#EXAMPLE
# Suppose you have a file named "Port-VLAN.txt" with the following content:
# 10ge 2/0/20 | vlan 160
# 10ge 2/0/21 | vlan 161
# Running the script with option 1 and providing the file path Port-VLAN.txt will change the assigned VLAN of 10ge 2/0/20 to vlan 160 and 10ge 2/0/21 to vlan 161.
# Alternatively, if you have a file named "PortList.txt" with the following content:
# 10ge 2/0/20
# 10ge 2/0/21
# Running the script with option 2, providing the file path PortList.txt, and entering a VLAN (e.g., vlan 160), will change the assigned VLAN of both 10ge 2/0/20 and 10ge 2/0/21 to vlan 160.


from netmiko import ConnectHandler, NetMikoAuthenticationException
from datetime import datetime
import getpass

# Prompting for credentials
def get_credentials():
    username = input("Enter your username: ")
    password = getpass.getpass()  # Securely prompts for password
    return username, password


# Function to read a list of port and vlan pairs from a file
def get_ports_and_vlans_from_file():
    ports = []
    vlans = []
    while True:
        try:
            file_path = input("Enter your file path: ")
            with open(f'{file_path}','r') as file:
                for line in file:
                    port, vlan = line.strip().split(" | ")
                    ports.append(port)
                    vlans.append(vlan)
                return ports, vlans
        
        except FileNotFoundError:
            print("File not found. Please try again!")
            continue #If the file is not found, countinue the loop


# Function to read a list of ports from a file
def get_ports_from_file():
    while True:
        try:
            file_path = input("Enter your file path: ")
            with open(f'{file_path}', 'r') as file:
                return file.read().splitlines()
        except FileNotFoundError:
            print("*****File not found. Please try again*****")
            continue  # Continue if unvalid


# Function to display current vlan info
def get_current_vlan_info(conn, vlan):
    out = conn.send_command(f"display {vlan}")
    print(f"BELOW IS YOUR {vlan}")
    print(out)


# Function to display current port info
def get_current_switchport_info(conn, port):
    out = conn.send_command(f"display interface {port}")
    print(f"BELOW IS YOUR PORT {port}")
    print(out)


#Function to backup configuration to a file
def backup_config(conn):
    backup = conn.send_command('display current-configuration')
    timestamp = datetime.now().strftime("%d_%m_%Y_%H_%M")
    backup_file = f"./backup_files/backup_config_{timestamp}.txt"
    with open(f'{backup_file}','w') as f:
        f.write(backup)
        print(f"Backup configuration has been saved to '{backup_file}'")


# Function to add vlan to switch port
def add_vlan_to_switchport(conn, port, vlan):
    conn.enable()
    config_commands = [
        f'interface {port}',
        'port link-type access',
        f'port default {vlan}',
		'commit'
    ]
    output = conn.send_config_set(config_commands)
    print(output)



def check_port_exists(conn, port):
    output = conn.send_command(f"display interface {port}")
    if "Wrong parameter found at '^' position." in output or "Error: Incomplete command found at '^' position." in output:
        return False
    else:
        return True



def check_vlan_exists(conn, vlan):
    output = conn.send_command(f"display {vlan}")
    if "Wrong parameter found at '^' position." in output or "Error: Incomplete command found at '^' position." in output:
        return False
    else:
        return True


def main():
    while True:
        username, password = get_credentials() # Get username and password
        connection_info = {
            'device_type': 'huawei',
            'host': '10.224.130.1',
            'port': 22,
            'username': username,
            'password': password
            }
        
        try:
            with ConnectHandler(**connection_info) as conn: # Connect to device
                print("Connected successfully")
                while True:
                    # Prompt the user to choose an option
                    confirmation = input("Type '1' to enter the file path. Type '2' to apply to assign a VLAN for many Ports: ")
                    if confirmation == "1":
                        ports, vlans = get_ports_and_vlans_from_file()  # Get ports and vlans from a file
                        
                        for vlan in vlans:
                            get_current_vlan_info(conn, vlan) # Get current vlan info

                        for port in ports:
                            get_current_switchport_info(conn, port) # Get current port info

                        for port, vlan in zip(ports, vlans):
                            print(f"Assign {vlan} to port: {port}")

                        while True:                    
                            confirmation = input("Do you want to execute the script? Yes/ No: ") # Confirm if the user wants to change all descriptions
                            if confirmation.lower() == "yes":
                                backup_config(conn) # Backup configuraiton
                                for port, vlan in zip(ports,vlans):
                                    add_vlan_to_switchport(conn, port, vlan) # Assign vlan to port
                                break

                            if confirmation.lower() == "no":
                                print("Operation cancelled!")
                                break
                        
                        break

                    if confirmation == "2":
                        ports = get_ports_from_file() # Get ports from a file                        
                        while True:
                          vlan = input("Enter your VLAN to assign: ")
                          if check_vlan_exists(conn, vlan):
                            break
                          
                          else:
                              print(f"VLAN '{vlan}' does not exist. Please try again.")
                              continue
                          
                        get_current_vlan_info(conn, vlan) # Get current vlan info

                        for port in ports:
                          get_current_switchport_info(conn, port) # Get current port info

                        while True:
                          confirmation = input(f"Do you want to assign {vlan} to all ports: {ports}? Yes/ No: ")
                          if confirmation.lower() == "yes":
                              backup_config(conn) # Backup configuration
                              for port in ports:
                                  add_vlan_to_switchport(conn, port, vlan) # Assign vlan to port
                              break
                          
                          if confirmation.lower() == "no":
                              print("Operation cancelled!")
                              break
                          
                          else:
                              continue
                        break

                    else:
                      continue
            break

        except NetMikoAuthenticationException:
            print("Invalid credentials. Please try again.")
            continue
        except Exception as e:
            print(f"An error has occured: {e}")
            break

if __name__ == "__main__":
    main()