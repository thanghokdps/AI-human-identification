import io
import socket
import struct
import time
import picamera
import serial

ser=serial.Serial('/dev/ttyACM0',9600,timeout=1)
ser.flush()
#Connect to Arduino 
# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
client_socket = socket.socket()
client_recv_data=socket.socket()
client_socket.connect(('192.168.1.239', 8200))
client_recv_data.connect(('192.168.1.239', 8200))

# Make a file-like object out of the connection
connection = client_socket.makefile('wb')
check=True

try:
   while True:
        with picamera.PiCamera() as camera:
            camera.framerate=3
            camera.vflip=True
            camera.resolution = (640, 480)
            # Start a preview and let the camera warm up for 2 seconds
            #camera.start_preview()
            #time.sleep(2)

            # Note the start time and construct a stream to hold image data
            # temporarily (we could write it directly to connection but in this
            # case we want to find out the size of each capture first to keep
            # our protocol simple)
            start = time.time()
            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream,'jpeg'): 
                # Write the length of the capture to the stream and flush to
                # ensure it actually gets sent
                connection.write(struct.pack('<L', stream.tell()))
                connection.flush()
                # Rewind the stream and send the image data over the wire
                stream.seek(0)
                connection.write(stream.read())
                # If we've been capturing for more than 30 seconds, quit
                # Reset the stream for the next capture
                stream.seek(0)
                stream.truncate()
            
                led_input=client_recv_data.recv(1024).decode()
                if led_input=="0":
                    print(led_input)
                    ser.write(b"0\n")
                    if check:
                        line = ser.readline().decode('utf-8').rstrip()
                        client_recv_data.send(line.encode())
                        print(line)
                        check=False
                    client_recv_data.send("0".encode())
                    #led_off
                if led_input=="1":
                    print(led_input)
                    #led_on
                    ser.write(b"1\n")
                    check=True
        # Write a length of zero to the stream to signal we're done
            connection.write(struct.pack('<L', 0))
finally:
    connection.close()
    client_socket.close()
