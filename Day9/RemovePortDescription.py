#NOTES
# Name: AddPortDescription.py
# Author:  Duc Le
# Version:  1.0
# Major Release History:

#DESCRIPTION
# The script prompts the user for their username and password to connect to Huawei Core Switch
# Then it reads a file to get a list of ports, retrieves the current description of each port, and provides options to remove all descriptions

#REQUIREMENT
# Credentials to access to the Huawei network device.

#INPUTS
# 1. User's username and password for the Huawei network device.
# 2. File path containing a list of ports.

#OUTPUTS
# Backup is saved in ./backup_files/
# The output of the new descriptions are printed to the console.

#EXAMPLE
# Running the script and you will be prompted a file path containing ports list
# Enter the file path -> Check current description -> confirm if user wants to remove all descriptions -> Execute the request

from netmiko import ConnectHandler, NetMikoAuthenticationException  # Import required libraries
from datetime import datetime
import getpass

# Prompting for credentials
def get_credentials():
    username = input("Enter your username: ")
    password = '12345678a@' #getpass.getpass()  # Securely prompts for password
    return username, password


# Function to read a list of ports from a file
def get_ports_from_file():
    while True:
        try:
            # Open file -> read its contents and split the lines
            file_path = input("Enter your file path: ")
            with open(f'{file_path}', 'r') as file:
                return file.read().splitlines()
            
        except FileNotFoundError: # Catch the invalid file error
            print("*****File not found. Please try again*****")
            continue  # Continue if invalid


# Function to check current description of a port
def get_current_description(conn, port):
        out = conn.send_command(f"display interface {port}") # Send command to device
        lines = out.split('\n') # Split output into lines
        for line in lines:
            if "Description:" in line: # Check if the line contains the keyword "Description:"
                return line.split ("Description:")[1].strip() # Extract the description


# Function to remove description of a port
def remove_port_description(conn, port):
    conn.enable()  # Enable privileged mode
    config_commands = [ # Send commands to device
        f"interface {port}",
        "undo description",
        "commit"
    ]
    out = conn.send_config_set(config_commands)
    print(out)


#Function to backup configuration to a file
def backup_config(conn):
    backup = conn.send_command('display current-configuration') # Send command to device
    timestamp = datetime.now().strftime("%d_%m_%Y_%H_%M")
    backup_file = f"./backup_files/backup_config_{timestamp}.txt" # Create a new file to save backup
    with open(f'{backup_file}','w') as f: # Open the file and save backup
        f.write(backup)
        print(f"Backup configuration has been saved to '{backup_file}'")


# Main function
def main():
    while True:
        username, password = get_credentials()  # Get username and password
        # Device's information
        connection_info = {
            'device_type': 'huawei',
            'host': '10.224.130.1',
            'port': 22,
            'username': username,
            'password': password
        }

        try:
            with ConnectHandler(**connection_info) as conn:  # Connect to device
                print("Connected successfully")
                ports = get_ports_from_file()  # Get list of ports from file

                for port in ports:
                    print(f"The current description of port '{port}' is: {get_current_description(conn, port)}")  # Print current description

                while True:
                    confirmation = input(f"Do you want to remove all descriptions? Yes/ No: ") # Confirm if the user wants to remove all descriptions
                    if confirmation.lower() == 'yes':
                        backup_config(conn)  # Backup configuration
                        for port in ports:
                            remove_port_description(conn, port)  # Remove description for each port
                        print("All descriptions after deleted:")
                        for port in ports:
                            print(f"The current description of port '{port}' is: {get_current_description(conn, port)}")  # Print new description
                        break

                    if confirmation.lower() == 'no':
                        print("Operation cancelled!")
                        break

                    else:
                        print("*****Invalid input. Please try again*****")
                        continue
            break

        except NetMikoAuthenticationException: # Catch the authentication errors
            print("*****Invalid credentials, please try again*****")
            continue

        except Exception as e: # Catch other errors
            print(f"An error has occurred: {e}")
            break

if __name__ == "__main__":
    main()