"""
    Pre-check current port description.(Show all port description)
    Yes/No option for execution.
"""

from netmiko import ConnectHandler, NetMikoAuthenticationException
import getpass

# Prompting for credentials
def get_credentials():
      username = input("Enter your username: ")
      password = getpass.getpass()
      return username, password

def get_port_and_newdescription():
      port = input("Enter your Port: ")
      newdescription = input("Enter your Description: ")
      return port, newdescription

def get_current_description(conn, port):
      out = conn.send_command(f"display interface {port}")
      lines = out.split('\n')
      for line in lines:
           if "Description:" in line:
                return line.split ("Description:")[1].strip()

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
                        port, newdescription = get_port_and_newdescription()
                        description = get_current_description(conn, port)
                        while True:
                              confirmation = input(f"Do you want to change port description of '{port}' from '{description}' to '{newdescription}'? Yes/ No: ")
                              if confirmation.lower() == "yes":
                                    change_description(conn, port, newdescription)
                                    break
                              if confirmation.lower() == "no":
                                    print("Operation cancelled!")
                                    break
                              else:
                                    continue
                        break
            except NetMikoAuthenticationException:
                  print("Invalid credentials, please try again")
                  continue
            except Exception as e:
                  print(f"An error has occured: {e}")
                  break

if __name__ == "__main__":
    main()