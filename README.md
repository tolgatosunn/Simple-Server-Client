## Simple Server/Client
Server side can receive data from Client. It can perform deserialisation if the data is deserialised. It can perform decryption if the data is encrypted.
It has configurable option to print received data to screen and or to save received data to file. The format of file to be saved can be one of the following: txt, pickle, JSON and XML.

Client side can send data to Server. User can create, fill, serialize, and deliver a dictionary to a server or send a text file to a server after creating it. The pickling format of the dictionary can be pickle, JSON, or XML. The text can be encrypted within a text file. 

## Example of Usage
Both the server and the client must run in separate IDEs. 
The variables set in config.py provide the basis for the usage of two Python3 files.
In config.py, the host, port, and buffer size can be changed.
Additionally, config.py allows for the modification of the major function variables in simple_server.py and simple_client.py.
The settings for the simple_server.py and simple_client.py will be saved in configfile.ini after running config.py.

## Performing Unit Tests
By altering the variables in config.py, it may set unit tests. The repository attachment contains the text files.
In the "Tests" folder are supplied common unit tests with explanations.
simple_client.py's unit tests are provided by client_unit_tests.py, while simple_server.py's unit tests are provided by server_unit_tests.py.
The "Test Document" contains a description of each unit test's objectives.

## Requirements
There are extra packages that must be installed in order to use the program which are mentioned in requirements.txt as attached.

## Contributing
Allowing pull requests. If there are any new requirements, please update the test directory when donating. 