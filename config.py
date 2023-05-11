import configparser

config = configparser.ConfigParser()

# Add the structure to the file we will create
config.add_section('setting')
config.set('setting', 'host', '127.0.0.1')
config.set('setting', 'port', '9090')
config.set('setting', 'buffer', '4096')

# Write the new structure to the new file
filename = 'configfile.ini'
with open(filename, 'w') as f:
    config.write(f)