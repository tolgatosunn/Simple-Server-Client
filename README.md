## Simple Server/Client
Server side can receive data from Client. It keeps looping without closing server as default. It can perform deserialisation if the data is deserialised. It can perform decryption if the data is encrypted.
It has configurable option to print received data to screen and or to save received data to file. The format of file to be saved can be one of the following: txt, pickle, JSON and XML.

Client side can send data to Server. User can create, fill, serialize, and deliver a dictionary to a server or send a text file to a server after creating it. The pickling format of the dictionary can be pickle, JSON, or XML. The text can be encrypted within a text file. 

## Example of Usage
Server and Client shall be ran in two seperated IDE. The usage of two Python3 files is shown as below:

For Simple Server.py, main function:
```python from line 233
# main function to receive data from client
# if PRINT is True, received data will be printed to screen
# if SAVE is True, received data will be saved to file
# FILE can one of the format: txt, Pickle, JSON or XML
receivefromClient(PRINT, SAVE, FILE)
```

For Simple Client.py, main function:
```python from line 171
# USER_INPUT can be dictionary or text file in txt format
# if ENCRYPT is True, data to be sent will be encrypted/serialised, and vice versa
# For dictionary, one of the pickling format: Binary, JSON or XML shall be selected.
# Please omit the input of FORMAT if text file name is input
sendtoServer(USER_INPUT, ENCRYPT, FORMAT)
```

The host, port and buffer size can be modified in config.py.
Also, the variables for main function in Simple Server.py and Simple Client.py can be changed in config.py.
After running the config.py, the settings for the Simple Server.py and Simple Client.py will be stored in configfile.ini.

## Performing Unit Tests
It is able to set unit tests by changing the variables in the config.py. The text files are attached in repository. 

## Requirements
There are extra packages that must be installed in order to use the program which are mentioned in requirements.txt as attached.

## Contributing
Allowing pull requests. If there are any new requirements, please update the test directory when donating. 