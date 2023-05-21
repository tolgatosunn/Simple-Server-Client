import codecs
from configparser import ConfigParser
import inspect
import io
import json
import pickle
import socket
import sys
#from typing import Self
import unittest
import xmltodict
from io import StringIO
import os
from unittest.mock import patch

import xml
from dict2xml import dict2xml


# to allow import of the file from the parent directory
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 


import simple_server as SimpleServer
import simple_client as SimpleClient


def create_mock_config_file():
    config = ConfigParser()
    config.add_section('setting')
    config.set('setting', 'host', 'localhost')
    config.set('setting', 'port', '8080')
    config.set('setting', 'buffer', '1024')
    config.add_section('server')
    config.set('server', 'print', 'True')
    config.set('server', 'save', 'False')
    config.set('server', 'file', 'csv')
    
    with open('configfile.ini', 'w') as config_file:
        config.write(config_file)


class TestSimpleServer(unittest.TestCase):
    
    def setUp(self):
        self.data = "{'Test': 1, 'Data': 2, 'Sample': 3}"
        self.badData = "This is bad data"
        self.testXml = 'test'
        create_mock_config_file()
        
    def tearDown(self):
        if os.path.exists('test.txt'):
           os.remove('test.txt')
        if os.path.exists('test.pickle'):
           os.remove('test.pickle')
        if os.path.exists('test.json'):
           os.remove('test.json')
        if os.path.exists('test.xml'):
           os.remove('test.xml')
        if os.path.exists('config.ini'):
            os.remove('config.ini')
    
    # Test to see if a dictionary i correctly matched
    def test_is_dictionary_stream_with_dictionary(self):
        self.assertTrue(SimpleServer.is_dictionary_stream(self.data))
    
    # Test to see if is_dictionary_stream returns false when the data is not a dictionary
    def test_is_dictionary_stream_with_bad_data(self):
        self.assertTrue(not SimpleServer.is_dictionary_stream(self.badData))
      

    def test_is_pickle_stream_with_pickle(self):
        self.assertTrue(SimpleServer.is_pickle_stream(str(pickle.dumps(self.data))))
        
    def test_is_pickle_stream_with_bad_pickle_data(self):
        self.assertTrue(not SimpleServer.is_pickle_stream(self.badData))
        
    #Test JSON 
    def test_is_json_stream_with_JsonString(self):
         jsondata=json.dumps(self.data)
         self.assertTrue(SimpleServer.is_json_stream(jsondata))
         
    def test_is_json_stream_with_bad_data(self):
        self.assertTrue(not SimpleServer.is_json_stream(self.badData))   
         
         
    #Test xml stream 
    def test_is_xml_stream_with_xml(self) :
        xmldata=dict2xml(self.data, wrap ='root', indent =' ')#
        result = self.assertTrue(SimpleServer.is_xml_stream(xmldata))
        return result
    
    def test_is_xml_stream_with_bad_data(self):
        result = self.assertTrue(not SimpleServer.is_xml_stream(self.badData))
        return result

    #Test data_decryption
    def test_is_decryption_with_encypted_data(self):
        encryptedData =  SimpleClient.data_encryption(self.data, True)
        expectedResult = str(self.data)
        
        # check encyption works
        result = self.assertEqual(SimpleServer.data_decryption(encryptedData),expectedResult)
        
    def test_is_decryption_with_unencypted_data(self): 
        expectedResult = str(self.data)
        # check encyption works
        result = self.assertEqual(SimpleServer.data_decryption(str(self.data)),expectedResult) 
        
    def test_save2File_txt(self):
        with patch('sys.stdout', new=StringIO()) as fake_output:
            SimpleServer.save_file('test data', 'test.txt')
            self.assertEqual(fake_output.getvalue().strip(), 'The text file in txt format is created.')
        with open('test.txt') as f:
            self.assertEqual(f.read(), 'test data')

    def test_save_File_pickle(self):
        with patch('sys.stdout', new=StringIO()) as fake_output:
            SimpleServer.save_file(self.data, 'test.pickle')
            self.assertEqual(fake_output.getvalue().strip(), 'The text file in pickle format is created.')
        with open('test.pickle', 'rb') as f:
            self.assertEqual(pickle.load(f), self.data)

    def test_save_File_json(self):
        with patch('sys.stdout', new=StringIO()) as fake_output:
            SimpleServer.save_file(self.data, 'test.json')
            self.assertEqual(fake_output.getvalue().strip(), 'The text file in json format is created.')
        with codecs.open('test.json', 'r', encoding='utf-8') as f:
            self.assertEqual(json.load(f), self.data)

    def test_save_File_xml(self):
        with patch('sys.stdout', new=StringIO()) as fake_output:
            SimpleServer.save_file(self.testXml, 'test.xml')
            self.assertEqual(fake_output.getvalue().strip(), 'The text file in xml format is created.')
        with open('test.xml', 'r') as f:
            self.assertEqual(f.read(), '<root>test</root>')

    def test_save_File_invalid_format(self):
        with patch('sys.stdout', new=StringIO()) as fake_output:
            with self.assertRaises(SystemExit):
                SimpleServer.save_file('test data', 'test.jpg')
            self.assertEqual(fake_output.getvalue().strip(), 'Error: Please select one of the format: txt, Pickle, JSON or XML.')  
    
    def test_reading_config_valid(self):
        expected_host = 'localhost'
        expected_port = 8080
        expected_buffer = 1024
        expected_print = True
        expected_save = False
        expected_format = 'csv'

        with patch('sys.stdout', new=StringIO()) as fake_output:
            result = SimpleServer.reading_config()

        self.assertEqual(result[0], expected_host)
        self.assertEqual(result[1], expected_port)
        self.assertEqual(result[2], expected_buffer)
        self.assertEqual(result[3], expected_print)
        self.assertEqual(result[4], expected_save)
        self.assertEqual(result[5], expected_format)
        self.assertIn('The config file exists and all the parameters have been assigned.', fake_output.getvalue())

    @patch('socket.socket')
    def test_create_socket_success(self, mock_socket):
        mock_socket.return_value = "mock_socket_object"

        result = SimpleServer.create_socket()

        self.assertEqual(result, "mock_socket_object")
        mock_socket.assert_called_once_with(socket.AF_INET, socket.SOCK_STREAM)
        
    @patch('socket.socket')
    def test_connect_client_success(self, mock_socket):
        mock_socket_object = mock_socket.return_value
        mock_bind = mock_socket_object.bind
        mock_listen = mock_socket_object.listen
        mock_accept = mock_socket_object.accept

        mock_bind.return_value = None
        mock_listen.return_value = None
        mock_accept.return_value = ("mock_client_socket", "mock_address")

        server_host = "127.0.0.1"
        server_port = 8080

        result = SimpleServer.connect_client(mock_socket_object, server_host, server_port)

        self.assertEqual(result, "mock_client_socket")
        mock_bind.assert_called_once_with((server_host, server_port))
        mock_listen.assert_called_once_with(5)
        mock_accept.assert_called_once()
        
    def test_receive_from_client_dictionary_stream(self):
        received = {"key": "value"}
        socket_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        result = SimpleServer.receive_from_client(received, socket_s)
        
        self.assertEqual(result, str(received))
        socket_s.close()

    def test_receive_from_client_pickle_stream(self):
        received = str(pickle.dumps("data"))
        socket_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        result = SimpleServer.receive_from_client(received, socket_s)
        
        self.assertEqual(result, "data")
        socket_s.close()

    def test_receive_from_client_json_stream(self):
        received = json.dumps({"key": "value"})
        socket_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        result = SimpleServer.receive_from_client(received, socket_s)
        
        self.assertEqual(result, received)
        socket_s.close()

    def test_receive_from_client_xml_stream(self):
        received = "<root><key>value</key></root>"
        socket_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        result = SimpleServer.receive_from_client(received, socket_s)
        
        self.assertEqual(result, str({"root": {"key": "value"}}))
        socket_s.close()

    def test_receive_from_client_data_decryption(self):
        received = "encrypted_data"
        socket_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        result = SimpleServer.receive_from_client(received, socket_s)
        
        self.assertEqual(result, str(received))
        socket_s.close()
        
    def test_printing_data(self):
        data_received = "This is the received data."
        expected_output = "The received data: This is the received data.\n"

        # Redirect stdout to capture the print output
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Call the function
        SimpleServer.printing_data(data_received)

        # Get the printed output
        actual_output = captured_output.getvalue()

        # Reset stdout
        sys.stdout = sys.__stdout__

        # Assert the printed output matches the expected output
        self.assertEqual(actual_output, expected_output)

        
if __name__ == '__main__':
    try:
        unittest.main()
    except Exception:
        print("Not all tests passed")
    except SystemExit:
        print("Done")
        
        
        