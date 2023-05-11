# -*- coding: utf-8 -*-
"""
Title: Simple Client
Author: Fu W.W. Howard
GitHub: https://github.com/fujaidesu
Date: 08 May 2023
Code version: 1.4

Description:
Python3 file for Client sending data to Server.
User can create, fill, serialize, and deliver a dictionary to a server
or send a text file to a server after creating it.
The pickling format of the dictionary can be binary, JSON, or XML.
The text can be encrypted within a text file.

Modification(s):
1. Add function to read file in txt format.
2. host and port are read from configure file.
3. Add pickling_format parameter to main function.

"""

import socket
import json
import os
import pickle
from cryptography.fernet import Fernet
from dict2xml import dict2xml
import configparser
import sys


# function to serialise dictionary
def dict_serialisation(dictionary, serialise, data_format):
    # check if the data needs to be serialised
    # if yes, perform erialisation
    if (serialise):        
        if data_format == 'binary':
            # serialise data using json
            #data = json.dumps(dictionary).encode('utf-8')
            data = pickle.dumps(dictionary)
            data2send = str(data)
        elif data_format == 'json':
            # serialise data using json
            data = json.dumps(dictionary)
            data2send = data
        elif data_format == 'xml':
            # serialise data using xml
            data = dict2xml(dictionary, wrap ='root', indent =' ')
            data2send = data
        print('Data is serialised.')
    else:
        data2send = dictionary
    return str(data2send)

# function to perform encryption
def data_encryption(data, encryption):
    # check if the data needs to be encrypted
    # if yes, perform encryption
    if encryption == True:
        # encryption label
        ENCRYPTED = "<ISENCRYPTED>"
        # perform encryption
        key = Fernet.generate_key()
        fernet = Fernet(key)
        encMessage = fernet.encrypt(str(data).encode())
        # combine the key, encryption label and encrypted message as format of data packet
        data2send = str(key.decode())+ENCRYPTED+str(encMessage.decode())
        print('Data is encrypted.')
    else:
        data2send = data
    return str(data2send)
      
# function to read data from text file
def readFile(filename):
    try:
        dir_path = os.path.dirname(os.path.realpath(__file__)) 
        # get file path
        filepath = dir_path+"\\"+filename
        # check if file exists
        # get the file size
        filesize = os.path.getsize(filepath) 
        # continue if file exists
        if filesize > 0:
            with open(filepath, 'r') as f:
                data = f.read()
        return data
    except Exception: 
        # prevent input file which does not exist
        print('No such file.')

# main function to send data to server 
def sendtoServer(input, encryption, pickling_format):
    
    #Read configfile.ini file
    config_obj = configparser.ConfigParser()
    try:
        filename = 'configfile.ini'
        dir_path = os.path.dirname(os.path.realpath(__file__)) 
        # get file path
        filepath = dir_path+"\\"+filename
        # check if file exists
        # get the file size
        filesize = os.path.getsize(filepath) 
        # continue if file exists
        if filesize > 0:
            print('The config file does exist')

            config_obj.read(filepath)
            param = config_obj["setting"]
            SERVER_HOST = param["host"]
            SERVER_PORT = int(param["port"])
    except Exception: 
        # prevent input file which does not exist
        print('Configure file does not exist.')
        sys.exit()


    try:
        # Create a client socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('A client socket is created.')
    except Exception:
        print('Fail to create client socket.')
        sys.exit()

        
    try:
        # Connect to the server
        s.connect((SERVER_HOST, SERVER_PORT))
        print('The client has connected to the server')
    except Exception:
        print('Fail to connect to the server.')
        sys.exit()

        
    # if user input a dictionary
    if isinstance(input, dict):
            
        try:
            # serialise data in diferent format
            data2send = dict_serialisation(input, encryption, pickling_format)
                
            # send data to server   
            s.send(str(data2send).encode())
            print('Data is sent to server.')
        except:
            print('Please select one of the pickling format: Binary, JSON or XML.')

    # if user input a text file
    # format shall be txt 
    elif isinstance(input, str):
        
        # check format of text file
        if input[-4:] == '.txt':
            
            # read content of text file
            data = readFile(input)
            
            if data is not None:
                # check if the data needs to be encrypted
                # if yes, perform encryption
                data2send = data_encryption(data, encryption)
                
                # send data to server   
                s.send(str(data2send).encode())
                print('Data is sent to server.')
        else:
            # prevent unexpected input of file format
            print('Please input text file in txt format.')
    else:
        # prevent unexpected input
        print('Please input a dictionary or text file in txt format.')
    # close the socket
    s.close()

if __name__ == "__main__":
    
    # define default data format for dictionary serialisation
    pickling_format = 'binary'
    #pickling_format = 'json'
    #pickling_format = 'xml'
        
    # test data
    userinput = {'Test': 1, 'Data': 2, 'Sample': 3}
    #userinput = "test1.txt" # content is dictionary
    #userinput = "test2.txt" # content is string

    # input can be dictionary or text file in txt format
    # if encryption/serialisation is True, data to be sent will be encrypted/serialised, and vice versa
    # For dictionary, one of the pickling format: Binary, JSON or XML shall be selected.
    # Please omit the input of pickling_format if text file name is input
    sendtoServer(userinput, True, pickling_format)
