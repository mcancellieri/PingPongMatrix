import time

# Some constants
X_DIMENSION = 32
Y_DIMENSION = 16
GRAVITY = 0.3


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



    # If ball has gone out of bounds as a result of the position adjustment, bring it back

    return ballInput

def drawBall(position):
    # do something here
    return True


### END OF FUNCTIONS

# Ball object...
ball = {
    'xpos': 10.0,
    'ypos': 10.0,
    'xvelocity': 1.0,
    'yvelocity': 0.0
}

#Main logic loop - draw ball, wait a while, update balls position, repeat...
while True:
    #Draw ball here - round the x and y positions since they are decimal/floats
    LEDposition = getpositionfromxy(round(ball['xpos']),round(ball['ypos']))
    drawBall(LEDposition)
    # Following line for debugging, can be removed...
    print(ball)
    time.sleep(0.1)
    ball = updateball(ball)


