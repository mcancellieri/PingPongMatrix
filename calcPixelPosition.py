# Some constants
X_DIMENSION = 32
Y_DIMENSION = 16

def getpositionfromxy(x, y):
    position = ((y-1) * X_DIMENSION) + x
    return position

def getxyfromposition(position):
    completerows = position // X_DIMENSION
    remainder = position % X_DIMENSION
    y = completerows + 1
    x = remainder
    return (x,y)

x = 14
y = 1
print('Get position from x y: ',(x,y))
print(getpositionfromxy(x,y))

print('\n')

position = 240
print('Get x y from position: ',position)
print(getxyfromposition(position))