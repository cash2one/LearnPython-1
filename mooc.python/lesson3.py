import math

score = 60

if score >= 60:
    print 'yes'
else:
    print 'no'

if score >= 90:
    print 'a'
elif score >= 80:
    print 'b'
elif score >= 70:
    print 'c'
else:
    print 'f'

i = 1
s = 0

while i < 10:
    s += 1
    i += 1
print s

e = 1
for i in range(1, 100):
    e += 1.0 / math.factorial(i)
    print e

n = 6

while n != 1:
    if n % 2 == 0:
        n /= 2
    else:
        n = 3 * n + 1
    print n
