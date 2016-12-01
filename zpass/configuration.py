import os, configparser


default_config = '''
[passwords]
default_type = alphanumeric
default_alphanumeric_length = 12
default_mnemonic_length = 4
default_show_password = False
default_copy_password = False
default_headers = type,subtype,description,location,username
'''


data_directory = os.path.expanduser('~/.config/zpass/')
config_file = data_directory + 'zpass.ini'


if not os.path.exists(data_directory):
    os.makedirs(data_directory)
if not os.path.isfile(config_file):
    with open(config_file, 'w') as f:
        f.write(default_config)


config = configparser.RawConfigParser(allow_no_value=True)
config.read(config_file)
default_type                = config.get('passwords', 'default_type')
default_alphanumeric_length = config.get('passwords', 'default_alphanumeric_length')
default_mnemonic_length     = config.get('passwords', 'default_mnemonic_length')
default_show_password       = config.getboolean('passwords', 'default_show_password')
default_copy_password       = config.getboolean('passwords', 'default_copy_password')
headers = config.get('passwords','default_headers').split(',')
