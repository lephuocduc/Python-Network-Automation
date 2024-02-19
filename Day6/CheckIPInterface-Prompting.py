# Scripting for username and password asking once connect to the devices.

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

with ConnectHandler(**connection_info) as conn:
    out = conn.send_command("display ip interface brief")

print(out)
