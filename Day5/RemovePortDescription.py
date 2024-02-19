from netmiko import ConnectHandler

connection_info = {
        'device_type' : 'huawei',
        'host' : '10.224.130.1',
        'username' : 'admin',
        'password' : '12345678a@',
        'port' : '22',
}

with ConnectHandler (**connection_info) as conn:
    conn.enable()
    config_commands = [
            "interface 10GE 2/0/20",
            "undo description",
            "commit"
            ]
    out = conn.send_config_set(config_commands)
    print(out)