"""
    Pre-check current port description.(Show all port description)
    Yes/No option for execution.
"""

from netmiko import ConnectHandler, NetMikoAuthenticationException
import getpass

def get_credentials():
    username = input("Enter your username: ")
    password = getpass.getpass()
    return username, password

def get_port():
    port = input("Enter your port to remove description: ")
    return port

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
                port = get_port()
                description = get_current_description(conn, port)
                while True:
                    confirmation = input(f"Do you want to remove port description of '{port}' from '{description}'? Yes/ No: ")
                    if confirmation.lower() == 'yes':
                        remove_port_description(conn, port)
                        break
                    if confirmation.lower() == 'no':
                        print("Operation cancelled!")
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