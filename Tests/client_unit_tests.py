'''
This module performs unit tests of the functions in
"simple_client.py" module in the Simple Server Client Project.
'''

import unittest
from unittest.mock import patch, Mock
import sys
import json
from io import StringIO
import os
import socket
import configparser
import inspect
from cryptography.fernet import Fernet


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from simple_client import dict_serialisation, data_encryption, read_file\
, reading_config, create_socket, connect_server, text_file_process\
, dictionary_process, send_to_server, main_function



class ConfigFileFunctions():
    '''
    This class contains functions that create and read config file.
    '''

    def config_parser():
        '''
        This function creates a mock config file
        to use in the test functions.
        '''
        config = configparser.ConfigParser()

        # setting common setting
        config.add_section('setting')
        config.set('setting', 'host', '127.0.0.1')
        config.set('setting', 'port', '9090')
        config.set('setting', 'buffer', '4096')

        # setting user inputs for client side
        config.add_section('client')
        userinput = "test1.txt" # content is dictionary
        config.set('client', 'userinput', userinput)
        config.set('client', 'encryption', 'True')
        pickling_format = 'xml'
        config.set('client', 'format', pickling_format)

        # setting user inputs for server side
        config.add_section('server')
        config.set('server', 'print', 'True')
        config.set('server', 'save', 'True')
        config.set('server', 'file', userinput)

        # write the new structure to the new file
        filename = 'configfile.ini'
        with open(filename, 'w', encoding="utf-8") as fill:
            config.write(fill)


    def reading_config_file():
        '''
        This function reads a mock config file
        to get variables for the test functions.
        '''

        config_obj = configparser.ConfigParser()
        sys.path.append("..")
        config_obj.read('configfile.ini')
        # Reading common settings
        param = config_obj["setting"]
        server_host = param["host"]
        server_port = int(param["port"])
        # Reading Server settings
        param_server = config_obj["server"]
        print_ = param_server["print"]
        save_ = param_server["save"]
        file_ = param_server["file"]
        # Reading Client settings
        param_client = config_obj["client"]
        userinput = param_client["userinput"]
        encryption = param_client["encryption"]
        format_ = param_client["format"]

        return server_host, server_port, print_, save_, file_, userinput, encryption, format_



class TestDictionarySerialisation(unittest.TestCase):
    '''
    This class performs unit tests of
    the "dict_serialisation" function in the simple_client module.
    '''

    def test_dict_serialisation_binary_serialisation(self):
        '''
        Tests the binary serialization of the `dict_serialisation`
        function with a sample dictionary.
        '''

        # Assigning test variables
        dictionary = "{'Test': 1, 'Data': 2, 'Sample': 3}"
        serialise = True
        data_format = 'binary'
        exp_output = str(b"\x80\x04\x95'\x00\x00\x00\x00\x00\x00\x00\x8c#\
{'Test': 1, 'Data': 2, 'Sample': 3}\x94."
                         )
        # Test Case
        # Catching print of the function to not show on the console
        with open(os.devnull, 'w', encoding="utf-8") as catch:
            sys.stdout = catch
            act_output = str(dict_serialisation(dictionary, serialise, data_format))
            sys.stdout = sys.__stdout__
        self.assertEqual(act_output, exp_output)


    def test_dict_serialisation_json_serialisation(self):
        '''
        Tests the json serialization of the `dict_serialisation`
        function with a sample dictionary.
        '''
        # Assigning test variables
        dictionary = "{'Test': 1, 'Data': 2, 'Sample': 3}"
        serialise = True
        data_format = 'json'
        exp_output = str('"{\'Test\': 1, \'Data\': 2, \'Sample\': 3}"')

        # Test Case
        # Catching print of the function to not show on the console
        with open(os.devnull, 'w', encoding="utf-8") as catch:
            sys.stdout = catch
            act_output = str(dict_serialisation(dictionary, serialise, data_format))
            sys.stdout = sys.__stdout__
        self.assertEqual(act_output, exp_output)


    def test_dict_serialisation_xml_serialisation(self):
        '''
        Tests the xml serialization of the `dict_serialisation`
        function with a sample dictionary.
        '''
        # Assigning test variables
        dictionary = "{'Test': 1, 'Data': 2, 'Sample': 3}"
        serialise = True
        data_format = 'xml'
        exp_output = str("<root>{'Test': 1, 'Data': 2, 'Sample': 3}</root>")

        # Test Case
        # Catching print of the function to not show on the console
        with open(os.devnull, 'w', encoding="utf-8") as catch:
            sys.stdout = catch
            act_output = str(dict_serialisation(dictionary, serialise, data_format))
            sys.stdout = sys.__stdout__
        self.assertEqual(act_output, exp_output)


    def test_dict_serialisation_no_serialisation(self):
        '''
        Tests the `dict_serialisation` function
        when no serialization is required.
        '''
        # Assigning test variables
        dictionary = "{'Test': 1, 'Data': 2, 'Sample': 3}"
        serialise = False
        data_format = 'xml'
        exp_output = str("{'Test': 1, 'Data': 2, 'Sample': 3}")
        # Test Case
        # Catching print of the function to not show on the console
        with open(os.devnull, 'w', encoding="utf-8") as catch:
            sys.stdout = catch
            act_output = str(dict_serialisation(dictionary, serialise, data_format))
            sys.stdout = sys.__stdout__
        self.assertEqual(act_output, exp_output)


