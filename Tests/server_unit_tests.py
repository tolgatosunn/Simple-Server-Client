import codecs
import inspect
import json
import pickle
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

class TestSimpleServer(unittest.TestCase):
    
    def setUp(self):
        self.data = "{'Test': 1, 'Data': 2, 'Sample': 3}"
        self.badData = "This is bad data"
        self.testXml = 'test'
        
    def tearDown(self):
        if os.path.exists('test.txt'):
           os.remove('test.txt')
        if os.path.exists('test.pickle'):
           os.remove('test.pickle')
        if os.path.exists('test.json'):
           os.remove('test.json')
        if os.path.exists('test.xml'):
           os.remove('test.xml')
    
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
            SimpleServer.save2File('test data', 'test.txt')
            self.assertEqual(fake_output.getvalue().strip(), 'The text file in txt format is created.')
        with open('test.txt') as f:
            self.assertEqual(f.read(), 'test data')

    def test_save2File_pickle(self):
        with patch('sys.stdout', new=StringIO()) as fake_output:
            SimpleServer.save2File(self.data, 'test.pickle')
            self.assertEqual(fake_output.getvalue().strip(), 'The text file in pickle format is created.')
        with open('test.pickle', 'rb') as f:
            self.assertEqual(pickle.load(f), self.data)

    def test_save2File_json(self):
        with patch('sys.stdout', new=StringIO()) as fake_output:
            SimpleServer.save2File(self.data, 'test.json')
            self.assertEqual(fake_output.getvalue().strip(), 'The text file in json format is created.')
        with codecs.open('test.json', 'r', encoding='utf-8') as f:
            self.assertEqual(json.load(f), self.data)

    def test_save2File_xml(self):
        with patch('sys.stdout', new=StringIO()) as fake_output:
            SimpleServer.save2File(self.testXml, 'test.xml')
            self.assertEqual(fake_output.getvalue().strip(), 'The text file in xml format is created.')
        with open('test.xml', 'r') as f:
            self.assertEqual(f.read(), '<root>test</root>')

    def test_save2File_invalid_format(self):
        with patch('sys.stdout', new=StringIO()) as fake_output:
            with self.assertRaises(SystemExit):
                SimpleServer.save2File('test data', 'test.jpg')
            self.assertEqual(fake_output.getvalue().strip(), 'Error: Please select one of the format: txt, Pickle, JSON or XML.')  
        

        
if __name__ == '__main__':
    try:
        unittest.main()
    except Exception:
        print("Not all tests passed")
    except SystemExit:
        print("Done")
        