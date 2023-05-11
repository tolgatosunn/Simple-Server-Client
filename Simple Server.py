# -*- coding: utf-8 -*-
"""
Title: Simple Server
Author: Fu W.W. Howard
GitHub: https://github.com/fujaidesu
Date: 08 May 2023
Code version: 1.4

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
1. Add functions to check the type of received data.
2. Add function to save file in txt format.
3. host, port and buffer size are read from configure file.
4. Add main function for receiving data from client.

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
        else:
            data_received = data
        return data_received
    except Exception:
        print('Fail to decrypt data.')

# function to save data content to text file
# format can be pickle, JSON or XML
def save2File(data_received, file_format):
    if file_format == 'txt':
        txtFile = "received.txt"
        with open(txtFile, 'w') as f:
            f.write(data_received)
            f.close()
            print('The text file in txt format is created.')
    elif file_format == 'pickle':
        # serialise data to disk using pickle
        pickleFile = "received.pickle"
        with open(pickleFile, 'wb') as f:
            pickle.dump(data_received, f)
            f.close()
            print('The text file in pickle format is created.')
    elif file_format == 'json':
        # serialise data to disk using json
        jsonFile = 'received.json'
        with codecs.open(jsonFile, 'w', encoding='utf-8') as f:
            json.dump(data_received, f)
            f.close()
            print('The text file in json format is created.')
    elif file_format == 'xml':
        # serialise data to disk using xml
        xmlFile = 'received.xml'
        with open(xmlFile, 'w') as f:
            xml = dict2xml(data_received, wrap='root', indent=' ')
            f.write(xml)
            f.close()
            print('The text file in xml format is created.')
    else:
        # prevent unexpected input of file format
        print('Please specific the file type.')

# main function to receive data from client
def receivefromClient(enable_printing, enable_file, file_format):
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
        print('Configure file does not exist.')

    try:
        # create the TCP server socket
        s = socket.socket()
        
        # bind the socket to our local address
        s.bind((SERVER_HOST, SERVER_PORT))
        
        # enabling our server to accept connections
        # The amount of unaccepted connections that the system
        # will tolerate before rejecting additional connections is 5
        s.listen(5)
        
        # flag to show connection to client
        connected = True
    except Exception:
        print('Fail to create socket.')

    # configurable option to print received data to screen
    enable_printing = True

    # configurable option to save received data to file
    enable_file = True

    # keep looping without closing server as default
    while connected:
        try:
            # accept any connection
            client_socket, address = s.accept()
            print('Connected to client.')
        except Exception:
            print('An existing connection to client side is closed.')
        
        try:
            # receive data using client socket, not server socket
            received = client_socket.recv(BUFFER_SIZE).decode()
            
            # check if the data is received
            if len(received) > 0:
                    
                print('Data is received.')
                
                # check the type of received data and perform deserialisation/decryption
                if is_dictionary_stream(received):
                    data_received = received
                elif is_pickle_stream(received):
                    data_received = pickle.loads(eval(received))
                elif is_json_stream(received):
                    data_received = json.loads(received)
                elif is_xml_stream(received):
                    data_received = xmltodict.parse(received)
                else:
                    data_received = data_decryption(received)
                    
                if data_received is not None:
                    # print received data to screen
                    if enable_printing:
                        print('The received data:')
                        print(data_received)

                    # save received data to file
                    # format can be one of the following: txt, Pickle, JSON and XML
                    if enable_file:

                        if file_format in ['txt','pickle','json','xml']:
                            # save data to text file
                            save2File(data_received, file_format)
                        else:
                            print('Please select one of the format: txt, Pickle, JSON or XML.')    
        except Exception:
            print('Fail to receive data.')

if __name__ == "__main__":
    
    # define default output file format
    #file_format = 'txt'
    #file_format = 'pickle'
    #file_format = 'json'
    file_format = 'xml'
                        
    # main function to receive data from client
    # if enable_printing is True, received data will be printed to screen
    # if enable_file is True, received data will be saved to file
    # file_format can one of the format: txt, Pickle, JSON or XML
    receivefromClient(True, True, file_format)
    