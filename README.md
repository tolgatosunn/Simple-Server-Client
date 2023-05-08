## Simple Server/Client
Server side can receive data from Client. It keeps looping without closing server as default. It can perform deserialisation if the data is deserialised. It can perform decryption if the data is encrypted.
It has configurable option to print received data to screen and or to save received data to file. The format of file to be saved can be one of the following: txt, pickle, JSON and XML.

Client side can send data to Server. User can create, fill, serialize, and deliver a dictionary to a server or send a text file to a server after creating it. The pickling format of the dictionary can be pickle, JSON, or XML. The text can be encrypted within a text file. 

## Example of Usage
Server and Client shall be ran in two seperated IDE. The usage of two Python3 files is shown as below:

For Simple Server.py:
```python from line 220
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
```

For Simple Client.py:
```python from line 165
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
```

The host, port and buffer size can be modified in config.py.
After running the config.py, the settings for the Simple Server.py and Simple Client.py will be stored in configfile.ini.

## Performing Unit Tests
It is able to set unit tests inside Client Python3 file to test the main function. The text file is attached in repository. 
```python from line 172
# test data
userinput = {'Test': 1, 'Data': 2, 'Sample': 3}
#userinput = "test1.txt" # content is dictionary
#userinput = "test2.txt" # content is string
```

## Requirements
There are extra packages that must be installed in order to use the program which are mentioned in requirements.txt as attached.

## Contributing
Allowing pull requests. If there are any new requirements, please update the test directory when donating. 