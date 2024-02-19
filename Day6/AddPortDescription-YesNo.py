"""
    Pre-check current port description.(Show all port description)
    Yes/No option for execution.
"""

from netmiko import ConnectHandler
import getpass

# Prompting for credentials
username = input("Enter your username: ")
password = getpass.getpass()

connection_info = {
    'device_type': 'huawei',
    'host': '10.224.130.1',
    'port': 22,
    'username': username,
    'password': password
}

port = input("Enter your Port: ")
newdescription = input("Enter your Description: ")
description = ""

with ConnectHandler(**connection_info) as conn:
	out = conn.send_command(f"display interface {port}")
	lines = out.split('\n')
	for line in lines:
		if "Description:" in line:
			description = line.split ("Description:")[1].strip()
			break

confirmation = input(f"Do you want to change port description of {port} from {description} to {newdescription}? Yes/ No: " )

if confirmation.lower() == 'yes':
    with ConnectHandler (**connection_info) as conn:
        conn.enable()
        config_commands = [
                f"interface {port}",
                f"description {newdescription}",
                "commit"
                ]
        out = conn.send_config_set(config_commands)
        print(out)
else:
    print("Operation cancelled.")