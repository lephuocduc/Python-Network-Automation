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

# Function to get username and password from user input
def get_credentials():
    username = input("Enter your username: ")
    password = getpass.getpass()  # Securely get password without displaying it
    return username, password


# Function to get list of ports from a file
def get_ports_from_file():
    while True:
        try:
            filepath = input("Enter your file path: ")
            with open(f'{filepath}', 'r') as file:
                return file.read().splitlines()  # Read file and return list of lines
        except FileNotFoundError:
            print("*****File not found. Please try again*****")
            continue


# Function to get current description of a port
def get_current_description(conn, port):
    out = conn.send_command(f"display interface {port}")  # Send command to get interface info
    lines = out.split('\n')  # Split output into lines
    for line in lines:
        if "Description:" in line:
            return line.split("Description:")[1].strip()  # Return description if found


# Function to remove description of a port
def remove_port_description(conn, port):
    conn.enable()  # Enable privileged mode
    config_commands = [
        f"interface {port}",
        "undo description",  # Remove description
        "commit"  # Commit changes
    ]
    out = conn.send_config_set(config_commands)  # Send configuration commands
    print(out)  # Print output


# Function to backup current configuration
def backup_config(conn):
    backup = conn.send_command('display current-configuration')  # Get current configuration
    timestamp = datetime.now().strftime("%d_%m_%Y_%H_%M")  # Get current timestamp
    with open(f'./backup_files/backup_config.txt_{timestamp}', 'w') as f:
        f.write(backup)  # Write backup to file
    print("Backup configuration has been saved to backup_config.txt")


# Main function
def main():
    while True:
        username, password = get_credentials()  # Get username and password
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
                    confirmation = input(f"Do you want to remove all descriptions? Yes/ No: ")
                    if confirmation.lower() == 'yes':
                        backup_config(conn)  # Backup configuration
                        for port in ports:
                            remove_port_description(conn, port)  # Remove description for each port
                        print("All descriptions after deleted:")
                        for port in ports:
                            print(f"The current description of port '{port}' is: {get_current_description(conn, port)}")  # Print new description
                        break
                    elif confirmation.lower() == 'no':
                        print("Operation cancelled!")
                        break
                    else:
                        continue
            break

        except NetMikoAuthenticationException:
            print("*****Invalid credentials, please try again*****")
            continue

        except Exception as e:
            print(f"An error has occurred: {e}")


if __name__ == "__main__":
    main()