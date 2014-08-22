mystring = "Let's do this"
print dir(mystring)

print mystring.swapcase()

a= 1
b =2
c = a+b
print type(a), type(b), type(c)

a = 1
b = 2.0
c = a + b
print type(a), type(b), type(c)

a = 1
b = 2
c = a / b
print c, type(c)

a = 1.0
b = 2.0
c = a / b
print c, type(c)


a = 1
b = 2
c = float(a) / b
print c, type(c)


voltages = [-2.0, -1.0, 0.0, 1.0, 2.0]
print type(voltages)

print voltages[0]
print voltages[3]
print voltages[-1]
print voltages[1:3]
print len(voltages)
print voltages[1:4]
print voltages[2:]
print voltages[:2]
print voltages[:]
voltages.append(7.0)
print voltages


# Flow control
print 2+2 == 4
print 5 < 3.5

print 5 < 3.5 or 4==5-1
print 5 < 3.5 and 4==5-1

print 5 < 3.5 or not 'lunch' == 'breakfast'

x = 15
if x < 0:
    print "x is negative"
elif x == 0:
    print "x is zero"
elif x > 0:
    print "x is positive"
else:
    print "x is weird", x

# For loops

fruits = ['apples', 'oranges', 'bananas']
for fruit in fruits:
    print fruit

for i in range(len(fruits)):
    print i, fruits[i]

fruits = ['apples', 'oranges', 'bananas']
prices = [0.49, 0.99, 0.32]

for i in range(len(fruits)):
    print prices[i], fruits[i]

for marketprice, fruit in zip(prices, fruits):
    print marketprice, fruit

print prices, fruits
