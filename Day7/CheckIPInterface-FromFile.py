# Create a list of interface randomly. Then apply the Python script to check the information automatically -> export to a file (txt or CSV…)
from netmiko import ConnectHandler, NetMikoAuthenticationException
from datetime import datetime
import getpass

# Prompt for username and password
def get_credentials():
    username = input("Enter your username: ")
    password = getpass.getpass()
    return username, password

def get_vlans():
    with open('VLANList.txt','r') as file:
        return file.read().splitlines()

def display_ip_interface(conn, vlan, file):
    out = conn.send_command(f"display ip interface {vlan}")
    print(out)
    print(out, file=file)
    
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
                vlans = get_vlans()
                timestampt = datetime.now().strftime("%d_%m_%y_%H_%M")
                with open(f'CheckIPInterface_Output_{timestampt}.txt','w') as f:
                    for vlan in vlans:
                        display_ip_interface(conn, vlan, f)
            break
        except NetMikoAuthenticationException:
            print("Invalid credentials. Please try again.")
            continue
        except Exception as e:
            print(f"An error has occured {e}")
            break

if __name__ == "__main__":
    main()