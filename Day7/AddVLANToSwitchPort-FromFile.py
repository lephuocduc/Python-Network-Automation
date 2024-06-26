""" ...
    *Assign VLAN to switch port:*

    Pre-check all vlan infor & vlan interface.
    Yes/No option for execution.
    1. Choose Yes -> Export backup configuration file for port -> execute the script changing configuration. (Many ports to be assigned to one Vlan / Many ports to be assigned to many appropriate VLAN)
    2. Choose No -> Stop the script.  
"""

from netmiko import ConnectHandler, NetMikoAuthenticationException
from datetime import datetime
import getpass

def get_credentials():
    username = input("Enter your username: ")
    password = getpass.getpass()
    return username, password

def get_ports_and_vlans():
    ports = []
    vlans = []
    with open("Port-Vlan.txt",'r') as file:
        for line in file:
            port, vlan = line.strip().split(" | ")
            ports.append(port)
            vlans.append(vlan)
    return ports, vlans

def get_current_vlan_info(conn, vlan):
    out = conn.send_command(f"display {vlan}")
    print(f"BELOW IS YOUR {vlan}")
    print(out)

def get_current_switchport_info(conn, port):
    out = conn.send_command(f"display interface {port}")
    print(f"BELOW IS YOUR PORT {port}")
    print(out)

def backup_config(conn):
    backup = conn.send_command('display current-configuration')
    timestamp = datetime.now().strftime("%d_%m_%Y_%H_%M")
    with open(f'./backup_files/backup_config.txt_{timestamp}','w') as f:
        f.write(backup)
        print("Backup configuration has been saved to backup_config.txt")

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
                ports, vlans = get_ports_and_vlans()
                for vlan in vlans:
                    get_current_vlan_info(conn, vlan)
                for port in ports:
                    get_current_switchport_info(conn, port)
                for port, vlan in zip(ports, vlans):
                    print(f"Assign {vlan} to port: {port}")
                while True:                    
                    confirmation = input("Do you want to execute the script? Yes/ No: ")
                    if confirmation.lower() == "yes":
                        backup_config(conn)
                        for port, vlan in zip(ports,vlans):
                            add_vlan_to_switchport(conn, port, vlan)
                        break
                    if confirmation.lower() == "no":
                        print("Operation cancelled!")
                        break
                break
        except NetMikoAuthenticationException:
            print("Invalid credentials. Please try again.")
            continue
        except Exception as e:
            print(f"An error has occured: {e}")
            break

if __name__ == "__main__":
    main()