# Given a .json file, creates a double line graph of total lines of Code (Test and All) at each Commit

import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

fp = open("flask.json", "r")
data = json.load(fp)
fp.close()

xData = []
yData = []
yData2 = []
y = 0
y2 = 0
for i in range(len(data["test_lines_per_commit"])):
    xData.append(i+1)
    y = y + data["test_lines_per_commit"][i]
    y2 = y2 + data["total_lines_per_commit"][i]
    yData.append(y)
    yData2.append(y2)

x = xData
y = yData
y2 = yData2

fig, ax = plt.subplots()
ax.plot(x, y, label="Total Test Lines of Code")
ax.plot(x, y2, label="Total Lines of Code")
ax.legend()

ax.set(xlabel="Commit #", ylabel="Total Lines of Code", title="Total Lines of Code At Each Commit")
ax.grid()
plt.show()
