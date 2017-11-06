import spidev
import time
import MySQLdb
import RPi.GPIO as GPIO


db=MySQLdb.connect("localhost","grp12","1234","tempsensor")
curs=db.cursor()

buzzer_pin= 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)


spi=spidev.SpiDev()
spi.open(0,0)


def buzz(pitch, duration):
	#period=1.0/ pitch
	#delay= period/2
	#cycles=int(duration*pitch)
	#for i in range(cycles):
	GPIO.output(buzzer_pin, True)
	time.sleep(duration)
	GPIO.output(buzzer_pin, False)
	#time.sleep(duration)



def analog_read(channel):
	r=spi.xfer2([1, (8 + channel) << 4,0])
	adc_out=((r[1]&3) << 8) + r[2]
	return adc_out

while True:
	reading=analog_read(0)
	voltage=reading * 3.3 / 1024
	temp_c=voltage * 100 + 26
	temp_f=temp_c * 9.0 / 5.0 + 32
	print("Temp C=%f\t\tTemp f=%f" % (temp_c, temp_f))
	curs.execute("INSERT INTO soiltemp(temp_c, temp_f) VALUES('%s','%s')", (temp_c, temp_f))
	if temp_c>27:
		buzz(500, 2)

	time.sleep(1)
	db.commit()

	