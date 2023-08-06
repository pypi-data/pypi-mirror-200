import spidev
import sys
from spidev import SpiDev
from numpy import interp
from time import sleep
import RPi.GPIO as GPIO
import smbus
class tclab:
        
    #construction and deatruction#######################################
    def __init__(self):
        '''set default value'''
        self._Q1 = 0
        self._Q2 = 0
        self._T1 = 21
        self._T2 = 21
        self._LED =100
        
        self.connect()
        self.LED(100)
        
    def __exit__(self):
        self.close()
        
    def __enter__(self):
        return self
    
    def __exit__(self):
        self.close()
        return
    
    def connect(self):
        
        '''set pins'''
        GPIO.setwarnings(False)
        self.led_pin = 18
        self.Q1_pin = 24
        self.Q2_pin = 23
        self.T1_ch = 0
        self.T2_ch = 2
        #try:
        '''setup GPIO'''
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.led_pin,GPIO.OUT)
        GPIO.setup(self.Q1_pin,GPIO.OUT)
        GPIO.setup(self.Q2_pin,GPIO.OUT)
        '''setup I2C'''
        self.fcp8591setup(0x48)
        #self.spi = spi()
        '''setup PWM'''
        self.LEDpwm = GPIO.PWM(self.led_pin, 100)
        self.LEDpwm.start(100)
        self.Q1pwm = GPIO.PWM(self.Q1_pin, 100)
        self.Q1pwm.start(0)
        self.Q2pwm = GPIO.PWM(self.Q2_pin, 100)
        self.Q2pwm.start(0)
        print("Connect to tclab successfully")
        #except:
                #print("Can not connect to tclab. pleace check")
                #sys.exit()
                
    def fcp8591setup(self,addr):
        self.addr=addr
        self.bus=smbus.SMBus(1)
    #set pwm output#####################################################    
    def LED(self, led=0):
        self.LEDpwm.ChangeDutyCycle(led)
        
    def Q1(self, q1=0):
        if q1<0 :
            q1=0
        if q1>100:
            q1=100
        self.Q1pwm.ChangeDutyCycle(q1)
        
    def Q2(self, q2=0):
        if q2<0:
            q2=0
        if q2>100:
            q2=100
        self.Q2pwm.ChangeDutyCycle(q2)

    #get temperature####################################################
    def T1(self):
        data=0
        for i in range(1,11):
            self.bus.write_byte(self.addr,0x40)
            data=data+self.bus.read_byte(self.addr)
        data=data/10
        T1=Converttemp(data)
        return T1
        '''data = 0
        for i in range(1,11):
            data=data+self.spi.analoginput(self.T1_ch)
        data=data/10
        T1 = Converttemp(data)
        return T1'''
    
    def T2(self):
        data=0
        for i in range(1,11):
            self.bus.write_byte(self.addr,0x42)
            data=data+self.bus.read_byte(self.addr)
        data=data/10
        T2=Converttemp(data)
        return T2
        '''data = 0
        for i in range(1,11):
            data=data+self.spi.analoginput(self.T2_ch)
        data=data/10
        T2 = Converttemp(data)
        return T2'''
    
    def close(self):
        
        '''turn off heater'''
        self.Q1(0)
        self.Q2(0)
        
        self.LED(0)
        print("Disconnect successfully")
        return
    
class spi:
    def __init__(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0,0)
    def analoginput(self,channel):
    
        '''setup analog input using mcp3008'''
        self.spi.max_speed_hz = 1350000
        adc = self.spi.xfer2([1,(8+channel)<<4,0])
        data = ((adc[1]&3)<<8)+adc[2]
        return data

#convert analog input into voltd or temperature#########################
def Convertvolts(data):
    volts = (data * 330)/float(255)
    return volts

def Converttemp(data):
    temp = (data * 1.33333)-50
    return temp
        
        
    

