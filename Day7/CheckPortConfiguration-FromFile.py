#DONE Create a list of port randomly. Then apply the Python script to check the information automatically -> export to a file (txt or CSV…)

from netmiko import ConnectHandler, NetMikoAuthenticationException
from datetime import datetime
import getpass

# Prompting for username and password
def get_credentials():
	username = input("Enter your username: ")
	password = getpass.getpass()
	return username, password

def get_ports(): # Open PortList.txt and read its contents
	with open('PortList.txt', 'r') as file:
	    return file.read().splitlines()

def check_port_configuration(conn, port):
	out = conn.send_command(f"display interface {port}")
	return out

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
				print("Connected Successfully")
				ports = get_ports()
				timestamp = datetime.now().strftime("%d_%m_%y_%H_%M")
				with open(f"./PortConfiguration/CheckPortConfiguration_Output_{timestamp}.txt",'w') as f:
					for port in ports:
						out = check_port_configuration(conn, port)
						print(out)
						print(out, file=f)
				break
		except NetMikoAuthenticationException:
			print("Invalid credentials, please try again!")
			continue
		except Exception as e:
			print(f"An error has occured: {e}")
			break

if __name__ == "__main__":
	main()