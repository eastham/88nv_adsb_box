#!/usr/bin/python3
import json
import time
import os
import threading
import RPi.GPIO as GPIO
#import Adafruit_GPIO.SPI as SPI
#import Adafruit_SSD1306
import adafruit_ssd1306
from PIL import ImageFont, Image, ImageDraw
from netifaces import interfaces, ifaddresses, AF_INET

LEDPIN = 4
BUTTONPIN = 27

STATS1090 = "/usr/share/graphs1090/data-symlink/data/status.json"
STATS978 = "/usr/share/graphs1090/978-symlink/data/status.json"
DETAILSTATS = "/usr/share/graphs1090/data-symlink/data/stats.json"
WLANFILE = "/home/pi/wpa_supp.default"
WLANTARGET = "/etc/wpa_supplicant/wpa_supplicant.conf"

disp = draw = image = font = False
booted = False
pauseloop = False
resetlock = threading.Lock()
displaylock = threading.Lock()

def getstats(fn):
    try:
        fd = open(fn)
        json_result = json.load(fd)
        return json_result['aircraft_with_pos']
    except:
        return "xxx"

def getrssi():
    try:
        fd = open(DETAILSTATS)
        json_result = json.load(fd)
        peak = json_result['last1min']['local']['peak_signal']
    except:
        peak = "None"
    return peak

def getwlanip():
    return [i['addr'] for i in ifaddresses("wlan0").setdefault(AF_INET, [{'addr':'No IP addr'}] )][0]

def buttonwait(sec):
    global pauseloop
    pauseloop = True
    for i in range(sec*4):
        GPIO.output(LEDPIN, GPIO.HIGH)
        time.sleep(.12)
        GPIO.output(LEDPIN, GPIO.LOW)
        time.sleep(.12)
        if GPIO.input(BUTTONPIN):
            clearscreen()
            GPIO.output(LEDPIN, GPIO.LOW)
            pauseloop = False
            return False

    GPIO.output(LEDPIN, GPIO.LOW)
    clearscreen()
    return True

def button_callback(channel):
    if booted: halt_callback(channel)
    else: reset_callback(channel)
    
def halt_callback(channel):
    displaylock.acquire()
    clearscreen()
    writeline(0, "Hold to halt system")
    showtext()
    if not buttonwait(5):
        displaylock.release()
        return
    resetlock.acquire()

    clearscreen()
    writeline(0, "Halting system.")
    showtext()
    time.sleep(1)
    os.system("/usr/bin/sync")
    time.sleep(2)
    os.system("sudo /usr/sbin/halt")

    resetlock.acquire()
    
def reset_callback(channel):
    displaylock.acquire()
    clearscreen()
    writeline(0, "Hold to reset wifi")
    showtext()
    if not buttonwait(3):
        displaylock.release()
        return
    resetlock.acquire()

    clearscreen()
    writeline(0, "Resetting wifi")
    showtext()

    # copy in default supplicant
    os.system(f"sudo cp {WLANFILE} {WLANTARGET}")  # XXX MODIFY THIS FILE
    time.sleep(1)
    
    # reboot
    clearscreen()
    writeline(0, "Rebooting.")
    showtext()
    time.sleep(1)
    os.system("sudo /usr/sbin/reboot")

def pinsetup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LEDPIN, GPIO.OUT)
    GPIO.setup(BUTTONPIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.output(LEDPIN, GPIO.HIGH)


def screensetup():
    global draw, disp, image, font

    time.sleep(1)
    print("starting screen setup")
    #disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
    from board import SCL, SDA
    import adafruit_ssd1306
    import busio
    i2c = busio.I2C(SCL, SDA)
    disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
    #disp.begin()

    time.sleep(1)
    # Clear display.
    disp.fill(0)
    disp.show()

    font = ImageFont.load_default(size=11)
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)
    clearscreen()

def clearscreen():
    if draw: draw.rectangle((0,0,128,64), outline=0, fill=0)

def writeline(linenum, text):
    if draw:
        draw.text((4, -2+(linenum*9)), text, font=font, fill=255)
#    print(text)
    
def showtext():
    if disp:
        disp.image(image)
        disp.show()

def gettemp():
    fn = "/sys/class/thermal/thermal_zone0/temp"
    with open(fn) as f:
        firstline = f.readline().rstrip()
    return int(firstline)/1000


### START

pinsetup()
#GPIO.add_event_detect(BUTTONPIN, GPIO.FALLING, callback=button_callback, bouncetime=150)
#try:
screensetup()
#except:
#    print("caught screen setup exception")
    
clearscreen()
writeline(0, "Booting...")
#writeline(2, "Hold button to reset")
#writeline(3, "      wifi")
showtext()

for x in range(10):
    GPIO.output(LEDPIN, GPIO.HIGH)
    time.sleep(.5)
    GPIO.output(LEDPIN, GPIO.LOW)
    time.sleep(.5)
    
booted = True
spinarr="|/-\\|/-\\"
spinoff=0
temp = gettemp()

while True:
    displaylock.acquire()
    clearscreen()

    str = f"IP: {getwlanip()}"
    writeline(0, str)

    str = f"1090 aircraft: {getstats(STATS1090)}"
    #print(str)
    writeline(2, str)
     
    str = f"978 aircraft: {getstats(STATS978)}"
    #print(str)
    writeline(3, str)

    str = f"Peak RSSI: {getrssi()}"
    writeline(4, str)
  

    if spinoff == len(spinarr):
        spinoff = 0
        temp = gettemp()
    str = f"Temp: {temp:.1f}    {spinarr[spinoff]}"
    spinoff += 1
    writeline(6, str)
    showtext()
    displaylock.release()
    time.sleep(1)

    while pauseloop:
          time.sleep(.25)

