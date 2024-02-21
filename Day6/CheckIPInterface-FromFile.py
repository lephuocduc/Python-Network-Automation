# Check IP interface: Create a list of interface randomly. Then apply the Python script to check the information automatically.

from netmiko import ConnectHandler, NetMikoAuthenticationException
import getpass

# Prompt for username and password
def get_credentials():
    username = input("Enter your username: ")
    password = getpass.getpass()
    return username, password

def get_vlans():
    with open('VLANList.txt','r') as file:
        return file.read().splitlines()

def display_ip_interface(conn, vlan):
    out = conn.send_command(f"display ip interface {vlan}")
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
                vlans = get_vlans()
                for vlan in vlans:
                    display_ip_interface(conn, vlan)
        except NetMikoAuthenticationException:
            print("Invalid credentials. Please try again.")
            continue
        except Exception as e:
            print(f"An error has occured {e}")
            break

if __name__ == "__main__":
    main()