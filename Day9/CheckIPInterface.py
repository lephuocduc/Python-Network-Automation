#NOTES
# Name: CheckIPInterface.py
# Author:  Duc Le
# Version:  1.0
# Major Release History:

#DESCRIPTION
# The script prompts the user for their username and password to connect to Huawei Core Switch
# It then provides the user with two options:
# 1. Enter a file path containing a list of interfaces to check their IP interface details.
# 2. Check the IP interface details for all interfaces on the device.
# The output of the requested action is printed to the console and written to a file.

#REQUIREMENT
# Credentials to access to the Huawei network device.

#INPUTS
# 1. User's username and password for the Huawei network device.
# 2. File path containing a list of interfaces (if option 1 is chosen).

#OUTPUTS
# 1. Output of the 'display ip interface' command for the specified ports (if option 1 is chosen).
# 2. Output of the 'display ip interface brief' command for all ports (if option 2 is chosen).
# The output of the requested action is printed to the console and written to a file in the './PortConfiguration/' directory.

#EXAMPLE
# When the user runs the script, they will be prompted to enter their username and password.
# After a successful authentication, the user will be asked to either enter a file path containing a list of interfaces (option 1) or check all IP interfaces (option 2).
# If option 1 is chosen, the script will read the interfaces from the provided file and check the IP interface details for each interface, printing the output to the console and writing it to a file.
# If option 2 is chosen, the script will check the IP interface details for all interfaces and print the output to the console and write it to a file.


from netmiko import ConnectHandler, NetMikoAuthenticationException
from datetime import datetime
import getpass

# Function to prompt user for username and password
def get_credentials():
    username = input("Enter your username: ")
    password = getpass.getpass()  # Securely prompts for password
    return username, password


# Function to read a list of interfaces from a file
def get_interfaces_from_file():
    while True:
        try:
            # Open file -> read its contents and split the lines
            file_path = input("Enter your file path: ") 
            with open(f'{file_path}', 'r') as file:
                return file.read().splitlines()
            
        except FileNotFoundError: # Catch the invalid file error
            print("*****File not found. Please try again*****")
            continue  # Continue if invalid


# Function to check the IP interface details
def check_ip_interface(conn, interface):
    out = conn.send_command(f"display ip interface {interface}") # Send command to device
    print(out)


# Function to check all IP interfaces
def check_all_ip_interfaces(conn):
    out = conn.send_command("display ip interface brief") # Send command to device
    print(out)


# main
def main():
    while True:
        username, password = get_credentials() # Get username and password
        # Device's information
        connection_info = {
            'device_type': 'huawei',
            'host': '10.224.130.1',
            'port': 22,
            'username': username,
            'password': password
        }

        try:
            with ConnectHandler(**connection_info) as conn: # Connect to device
                print("Connected Successfully")
                timestamp = datetime.now().strftime("%d_%m_%y_%H_%M")

                while True:
                    # Prompt user for "1" or "2" option
                    confirmation = input(
                        "Type '1' to enter your file path. \n"
                        "Type '2' to check all IP Interaces: ")
                    
                    if confirmation == "1":
                        interfaces = get_interfaces_from_file() # Get list of interfaces from file
                        with open(f'./IPInterface/CheckIPInterface_Output_{timestamp}.txt', 'w') as f: # Open the file and write the output to it
                            for interface in interfaces:
                                out = check_ip_interface(conn, interface) # Check ip interface
                                print(out, file=f) # Output to a file
                        break

                    if confirmation == "2":
                        with open(f'./IPInterface/CheckIPInterface_Output_{timestamp}.txt', 'w') as f: # Open the file and write the output to it
                            out = check_all_ip_interfaces(conn) # Check all ip interfaces
                            print(out, file=f) # Output to a file
                        break

                    # Continue to the loop until user types "1" or "2"
                    else:
                        print("*****Invalid input. Please try again*****")
                        continue
                break

        except NetMikoAuthenticationException: # Catch the authentication errors
            print("*****Invalid credentials, please try again*****")
            continue

        except Exception as e: # Catch other errors
            print(f"An error has occurred {e}")


if __name__ == "__main__":
    main()