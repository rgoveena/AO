import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pyexcel as pe
import datetime
import sys

#INTERPRETING CSV FILE
try:
	records = pe.get_records(file_name="python-scripts/uploaded-files/"+sys.argv[1]+".csv") #records is a list containing dictionaries
	#file path is relative to where node is running (query-node)
	#script will not work if called on separately because of file path
except Exception as inst:
	print(type(inst))
	print(inst.args)
	print(inst)
#records is a list containing dictionaries

time = []
value = []

columns = len(records[0])
i = 1
while i < columns:
  value.append([])
  i += 1 

#time conversion function
def datetime_to_float(d):
    epoch = datetime.datetime.utcfromtimestamp(0)
    total_seconds =  (d - epoch).total_seconds()
    # total_seconds will be in decimals (millisecond precision)
    return total_seconds

baseTime = datetime_to_float(records[0].values()[0]) #assuming first column of csv is always datetime format


for record in records:
	time.append(datetime_to_float(record.values()[0])-baseTime)
	i = 1
	while i < columns:
		if (record.values()[i]!=''):
			value[i-1].append(record.values()[i])
		else:
			value[i-1].append(0)
		i += 1

# PLOTTING
fig, ax = plt.subplots()

i = 1
for val in value:
	ax.plot(time, val, label=records[0].keys()[i])
	i += 1

plt.title(sys.argv[1], x=0.1)
ax.set(ylabel=records[0].keys()[1], xlabel='TIME (IN SEC) AFTER '+unicode(records[0].values()[0]))
ax.legend(bbox_to_anchor=(1, 1.12))
ax.grid()

fig.savefig("public/graphs/"+sys.argv[1]+".png")

print('"'+sys.argv[1]+'"')
#plt.show() #will give as pop up screen