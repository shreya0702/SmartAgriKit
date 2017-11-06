import spidev
import time
import MySQLdb
import RPi.GPIO as GPIO
import Adafruit_DHT

sensor = Adafruit_DHT.DHT11
pin = 20

db=MySQLdb.connect("localhost","grp12","1234","tempsensor")
curs=db.cursor()


buzzer_pin= 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)


GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)


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
	

	input_state=GPIO.input(18)
	if input_state == False:
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
	
	input_state2=GPIO.input(26)
	if input_state2 == False:
		
		humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
		if humidity is not None and temperature is not None:
			print 'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)
			#curs.execute("INSERT INTO igdtuw1(temp,hum,time,date) Values(%s,%s,now(),now())" % (temperature, humidity))
			#db.commit() 
		if temperature>27 or humidity<30:
			buzz(500, 2)
		time.sleep(2)

	

	