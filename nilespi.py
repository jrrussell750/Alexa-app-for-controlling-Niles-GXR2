import logging
import os
import socket
import re
 
from flask import Flask
from flask_ask import Ask, request, session, question, statement
 
app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

@ask.launch
def launch():
    speech_text = 'Niles pi speaking. What do you want?'
    return question(speech_text).reprompt(speech_text).simple_card(speech_text)
 
@ask.intent('setintent', mapping = {'set':'set'})
def set(zone, input):
    global zonenum
    zonenum = b"\x24"
    if(zone=="1" or zone=="living room"):
        zonenum = b"\x21"
    elif(zone=="2" or zone=="kitchen"):
        zonenum = b"\x22"
    elif(zone=="3"):
        zonenum = b"\x23"
    elif(zone=="4" or zone=="patio"):
        zonenum = b"\x24"
    elif(zone=="5" or zone=="master bath"):
        zonenum = b"\x25"
    elif(zone=="6" or zone=="basement"):
        zonenum = b"\x26"

    global inputnum
    inputnum = b"\x04"    
    if(input=="1" or input=="a.m. FM"):
        inputnum = b"\x01"
    elif(input=="2" or input=="1 pen's music" or input=="music" ):
        inputnum = b"\x02"
    elif(input=="3" or input=="TV"):
        inputnum = b"\x03"
    elif(input=="4" or input=="echo"):
        inputnum = b"\x04"
    elif(input=="5" or input=="glen"):
        inputnum = b"\x05"
    elif(input=="6" or input=="John"):
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
def set(previousnext, input):
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

@ask.intent('volumeintent', mapping = {'volume':'volume'})
def set(updn, zone):
    global zonenum
    zonenum = b"\x24"
    if(zone=="1" or zone=="living room"):
        zonenum = b"\x21"
    elif(zone=="2" or zone=="kitchen"):
        zonenum = b"\x22"
    elif(zone=="3"):
        zonenum = b"\x23"
    elif(zone=="4" or zone=="patio"):
        zonenum = b"\x24"
    elif(zone=="5" or zone=="master bath"):
        zonenum = b"\x25"
    elif(zone=="6" or zone=="basement"):
        zonenum = b"\x26"

    global volupdn
    volupdn = b"\x0c"    
    if(updn=="up" or updn=="higher"):
        volupdn = b"\x0c"
    elif(updn=="down" or updn=="lower"):
        volupdn = b"\x0d"
    
    MESSAGE = b"\x00\x0e\x00" + zonenum + b"\x00\x0b\x61\x06" + volupdn + b"\x00\xff"
    UDP_IP = "10.100.0.1"
    UDP_PORT = 6001
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for x in range(6):
        sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    sock.close()

    return statement(input + ' selected for ' + zone)

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
