# -*- coding: utf-8 -*-
"""
Title: Simple Server
Author: Fu W.W. Howard
GitHub: https://github.com/fujaidesu
Date: 18 May 2023
Code version: 1.6

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
1. Add reading_config function.
2. Add create_socket function.
3. Add connect_client function.
4. Add printing_data function.
5. Add receive_from_client function.
6. Add main_function function.
"""

import sys
import os
import socket
import configparser
import codecs
import json
import pickle
import ast
from dict2xml import dict2xml
import xmltodict
from cryptography.fernet import Fernet


def is_dictionary_stream(stream):
    """
    function to check if the data is dictionary
    """
    try:
        if isinstance(ast.literal_eval(stream), dict):
            return True
    except Exception:
        return False

def is_pickle_stream(stream):
    """
    function to check if the data is in pickle format
    """
    try:
        data = pickle.loads(ast.literal_eval(stream))
        if data is not None:
            return True
    except Exception:
        return False

def is_json_stream(stream):
    """
    function to check if the data is in json format
    """
    try:
        data = json.loads(stream)
        if data is not None:
            return True
    except Exception:
        return False

def is_xml_stream(stream):
    """
    function to check if the data is in xml format
    """
    try:
        data = xmltodict.parse(stream)
        if data is not None:
            return True
    except Exception:
        return False

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
            user_input = config_obj["server"]
            enable_print = ast.literal_eval(user_input["print"])
            enable_save = ast.literal_eval(user_input["save"])
            file_format = user_input["file"]
            print('The config file exists and all the parameters have been assigned.')
            return server_host, server_port, buffer_size, enable_print, enable_save, file_format
    except Exception:
        # prevent input file which does not exist
        print('Error: The config file does not exist')
        sys.exit()

def create_socket():
    """
    function to create a server socket
    """
    try:
        socket_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("The server socket is created. Waiting for connection.")
        return socket_s
    except Exception:
        print('Error: Fail to create server socket.')
        sys.exit()

def connect_client(socket_s, server_host, server_port):
    """
    function to connect to the client
    """
    try:
        # bind the socket to our local address
        socket_s.bind((server_host, server_port))
        # enabling our server to accept connections
        # The amount of unaccepted connections that the system
        # will tolerate before rejecting additional connections is 5
        socket_s.listen(5)
        # accept any connection
        client_socket = socket_s.accept()[0]
        print('Connected to client.')
        return client_socket
    except Exception:
        print('Error: Fail to connect to the client.')
        sys.exit()

def data_decryption(data):
    """
    function to perform decryption
    """
    try:
        # encryption label
        encrypted = "<ISENCRYPTED>"

        if encrypted in data:
            # get the key and encrypted message
            key, message = str(data).split(encrypted)
            fernet = Fernet(key)
            # use the key to decrypt message
            message = fernet.decrypt(message)
            data_received = message.decode()
            print('Received data is decrypted.')
        else:
            data_received = data
        return data_received
    except Exception:
        print('Error: Fail to decrypt data.')
        sys.exit()

def receive_from_client(received, socket_s):
    """
    function to receive data from client
    """
    # check if the data is received
    if len(received) > 0:
        print('Data is received.')
        # check the type of received data and perform deserialisation/decryption
        if is_dictionary_stream(received):
            print('Received data is a dictionary.')
            data_received = str(received)
        elif is_pickle_stream(received):
            print('Received data is pickled.')
            data_received = str(pickle.loads(ast.literal_eval(received)))
        elif is_json_stream(received):
            print('Received data is in JSON format')
            data_received = str(json.loads(received))
        elif is_xml_stream(received):
            print('Received data is in XML format')
            data_received = str(xmltodict.parse(received))
        else:
            data_received = str(data_decryption(received))
        # close the socket
        socket_s.close()
        print("The task is completed. And the connection is closed.")
        return data_received
    else:
        print('Error: Received no data. Probably, the input file is empty.')
        sys.exit()

def printing_data(data_received):
    """
    function to print received data to screen
    """
    print('The received data: ' + data_received)

def save_file(data_received, file):
    """
    function to save data content to text file
    format can be txt, pickle, JSON or XML
    """
    # get the file name and file format
    file_format = str(file).split('.')[1]
    if file_format in ['txt','pickle','json','xml']:
        if file_format == 'txt':
            # save data to txt file
            with open(file, 'w') as myfile:
                myfile.write(data_received)
                print('The text file in txt format is created.')
        elif file_format == 'pickle':
            # save data to pickle file
            with open(file, 'wb') as myfile:
                pickle.dump(data_received, myfile)
                print('The text file in pickle format is created.')
        elif file_format == 'json':
            # save data to json file
            with codecs.open(file, 'w', encoding='utf-8') as myfile:
                json.dump(data_received, myfile)
                print('The text file in json format is created.')
        elif file_format == 'xml':
            # save data to xml file
            with open(file, 'w') as myfile:
                xml = dict2xml(data_received, wrap='root', indent=' ')
                myfile.write(xml)
                print('The text file in xml format is created.')
    else:
        # prevent unexpected input of file format
        print('Error: Please select one of the format: txt, Pickle, JSON or XML.')
        sys.exit()

def main_function():
    """
    main function to receive data from client
    """
    #Read configfile.ini file
    server_host, server_port, buffer_size, enable_print, enable_save, file_format = reading_config()
    # Create a client socket
    socket_s = create_socket()
    # Connect to the client
    client_socket = connect_client(socket_s, server_host, server_port)
    # receive data using client socket, not server socket
    received = client_socket.recv(buffer_size).decode()
    data_received = receive_from_client(received, socket_s)
    if enable_print:
        printing_data(data_received)
    if enable_save:
        save_file(data_received, file_format)

if __name__ == "__main__":
    main_function()
