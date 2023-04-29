# -*- coding: utf-8 -*-
"""
Title: Simple Server
Author: Fu W.W. Howard
GitHub: https://github.com/fujaidesu
Date: 29 Apr 2023
Code version: 1.1

Description:
Python3 file for Server receiving data from Client.
It keeps looping without closing server as default.
It can perform decryption if the data is encrypted.
It has configurable option to print received data to screen
and or to save received data to file.
The format of file to be saved can be one of the following:
pickle, JSON and XML.
"""

import socket
from cryptography.fernet import Fernet
import pickle
import json
import codecs

# device's IP address
# 127.0.0.1 is the IP address of the local computer
# port needs to match what the client has specified
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 9090

# receive 4096 bytes each time
BUFFER_SIZE = 4096

# Encryption label
ENCRYPTED = "<ISENCRYPTED>"

# create the TCP server socket
s = socket.socket()

# bind the socket to our local address
s.bind((SERVER_HOST, SERVER_PORT))

# enabling our server to accept connections
# The amount of unaccepted connections that the system
# will tolerate before rejecting additional connections is 5
s.listen(5)

# configurable option to print received data to screen
enable_printing = True

# configurable option to save received data to file
enable_file = True

# keep looping without closing server as default
while True:
    # accept any connection
    client_socket, address = s.accept()

    # receive data using client socket, not server socket
    received = client_socket.recv(BUFFER_SIZE).decode()

    # check if the data is received
    if len(received) > 0:
        # check if the data is encrypted
        # if yes, perform decryption
        if ENCRYPTED in received:
            # get the key and encrypted message
            key, encMessage = received.split(ENCRYPTED)
            fernet = Fernet(key)
            # use the key to decrypt message
            decMessage = fernet.decrypt(encMessage)
            data_received = decMessage.decode()
        else:
            data_received = received

        # print received data to screen
        if enable_printing:
            print('The received data:')
            print(data_received)

        # save received data to file
        # format can be one of the following: binary, JSON and XML
        if enable_file:
            # define default output file format
            #file_format = 'pickle'
            #file_format = 'json'
            file_format = 'xml'

            if file_format == 'pickle':
                # serialise data to disk using pickle
                pickleFile = "received.pickle"
                with open(pickleFile, 'wb') as f:
                    pickle.dump(data_received, f)
                    print('The text file in pickle format is created.')
            elif file_format == 'json':
                # serialise data to disk using json
                jsonFile = 'received.json'
                with codecs.open(jsonFile, 'w', encoding='utf-8') as f:
                    json.dump(data_received, f)
                    print('The text file in json format is created.')
            elif file_format == 'xml':
                # serialise data to disk using xml
                xmlFile = 'received.xml'
                with open(xmlFile, 'w') as f:
                    f.write(data_received)
                    print('The text file in xml format is created.')
            else:
                # prevent unexpected input of file format
                print('Please specific the file type.')
