#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import textwrap
import json
import random

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

def get_quote():
    filename = "/home/pi/Desktop/PiProject/e-Paper/RaspberryPi_JetsonNano/python/examples/quotes.json"
    with open(filename, encoding="utf8") as json_file:
        data = json.load(json_file)
        r = random.randint(0,len(data)-1)
        title = data[r]['from']
        message = data[r]['text']
        return title, message
    

try:
    logging.info("epd2in13_V2 Demo")
    
    epd = epd2in13_V2.EPD()
    logging.info("init and Clear")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)

    # Drawing on the image
    font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    
    time_image = Image.new('1', (epd.height, epd.width), 255)
    time_draw = ImageDraw.Draw(time_image)
    
    epd.displayPartBaseImage(epd.getbuffer(time_image))
    
    epd.init(epd.PART_UPDATE)
    num = 0
    while (True):
        title, message = get_quote()
        message = textwrap.fill(message, width=35)
        time_draw.rectangle((0, 0, 300, 135), fill = 0)
        time_draw.text((5, 100), textwrap.fill(title,width=34), font = font15, fill = 255)
        time_draw.text((5, 0), textwrap.fill(message,width=34), font = font15, fill = 255)
        epd.displayPartial(epd.getbuffer(time_image))
        num = num + 1
        logging.info("Sleep")
        time.sleep(1)
        if(num == 5):
            break
    # epd.Clear(0xFF)
    logging.info("Clear...")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)
    
    logging.info("Goto Sleep...")
    epd.sleep()
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13_V2.epdconfig.module_exit()
    exit()
