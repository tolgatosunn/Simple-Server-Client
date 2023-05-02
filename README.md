## Simple Server/Client
Server side can receive data from Client. It keeps looping without closing server as default. It can perform decryption if the data is encrypted.
It has configurable option to print received data to screen and or to save received data to file. The format of file to be saved can be one of the following: pickle, JSON and XML.

Client side can send data to Server. User can create, fill, serialize, and deliver a dictionary to a server or send a text file to a server after creating it. The pickling format of the dictionary can be pickle, JSON, or XML. The text can be encrypted within a text file. 

## Example of Usage
Server and Client shall be ran in two seperated IDE. The usage of two Python3 files is shown as below:

For Server side, it has configurable option to print received data to screen and or to save received data to file.
```python from line 50
# configurable option to print received data to screen
enable_printing = True

# configurable option to save received data to file
enable_file = True
```
The format of output file can also be set inside the program.
```python from line 120
# define default output file format
#file_format = 'pickle'
#file_format = 'json'
file_format = 'xml'
```

For Client side, User can set the value of encryption to be True or False to determine whether data to be sent is necessary to be encrypted.
```python from line 174
# filename can be dictionary or text file in pickle, JSON or XML format. 
# if encryption is True, data to be sent will be encrypted, and vice versa.
sendtoServer(filename, True)
```
Also, user can serialise the dictionary in binary, JSON, or XML format.
```python from line 90
# define default data format
#data_format = 'binary'
#data_format = 'json'
data_format = 'xml'

# serialise data in diferent format
data = data_serialisation(filename, data_format)
```

## Performing Unit Tests
It is able to set unit tests inside Client Python3 file to test the main function. The text file is attached in repository. 
```python from line 156
# Initialisation of dictionary 
lst = {'Test': 1, 'Data': 2, 'Sample': 3}

# serialise data to disk using json 
converted_dict = json.dumps(lst)

# test data
# the name of file to send
filename = lst
#filename = "test.json"
#filename = "test.pickle"
#filename = "test.xml"
#filename = converted_dict
```

## Requirements
There are extra packages that must be installed in order to use the program which are mentioned in requirements.txt as attached.

## Contributing
Allowing pull requests. If there are any new requirements, please update the test directory when donating. 