    # -*- coding: utf-8 -*-
"""
Title: Simple Client
Author: Fu W.W. Howard
GitHub: https://github.com/fujaidesu
Date: 18 May 2023
Code version: 1.7

Description:
Python3 file for Client sending data to Server.
User can create, fill, serialize, and deliver a dictionary to a server
or send a text file to a server after creating it.
The pickling format of the dictionary can be binary, JSON, or XML.
The text can be encrypted within a text file.

Modification(s):
1. Add reading_config function.
2. Add create_socket function.
3. Add connect_server function.
4. Add text_file_process function.
5. Add dictionary_process function.
6. Add send_to_server function.
"""

import sys
import os
import socket
import configparser
import json
import pickle
import ast
from dict2xml import dict2xml
from cryptography.fernet import Fernet


def dict_serialisation(dictionary, serialise, dataformat):
    """
    function to serialise dictionary
    check if the data needs to be serialised
    if yes, perform serialisation
    """
    if serialise:
        if dataformat == 'binary':
            try:
                # serialise data using pickle
                data = pickle.dumps(dictionary)
                data2send = str(data)
                print('The dictionary has been serialized in binary')
            except Exception:
                print('Error: An error occurred while serialization in binary')
                sys.exit()
        elif dataformat == 'json':
            try:
                # serialise data using json
                data = json.dumps(dictionary)
                data2send = data
                print('The dictionary has been serialized in json')
            except Exception:
                print('Error: An error occurred while serialization in JSON')
                sys.exit()
        elif dataformat == 'xml':
            try:
                # serialise data using xml
                data = dict2xml(dictionary, wrap ='root', indent =' ')
                data2send = data
                print('The dictionary has been serialized in xml')
            except Exception:
                print('Error: An error occurred while serialization in XML')
                sys.exit()
    else:
        data2send = dictionary
    return str(data2send)

def data_encryption(data, encryption):
    """
    function to perform encryption
    check if the data needs to be encrypted
    if yes, perform encryption
    """
    try:
        if encryption:
            # encryption label
            encrypted = "<ISENCRYPTED>"
            # perform encryption
            key = Fernet.generate_key()
            fernet = Fernet(key)
            message = fernet.encrypt(str(data).encode())
            # combine the key, encryption label and encrypted message as format of data packet
            data2send = str(key.decode())+encrypted+str(message.decode())
            print('Data is encrypted.')
        else:
            data2send = data
            print('No encryption required')
        return str(data2send)
    except Exception:
        print('Error: An error occurred during the encryption.')
        sys.exit()

def read_file(filename, buffer_size):
    """
    function to read data from text file
    """
    try:
        # get folder path
        dir_path = os.path.dirname(os.path.realpath(filename))
        # get file path
        filepath = dir_path+"\\"+filename
        # check if file exists
        # get the file size
        filesize = os.path.getsize(filepath)
        # continue if file exists
        if filesize < buffer_size and filesize < 8192:
            if filesize > 0:
                with open(filepath, 'r', encoding = 'utf-8') as myfile:
                    read_data = myfile.read().splitlines()
                    data = ''.join(read_data)
                    return data
            else:
                print('Error: The file must contain data.')
                sys.exit()
        else:
            print('Error: The file size should not be greater buffer size and 8192 bytes.')
            sys.exit()

    except Exception:
        # prevent input file which does not exist
        print('Error: Txt file can not be found.')
        sys.exit()

def reading_config():
    """
    function to read configfile.ini file
    """
    config_obj = configparser.ConfigParser()
    try:
        filename = 'configfile.ini'
        dir_path = os.path.dirname(os.path.realpath(filename))
        # get file path
        filepath = dir_path+"\\"+filename
        # check if file exists
        # get the file size
        filesize = os.path.getsize(filepath)
        # continue if file exists
        if filesize > 0:
            config_obj.read(filepath)
            param = config_obj["setting"]
            server_host = param["host"]
            server_port = int(param["port"])
            buffer_size = int(param["buffer"])
            input_ = config_obj["client"]
            user_input = input_["userinput"]
            encrypt = ast.literal_eval(input_["encryption"])
            data_format = input_["format"]
            print('The config file exists and all the parameters have been assigned.')
            return server_host, server_port, buffer_size, user_input, encrypt, data_format
    except Exception:
        # prevent input file which does not exist
        print('Error: The config file does not exist')
        sys.exit()

def create_socket():
    """
    function to create a client socket
    """
    try:
        socket_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('A client socket is created.')
        return socket_s
    except Exception:
        print('Error: Fail to create client socket.')
        sys.exit()

def connect_server(socket_s, server_host, server_port):
    """
    function to connect to the server
    """
    try:
        socket_s.connect((server_host, server_port))
        print('Connected to server.')
    except Exception:
        print('Error: Fail to connect to the server.')
        sys.exit()

def text_file_process(user_input, encryption, buffer_size):
    """
    function to read content of text file
    check if the data needs to be encrypted
    if yes, perform encryption
    """
    data = read_file(user_input, buffer_size)
    if data is not None:
        data2send = data_encryption(data, encryption)
        return data2send
    else:
        return None

def dictionary_process(input_, picling_format):
    """
    function to serialise dictionary
    """
    if picling_format in ['binary','json','xml']:
        serialise = 1
    else:
        serialise = 0
    data2send = dict_serialisation(input_, serialise, picling_format)
    return data2send

def send_to_server(data2send, socket_s):
    """
    function to send data to server
    """
    try:
        socket_s.send(str(data2send).encode())
        print('Data is sent to server.')
    except Exception:
        print('Error: An error occurred while sending the data.')
        sys.exit()
    # close the socket
    socket_s.close()
    print('Task Completed. Connection is closed.')

def main_function():
    """
    main function to send data to server
    """
    # Read configfile.ini file
    server_host, server_port, buffer_size, user_input, encrypt, data_format = reading_config()
    # Create a client socket
    socket_s = create_socket()
    # Connect to the server
    connect_server(socket_s, server_host, server_port)
    # Check user input first
    if user_input[-4:]=='.txt':
        data2send = text_file_process(user_input, encrypt, buffer_size)
    else:
        try:
            isdictionary = ast.literal_eval(user_input)
        except Exception:
            print('Error: Input must be a txt file or a dictionary.')
            sys.exit()
        if isinstance(isdictionary, dict):
            data2send = dictionary_process(user_input, data_format)
    send_to_server(data2send, socket_s)

if __name__ == "__main__":
    main_function()
