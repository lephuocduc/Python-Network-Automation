#NOTES
#	Name: CheckIPInterface.py
#	Author:  Duc Le
#	Version:  1.0
#	Major Release History:

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
# The output of the requested action is printed to the console and written to a file in the './IPInterface/' directory.

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
            file_path = input("Enter your file path: ")
            with open(f'{file_path}', 'r') as file:
                return file.read().splitlines()
        except FileNotFoundError:
            print("*****File not found. Please try again*****")
            continue  # Continue if unvalid


# Function to check the IP interface details
def check_ip_interface(conn, interface):
    out = conn.send_command(f"display ip interface {interface}")
    print(out)


# Function to check all IP interfaces
def check_all_ip_interfaces(conn):
    out = conn.send_command("display ip interface brief")
    print(out)


# Function to check if an interface exists
def check_interface_exists(conn, interface):
    output = conn.send_command(f"display ip interface {interface}")
    # Checks for specific error messages in the output
    if "Wrong parameter found at '^' position." in output or \
       "Error: Incomplete command found at '^' position." in output:
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
                timestamp = datetime.now().strftime("%d_%m_%y_%H_%M")
                # Generates a timestamp for the output file
                while True:
                    confirmation = input(
                        "Type '1' to enter your file path. \n"
                        "Type '2' to check all IP Interaces: ")
                    if confirmation == "1":
                        # Prompt user for file path until valid
                        interfaces = get_interfaces_from_file()
                        # Print the output to the console and creates a file to write the output
                        with open(f'./IPInterface/CheckIPInterface_Output_{timestamp}.txt', 'w') as f:
                            for interface in interfaces:
                                out = check_ip_interface(conn, interface)
                                print(out, file=f)
                        break
                    if confirmation == "2":
                        # Print the output to the console and creates a file to write the output
                        with open(f'./IPInterface/CheckIPInterface_Output_{timestamp}.txt', 'w') as f:
                            out = check_all_ip_interfaces(conn)
                            print(out, file=f)
                        break
                    # Continue to the loop until user types "1" or "2"
                    else:
                        print("*****Unvalid input. Please try again*****")
                        continue
                break
        except NetMikoAuthenticationException:
            print("*****Invalid credentials, please try again*****")
            continue
        except Exception as e:
            print(f"An error has occurred {e}")


if __name__ == "__main__":
    main()