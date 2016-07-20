import random


def print_sum(start, stop):
    result = 0
    for i in range(start, stop):
        result += i
    print 'sum is', result
    return result


def is_palin(num):
    pass


def is_prime(num):
    pass


def is_leap_year(year):
    if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
        return True
    else:
        return False


def get_num_of_days_in_month(year, month):
    if month in (1, 3, 5, 7, 8, 10, 12):
        return 31
    elif month in (4, 6, 9, 11):
        return 30
    elif is_leap_year(year):
        return 29
    else:
        return 28


def get_total_num_of_day(year, month):
    days = 0
    for y in range(1800, year):
        if is_leap_year(year):
            days += 366
        else:
            days += 365
    for m in range(1, month):
        days += get_num_of_days_in_month(year, m)
    return days


def get_start_day(year, month):
    return (3 + get_total_num_of_day(year, month)) % 7


print get_start_day(2033, 12)


def p(num):
    if num == 1 or num == 0:
        return 1
    else:
        return num * p(num - 1)


print p(3)


def fib(n):
    if n == 1 or n == 2:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


print fib(4)


def parking(low, high):
    if high - low < 1:
        return 0
    else:
        x = random.uniform(low, high - 1)
        return parking(low, x) + 1 + parking(x + 1, high)


s = 0
for i in range(10000):
    s += parking(0, 5)

print s / 10000
