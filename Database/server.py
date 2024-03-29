 
# import serial
# import sqlite3
# import datetime
# import time
# from PIL import Image
# import io

# con = sqlite3.connect('test.db')  #connection to database

# cur = con.cursor() #cursor obj
# cur.execute('''CREATE TABLE IF NOT EXISTS images(
#             file_name TEXT
#             byte_array BLOB
# )''')
# con.commit()

# ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=3)  #serial obj

# bytes_received = b''

# def isValidImage(data):
#     return data.startswith(b'\xFF\xD8') and data.endswith(b'\xFF\xD9')

# def genFileName():
#     cur_datetime = datetime.datetime.now()
#     return f'{cur_datetime.year}_{cur_datetime.month}_{cur_datetime.day}'

# bytes_received =+ ser.read()
# time.sleep(3.0) # wait for timeout to be over

# if(isValidImage(bytes_received)):
#     #reconstruct image and store it in appropriate filepath
#     #store filepath in database
#     #store byte array in databse
#     image_stream = io.BytesIO(bytes_received)
#     image = Image.open(image_stream)
#     filename = genFileName
#     image.save(filename)

#     cur.execute('''INSERT INTO images
#                 (file_name, byte_array) 
#                 VALUES (filename, ?)''', bytes_received)

import socket 
import datetime


def genFileName():
    cur_datetime = datetime.datetime.now()
    return f'{cur_datetime.year}_{cur_datetime.month}_{cur_datetime.day}'

destDir = "Database/"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 5001))
server.listen() 
print("server is listening!")

client,addr = server.accept()

imageSizeData = client.recv(4)
imageSize = int.from_bytes(imageSizeData,'big')
print("image size: ", imageSize)

image = b''
while len(image) < imageSize:
    packet = client.recv(4096)
    if not packet:
        break
    image += packet


print("image reveived")
fileName = genFileName()

with open(f'{fileName}.jpg', 'wb') as image_file:
    image_file.write(image)

print("image saved!")

client.close()

server.close()






    















