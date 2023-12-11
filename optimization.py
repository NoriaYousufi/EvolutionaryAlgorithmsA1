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
