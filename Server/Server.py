import io
import cv2
import socket
import struct
from PIL import Image
import numpy as np
import time
import PBL5
import DBWork

server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8200))
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
conn,addr=server_socket.accept()#response data
check=True
try:
    while True:
        # Read the length of the image as a 32-bit unsigned long. If the
        # length is zero, quit the loop
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break
        # Construct a stream to hold the image data and read the image
        # data from the connection
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        # Rewind the stream, open it as an image with PIL and do some
        # processing on it
        image_stream.seek(0)
        image = Image.open(image_stream).convert('RGB')
        open_cv_image = np.array(image)
        #open_cv_image = open_cv_image.copy()
        # cv2.imwrite("detection.jpg", open_cv_image)
        # image = cv2.imread('detection.jpg')
        if PBL5.detection(open_cv_image)==False:
            if check:
                start_time=time.time()
                DBWork.LightStatus(0)
                check=False
            if time.time()-start_time>5:#After 3 minutes No Human-> Led OFF
                print("OFF")
                conn.send("0".encode())
                DBWork.Consumption(float(conn.recv(1024).decode()))
            else:
                conn.send("-1".encode())
        else:
            conn.send("1".encode())
            if check==False:
                DBWork.LightStatus(1)
                #DBWork.addImage()
            check=True
            print("ON")
        cv2.imshow('Network Image', open_cv_image)
        cv2.waitKey(1)
finally:
    connection.close()
    server_socket.close()









