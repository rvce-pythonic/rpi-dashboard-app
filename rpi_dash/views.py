from __future__ import unicode_literals
from django.shortcuts import render
from django.views.generic import View, TemplateView
import Adafruit_DHT
import RPi.GPIO as GPIO
from django.http import HttpResponseRedirect
import sys
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Create your views here.



def homepage(request):  # render index.html
    humid, temp = Adafruit_DHT.read_retry(11, 4)
    return render(request, 'index.html', {"tempdata": temp, "humiddata": humid})  # send temperature and humididty data


class led(View):  # led ON and OFF
    def post(self, request):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(14, GPIO.OUT)  # PIN NO 14
        if (GPIO.input(14)):  # check if pin is in HIGH status
            print(" on - > off ")
            GPIO.output(14, False)
        else:
            print(" off -> on ")
            GPIO.output(14, True)
        return HttpResponseRedirect("/")  # redirect to index . html page


class oled(View):  # oled
    def post(self, request):
        lines = [request.POST.get('oleddata')]  # get form data from post request
        disp = Adafruit_SSD1306.SSD1306_128_64(rst=25, dc=24, sclk=11, din=10, cs=8)  # 7 pin oled
        disp.begin()
        disp.clear()
        disp.display()
        width = disp.width
        height = disp.height
        image = Image.new('1', (width, height))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        padding = -2
        top = padding
        bottom = height - padding
        x = 0
        font = ImageFont.load_default()
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        extra1 = 0
        extra2 = 0
        for i in range(0, len(lines)):
            draw.text((x + extra1, top + extra2), str(lines[i]), font=font, fill=255)  # extra1 +=15
            extra2 += 8
        disp.image(image)
        disp.display()
        return HttpResponseRedirect("/")
