#! /usr/bin/<a href="http://lib.csdn.net/base/11" class='replace_word' title="undefined" target='_blank' style='color:#df3434; font-weight:bold;'>Python</a>
# Filename: inherit.py
# Author: yanggang

class SchoolMember:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        print 'init SchoolMember: ', self.name

    def tell(self):
        print 'name:%s; age:%s' % (self.name, self.age)


class Teacher(SchoolMember):
    def __init__(self, name, age, salary):
        SchoolMember.__init__(self, name, age)
        self.salary = salary
        print 'init Teacher: ', self.name

    def tell(self):
        SchoolMember.tell(self)
        print 'salary: ', self.salary


class Student(SchoolMember):
    def __init__(self, name, age, marks):
        SchoolMember.__init__(self, name, age)
        self.marks = marks
        print 'init Student: ', self.name

    def tell(self):
        SchoolMember.tell(self)
        print 'marks: ', self.marks


def main():
    t = Teacher('yanggang', 20, 1000)
    s = Student('liming', 12, 86)
    members = [t, s]

    print

    for member in members:
        member.tell()


if __name__ == "__main__":
    main()
