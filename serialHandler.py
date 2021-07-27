import numpy as np
import sys
import glob
import serial


class Serial():
    def __init__(self,
                 serialPort='COM9',
                 serialBaud=1500000,
                 serialDataNumber=8,
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
        self.serialConnection.close()
        print('Successfully disconnected from port ', self.Port)
