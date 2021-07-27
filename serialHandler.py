import numpy as np
import sys
import glob
import serial

from threading import Thread
import struct


class Serial():
    def __init__(self,
                 serialPort='COM9',
                 serialBaud=1500000,
                 serialDataNumber=2,
                 serialDataBytesSize=2
                 ):

        self.Port = serialPort
        self.Baud = serialBaud
        self.DataUnpacked = []
        self.DataFormatted = np.empty((0, serialDataNumber))
        self.DataNumber = serialDataNumber
        self.DataBytesSize = serialDataBytesSize
        self.DataNeeded = 100

        self.isRun = False
        self.isReceiving = False
        self.thread = None

    def scanAllPort(self):
        """Lists Serial Port Names

        Raises:
            EnvironmentError: On unsupported or unkown platforms

        Returns:
            Array of string: A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass

        print('List Ports : ', result)
        return result

    def connect(self, port):
        self.Port = port
        print('Trying to connect to: ' + str(self.Port) +
              ' at ' + str(self.Baud) + ' BAUD.')
        try:
            self.serialConnection = serial.Serial(
                self.Port, self.Baud, timeout=4)
            # serialConnection.set_buffer_size(rx_size = 40000, tx_size = 12800)
            self.serialConnection.reset_input_buffer()
            print('Connected to ' + str(self.Port) +
                  ' at ' + str(self.Baud) + ' BAUD.')
            return True
        except:
            print("Failed to connect with " + str(self.Port) +
                  ' at ' + str(self.Baud) + ' BAUD.')
            return False

    def disconnect(self):
        self.serialConnection.write('s'.encode('ascii'))
        self.serialConnection.flushInput()
        self.serialConnection.close()
        print('Successfully disconnected from port ', self.Port)

    def startReceiving(self):
        if self.thread == None:
            self.thread = Thread(target=self.bgSerialPoolingThread)
            self.thread.start()
            self.isRun = True
        else:
            print("Failed to start pooling, an active thread already started")

    def bgSerialPoolingThread(self):
        # Prepare The Hardware and Serial Buffer
        self.serialConnection.write('s'.encode('ascii'))
        self.serialConnection.flushInput()
        self.serialConnection.write('g'.encode('ascii'))
        n = self.DataNumber
        while self.isRun:
            self.DataUnpacked = []
            self.isReceiving = True
            self.serialRAWData = bytearray(self.serialConnection.read(
                self.DataNeeded * self.DataNumber * self.DataBytesSize))
            for x in range(int(len(self.serialRAWData) / self.DataBytesSize)):
                value = struct.unpack('H', self.serialRAWData[
                    x * self.DataBytesSize: x * self.DataBytesSize + self.DataBytesSize])
                self.DataUnpacked.append(value)
            data2Format = [x[0] for x in self.DataUnpacked]
            dataReshaped = [
                data2Format[i * n: (i + 1) * n] for i in range((len(data2Format) + n - 1) // n)]
            print(self.DataFormatted.shape)
            self.DataFormatted = np.concatenate(
                (self.DataFormatted, dataReshaped), axis=0)
            self.isReceiving = False

    def getDataFormatted(self):
        buff = self.DataFormatted
        self.DataFormatted = np.empty((0, self.DataNumber))
        return buff

    def stopReceiving(self):
        print("Closing")
        self.isRun = False
        self.thread.join()
        self.thread = None
        self.serialConnection.write('s'.encode('ascii'))
        self.serialConnection.flushInput()
