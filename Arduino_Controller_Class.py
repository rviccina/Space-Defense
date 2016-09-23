import serial
import time

"Arduino Controller Object"
class Arduino_Controller(object):
    def __init__(self, path):
        self.path = path
        self.arduino = serial.Serial(self.path, 9600, timeout = 5)
        self.nums = "0123456789"
        self.angle = 0
        self.is_Button_Pressed = False

    "Arduino Thread Function"
    def get_Data(self):
        time.sleep(1)
        self.arduino.flush()
        while(True):
            try:
                dataRecieved = str(self.arduino.readline())
                angle_val = dataRecieved[3:6]
                button_state = dataRecieved[2] 
                if(angle_val[2] in self.nums):
                    angle = int(angle_val)
                elif(angle_val[1] in self.nums):
                    angle = int(angle_val[:2])
                else:
                    angle = int(angle_val[0])

                self.angle = angle
                if(button_state == "T"):
                    self.is_Button_Pressed = True
                else:
                    self.is_Button_Pressed = False
                self.arduino.flush()
            except:
                pass