from netmiko import ConnectHandler, NetMikoAuthenticationException
import getpass

def get_credentials():
    username = input("Enter your username: ")
    password = getpass.getpass()
    return username, password
"""
def test_connection(connection_info):
    with ConnectHandler(**connection_info) as conn:
        conn.disconnect()
        return "Connected successfully"
"""

def get_port_and_vlan():
    port = input("Enter your port: ")
    vlan = input("Enter your Vlan to remove: ")
    return port, vlan

def get_current_vlan_info(conn, vlan):
    out = conn.send_command(f"display {vlan}")
    print(f"BELOW IS YOUR {vlan}")
    print(out)

def get_current_switchport_info(conn, port):
    out = conn.send_command(f"display interface {port}")
    print(f"BELOW IS YOUR PORT {port}")
    print(out)

def remove_vlan_outof_switchport(conn, port, vlan):
    conn.enable()
    config_commands = [
        f'interface {port}',
        f'undo port default {vlan}',
		'commit'
    ]
    output = conn.send_config_set(config_commands)
    print(output)

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
                port, vlan = get_port_and_vlan()
                get_current_vlan_info(conn, vlan)
                get_current_switchport_info(conn, port)
                while True:
                    confirmation = input(f"Do you want to remove {vlan} out of {port}? Yes/ No: ")
                    if confirmation.lower() == "yes":
                        remove_vlan_outof_switchport(conn, port, vlan)
                        break
                    if confirmation.lower() == "no":
                        print("Operation cancelled!")
                        break
                    else:
                        continue
                break
        except NetMikoAuthenticationException:
            print("Invalid credentials. Please try again.")
            continue
        except Exception as e:
            print(f"An error has occured: {e}")
            break

if __name__ == "__main__":
    main()