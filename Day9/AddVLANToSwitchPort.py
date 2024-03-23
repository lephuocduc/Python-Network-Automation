"""
  Assign VLAN to switch port:

Pre-check all vlan infor & vlan interface.

Yes/No option for execution.

1.Choose Yes -> Export backup configuration file for port -> execute the script changing configuration. (Many ports to be assigned to one Vlan / Many ports to be assigned to many appropriate VLAN)

2.Choose No -> Stop the script.  
*Need standardizing
"""
#Script done, need standardizing

from netmiko import ConnectHandler, NetMikoAuthenticationException
from datetime import datetime
import getpass

def get_credentials():
    username = input("Enter your username: ")
    password = getpass.getpass()
    return username, password

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
    backup_file = f"./backup_files/backup_config_{timestamp}.txt"
    with open(f'{backup_file}','w') as f:
        f.write(backup)
        print(f"Backup configuration has been saved to '{backup_file}'")

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
                while True:
                    confirmation = input("Type '1' to enter the file path. Type '2' to apply to assign a VLAN for many Ports: ")
                    if confirmation == "1":
                        ports, vlans = get_ports_and_vlans_from_file()

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

                    if confirmation == "2":
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
                        
                        while True:
                          vlan = input("Enter your VLAN to assign: ")
                          if check_vlan_exists(conn, vlan):
                            break
                          
                          else:
                              print(f"VLAN '{vlan}' does not exist. Please try again.")
                              continue
                          
                        get_current_vlan_info(conn, vlan)
                        for port in ports:
                          get_current_switchport_info(conn, port)
                        while True:
                          confirmation = input(f"Do you want to assign {vlan} to all ports: {ports}? Yes/ No: ")
                          if confirmation.lower() == "yes":
                              backup_config(conn)
                              for port in ports:
                                  add_vlan_to_switchport(conn, port, vlan)
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