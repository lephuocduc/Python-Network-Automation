from netmiko import ConnectHandler

connection_info = {
    'device_type': 'huawei',
    'host': '10.224.130.1',
    'port': 22,
    'username': 'admin',
    'password': '12345678a@'
}

port = input("Enter your port: ")

with ConnectHandler(**connection_info) as conn:
	out = conn.send_command(f"display interface {port}")
	lines = out.split('\n')
	for line in lines:
		if "Description:" in line:
			description = line.split ("Description:")[1].strip()
			print(description)
			break