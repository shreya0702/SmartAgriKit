import RPi.GPIO as GPIO
import time

buzzer_pin= 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def buzz(pitch, duration):
	period=1.0/ pitch
	delay= period/2
	cycles=int(duration*pitch)
	for i in range(cycles):
		GPIO.output(buzzer_pin, True)
		time.sleep(1)
		GPIO.output(buzzer_pin, False)
		time.sleep(1)

while True:
	pitch_s=raw_input("Enter Pitch (200 to 2000): ")
	pitch= float(pitch_s)
	duration_s=raw_input("Enter duration (Seconds): ")
	duration=float(duration_s)
	buzz(pitch, duration)