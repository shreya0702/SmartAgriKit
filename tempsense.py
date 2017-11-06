import spidev
import time

spi=spidev.SpiDev()
spi.open(0,0)

def analog_read(channel):
	r=spi.xfer2([1, (8 + channel) << 4,0])
	adc_out=((r[1]&3) << 8) + r[2]
	return adc_out

while True:
	reading=analog_read(1)
	voltage=reading * 3.3 / 1024
	temp_c=voltage * 100 +26
	print("temp=")
	print (temp_c)
        #print("Reading=%d\ttemp=%f" % (reading, temp))
	time.sleep(1)
