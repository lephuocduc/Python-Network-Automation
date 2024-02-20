from netmiko import ConnectHandler

connection_info = {
    'device_type': 'huawei',
    'host': '10.224.130.1',
    'port': 22,
    'username': 'admin',
    'password': '12345678a@'
}

with ConnectHandler(**connection_info) as conn:
	 out = conn.send_command("display ip interface brief")


print(out)