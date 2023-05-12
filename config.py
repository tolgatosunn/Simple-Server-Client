# -*- coding: utf-8 -*-
"""
Title: config
Author: Fu W.W. Howard
GitHub: https://github.com/fujaidesu
Date: 12 May 2023
Code version: 1.1

Description:
Python3 file for creating varibles for simple server and client.

Modification(s):
1. Add server section for server varibles input.
2. Add client section for client varibles input.
3. Add printing for easy flow catching.

"""

import configparser

config = configparser.ConfigParser()

# add the structure to the file
# common setting
config.add_section('setting')
config.set('setting', 'host', '127.0.0.1')
config.set('setting', 'port', '9090')
config.set('setting', 'buffer', '4096')

# user input for server side
config.add_section('server')
config.set('server', 'print', 'True')
config.set('server', 'save', 'True')
filename = 'received.txt'
#filename = 'received.json'
#filename = 'received.pickle'
#filename = 'received.xml'
config.set('server', 'file', filename)

# user input for client side
config.add_section('client')
userinput = "{'Test': 1, 'Data': 2, 'Sample': 3}"
#userinput = "test1.txt" # content is dictionary
#userinput = "test2.txt" # content is string
config.set('client', 'userinput', userinput)
config.set('client', 'encryption', 'True')
pickling_format = 'binary'
#pickling_format = 'json'
#pickling_format = 'xml'
config.set('client', 'format', pickling_format)

# write the new structure to the new file
filename = 'configfile.ini'
with open(filename, 'w') as f:
    config.write(f)
    print('Succeed to create config file.')