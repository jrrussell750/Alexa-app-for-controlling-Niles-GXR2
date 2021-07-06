import logging
import os
import socket
import re
import time
from array import *
 
from flask import Flask
from flask_ask import Ask, request, session, question, statement
 
app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

@ask.launch
def launch():
    MESSAGE = b"\x00\x0e\x00\x21\x00\x0b\x61\x06\x04\x00\xff"
    UDP_IP = "10.100.0.1"
    UDP_PORT = 6001
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    sock.close()
    speech_text = 'Niles pi speaking. What do you want?'
    return question(speech_text).reprompt(speech_text).simple_card(speech_text)
 
@ask.intent('setzoneintent', mapping = {'setzone':'setzone'})
def setzoneintent(zone, input):
    global zonenum
    zonenum = b"\x24"
    if(zone=="zone 1" or zone=="living room"):
        zonenum = b"\x21"
    elif(zone=="zone 2" or zone=="kitchen"):
        zonenum = b"\x22"
    elif(zone=="zone 3"):
        zonenum = b"\x23"
    elif(zone=="zone 4" or zone=="patio"):
        zonenum = b"\x24"
    elif(zone=="zone 5" or zone=="master bath"):
        zonenum = b"\x25"
    elif(zone=="zone 6" or zone=="basement"):
        zonenum = b"\x26"

    global inputnum 
    inputnum = b"\x04"    
    if(input=="input 1" or input=="a.m. FM"):
        inputnum = b"\x01"
    elif(input=="input 2" or input=="1 pen's music" or input=="music" ):
        inputnum = b"\x02"
    elif(input=="input 3" or input=="TV"):
        inputnum = b"\x03"
    elif(input=="input 4" or input=="echo"):
        inputnum = b"\x04"
    elif(input=="input 5" or input=="glen"):
        inputnum = b"\x05"
    elif(input=="input 6" or input=="John"):
        inputnum = b"\x06"
    elif(input=="off"):
        inputnum = b"\x0a"
        
    MESSAGE = b"\x00\x0e\x00" + zonenum + b"\x00\x0b\x61\x06" + inputnum + b"\x00\xff"
    UDP_IP = "10.100.0.1"
    UDP_PORT = 6001
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    sock.close()

    return statement(input + ' selected for ' + zone)

@ask.intent('gotointent', mapping = {'goto':'goto'})
def prevnext(previousnext, input):
    global navnum
    navnum = b"\x2b"
    if(previousnext=="next" or previousnext=="next song"):
        navnum = b"\x2c"
    elif(previousnext=="previous" or previousnext=="previous song"):
        navnum = b"\x2b"

    global inputnum
    inputnum = b"\x82"    
    if(input=="1" or input=="a.m. FM"):
        inputnum = b"\x81"
    elif(input=="2" or input=="1 pen's music" or input=="music" ):
        inputnum = b"\x82"
    elif(input=="3" or input=="TV"):
        inputnum = b"\x83"
    elif(input=="4" or input=="echo"):
        inputnum = b"\x84"
    elif(input=="5" or input=="glen"):
        inputnum = b"\x85"
    elif(input=="6" or input=="John"):
        inputnum = b"\x86"
        
    MESSAGE = b"\x00\x0e\x00" + inputnum + b"\x00\x0b\x61\x06" + navnum + b"\x00\xff"
    UDP_IP = "10.100.0.1"
    UDP_PORT = 6001
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    sock.close()

    return statement(previousnext + ' song has been selected for ' + input)

@ask.intent('setvolumeintent', mapping = {'setvolume':'setvolume'})
def setvolume(vollevel, zone):
    global zonenum
    zonenum = b"\x24"
    statusfile = open("GXR2status.txt", "r")
    statusarray = ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]  
    for i in range (0,12):
        statusarray[i] = statusfile.readline()
        print(statusarray[i])
    statusfile.close() 
    
    if(zone=="zone 1" or zone=="living room"):
        zonenum = b"\x21"
        i = 6
    elif(zone=="zone 2" or zone=="kitchen"):
        zonenum = b"\x22"
        i = 7
    elif(zone=="zone 3"):
        zonenum = b"\x23"
        i = 8
    elif(zone=="zone 4" or zone=="patio"):
        zonenum = b"\x24"
        i = 9
    elif(zone=="zone 5" or zone=="master bath"):
        zonenum = b"\x25"
        i = 10
    elif(zone=="zone 6" or zone=="basement"):
        zonenum = b"\x26"
        i = 11
    currentlevel = statusarray[i]
    UDP_IP = "10.100.0.1"
    UDP_PORT = 6001
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if (int(currentlevel) > (int(vollevel) * 10)):
        delta = int(currentlevel) - (int(vollevel) * 10)
        MESSAGE = b"\x00\x0e\x00" + zonenum + b"\x00\x0b\x61\x06\x0d\x00\xff"
        for x in range(0, delta):
            sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
            time.sleep(.01)
    else:
        delta = (int(vollevel) * 10) - int(currentlevel)
        MESSAGE = b"\x00\x0e\x00" + zonenum + b"\x00\x0b\x61\x06\x0c\x00\xff"
        for x in range (0, delta):
            sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
            time.sleep(.01)
    sock.close()
    return statement('volume set to ' + vollevel + ' in ' + zone)

@ask.intent('alloffintent')
def alloff():
    MESSAGE = b"\x00\x0e\x00\x21\x00\x0b\x61\x06\x0a\x02\xff"
    UDP_IP = "10.100.0.1"
    UDP_PORT = 6001
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    sock.close()
    return statement('All zones are off')
    
@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'When prompted, say the zone or input that you want to set.  For example set living room to f.m. AM.'
    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)
 
@ask.session_ended
def session_ended():
    return "{}", 200
 
if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True)