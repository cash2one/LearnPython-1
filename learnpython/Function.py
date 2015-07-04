# coding=utf-8
# !/usr/bin/python

# 可写函数说明
def printme(str):
    "打印任何传入的字符串"
    print str;
    return;

# 调用printme函数
printme(123);

# 可写函数说明
def printme(str):
    "打印任何传入的字符串"
    print str;
    return;

# 调用printme函数
printme(str="My string");

# 可写函数说明
def printinfo(name, age):
    "打印任何传入的字符串"
    print "Name: ", name;
    print "Age ", age;
    return;

# 调用printinfo函数
printinfo(age=50, name="miki");

# 可写函数说明
def printinfo1(name, age=35):
    "打印任何传入的字符串"
    print "Name: ", name;
    print "Age ", age;
    return;

# 调用printinfo函数
printinfo1(age=50, name="miki");
printinfo1(name="miki");

# 可写函数说明
def printinfo2(arg1, *vartuple):
    "打印任何传入的参数"
    print "输出: "
    print arg1
    for var in vartuple:
        print var
    return;

# 调用printinfo 函数
printinfo2(10);
printinfo2(70, 60, 50);


# 调用sum函数
print "Value of total : ", sum(10, 20)
print "Value of total : ", sum(20, 20)

# 可写函数说明
def sum(arg1, arg2):
    # 返回2个参数的和."
    total = arg1 + arg2
    print "Inside the function : ", total
    return total;

# 调用sum函数
total = sum(10, 20);
print "Outside the function : ", total
