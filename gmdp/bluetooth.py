import serial
import time

class Connector:
    def __init__(self, port, seat_id):
        print("test")
        self.port = port
        self.seat_id = seat_id
        #try:
        self.connection = serial.Serial(port, 38400)
        #except:
            #print("Connection is already established")

    def Wvalue(self, c):
        self.connection.write(str.encode(str(c)))

    def Rvalue(self):
        return self.connection.read(self.connection.inWaiting())

    def Flush(self):
        self.connection.flushInput()

    def __del__(self):
        print("bye mf")
        self.connection.close()
