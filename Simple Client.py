# -*- coding: utf-8 -*-
"""
Title: Simple Client
Author: Fu W.W. Howard
GitHub: https://github.com/fujaidesu
Date: 29 Apr 2023
Code version: 1.1

Description:
Python3 file for Client sending data to Server.
User can create, fill, serialize, and deliver a dictionary to a server
or send a text file to a server after creating it.
The pickling format of the dictionary can be pickle, JSON, or XML.
The text can be encrypted within a text file.
"""

import socket
import json
import codecs
import os
import pickle
import xmltodict
from cryptography.fernet import Fernet

# main function to send data to server
# filename can be dictionary or text file in pickle, JSON or XML format.
# if encryption is True, data to be sent will be encrypted, and vice versa.
def sendtoServer(filename, encryption):
    
    # Encryption label
    ENCRYPTED = "<ISENCRYPTED>"
    
    # device's IP address
    # 127.0.0.1 is the IP address of the local computer
    # port needs to match what the server has specified
    SERVER_HOST = "127.0.0.1"
    SERVER_PORT = 9090

    # Create a client socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    s.connect((SERVER_HOST, SERVER_PORT))  

    # if user input a dictionary
    if isinstance(filename, dict):
        
        # serialise data to disk using json
        data = json.dumps(filename)
        
        # check if the data needs to be encrypted
        # if yes, perform encryption
        if encryption == False:
            # send data to server
            s.send(data.encode())
        else:
            # perform encryption
            key = Fernet.generate_key()
            fernet = Fernet(key)
            encMessage = fernet.encrypt(data.encode())
            data2send = str(key.decode())+ENCRYPTED+str(encMessage.decode())
            # send the key and encrypted message to server
            s.send(str(data2send).encode())
        
        print('Data is sent to server.')
        
    # if user input a text file
    # format can be one of the following: binary, JSON and XM  
    elif isinstance(filename, str):
        
        # get format of text file
        file_name, file_extension = os.path.splitext(filename)

        # check format of text file
        if file_extension == '.json' or file_extension == '.pickle' or file_extension == '.xml':
                      
            # get the file size
            filesize = os.path.getsize(filename)

            try:   
                # check if file exists
                if filesize > 0:

                    # read data from text file with different format
                    if file_extension == '.json':
                        with codecs.open(filename, 'rb', encoding='utf-8') as f:
                            data = json.load(f)
                    elif file_extension == '.pickle':
                        with open(filename, "rb") as f:
                            data = pickle.load(f)
                    elif file_extension == '.xml':
                        with open(filename, "r") as f:
                            xml_content = f.read()
                            data = xmltodict.parse(xml_content)
                    
                    # check if the data needs to be encrypted
                    # if yes, perform encryption
                    if encryption == False:
                        # send data to server
                        s.send(str(data).encode())
                    else:
                        # perform encryption
                        key = Fernet.generate_key()
                        fernet = Fernet(key)
                        encMessage = fernet.encrypt(str(data).encode())
                        data2send = str(key.decode())+ENCRYPTED+str(encMessage.decode())
                        # send the key and encrypted message to server
                        s.send(str(data2send).encode())
                    print('Data is sent to server.')
            except EOFError: 
                # prevent input file which does not exist
                print('no such file.')
        else:
            # prevent unexpected input of file format
            print('Please input text file in pickle, JSON or XML format.')
    else:
        # prevent unexpected input
        print('Please input a dictionary or text file in pickle, JSON or XML format.')       
    
    # close the socket
    s.close()

# Initialisation of dictionary
lst = {'Test': 1, 'Data': 2, 'Sample': 3}

# serialise data to disk using json
converted_dict = json.dumps(lst)

# test data
# the name of file to send
filename = lst
#filename = "test.json"
#filename = "test.pickle"
#filename = "test.xml"
#filename = converted_dict

if __name__ == "__main__":
    
    # filename can be dictionary or text file in pickle, JSON or XML format.
    # if encryption is True, data to be sent will be encrypted, and vice versa.
    sendtoServer(filename, True)
