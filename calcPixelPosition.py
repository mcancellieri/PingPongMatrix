# Some constants
X_DIMENSION = 32
Y_DIMENSION = 16

def getpositionfromxy(x, y):
    position = (y * X_DIMENSION) + x
    return position

def getxyfromposition(position):
    completerows = position // X_DIMENSION
    remainder = position % X_DIMENSION
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
        maxValueInRow = X_DIMENSION * (row + 1)
        return maxValueInRow - column

# Some tests
x = 33
y = 0
print('Get position from x y: ',(x,y))
print(getpositionfromxy(x,y))

print('\n')

print('Get flipped position from x y: ',(x,y))
print(flipposition(getpositionfromxy(x,y)))

print('\n')

position = 240
print('Get x y from position: ',position)
print(getxyfromposition(position))