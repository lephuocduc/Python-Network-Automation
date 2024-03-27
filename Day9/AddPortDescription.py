#NOTES
# Name: AddPortDescription.py
# Author:  Duc Le
# Version:  1.0
# Major Release History:

#DESCRIPTION
# The script prompts the user for their username and password to connect to Huawei Core Switch
# It then provides the user with two options:
# 1. Reading a file with a list of port and new description pairs and applying the new descriptions to the corresponding ports, 
# 2. Reading a file with a list of ports and applying a new description to all ports in the list.

#REQUIREMENT
# Credentials to access to the Huawei network device.

#INPUTS
# 1. User's username and password for the Huawei network device.
# 2. File path containing a list of port and new description pairs (if option 1 is chosen).
# 3. File path containing a list of ports (if option 2 is chosen).

#OUTPUTS
# Backup is saved in ./backup_files/
# The output of the new descriptions are printed to the console.

#EXAMPLE
# Suppose you have a file named "PortDescription.txt" with the following content:
# 10ge 2/0/20 | Port1_Description
# 10ge 2/0/21 | Port2_Description
# Running the script with option 1 and providing the file path "PortDescription.txt" will change the descriptions of 10ge 2/0/20 to "Port1_Description" and 10ge 2/0/21 to "Port2_Description".
# Alternatively, if you have a file named "PortList.txt" with the following content:
# 10ge 2/0/20
# 10ge 2/0/21
# Running the script with option 2, providing the file path "PortList.txt", and entering a new description (e.g., "NewDescription"), will change the descriptions of both "10ge 2/0/20" and "10ge 2/0/21" to "NewDescription".


from netmiko import ConnectHandler, NetMikoAuthenticationException
from datetime import datetime
import getpass

# Prompting for credentials
def get_credentials():
    username = input("Enter your username: ")
    password = getpass.getpass()  # Securely prompts for password
    return username, password


# Function to read a list of port and description pairs from a file
def get_ports_and_new_descriptions_from_file():
    ports =[]
    new_descriptions = []
    while True:
        try:
            file_path = input("Enter your file path: ")
            with open(f'{file_path}','r') as file:
                for line in file:
                    port, new_description = line.strip().split(" | ")
                    ports.append(port)
                    new_descriptions.append(new_description)
            return ports, new_descriptions

        except FileNotFoundError:
            print("*****File not found. Please try again*****")
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


# Function to check current description of a port
def get_current_description(conn, port):
      out = conn.send_command(f"display interface {port}")
      lines = out.split('\n')
      for line in lines:
           if "Description:" in line:
                return line.split ("Description:")[1].strip()


#Function to backup configuration to a file
def backup_config(conn):
    backup = conn.send_command('display current-configuration')
    timestamp = datetime.now().strftime("%d_%m_%Y_%H_%M")
    with open(f'./backup_files/backup_config.txt_{timestamp}','w') as f:
        f.write(backup)
        print("Backup configuration has been saved to backup_config.txt")


#Function to change description
def change_description(conn, port, new_description):
      conn.enable()
      config_commands = [
            f"interface {port}",
            f"description {new_description}",
            "commit"
            ]
      out = conn.send_config_set(config_commands)
      print(out)


# main
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
            # Establish a connection to the device
            with ConnectHandler(**connection_info) as conn: # Connect to device
                print("Connected Successfully")

                while True:
                    # Prompt the user to choose an option
                    confirmation = input(
                        "Type '1' to enter the path. \n" 
                        "Type '2' to apply new description for a list of ports: "
                        )
                    
                    if confirmation == "1":
                        ports, new_descriptions = get_ports_and_new_descriptions_from_file() #Get ports and new descriptions from a file
                        for port, new_description in zip(ports, new_descriptions):
                            print(f"Change description of port '{port}' from '{get_current_description(conn, port)}' to '{new_description}'") # Print the current and new descriptions for each port
                        while True:
                            confirmation = input("Do you want to execute the script? Yes/ No: ") # Confirm if the user wants to change all descriptions
                            if confirmation.lower() == "yes":
                                backup_config(conn) # Backup the current configuration
                                for port, new_description in zip(ports, new_descriptions): # Change the descriptions for each port
                                    change_description(conn, port, new_description)
                                print("All descriptions after changed")
                                for port in ports:
                                    print(f"The current description of port '{port}' is: {get_current_description(conn, port)}") # Print the new descriptions for each port
                                break
                            if confirmation.lower() == "no":
                                print("Operation cancelled!")
                                break
                            else:
                                continue
                        break

                    if confirmation == "2":
                        ports = get_ports_from_file() # Get ports from a file
                        new_description = input("Enter new description: ")
                        for port in ports:
                            print(f"The current description of port '{port}' is: {get_current_description(conn, port)}") # Print the current descriptions for each port
                        while True:
                            confirmation = input(f"Do you want to change all descriptions to '{new_description}'? Yes/ No: ") # Confirm if the user wants to change all descriptions
                            if confirmation.lower() == "yes":
                                backup_config(conn) # Backup the current configuration
                                for port in ports:
                                    change_description(conn, port, new_description) # Change the descriptions for each port
                                print("All descriptions after changed")
                                for port in ports:
                                    print(f"The current description of port '{port}' is: {get_current_description(conn, port)}") # Print the new descriptions for each port
                                break
                            if confirmation.lower() == "no":
                                print("Operation cancelled!")
                                break
                            else:
                                print("*****Invalid input. Please try again*****")
                                continue
                        break

                    else:
                        print("*****Invalid input. Please try again*****")
                        continue
                break

        except NetMikoAuthenticationException:
            # Handle authentication exception
            print("*****Invalid credentials, please try again*****")
            continue

        except Exception as e:
            # Handle other exceptions
            print(f"An error has occurred: {e}")          


if __name__ == "__main__":
    main()