"""
Remove port description:

Pre-check current port description.(Show all port description)

Yes/No option for execution.

1.Choose Yes -> Export backup configuration file for port -> execute the script changing configuration (Remove Many port description at the same time)

User to be asked for the path of the Port list or type All to execute the script follow the requirement (apply script for individual ports on list or all port of device)  

2.Choose No -> Stop the script. 
*Need Standardizing
"""

from netmiko import ConnectHandler, NetMikoAuthenticationException
from datetime import datetime
import getpass

def get_credentials():
    username = input("Enter your username: ")
    password = getpass.getpass()
    return username, password

def get_port(filepath):
    with open(f'{filepath}', 'r') as file:
	    return file.read().splitlines()

def get_current_description(conn, port):
    out = conn.send_command(f"display interface {port}")
    lines = out.split('\n')
    for line in lines:
        if "Description:" in line:
            return line.split ("Description:")[1].strip()

def remove_port_description(conn, port):
    conn.enable()
    config_commands = [
          f"interface {port}",
          "undo description",
          "commit"
    ]
    out = conn.send_config_set(config_commands)
    print(out)

def backup_config(conn):
    backup = conn.send_command('display current-configuration')
    timestamp = datetime.now().strftime("%d_%m_%Y_%H_%M")
    with open(f'./backup_files/backup_config.txt_{timestamp}','w') as f:
        f.write(backup)
        print("Backup configuration has been saved to backup_config.txt")

def check_port_exists(conn, port):
    output = conn.send_command(f"display interface {port}")
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
                timestamp = datetime.now().strftime("%d_%m_%y_%H_%M")
                while True:
                    confirmation1 = input("Type '1' to enter your file path. Type '2' to specify your Ports: ")
                    if confirmation1 == "1":
                        while True:
                            try:
                                filepath = input("Enter your file path: ")
                                ports = get_port(filepath)
                                break
                            except FileNotFoundError:
                                print("File now found. Please try again")
                                continue                        
                        for port in ports:
                            print(f"The current description of port '{port}' is: {get_current_description(conn, port)}")
                        while True:
                            confirmation = input(f"Do you want to remove all descriptions? Yes/ No: ")
                            if confirmation.lower() == 'yes':
                                backup_config(conn)
                                for port in ports:
                                    remove_port_description(conn, port)
                                print("All descriptions after deleted")
                                for port in ports:
                                    print(f"The current description of port '{port}' is: {get_current_description(conn, port)}")
                                break
                            if confirmation.lower() == 'no':
                                print("Operation cancelled!")
                                break
                            else: 
                                continue
                        break
                    if confirmation1 == "2":
                        ports = []
                        number = 1
                        while True:
                            port = input(f"Enter your port {number}: ")
                            if port == "":
                                break
                            else:  
                                if check_port_exists(conn, port):
                                    ports.append(port)
                                    number += 1
                                    continue
                                else:
                                    print(f"Port '{port}' does not exist. Please try again.")
                                    continue
                        for port in ports:
                            print(f"The current description of port '{port}' is: {get_current_description(conn, port)}")
                        while True:
                            confirmation = input("Do you want to remove all descriptions? Yes/ No: ")    
                            if confirmation.lower() == "yes":
                                backup_config(conn)
                                for port in ports:
                                    remove_port_description(conn, port)
                                print("All descriptions after deleted")
                                for port in ports:
                                    print(f"The current description of port '{port}' is: {get_current_description(conn, port)}")
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
            print("Invalid credentials, please try again!")
            continue
        except Exception as e:
            print(f"An error has occured: {e}")
            break
if __name__ == "__main__":
    main()