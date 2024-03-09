"""DONE
    Pre-check current port description.(Show all port description)
    Yes/No option for execution.
      1. Choose Yes -> Export backup configuration file for port -> execute the script changing configuration (Many Port to be added one Description / Many Ports to be added many appropriate descriptions)
      2. Choose No -> Stop the script.  
"""


from netmiko import ConnectHandler, NetMikoAuthenticationException
from datetime import datetime
import getpass

# Prompting for credentials
def get_credentials():
      username = input("Enter your username: ")
      password = getpass.getpass()
      return username, password

def get_ports_and_description():
      ports =[]
      newdescriptions = []
      with open('PortDescription.txt','r') as file:
            for line in file:
                  port, newdescription = line.strip().split(" | ")
                  ports.append(port)
                  newdescriptions.append(newdescription)
      return ports, newdescriptions

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

def change_description(conn, port, newdescription):
      conn.enable()
      config_commands = [
            f"interface {port}",
            f"description {newdescription}",
            "commit"
            ]
      out = conn.send_config_set(config_commands)
      print(out)

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
                        ports, newdescriptions = get_ports_and_description()
                        for port, newdescription in zip(ports, newdescriptions):
                              print(f"Change description of port '{port}' from '{get_current_description(conn,port)}' to '{newdescription}'")
                        while True:
                              confirmation = input("Do you want to execute the scipt? Yes/ No: ")
                              if confirmation.lower() == "yes":
                                    backup_config(conn)
                                    for port, newdescription in zip(ports, newdescriptions):
                                          change_description(conn, port, newdescription)
                                    print("All descriptions after changed")
                                    for port in ports:
                                          print(f"The current description of port '{port}' is: {get_current_description(conn, port)}")
                                    break
                              if confirmation.lower() == "no":
                                    print("Operation cancelled!")
                                    break
                        break
            except NetMikoAuthenticationException:
                  print("Invalid credentials, please try again")
                  continue
            except Exception as e:
                  print(f"An error has occured: {e}")
                  break

if __name__ == "__main__":
    main()
