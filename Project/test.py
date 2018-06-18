import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
import time
from web.Classes.HX711 import HX711
from web.Classes.DRV8825 import DRV8825
from Classes.Servo import Servo
from Classes.HCSR04 import HC_SR04

def main():
    try:
        stepper = DRV8825(21, 20)
        GPIO.setup(16, GPIO.OUT)
        GPIO.output(16, False)

        servo = Servo(22,50)

        hx = HX711(23, 24)
        hx.set_reading_format("LSB", "MSB")
        hx.set_reference_unit(327)
        hx.reset()
        hx.tare()

        afstandsmeter = HC_SR04(26, 19)

        while(1):
            stappen = 0
            teller= 0
            answer = int(input("Wat wilt u testen? \n - Stappenmoter <1>\n - Servo <2>\n - Gewichtssensor <3>\n - Afstandsmeter <4>"))
            if(answer==1):
                GPIO.output(16, True)
                while(stappen < 500):
                    stepper.on()
                    stappen += 1
                GPIO.output(16,False)
            elif(answer==2):
                servo.init()
                servo.servoOpen()
                time.sleep(2)
                servo.servoClose()
                time.sleep(2)
                servo.stopServo()
            elif(answer==3):
                while(teller < 10):
                    val = hx.get_weight(5)
                    print("gewicht: {0:.2f} g".format(val))
                    hx.power_down()
                    hx.power_up()
                    time.sleep(0.5)
                    teller += 1
            elif(answer==4):
                while (teller < 10):
                    print("De afstand is {0:.2f} cm".format(afstandsmeter.distance()))
                    time.sleep(0.5)
                    teller+=1
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.setwarnings(False)  # get rid of warning when no GPIO pins set up
        GPIO.cleanup()


if __name__ == '__main__':
    main()