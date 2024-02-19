from netmiko import ConnectHandler

connection_info = {
    'device_type': 'huawei',
    'host': '10.224.130.1',
    'port': 22,
    'username': 'admin',
    'password': '12345678a@'
}

with ConnectHandler(**connection_info) as conn:
		conn.enable()
    config_commands = [
        'interface 10GE 2/0/40',
        'port link-type access',
        'port default vlan 140',
				'commit'
    ]
    output = conn.send_config_set(config_commands)
    print(output)