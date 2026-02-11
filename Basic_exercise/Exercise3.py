temperatures = [15.5, 17.2, 14.8, 16.0, 18.3, 20.1, 19.5]
print("Wednesday: ", temperatures[1])
print("Max: ", max(temperatures))
print("Min: ", min(temperatures))
print("Average: ", round(sum(temperatures)/len(temperatures), 1))
count = 0
for i in temperatures:
    if i > 17:
        count += 1

print("Days above 17: ", count)
print("Sorted", sorted(temperatures))