class TestDataEncryption(unittest.TestCase):
    '''
    This class performs unit tests of the "data_encryption"
    function in simple_client module.
    '''

    def test_data_encryption(self):
        '''
        Tests the `data_encryption` function
        when encryption is required.
        '''
        # Assigning test variables
        test_data = "Hello University of Liverpool!"
        encryption = True
        encrypted = "<ISENCRYPTED>"

        # Calling encryption function
        # Catching print of the function to not show on the console
        with open(os.devnull, 'w', encoding="utf-8") as catch:
            sys.stdout = catch
            encrypted_data = data_encryption(test_data, encryption)
            sys.stdout = sys.__stdout__

        # Decrypting results of the "data_encryption" function
        key_act, enc_message_act = str(encrypted_data).split(encrypted)
        fernet_act = Fernet(key_act)
        dec_message_act = fernet_act.decrypt(enc_message_act)
        act_result = dec_message_act.decode()

        # Testing the results
        self.assertEqual(act_result, test_data)


    def test_data_no_encryption(self):
        '''
        Tests the `data_encryption` function
        when encryption is not required.
        '''
        # Assigning test variables
        test_data = "Hello University of Liverpool!"
        encryption = False

        # Calling encryption function
        # Catching print of the function to not show on the console
        with open(os.devnull, 'w', encoding="utf-8") as catch:
            sys.stdout = catch
            act_result = data_encryption(test_data, encryption)
            sys.stdout = sys.__stdout__
        # Testing the results
        self.assertEqual(act_result, test_data)


    @patch('simple_client.Fernet.generate_key')
    @patch('sys.stdout', new_callable=StringIO)
    def test_data_encryption_failure(self, mock_generate_key, mock_stdout):
        '''
        Tests the `data_encryption` function
        when encryption is failed.
        '''
        # Mocking the necessary dependencies
        mock_generate_key.side_effect = Exception('Mocked exception')

        # Check that the system exits
        with self.assertRaises(SystemExit):
            data_encryption('Test data', True)
            # Check that the error message was printed to the console
            self.assertEqual(mock_stdout.getvalue().strip(),
                             'Error: An error occurred during the encryption.')


class TestReadFile(unittest.TestCase):
    '''
    This class performs unit tests of the "read_file"
    function in simple_client module.
    '''

    @patch('sys.stdout', new_callable=StringIO)
    def test_reading_file_no_data(self, mock_stdout):
        '''
        Tests the `read_file` function
        with a file does not contain data.
        '''
        # Delete the content in testfile.txt
        with open('testfile.txt', 'w', encoding="utf-8") as catch:
            catch.write('')
        # Check that the system exits
        with self.assertRaises(SystemExit):
            read_file('testfile.txt')
            # Check that the error message was printed to the console
            self.assertEqual(mock_stdout.getvalue().strip(),
                             'Error: The file must contain data.')


    @patch('sys.stdout', new_callable=StringIO)
    def test_reading_file_no_file(self, mock_stdout):
        '''
        Tests the `read_file` function
        with a file does not exist.
        '''
        # Check that the system exits
        with self.assertRaises(SystemExit):
            read_file('nofile.txt')
            # Check that the error message was printed to the console
            self.assertEqual(mock_stdout.getvalue().strip(), 'Error: Txt file can not be found.')



