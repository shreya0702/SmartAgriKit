import RPi.GPIO as GPIO
from Tkinter import *
import time
import spidev


root=Tk()
var=StringVar()
var.set("Hello")

spi=spidev.SpiDev()
spi.open(0,0)

def analog_read(channel):
	r=spi.xfer2([1, (8 + channel) << 4,0])
	adc_out=((r[1]&3) << 8) + r[2]
	return adc_out


def soiltemp():
	
	l=Label(root, height=50, width=100, textvariable=var)
	l.pack()
	i=0
	while i<20:
		i=i+1
		reading=analog_read(0)
		voltage=reading * 3.3 / 1024
		temp_c=voltage * 100 + 26
		temp_f=temp_c * 9.0 / 5.0 + 32
		var.set(temp_c)
		time.sleep(1)	
		root.update_idletasks()
		i=i+1
	


button1= Button(text="Soil Temperature", command=soiltemp)
button1.pack()

pk=Tk()
pk.mainloop()