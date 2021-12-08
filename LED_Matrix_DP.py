
import os
import time, sys, os, re
from neopixel import * # See https://learn.adafruit.com/neopixels-on-raspberry-pi/software
from PIL import Image  # Use apt-get install python-imaging to install this
from rpi_ws281x import *
import re


def natural_key(string_):
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]

# LED strip configuration:
LED_COUNT      = 496      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 10   # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

# Speed of movement, in seconds (recommend 0.1-0.3)
SPEED=0.075

# Size of your matrix
MATRIX_WIDTH=31
MATRIX_HEIGHT=16

GRAVITY = 0.3


images= []

# This is the path where all the files are stored.
folder_path = '/home/pi/Downloads/ledmatrix/images2/'
# Open one of the files,
for data_file in sorted(os.listdir(folder_path)):
    images.append(data_file)
    i = sorted(images, key=natural_key)

for data_file in sorted(os.listdir(folder_path2)):
    images2.append(data_file)
    i2 = sorted(images2, key=natural_key)

myMatrix=[495,494,493,492,491,490,489,488,487,486,485,484,483,482,481,480,479,478,477,476,475,474,473,472,471,470,469,468,467,466,465,
          434,435,436,437,438,439,440,441,442,443,444,445,446,447,448,449,450,451,452,453,454,455,456,457,458,459,460,461,462,463,464,
          433,432,431,430,429,428,427,426,425,424,423,422,421,420,419,418,417,416,415,414,413,412,411,410,409,408,407,406,405,404,403,
          372,373,374,375,376,377,378,379,380,381,382,383,384,385,386,387,388,389,390,391,392,393,394,395,396,397,398,399,400,401,402,
          371,370,369,368,367,366,365,364,363,362,361,360,359,358,357,356,355,354,353,352,351,350,349,348,347,346,345,344,343,342,341,
          310,311,312,313,314,315,316,317,318,319,320,321,322,323,324,325,326,327,328,329,330,331,332,333,334,335,336,337,338,339,340,
          309,308,307,306,305,304,303,302,301,300,299,298,297,296,295,294,293,292,291,290,289,288,287,286,285,284,283,282,281,280,279,
          248,249,250,251,252,253,254,255,256,257,258,259,260,261,262,263,264,265,266,267,268,269,270,271,272,273,274,275,276,277,278,
          247,246,245,244,243,242,241,240,239,238,237,236,235,234,233,232,231,230,229,228,227,226,225,224,223,222,221,220,219,218,217,
          186,187,188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,
          185,184,183,182,181,180,179,178,177,176,175,174,173,172,171,170,169,168,167,166,165,164,163,162,161,160,159,158,157,156,155,
          124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,
          123,122,121,120,119,118,117,116,115,114,113,112,111,110,109,108,107,106,105,104,103,102,101,100, 99, 98, 97, 96, 95, 94, 93,
           62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92,
           61, 60, 59, 58, 57, 56, 55, 54, 53, 52, 51, 50, 49, 48, 47, 46, 45, 44, 43, 42, 41, 40, 39, 38, 37, 36, 35, 34, 33, 32, 31,
            0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]

#myMatrix.reverse()
#print (myMatrix)

# Feel free to write a fancy set of loops to populate myMatrix
# if you have a really big display! I used two cheap strings of
# 50 LEDs, so I just have a 12x8 grid = 96 LEDs
# I got mine from: http://www.amazon.co.uk/gp/product/B00MXW054Y
# I also used an 74AHCT125 level shifter & 10 amp 5V PSU
# Good build tutorial here:
# https://learn.adafruit.com/neopixels-on-raspberry-pi?view=all

# Check that we have sensible width & height
if MATRIX_WIDTH * MATRIX_HEIGHT != len(myMatrix):
  raise Exception("Matrix width x height does not equal length of myMatrix")

def allonecolour(strip,colour):
  # Paint the entire matrix one colour
  for i in range(strip.numPixels()):
    strip.setPixelColor(i,colour)
  strip.show()

def colour(r,g,b):
  # Fix for Neopixel RGB->GRB, also British spelling
  return Color(g,r,b)

def colourTuple(rgbTuple):
  return Color(rgbTuple[1],rgbTuple[0],rgbTuple[2])

