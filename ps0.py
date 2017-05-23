import numpy

x = int(input('Enter a number x:'))
y = int(input('Enter a number y:'))

def powerOf(x, y) :
    return x**y
    
power = powerOf(x, y)
log2 = numpy.log2(power)

print(str(x) + ' to the power of ' + str(y) + ': ' + str(power))
print('log2 of ' + str(power) + ': ' + str(log2))
