# -*- coding: utf-8 -*-
"""
Title: Simple Client
Author: Fu W.W. Howard
GitHub: https://github.com/fujaidesu
Date: 06 May 2023
Code version: 1.3

Description:
Python3 file for Client sending data to Server.
User can create, fill, serialize, and deliver a dictionary to a server
or send a text file to a server after creating it.
The pickling format of the dictionary can be binary, JSON, or XML.
The text can be encrypted within a text file.

Modification(s):
1. Add error handling.
2. Add function to serialise dictionary.

"""

import socket
import json
import codecs
import os
import pickle
from cryptography.fernet import Fernet
from dict2xml import dict2xml
import xmltodict

# function to serialise dictionary
def dict_serialisation(dictionary, data_format):
    # Format label
    BINARY = "<DICT2BINARY>"
    JSON = "<DICT2JSON>"
    XML = "<DICT2XML>"
    
    if data_format == 'binary':
        # serialise data using json
        #data = json.dumps(dictionary).encode('utf-8')
        data = pickle.dumps(dictionary)
        data2send = BINARY+str(data)
    elif data_format == 'json':
        # serialise data using json
        data = json.dumps(dictionary)
        data2send = JSON+data
    elif data_format == 'xml':
        # serialise data using xml
        data = dict2xml(dictionary, wrap ='root', indent =' ')
        data2send = XML+data
    return str(data2send)

# function to perform encryption
def data_encryption(data):
    # Encryption label
    ENCRYPTED = "<ISENCRYPTED>"
    # perform encryption
    key = Fernet.generate_key()
    fernet = Fernet(key)
    encMessage = fernet.encrypt(str(data).encode())
    # send the key and encrypted message to server
    data2send = str(key.decode())+ENCRYPTED+str(encMessage.decode())
    return str(data2send)
            
# function to read data from text file in different format
def readFile(filename, file_format):
    if file_format == '.json':
        with codecs.open(filename, 'rb', encoding='utf-8') as f:
            data = json.load(f)
    elif file_format == '.pickle':
        with open(filename, "rb") as f:
            data = pickle.load(f)
    elif file_format == '.xml':
        with open(filename, "r") as f:
            xml_content = f.read()
            data = xmltodict.parse(xml_content)
    return data

# main function to send data to server
# filename can be dictionary or text file in pickle, JSON or XML format.
# if encryption is True, data to be sent will be encrypted, and vice versa.
def sendtoServer(filename, encryption):
    
    # device's IP address
    # 127.0.0.1 is the IP address of the local computer
    # port needs to match what the server has specified
    SERVER_HOST = "127.0.0.1"
    SERVER_PORT = 9090

    try:
        # Create a client socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except Exception:
        print('Fail to create client socket.')
        return
        
    try:
        # Connect to the server
        s.connect((SERVER_HOST, SERVER_PORT))  
    except Exception:
        print('Fail to connect to the server.')
        return
        
    # if user input a dictionary
    if isinstance(filename, dict):
        
        # define default data format
        data_format = 'binary'
        #data_format = 'json'
        #data_format = 'xml'
            
        try:
            # serialise data in diferent format
            data = dict_serialisation(filename, data_format)
        
            # check if the data needs to be encrypted
            # if yes, perform encryption
            if encryption == True:
                data2send = data_encryption(data)
                print('Data is encrypted.')
            else:
                data2send = data
                
            # send data to server   
            s.send(str(data2send).encode())
            print('Data is sent to server.')
        except:
            print('Please select one of the format: Binary, JSON or XML.')

    # if user input a text file
    # format can be one of the following: binary, JSON and XM  
    elif isinstance(filename, str):
        
        # get format of text file
        file_name, file_format = os.path.splitext(filename)

        # check format of text file
        if file_format == '.json' or file_format == '.pickle' or file_format == '.xml':
                      
            try:  
                # check if file exists
                # get the file size
                filesize = os.path.getsize(filename) 
                
                # continue if file exists
                if filesize > 0:
                    # read data from text file in different format
                    data = readFile(filename, file_format)
                        
                    # check if the data needs to be encrypted
                    # if yes, perform encryption
                    if encryption == True:
                        data2send = data_encryption(data)
                        print('Data is encrypted.')
                    else:
                        data2send = data                    
                    # send data to server   
                    s.send(str(data2send).encode())
                    print('Data is sent to server.')
            except Exception: 
                # prevent input file which does not exist
                print('No such file.')
                      
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
