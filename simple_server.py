# -*- coding: utf-8 -*-
"""
Title: Simple Server
Author: Fu W.W. Howard
GitHub: https://github.com/fujaidesu
Date: 12 May 2023
Code version: 1.5

Description:
Python3 file for Server receiving data from Client.
It keeps looping without closing server as default.
It can perform deserialisation if the data is deserialised.
It can perform decryption if the data is encrypted.
It has configurable option to print received data to screen
and or to save received data to file.
The format of file to be saved can be one of the following:
txt, pickle, JSON and XML.

Modification(s):
1. Input main function variables from config file.
2. Delete close file procedures.
3. Delete redundant enable_printing and enable_file.
4. save2File function enables input of file name instead of file format.
5. Add error handling in save2File.
6. receivefromClient function enables input of file name instead of file format.
7. Add printing for easy flow catching.

"""

import socket
from cryptography.fernet import Fernet
import pickle
import json
import codecs
from dict2xml import dict2xml
import xmltodict
import os
import configparser
import sys

# check if the data is dictionary
def is_dictionary_stream(stream):
    try:
        if isinstance(eval(stream), dict):
            return True
    except Exception:
        return False
    
# check if the data is in pickle format
def is_pickle_stream(stream):
    try:
        data = pickle.loads(eval(stream))
        if data is not None:
            return True
    except Exception:
        return False

# check if the data is in json format
def is_json_stream(stream):
    try:
        data = json.loads(stream)
        if data is not None:
            return True
    except Exception:
        return False

# check if the data is in xml format
def is_xml_stream(stream):
    try:
        data = xmltodict.parse(stream)
        if data is not None:
            return True
    except Exception:
        return False

# function to perform decryption
def data_decryption(data):
    try:
        # encryption label
        ENCRYPTED = "<ISENCRYPTED>"

        if ENCRYPTED in data:
            # get the key and encrypted message
            key, encMessage = str(data).split(ENCRYPTED)
            fernet = Fernet(key)
            # use the key to decrypt message
            decMessage = fernet.decrypt(encMessage)
            data_received = decMessage.decode()
            print('Received data is decrypted')
        else:
            data_received = data
        return data_received
    except Exception:
        print('Error: Fail to decrypt data.')
        sys.exit()

# function to save data content to text file
# format can be txt, pickle, JSON or XML
def save2File(data_received, file):
    # get the file name and file format
    file_name, file_format = str(file).split('.')
    
    if file_format in ['txt','pickle','json','xml']:
        if file_format == 'txt':
            # save data to txt file
            with open(file, 'w') as f:
                f.write(data_received)
                print('The text file in txt format is created.')
        elif file_format == 'pickle':
            # save data to pickle file
            with open(file, 'wb') as f:
                pickle.dump(data_received, f)
                print('The text file in pickle format is created.')
        elif file_format == 'json':
            # save data to json file
            with codecs.open(file, 'w', encoding='utf-8') as f:
                json.dump(data_received, f)
                print('The text file in json format is created.')
        elif file_format == 'xml':
            # save data to xml file
            with open(file, 'w') as f:
                xml = dict2xml(data_received, wrap='root', indent=' ')
                f.write(xml)
                print('The text file in xml format is created.')
    else:
        # prevent unexpected input of file format
        print('Error: Please select one of the format: txt, Pickle, JSON or XML.') 
        sys.exit()

# main function to receive data from client
def receivefromClient(enable_printing, enable_file, file):
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
            BUFFER_SIZE = int(param["buffer"])
            
    except Exception: 
        # prevent input file which does not exist
        print('Error: The config file does not exist')

    try:
        # create the TCP server socket
        s = socket.socket()
        
        # bind the socket to our local address
        s.bind((SERVER_HOST, SERVER_PORT))
        
        # enabling our server to accept connections
        # The amount of unaccepted connections that the system
        # will tolerate before rejecting additional connections is 5
        s.listen(5)
        print('Waiting for connection.')
    except Exception:
        print('Error: Fail to create server socket.')
        sys.exit()

    try:
        # accept any connection
        client_socket, address = s.accept()
        print('Connected to client.')
    except Exception:
        print('Error: Fail to connect to the client')
        sys.exit()
    
    try:
        # receive data using client socket, not server socket
        received = client_socket.recv(BUFFER_SIZE).decode()

        # check if the data is received
        if len(received) > 0:  
            print('Data is received.')
            
            # check the type of received data and perform deserialisation/decryption
            if is_dictionary_stream(received):
                print('Received data is a dictionary.')
                data_received = str(received)
            elif is_pickle_stream(received):
                print('Received data is pickled.')
                data_received = str(pickle.loads(eval(received)))
            elif is_json_stream(received):
                print('Received data is in JSON format')
                data_received = str(json.loads(received))
            elif is_xml_stream(received):
                print('Received data is in XML format')
                data_received = str(xmltodict.parse(received))
            else:
                data_received = str(data_decryption(received))
                
            if data_received is not None:
                # print received data to screen
                if enable_printing:
                    print('The received data:')
                    print(data_received)

                # save received data to file
                # format can be one of the following: txt, Pickle, JSON and XML
                if enable_file:
                    # save data to text file
                    save2File(data_received, file)
                    
            # close the socket
            s.close()
            print('Task Completed. Connection is closed.')
        else:
            print('Error: Received no data. Probably, the input file is empty.')
            sys.exit()
    except Exception:
        print('Unexpected error occured.')

if __name__ == "__main__":
    
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
            input = config_obj["server"]
            PRINT = eval(input["print"])
            SAVE = eval(input["save"])
            FILE = input["file"]
            print('The config file exists and all the parameters have been assigned.')
            
            # main function to receive data from client
            # if PRINT is True, received data will be printed to screen
            # if SAVE is True, received data will be saved to file
            # FILE can one of the format: txt, Pickle, JSON or XML
            receivefromClient(PRINT, SAVE, FILE)
    except Exception: 
        # prevent input file which does not exist
        print('Error: The config file does not exist')
    