class TestReadingConfig(unittest.TestCase):
    '''
    This class performs unit tests of the "reading_config"
    function in simple_client module.
    '''

    def test_reading_config_success(self):
        '''
        Tests that the "reading_config" function
        gets all the necessary variables from the config file.
        '''
        # Creating config file
        ConfigFileFunctions.config_parser()
        # Reading the config file
        server_host, server_port, _, _, _, userinput, _, format_ = \
                       ConfigFileFunctions.reading_config_file()

        # Getting the variables from the "reading_config" function
        with open(os.devnull, 'w', encoding="utf-8") as catch:
            sys.stdout = catch
            host, port, userinput_, encrypt, _format_ = reading_config()
            sys.stdout = sys.__stdout__

        # Checking the results
        self.assertEqual(host, server_host)
        self.assertEqual(port, server_port)
        self.assertEqual(userinput_, userinput)
        self.assertTrue(encrypt)
        self.assertEqual(_format_, format_)


    @patch('sys.stdout', new_callable=StringIO)
    def test_reading_config_unsuccessful(self, mock_stdout):
        '''
        Tests that the "reading_config" function
        raises an error and exits the system when there is
        no config file.
        '''
        # Specify the path of config file
        file_path = 'configfile.ini'
        # Delete the config file
        os.remove(file_path)

        # Check the system exits
        with self.assertRaises(SystemExit):
            reading_config()
            # Check that the error message was printed to the console
            self.assertEqual(mock_stdout.getvalue().strip(), \
                             'Error: The config file does not exist')



class TestCreateSocket(unittest.TestCase):
    '''
    This class performs unit tests of the "create_socket"
    function in simple_client module.
    '''

    @patch('sys.stdout', new_callable=StringIO)
    def test_create_socket_success(self, mock_stdout):
        '''
        Tests that the "create_socket" function
        successfully creates a socket
        '''
        # Call the create_socket function
        soc = create_socket()

        # Check that the socket was created successfully
        self.assertIsInstance(soc, socket.socket)
        # Check that the informative message was printed to the console
        self.assertEqual(mock_stdout.getvalue().strip(), 'A client socket is created.')

        soc.close()


    @patch('sys.stdout', new_callable=StringIO)
    def test_create_socket_error(self, mock_stdout):
        '''
        Tests that the "create_socket" function
        raises an error message and exits the system
        when a socket can not be created.
        '''
        # Mock the socket.socket function to raise an exception
        with patch('socket.socket', side_effect=Exception()):
            # Call the create_socket function
            # Check that the systems exits
            with self.assertRaises(SystemExit):
                create_socket()
            # Check that the error message was printed to the console
            self.assertEqual(mock_stdout.getvalue().strip(), 'Error: Fail to create client socket.')



class TestConnectServer(unittest.TestCase):
    '''
    This class performs unit tests of the "connect_server"
    function in simple_client module.
    '''

    @patch('sys.stdout', new_callable=StringIO)
    def test_connect_server_success(self, mock_stdout):
        '''
        Tests that the "connect_server" function
        successfully connects the server
        '''
        # Create a mock socket object and server host and port
        s_mock = Mock(spec=socket.socket)
        # Read config file and assign the variables.
        server_host, server_port, _, _, _, _, _, _ = ConfigFileFunctions.reading_config_file()

        # Call the connect_server function
        connect_server(s_mock, server_host, server_port)

        # Check that the socket was connected to the server
        s_mock.connect.assert_called_once_with((server_host, server_port))
        # Check that the informative message was printed to the console
        self.assertEqual(mock_stdout.getvalue().strip(), 'Connected to server.')

        s_mock.close()


    @patch('sys.stdout', new_callable=StringIO)
    def test_connect_server_failure(self, mock_stdout):
        '''
        Tests that the "connect_server" function
        raises an error message and exits the system
        when the client can not connect the server.
        '''
        # Create a mock socket object
        s_mock = Mock(spec=socket.socket)
        # Create a mock exception
        s_mock.connect.side_effect = Exception('Can not connect.')
        # Read config file and assign the variables.
        server_host, server_port, _, _, _, _, _, _ = ConfigFileFunctions.reading_config_file()

        # Call the connect_server function
        # Check that the systems exits
        with self.assertRaises(SystemExit):
            connect_server(s_mock, server_host, server_port)
        # Check that the error message was printed to the console
        self.assertEqual(mock_stdout.getvalue().strip(), 'Error: Fail to connect to the server.')


