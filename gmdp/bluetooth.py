import serial
import time

class Connector:
    def __init__(self, port):

        self.port = port
        try:
            self.connection = serial.Serial(port, 9600)
        except:
            print("Connection is already established")

    def Wvalue(self, c):
        self.connection.write(str.encode(str(c)))

    def Rvalue(self):
        return self.connection.readline().decode()

    def terminate(self):
        self.connection.close()
