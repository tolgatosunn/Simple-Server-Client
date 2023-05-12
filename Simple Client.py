# -*- coding: utf-8 -*-
"""
Title: Simple Client
Author: Fu W.W. Howard
GitHub: https://github.com/fujaidesu
Date: 12 May 2023
Code version: 1.5

Description:
Python3 file for Client sending data to Server.
User can create, fill, serialize, and deliver a dictionary to a server
or send a text file to a server after creating it.
The pickling format of the dictionary can be binary, JSON, or XML.
The text can be encrypted within a text file.

Modification(s):
1. Input main function variables from config file.
2. sendtoServer function method of checking user input.
3. Add printing for easy flow catching.

"""

import socket
import json
import os
import pickle
from cryptography.fernet import Fernet
from dict2xml import dict2xml
import configparser

# function to serialise dictionary
def dict_serialisation(dictionary, serialise, data_format):
    # check if the data needs to be serialised
    # if yes, perform serialisation
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
        # get folder path
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
            config_obj.read(filepath)
            param = config_obj["setting"]
            SERVER_HOST = param["host"]
            SERVER_PORT = int(param["port"])
    except Exception: 
        # prevent input file which does not exist
        print('Configure file does not exist.')

    try:
        # Create a client socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except Exception:
        print('Fail to create client socket.')
        
    try:
        # Connect to the server
        s.connect((SERVER_HOST, SERVER_PORT)) 
        print('Connected to server.') 
    except Exception:
        print('Fail to connect to server.')
        
    # if user input a txt file
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
        # serialise data in diferent format
        data2send = dict_serialisation(input, encryption, pickling_format)
            
        # send data to server   
        s.send(str(data2send).encode())
        print('Data is sent to server.')
        
    # close the socket
    s.close()
    print('Client is closed.')

if __name__ == "__main__":

    #Read configfile.ini file
    config_obj = configparser.ConfigParser()
    try:
        filename = 'configfile.ini2'
        dir_path = os.path.dirname(os.path.realpath(__file__)) 
        # get file path
        filepath = dir_path+"\\"+filename
        # check if file exists
        # get the file size
        filesize = os.path.getsize(filepath) 
        # continue if file exists
        if filesize > 0:
            config_obj.read(filepath)
            input = config_obj["client"]
            USER_INPUT = input["userinput"]
            ENCRYPT = eval(input["encryption"])
            FORMAT = input["format"]
            
            # USER_INPUT can be dictionary or text file in txt format
            # if ENCRYPT is True, data to be sent will be encrypted/serialised, and vice versa
            # For dictionary, one of the pickling format: Binary, JSON or XML shall be selected.
            # Please omit the input of FORMAT if text file name is input
            sendtoServer(USER_INPUT, ENCRYPT, FORMAT)
    except Exception: 
        # prevent input file which does not exist
        print('Configure file does not exist.')
