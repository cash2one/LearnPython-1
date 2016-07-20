s = 'hello world'
print s

name = s + ' china'
print name

d = name * 3
print d

index = len(d)
print index


def vowles_count(s):
    count = 0
    for c in s:
        if c in 'aeiouAEIOU':
            count += 1
    return count


print vowles_count(d)

print s[2]
print s[1:2]
print s[-2:-1]
print s[::-1]

my_str = 'hello world'
my_str.replace('e', 'a')
print my_str

f = open('/Users/baidu/id.txt', 'r')
for line in f:
    line = line.strip()
    print line.title()
f.close()
