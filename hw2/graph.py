import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

test_data = open("time.txt", "r")
lines = test_data.readlines()
time = []
n = []
for line in lines:
    line = line.strip('\n ] [ ').split(' ')
    time.append(int(line[1]))
    n.append(int(line[0]))
test_data.close()
time.sort()
n.sort()
x = n[:-1]
y = time[:-1]
plt.plot(x, y, label="the relationship between N and the execution time")
plt.legend()
plt.xlabel("N")
plt.ylabel("time")
plt.savefig('time.png')
