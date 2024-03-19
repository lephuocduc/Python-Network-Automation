"""
Check IP interface: Create a list of interface randomly. Then apply the Python script to check the information automatically -> export to a file (txt or CSV…)

User to be asked for the path of the Port list or type All to execute the script follow the requirement (apply script for individual ports on list or all port of device)  
*Need Standardizing
"""

from netmiko import ConnectHandler, NetMikoAuthenticationException
from datetime import datetime
import getpass

# Prompt for username and password
def get_credentials():
    username = input("Enter your username: ")
    password = getpass.getpass()
    return username, password

def Get_Interface(filepath):
    with open(f'{filepath}','r') as file:
        return file.read().splitlines()

def check_ip_interface(conn, Interface):
    out = conn.send_command(f"display ip interface {Interface}")
    return out

def check_interface_exists(conn, Interface):
    output = conn.send_command(f"display ip interface {Interface}")
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
                print("Connected successfully")
                timestampt = datetime.now().strftime("%d_%m_%y_%H_%M")
                while True:
                    confirmation = input("Type '1' to enter your file path. Type '2' to check all IP Interaces: ")
                    if confirmation == "1":
                        while True:
                            try:
                                filepath = input("Enter your file path: ")
                                InterfaceList = Get_Interface(filepath)
                                break #exit loop when file is found
                            except FileNotFoundError:
                                print("File not found. Please try again!")
                                continue                        
                        with open(f'./IPInterface/CheckIPInterface_Output_{timestampt}.txt','w') as f:
                            for Interface in InterfaceList:
                                out = check_ip_interface(conn, Interface)
                                print(out)
                                print(out, file=f)
                        break
                    if confirmation == "2":
                        with open(f'./IPInterface/CheckIPInterface_Output_{timestampt}.txt','w') as f:
                                out = check_ip_interface(conn, "brief")
                                print(out)
                                print(out, file=f)
                        break
                    else:
                        continue
            break
        except NetMikoAuthenticationException:
            print("Invalid credentials. Please try again.")
            continue
        except Exception as e:
            print(f"An error has occured {e}")
            break

if __name__ == "__main__":
    main()