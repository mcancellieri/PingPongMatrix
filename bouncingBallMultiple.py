import time
from random import random

# Some constants
X_DIMENSION = 32
Y_DIMENSION = 16
GRAVITY = 0.3
NUMBER_OF_BALLS = 4
DELAY = 0.1

def getpositionfromxy(x, y):
    position = ((y-1) * X_DIMENSION) + x
    return position

def getxyfromposition(position):
    completerows = position // X_DIMENSION
    remainder = position % X_DIMENSION
    y = completerows + 1
    x = remainder
    return (x,y)

def updateball(ballInput):
    # Move the ball to it's new position
    ballInput['xpos'] += ballInput['xvelocity']
    ballInput['ypos'] += ballInput['yvelocity']

    # First check for side edge bounce, reverse the x velocity if we're at the edge
    if (ballInput['xpos'] <= 0) or (ballInput['xpos'] >= X_DIMENSION):
        ballInput['xvelocity'] = 0 - ballInput['xvelocity']

    # Check for floor bounce
    if (ballInput['ypos'] <= 0) or (ballInput['ypos'] >= X_DIMENSION):
        ballInput['yvelocity'] = 0 - ballInput['yvelocity']
        # if ball has gone under the ground, bring it back up
        if ballInput['ypos'] < 0:
            ballInput['ypos'] = 0 - ballInput['ypos']

    # Could also check for ceiling bounce here, or just ignore it and let the ball fly off the top
    # of the display, it should come back down eventually :-)

    # Apply the effects of gravity
    # Note we subtract from the ball's y-velocity since gravity is pulling down, not up
    ballInput['yvelocity'] -= GRAVITY

    return ballInput

def initialiseBall():
    ball = {
        'xpos': random() * X_DIMENSION,
        'ypos': (random() * Y_DIMENSION / 2) + (random() * Y_DIMENSION / 2),
        'xvelocity': random() * 2,
        'yvelocity': 0.0
    }
    return ball

def drawBall(position):
    # do something here
    return True

### END OF FUNCTIONS

# Array of ball objects
ballArray = []
for i in range(NUMBER_OF_BALLS):
    ballArray.append(initialiseBall())

# Main logic loop - Clear didplay, then repeat this for each ball...
# - draw ball, wait a while, update balls position, repeat... -
# Then finish up with a delay before repeating whole process again
while True:
    #Clear the LED display here, not inside the following loop...

    for i, ball in enumerate(ballArray):
        # Draw ball here - round the x and y positions since they are decimal/floats
        LEDposition = getpositionfromxy(round(ballArray[i]['xpos']), round(ballArray[i]['ypos']))
        drawBall(LEDposition)
        # Following line for debugging, can be removed...
        print(i, ball)
        ballArray[i] = updateball(ballArray[i])
    time.sleep(DELAY)