class TestTextFileProcess(unittest.TestCase):
    '''
    This class performs unit tests of the "text_file_process"
    function in simple_client module.
    '''

    def test_text_file_process_success(self):
        '''
        Tests that the "text_file_process" function
        successfully reads the txt file and returns the data.
        '''
        # Define the input and expected output
        input_ = 'test1.txt'
        encryption = False
        data = "{'Test': 1, 'Data': 2, 'Sample': 3}"

        # Create a mock read_file function that returns the data
        with patch('simple_client.read_file', return_value=data):
            # Catch the print of the function to not show on the console
            with open(os.devnull, 'w', encoding="utf-8") as catch:
                sys.stdout = catch
                # Call the text_file_process function
                result = text_file_process(input_, encryption)
                sys.stdout = sys.__stdout__

                # Check that the result matches with the data
                self.assertEqual(result, data)



class TestDictionaryProcess(unittest.TestCase):
    '''
    This class performs unit tests of the "dictionary_process"
    function in simple_client module.
    '''

    def test_dictionary_process_json(self):
        '''
        Tests that the "dictionary_process" function
        successfully serializes a dictionary in json.
        '''
        # Define a dictionary and pickling_format
        input_ = "{'Name': 'Tolga'}"
        pickling_format = 'json'
        # Define serilized expected_output
        expected_output = json.dumps(input_)

        # Check that the return from the function matches with expected_output
        # Catch the print of the function to not show on the console
        with open(os.devnull, 'w', encoding="utf-8") as catch:
            sys.stdout = catch
            # Call the text_file_process function
            self.assertEqual(dictionary_process(input_, pickling_format), expected_output)
            sys.stdout = sys.__stdout__


    def test_dictionary_process_no_serial(self):
        '''
        Tests that the "dictionary_process" function
        successfully returns the input itself when serialization
        is false.
        '''
        # Test with an invalid serialisation format
        input_ = "{'hi': 'bye'}"
        pickling_format = 'invalid_format'

        # Check that the return from the function matches with input_
        # Catch the print of the function to not show on the console
        with open(os.devnull, 'w', encoding="utf-8") as catch:
            sys.stdout = catch
            # Call the text_file_process function
            self.assertEqual(dictionary_process(input_, pickling_format), input_)
            sys.stdout = sys.__stdout__



class TestSendtoServer(unittest.TestCase):
    '''
    This class performs unit tests of the "send_to_server"
    function in simple_client module.
    '''

    def setUp(self):
        '''
        This function reads the config file, creates a server socket
        , activates the server socket and connects to the server.
        '''
        # Create a config file
        ConfigFileFunctions.config_parser()
        # Read the config file
        server_host, server_port, _, _, _, _, _, _ = \
                ConfigFileFunctions.reading_config_file()

        # Initialize server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((server_host, server_port))
        self.server_socket.listen()

        # Connect client socket to server socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((server_host, self.server_socket.getsockname()[1]))
        self.connection, _ = self.server_socket.accept()


    def test_send_to_server_success(self):
        '''
        Tests that the "send_to_server" function
        successfully connects to the server and sends data.
        '''
        # Define a dictionary
        data2send = {'name': 'Tolga', 'age': 34}
        # Run the "send_to_server" function
        # Catch the print of the function to not show on the console
        with open(os.devnull, 'w', encoding="utf-8") as catch:
            sys.stdout = catch
            send_to_server(data2send, self.client_socket)
            sys.stdout = sys.__stdout__
        # Check that the dictionary was sent successfully. And match with
        # the excepted result
        received_data = self.connection.recv(4096).decode()
        self.assertEqual(received_data.strip(), str(data2send))

        # Close sockets
        self.client_socket.close()
        self.connection.close()
        self.server_socket.close()


    def test_send_to_server_failure(self):
        '''
        Tests that the "send_to_server" function
        prints an error message and exits the system
        when an error occurs during data transmission.
        '''
        # call send_to_server with invalid data
        data2send = 'Tolga'
        no_socket = ''

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            # Call the send_to_server function
            # Check that the systems exits
            with self.assertRaises(SystemExit):
                send_to_server(data2send, no_socket)
            # Check that the error message was printed to the console
            self.assertEqual(mock_stdout.getvalue().strip(), \
                             'Error: An error occurred while sending the data.')

        # Close sockets
        self.client_socket.close()
        self.connection.close()
        self.server_socket.close()



