"""
Pre-check current port description.

Yes/No option for execution.

1.Choose Yes -> Export backup configuration file for port -> execute the script changing configuration (Many Port to be added one Description / Many Ports to be added many appropriate descriptions)

User to be asked for the path of the Port list or type All to execute the script follow the requirement (apply script for individual ports on list or all port of device)  

2.Choose No -> Stop the script.  

*Need Standardizing
"""
#Scrip done, need standardizing

from netmiko import ConnectHandler, NetMikoAuthenticationException
from datetime import datetime
import getpass

# Prompting for credentials
def get_credentials():
      username = input("Enter your username: ")
      password = getpass.getpass()
      return username, password

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
            print("File not found. Please try again!")
            continue #If the file is not found, countinue the loop

def get_current_description(conn, port):
      out = conn.send_command(f"display interface {port}")
      lines = out.split('\n')
      for line in lines:
           if "Description:" in line:
                return line.split ("Description:")[1].strip()
           
def backup_config(conn):
    backup = conn.send_command('display current-configuration')
    timestamp = datetime.now().strftime("%d_%m_%Y_%H_%M")
    with open(f'./backup_files/backup_config.txt_{timestamp}','w') as f:
        f.write(backup)
        print("Backup configuration has been saved to backup_config.txt")

def change_description(conn, port, new_description):
      conn.enable()
      config_commands = [
            f"interface {port}",
            f"description {new_description}",
            "commit"
            ]
      out = conn.send_config_set(config_commands)
      print(out)

def check_port_exists(conn, port):
    output = conn.send_command(f"display interface {port}")
    if "Wrong parameter found at '^' position." in output or "Error: Incomplete command found at '^' position." in output:
        return False
    else:
        return True

def main():
    #Main function
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
                while True:
                    confirmation = input("Type '1' to enter the path. Type '2' to apply a new description for all Ports: ")
                    if confirmation == "1":
                        ports, new_descriptions = get_ports_and_new_descriptions_from_file()                          
                        for port, new_description in zip(ports, new_descriptions):
                            print(f"Change description of port '{port}' from '{get_current_description(conn,port)}' to '{new_description}'")
                        while True:
                            confirmation = input("Do you want to execute the scipt? Yes/ No: ")
                            if confirmation.lower() == "yes":
                                backup_config(conn)
                                for port, new_description in zip(ports, new_descriptions):
                                    change_description(conn, port, new_description)
                                print("All descriptions after changed")
                                for port in ports:
                                    print(f"The current description of port '{port}' is: {get_current_description(conn, port)}")
                                break

                            if confirmation.lower() == "no":
                                print("Operation cancelled!")
                                break

                            else:
                                    continue
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

                        new_description = input("Enter new description: ")
                        for port in ports:
                            print(f"The current description of port '{port}' is: {get_current_description(conn, port)}")
                        while True:
                                confirmation = input(f"Do you want to change all descriptions to '{new_description}'? Yes/ No: ")
                                if confirmation.lower() == "yes":
                                    backup_config(conn)
                                    for port in ports:
                                            change_description(conn, port, new_description)
                                    print("All descriptions after changed")
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
            print("Invalid credentials, please try again")
            continue

        except Exception as e:
            print(f"An error has occured: {e}")                 

if __name__ == "__main__":
    main()