def initLeds(strip):
  # Intialize the library (must be called once before other functions).
  strip.begin()
  # Wake up the LEDs by briefly setting them all to white
  allonecolour(strip,colour(0,0,0))
  time.sleep(0.01)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def scroll():
    global SPEED
    file = '64_hohoho5.png'
    loadIm=Image.open(file)
    txtlines=[]
    match=re.search( r'^(?P<base>.*)\.[^\.]+$', file, re.M|re.I)
    if match:
      txtfile=match.group('base')+'.txt'
      if os.path.isfile(txtfile):
        print ("Found text file %s" % (txtfile))
        f=open(txtfile,'r')
        txtlines=f.readlines()
        f.close()
    x=0
    # Initialise a pointer for the current line in the text file
    tx=0

    while x<loadIm.size[0]-MATRIX_WIDTH:

      # Set the sleep period for this frame
      # This might get changed by a textfile command
      thissleep=SPEED

      # Set the increment for this frame
      # Typically advance 1 pixel at a time but
      # the FLIP command can change this
      thisincrement=1

      rg=loadIm.crop((x,0,x+MATRIX_WIDTH,MATRIX_HEIGHT))
      dots=list(rg.getdata())
  
      for i in range(len(dots)):
        strip.setPixelColor(myMatrix[i],colourTuple(dots[i]))
      strip.show()

      # Check for instructions from the text file
      if tx<len(txtlines):
        match = re.search( r'^(?P<start>\s*\d+)(-(?P<finish>\d+))?\s+((?P<command>\S+)(\s+(?P<param>\d+(\.\d+)?))?)$', txtlines[tx], re.M|re.I)
        if match:
          print ("Found valid command line %d:\n%s" % (tx,txtlines[tx]))
          st=int(match.group('start'))
          fi=st
          print ("Current pixel %05d start %05d finish %05d" % (x,st,fi))
          if match.group('finish'):
            fi=int(match.group('finish'))
          if x>=st and tx<=fi:
            if match.group('command').lower()=='speed':
              SPEED=float(match.group('param'))
              thissleep=SPEED
              print ("Position %d : Set speed to %.3f secs per frame" % (x,thissleep))
            elif match.group('command').lower()=='flip':
              thissleep=float(match.group('param'))
              thisincrement=MATRIX_WIDTH
              print ("Position %d: Flip for %.3f secs" % (x,thissleep))
            elif match.group('command').lower()=='hold':
              thissleep=float(match.group('param'))
              print ("Position %d: Hold for %.3f secs" % (x,thissleep))
            elif match.group('command').lower()=='jump':
              print ("Position %d: Jump to position %s" % (x,match.group('param')))
              x=int(match.group('param'))
              thisincrement=0
          # Move to the next line of the text file
          # only if we have completed all pixels in range
          if x>=fi:
            tx=tx+1
        else:
          print ("Found INVALID command line %d:\n%s" % (tx,txtlines[tx]))
          tx=tx+1

      x=x+thisincrement
      time.sleep(thissleep)

def animate():
    global i
    for each in range(0,2):
        for frame in i:
            file = str(folder_path + frame)
            im=Image.open(file)
            dots=list(im.getdata())
            for n in range(len(dots)):
                strip.setPixelColor(myMatrix[n],colourTuple(dots[n]))
            strip.show()
            time.sleep(0.075)

def show_image(file):
    im=Image.open(file)
    dots=list(im.getdata())
    for n in range(len(dots)):
        strip.setPixelColor(myMatrix[n],colourTuple(dots[n]))
    strip.show()
    time.sleep(3)

def fade():
    for each in range(127,0,-1):
        for n in range(0,495):
            strip.setPixelColor(myMatrix[n],colour(each,each,each))
        strip.show()

def getpositionfromxy(x, y):
    position = (y * MATRIX_WIDTH) + x
    return position

def getxyfromposition(position):
    completerows = position // MATRIX_WIDTH
    remainder = position % MATRIX_WIDTH
    y = completerows
    x = remainder
    return (x,y)

def flipposition(unflipped):
    #First, get the row, 0 is first row
    row = getxyfromposition(unflipped)[1]
    column = getxyfromposition(unflipped)[0]
    if row % 2 == 0:
        # even row, no need to do anything
        return unflipped
    else:
        # odd row.  numbers run down from high to low in this row, so subtract the x position from the max value.
        maxValueInRow = MATRIX_WIDTH * (row + 1)
        return maxValueInRow - column
            
def updateball(ballInput):
    # First check for side edge bounce, reverse the x velocity if we're at the edge
    if (ballInput['xpos'] <= 0) or (ballInput['xpos'] >= MATRIX_WIDTH):
        ballInput['xvelocity'] = 0 - ballInput['xvelocity']

    # Check for floor bounce
    if (ballInput['ypos'] <= 0) or (ballInput['ypos'] >= MATRIX_WIDTH):
        ballInput['yvelocity'] = 0 - ballInput['yvelocity']

    # Could also check for ceiling bounce here, or just ignore it and let the ball fly off the top
    # of the display, it should come back down eventually :-)

    # Apply the effects of gravity
    # Note we subtract from the ball's y-velocity since gravity is pulling down, not up
    ballInput['yvelocity'] -= GRAVITY

    # Now move the ball to it's new position
    ballInput['xpos'] += ballInput['xvelocity']
    ballInput['ypos'] += ballInput['yvelocity']

    return ballInput

def drawBall(position):
    #print (position)
    #print (type(position))
    pos = int(position)
    strip.setPixelColor(pos,colour(0,255,0))
    strip.show()
    time.sleep(0.05)
    strip.setPixelColor(pos,colour(0,0,0))
    strip.show()
    # do something here
    return True


### END OF FUNCTIONS

### Initialise LEDs

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
initLeds(strip)

# Ball object...
ball = {
    'xpos': 15.0,
    'ypos': 16.0,
    'xvelocity': 0.0,
    'yvelocity': 0.0
}

#Main logic loop - draw ball, wait a while, update balls position, repeat...
##while True:
##    #Draw ball here - round the x and y positions since they are decimal/floats
##    LEDposition = getpositionfromxy(round(ball['xpos']),round(ball['ypos']))
##    drawBall(LEDposition)
##    ball = updateball(ball)




scroll()
animate()
rainbow(strip)
theaterChase(strip, Color(127,   127,   127))  # White theater chase
theaterChase(strip, Color(127,   0,   0))  # Red theater chase
theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
show_image('nz_flag_8b.png')
fade()
allonecolour(strip,colour(0,0,0))
##print ('Done')




