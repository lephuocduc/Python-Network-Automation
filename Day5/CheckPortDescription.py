from netmiko import ConnectHandler

connection_info = {
    'device_type': 'huawei',
    'host': '10.224.130.1',
    'port': 22,
    'username': 'admin',
    'password': '12345678a@'
}

with ConnectHandler(**connection_info) as conn:
	out = conn.send_command("display interface 10GE 2/0/20")
	lines = out.split('\n')
	for line in lines:
		if "Description:" in line:
			description = line.split ("Description:")[1].strip()
			print(description)
			break