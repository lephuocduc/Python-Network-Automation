"""
    *Assign VLAN to switch port:*

    Pre-check all vlan infor & vlan interface.
    Yes/No option for execution.
"""

from netmiko import ConnectHandler
import getpass

def get_credentials():
    username = input("Enter your username; ")
    password = getpass.getpass()
    return username, password

def get_port_and_vlan():
    port = input("Enter your port: ")
    vlan = input("Enter your Vlan to assign: ")
    return port, vlan

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

def main():

    username, password = get_credentials()
    port, vlan = get_port_and_vlan()

if __name__ == "__main__":
    main()