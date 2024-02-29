"""DONE
    Pre-check current port description.(Show all port description)
    Yes/No option for execution.
    1. Choose Yes -> Export backup configuration file for port -> execute the script changing configuration (Remove Many port description at the same time)
    2. Choose No -> Stop the script.  
"""

from netmiko import ConnectHandler, NetMikoAuthenticationException
from datetime import datetime
import getpass

def get_credentials():
    username = input("Enter your username: ")
    password = getpass.getpass()
    return username, password

def get_ports():
    with open("PortList.txt","r") as file:
        return file.read().splitlines()

def get_current_description(conn, port):
    out = conn.send_command(f"display interface {port}")
    lines = out.split('\n')
    for line in lines:
        if "Description:" in line:
            description = line.split ("Description:")[1].strip()
    print(f"Current description of '{port}' is: {description}")

def backup_config(conn):
    backup = conn.send_command('display current-configuration')
    timestamp = datetime.now().strftime("%d_%m_%Y_%H_%M")
    with open(f'./backup_files/backup_config.txt_{timestamp}','w') as f:
        f.write(backup)
        print("Backup configuration has been saved to backup_config.txt")

def remove_port_description(conn, port):
    conn.enable()
    config_commands = [
          f"interface {port}",
          "undo description",
          "commit"
    ]
    out = conn.send_config_set(config_commands)
    print(out)


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
                ports = get_ports()
                for port in ports:
                    description = get_current_description(conn, port)
                while True:
                    confirmation = input(f"Do you want to remove the description of all ports? Yes/ No: ")
                    if confirmation.lower() == 'yes':
                        backup_config(conn)
                        for port in ports:
                            remove_port_description(conn, port)
                        break
                    if confirmation.lower() == 'no':
                        print("Operation cancelled!")
                        break
                break
        except NetMikoAuthenticationException:
            print("Invalid credentials, please try again!")
            continue
        except Exception as e:
            print(f"An error has occured: {e}")
            break
if __name__ == "__main__":
    main()