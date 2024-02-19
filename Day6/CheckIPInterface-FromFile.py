# Check IP interface: Create a list of interface randomly. Then apply the Python script to check the information automatically.

from netmiko import ConnectHandler
import getpass

# Prompt for username and password
username = input("Enter your username: ")
password = getpass.getpass()

connection_info = {
    'device_type': 'huawei',
    'host': '10.224.130.1',
    'port': 22,
    'username': username,
    'password': password
}

# Open VLANList.txt and read its contents
with open('VLANList.txt', 'r') as file:
    vlans = file.read().splitlines()

# Assign values to variable vlan
with ConnectHandler(**connection_info) as conn:
    for vlan in vlans:
        out = conn.send_command(f"display ip interface {vlan}")
        print(out)  # Print the output for each VLAN