class TestMainFunction(unittest.TestCase):
    '''
    This class performs unit tests of the "main_function"
    function in simple_client module.
    '''

    # Defining all mock inputs
    @patch('simple_client.reading_config')
    @patch('simple_client.create_socket')
    @patch('simple_client.connect_server')
    @patch('simple_client.text_file_process')
    @patch('simple_client.send_to_server')
    def test_main_function_with_text_file(self, mock_send_to_server,
                                          mock_text_file_process,
                                          mock_connect_server, mock_create_socket,
                                          mock_reading_config):
        '''
        Tests that the "main_function" function
        successfully connects to the server, reads a text file
        and sends the data.
        '''
        # Create a config file
        ConfigFileFunctions.config_parser()
        # Read the config file
        server_host, server_port, _, _, _, userinput,encryption, format_ = \
                ConfigFileFunctions.reading_config_file()

        userinput = "test2.txt"

        # Define mock return values
        mock_reading_config.return_value = (server_host, server_port, userinput, \
                                            encryption, format_)
        mock_text_file_process.return_value = "This is a text file for testing."

        # Call the main function
        main_function()

        # Assertions
        mock_create_socket.assert_called_once()
        mock_connect_server.assert_called_once_with(mock_create_socket.return_value,
                                                    server_host, server_port)
        mock_text_file_process.assert_called_once_with(userinput, encryption)
        mock_send_to_server.assert_called_once_with("This is a text file for testing.",
                                                    mock_create_socket.return_value)


    # Defining all mock inputs
    @patch('simple_client.reading_config')
    @patch('simple_client.create_socket')
    @patch('simple_client.connect_server')
    @patch('simple_client.dictionary_process')
    @patch('simple_client.send_to_server')
    def test_main_function_with_dictionary(self, mock_send_to_server, mock_dictionary_process,
                                           mock_connect_server,
                                           mock_create_socket, mock_reading_config):
        '''
        Tests that the "main_function" function
        successfully connects to the server, reads a dictionary
        and sends the data.
        '''
        # Create a config file
        ConfigFileFunctions.config_parser()
        # Read the config file
        server_host, server_port, _, _, _, userinput, encryption, format_ = \
                ConfigFileFunctions.reading_config_file()

        userinput = "{'Name': 'Tolga', 'University': 'UoL'}"

        # Define mock return values
        mock_reading_config.return_value = (server_host, server_port, userinput, \
                                            encryption, format_)
        mock_dictionary_process.return_value = {'Name': 'Tolga', 'University': 'UoL'}

        # Call the main function
        main_function()

        # Assertions
        mock_create_socket.assert_called_once()
        mock_connect_server.assert_called_once_with(mock_create_socket.return_value,
                                                    server_host, server_port)
        mock_dictionary_process.assert_called_once_with(userinput, format_)
        mock_send_to_server.assert_called_once_with({'Name': 'Tolga', 'University': 'UoL'},
                                                    mock_create_socket.return_value)


    # Defining all mock inputs
    @patch('simple_client.reading_config')
    @patch('simple_client.create_socket')
    @patch('simple_client.connect_server')
    def test_main_function_failure(self, mock_connect_server, mock_create_socket,
                                   mock_reading_config):
        '''
        Tests that the "main_function" function
        prints an error message and exits the system
        when the input is not a dictionary or text file.
        '''
        # Create a config file
        ConfigFileFunctions.config_parser()
        # Read the config file
        server_host, server_port, _, _, file_, _, _, _ = \
                ConfigFileFunctions.reading_config_file()

        # Define jpg file to fail the main_function
        file_ = 'UoL_logo.jpg'
        # Define mock return values
        mock_reading_config.return_value = (server_host, server_port, file_, False, 'txt')

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            # Call the main_function function
            # Check that the systems exits
            with self.assertRaises(SystemExit):
                main_function()
            # Check that the error message was printed to the console
            self.assertEqual(mock_stdout.getvalue().strip(),
                             'Error: Input must be a txt file or a dictionary.')



if __name__ == '__main__':
    unittest.main()
