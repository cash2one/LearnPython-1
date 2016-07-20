f = open("/Users/baidu/id.txt")
try:
    for line in f:
        print line,
finally:
    f.close()
