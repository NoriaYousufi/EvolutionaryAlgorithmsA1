import numpy as np

fo = open("./ga-optimization.txt", "r")
lines = list()
lines1 = list()
l = fo.readlines()[1:]
for line in l:
    if "LABS" in line:
        tmp = [x.strip() for x in line.split(",")][1:]
        lines.append([float(x) for x in tmp])
    elif "IsingRing" in line:
        tmp = [x.strip() for x in line.split(",")][1:]
        lines1.append([float(x) for x in tmp])

lines = np.array(lines)
lines1 = np.array(lines1)

print("GA")

maximum = np.argmax(lines[:,-1])
print("LABS", lines[maximum].tolist())

maximum = np.argmax(lines1[:, -1])
print("IsingRing", lines1[maximum].tolist())


fo = open("./es-optimization.txt", "r")
lines = list()
lines1 = list()
l = fo.readlines()[1:]
for line in l:
    if "LABS" in line:
        tmp = [x.strip() for x in line.split(",")][1:]
        lines.append([float(x) for x in tmp])
    elif "IsingRing" in line:
        tmp = [x.strip() for x in line.split(",")][1:]
        lines1.append([float(x) for x in tmp])

lines = np.array(lines)
lines1 = np.array(lines1)

print("ES")

maximum = np.argmax(lines[:,-1])
print("LABS", lines[maximum].tolist())

maximum = np.argmax(lines1[:, -1])
print("IsingRing", lines1[maximum].tolist())

l = [
    3.2467532467532467, 
 3.1806615776081424,
3.6231884057971016, 
 3.7993920972644375,
3.1806615776081424, 
 3.4626038781163433,
3.1806615776081424, 
3.6231884057971016, 
3.3875338753387534, 
3.9936102236421727, 
3.7993920972644375, 
 3.1806615776081424,
 5.020080321285141, 
3.6231884057971016, 
 4.325259515570934, 
3.3875338753387534, 
 4.716981132075472, 
3.117206982543641,
3.6231884057971016, 
 3.6231884057971016,
]
print(np.mean(l))