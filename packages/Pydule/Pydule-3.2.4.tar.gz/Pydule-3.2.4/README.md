# Pydule-TM

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)                 
[![Python 3.6](https://img.shields.io/badge/python-3.10.7-blue.svg)](https://www.python.org/downloads/release/python-3107/)   

## Functionality of Pydule

- Download Mp3 or Mp4 From Youtube
- Insert Elements in Tuple & String
- Generate Qrcode
- Text Translation
- Replace Letters in String
- Replace Elements in List and Tuple
- Check Weather of any City
- Open any File
- Play Songs
- Get Hex of a any Color
- Convert Text to Speech
- Restart or Shutdown Your System
- Search on Browser

## Usage

- Make sure you have Python installed in your system.
- Run Following command in the CMD.
 ```
  pip install Pydule
  ```
## Example

 ```
# test.py
import Pydule as py

# to Search 
py.search('Youtube')

# to Create Qrcode
text,filename='Hello World','Hello.png'
py.cqrcode(text,filename)

# to Get all Available Functions
py.functions() 

# to Open Calculator
py.openapp('calculator')

# to Download Youtube Audio
py.ytmp3('YOUR LINK HERE')

# to Download Youtube Video with Audio
py.ytmp4('YOUR LINK HERE')
  ```