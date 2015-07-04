__author__ = 'sunbeansoft'

print "Python is really a great language,", "isn't it?"

str = raw_input("Enter your input: ")
print "Received input is : ", str

str = input("Enter your input: ");
print "Received input is : ", str

fo = open("read.txt", "wb")
print "Name of the file: ", fo.name
print "Closed or not : ", fo.closed
print "Opening mode : ", fo.mode
print "Softspace flag : ", fo.softspace
fo.close();