import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import threading
import LCD1602

GPIO.setmode(GPIO.BCM)
myDHT = Adafruit_DHT.DHT11
dht11 = 21
motionPin = 23
greenLED =  5
redLED = 26
blueLED = 16
acUP = 13
acDOWN = 27
security = 25

doorState = "SAFE"
lightState = "OFF"

acON = 0
hvacType = "OFF"
index = 80
hvacTemp = 75
hvacTimeS = 0
hvacTimeE = 0
temp2 = 79
temp3 = 79
#Change to port of LCD
LCD1602.init(0x3f, 1)

#GPIO Setup for all Pi components
GPIO.setup(motionPin, GPIO.IN)
GPIO.setup(acUP, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(acDOWN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(security, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(greenLED, GPIO.OUT)
GPIO.setup(redLED, GPIO.OUT)
GPIO.setup(blueLED, GPIO.OUT)

#Check state of PIR Sensor, if 1 then turn Green LED on and update LCD,
#if 0 then turn off LED and update LCD accordingly
def motion():
    global lightState
    motion = GPIO.input(motionPin)
    print(motion)
    if (motion == 1):
        GPIO.output(greenLED, True)
        if (lightState != "ON"):
            lightState = "ON"
            LCDMain()
    else:
        GPIO.output(greenLED, False)
        if(lightState != "OFF"):
            lightState = "OFF"
            LCDMain()

#Check room temp index
def roomTemp():
    global index, doorState, acON, lightState, temp2, temp3
    hum, celsius = Adafruit_DHT.read(myDHT, dht11)
    time.sleep(1)

    #Convert measured temp to farenheit and calculate index with Irvine CIMIS humidity
    temp = round((celsius * (9/5)) + 32)
    index = round(((temp + temp2 + temp3) / 3) + (0.05 * 93))

    #Check index to be above 95 for fire alarm system
    if (index > 95):

        #Open doors and turn off HVAC, alert that doors are open
        doorState = "OPEN"
        acON = 0
        lightState = "OFF"
        GPIO.output(redLED, False)
        GPIO.output(blueLED, False)
        GPIO.output(greenLED, False)
        LCD1602.clear()
        LCD1602.write(0,0,"DOOR/WINDOW OPEN")
        time.sleep(1)

        #While the index is above 95, continue to show alerts, check index after each loop
        while(index > 95):
            LCD1602.clear()
            LCD1602.write(0,0,"EMERGENCY: FIRE!")
            LCD1602.write(0,1,"PLEASE EVACUATE!")
            GPIO.output(redLED, True)
            GPIO.output(blueLED, True)
            GPIO.output(greenLED, True)
            time.sleep(1)
            GPIO.output(redLED, False)
            GPIO.output(blueLED, False)
            GPIO.output(greenLED, False)
            index = round(temp + (0.05 * 93))
            print(index)

        #Once loop has ended check the hvac to see if system needs to turn on
        hvacCheck()
    temp3 = temp2
    temp2 = temp
    print(index)

#Increment desired temp and check to see if HVAC system should turn on
#update LCD with desired temp showing on LCD
def tempUp(self):
    global hvacTemp
    global index
    global acON
    global hvacType
    if (hvacTemp + 1 < 96):
        hvacTemp = hvacTemp + 1
        LCDMain()
        time.sleep(0.5)
        hvacCheck()
    print(hvacTemp)

#Decrement desired temp and check to see if HVAC system should turn on
#update LCD with desired temp showing on LCD
def tempDown(self):
    global index
    global hvacTemp
    global acON
    global hvacType
    if (hvacTemp - 1 > 64):
        hvacTemp = hvacTemp - 1
        LCDMain()
        time.sleep(0.5)
        hvacCheck()
    print(hvacTemp)

#Compare desired temp with current index
def hvacCheck():
    global index
    global hvacTemp
    global acON
    global hvacType, hvacTimeS, hvacTimeE

    #If the index is too much lower than desired temp, turn on heater and show it by
    #turning on RED LED and updating LCD to show HEATER ON then go back to updated default screen
    if(hvacTemp >= index + 3):
        GPIO.output(blueLED, False)
        GPIO.output(redLED, True)
        hvacType = "HEAT"
        if (acON != 1):
            hvacTimeS = time.time()
            LCD1602.clear()
            LCD1602.write(0,0,"   HVAC HEAT")
            time.sleep(3)
            LCDMain()
        acON = 1

    #If the index is too much higher than desired temp, turn on heater and show it by
    #turning on BLUE LED and updating LCD to show AC ON then go back to updated default screen
    elif(hvacTemp <= index - 3):
        GPIO.output(blueLED, True)
        GPIO.output(redLED, False)
        hvacType = "COOL"
        if (acON != 1):
            hvacTimeS = time.time()
            LCD1602.clear()
            LCD1602.write(0,0,"    HVAC AC")
            time.sleep(3)
            LCDMain()
        acON = 1

    #If index isnt too much higher or lower than desired temp, turn off HVAC system and calculate
    #the costs of HVAC for that period if it was on.
    else:
        GPIO.output(redLED, False)
        GPIO.output(blueLED, False)
        hvacTimeE = time.time()
        totalTime = round((hvacTimeE - hvacTimeS), 2)
        if(acON != 0):
            if(hvacType == "HEAT"):
                kWh = round((36 * (totalTime / 60)), 2)
            elif(hvacType == "COOL"):
                kWh = round((18 * (totalTime / 60)), 2)
            cost = kWh * .5
            hvacType = "OFF"
            LCD1602.clear()
            LCD1602.write(0,0,"    HVAC OFF")
            time.sleep(3)
            LCD1602.clear()
            LCD1602.write(0,0,"Energy: {}KWh".format(kWh))
            LCD1602.write(0,1,"Cost: ${}".format(cost))
            time.sleep(3)
            LCDMain()
        acON = 0

#Check for state of DOORS/WINDOWS
def doors(pin):
    global doorState
    global acON, hvacType
    print("PRESS")
    #If they were closed, open them and turn off HVAC, alert user and return to default screen
    if(doorState != "OPEN"):
        doorState = "OPEN"
        acON = 0
        hvacType = "OFF"
        GPIO.output(redLED, False)
        GPIO.output(blueLED, False)
        LCD1602.clear()
        LCD1602.write(0,0,"DOOR/WINDOW OPEN")
        LCD1602.write(0,1, "  HVAC HALTED")
        time.sleep(3)
        LCDMain()
        time.sleep(0.5)

    #If they were open, close them and check HVAC to see if it should be turned on. Update that
    #Doors closed and HVAC back up, then return to default screen
    elif(doorState != "SAFE"):
        doorState = "SAFE"
        hvacCheck()
        LCD1602.clear()
        LCD1602.write(0,0, "  DOORS CLOSED")
        LCD1602.write(0,1, "  HVAC BACK UP")
        time.sleep(3)
        LCDMain()
        time.sleep(0.5)

#Update Default screen with correct information
def LCDMain():
    global index
    global hvacTemp
    global doorState
    global hvacType, lightState
    time.sleep(1)
    LCD1602.clear()
    LCD1602.write(0,0, "{}/{}     D:{}".format(hvacTemp, index, doorState))
    LCD1602.write(0,1, "H:{}     L:{}".format(hvacType, lightState))

GPIO.add_event_detect(acUP, GPIO.RISING, callback = tempUp, bouncetime=2500)
GPIO.add_event_detect(acDOWN, GPIO.RISING, callback = tempDown, bouncetime=2500)
GPIO.add_event_detect(security, GPIO.RISING, callback = doors, bouncetime=5000)

try:
    LCDMain()
    GPIO.output(redLED, False)
    GPIO.output(blueLED, False)
    while True:
        if __name__ == "__main__":
            tempThread = threading.Thread(target = roomTemp, args = ())
            motionThread = threading.Thread(target = motion, args = ())
            tempThread.start()
            motionThread.start()
            tempThread.join()
            motionThread.join()
finally:
    GPIO.cleanup()
    time.sleep(1)
    LCD1602.clear()