list = [5.4, 'hello', 2]
print list[2]
print list[1:3]

nums = []
for i in range(10):
    nums.append(float(raw_input()))
s = 0
for num in nums:
    s += num
avg = s / len(nums)
avg1 = sum(nums) / len(nums)

print avg
print avg1
