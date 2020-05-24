

import pandas
import matplotlib.pyplot as plt
import numpy as np
import math
import cv2
from PIL import Image
import datetime
from scipy import stats

df = pandas.read_csv('../data/finalData.csv')
df2 = pandas.read_csv('../data/moodLogFinal.csv')
df3 = pandas.read_csv('../data/moodLogFinalAfter.csv')
df4 = pandas.read_csv('../data/moodLogFinalAll.csv')


# Variables:
chunkSize = 5 #minutes
shouldPlot = True

# Initialize:
lamp1avg = 0
lamp2avg = 0
lamp3avg = 0
luxAvg = 0
colorTemperatureAvg = 0
redAvg = 0
greenAvg = 0
blueAvg = 0

chunkItemCounter = 0
prevMinute = -1
chunks = []

timestampList = []
lamp1List = []
lamp2List = []
lamp3List = []
luxList = []
colorTemperatureList = []
redList = []
greenList = []
blueList = []

print("Data size:", len(df))

i = 0

for i in range(len(df)): # Goes through all elements in dataset
#for i in range(25150): # before
#for i in range(25150, len(df)): # after
#while(df['Timestamp'][i] < 1587573900000):
	# Date stuff:
	date = datetime.datetime.fromtimestamp(df['Timestamp'][i] / 1e3)
	thisMinute = int(date.strftime("%M"))

	# Add values:
	lamp1avg = lamp1avg + df['Lamp1'][i]
	lamp2avg = lamp2avg + df['Lamp2'][i]
	lamp3avg = lamp3avg + df['Lamp3'][i]
	luxAvg = luxAvg + df['Lux'][i]
	colorTemperatureAvg = colorTemperatureAvg + df['ColorTemperature'][i]
	redAvg = redAvg + df['Red'][i]
	greenAvg = greenAvg + df['Green'][i]
	blueAvg = blueAvg + df['Blue'][i]

	chunkItemCounter += 1

	#print(thisMinute, chunkSize, thisMinute % chunkSize == 0)
	#print(thisMinute != prevMinute)

	if (thisMinute % chunkSize == 0 and thisMinute != prevMinute):

		chunk = {
			"time": df['Timestamp'][i],
			"lamp1": lamp1avg / chunkItemCounter,
			"lamp2": lamp2avg / chunkItemCounter,
			"lamp3": lamp3avg / chunkItemCounter,
			"lux": luxAvg / chunkItemCounter,
			"colorTemperature": colorTemperatureAvg / chunkItemCounter,
			"red": redAvg / chunkItemCounter,
			"green": greenAvg / chunkItemCounter,
			"blue": blueAvg / chunkItemCounter
		}

		timestampList.append(df['Timestamp'][i])
		lamp1List.append(lamp1avg / chunkItemCounter)
		lamp2List.append(lamp2avg / chunkItemCounter)
		lamp3List.append(lamp3avg / chunkItemCounter)
		luxList.append(luxAvg / chunkItemCounter)
		colorTemperatureList.append(colorTemperatureAvg / chunkItemCounter)
		redList.append(redAvg / chunkItemCounter)
		greenList.append(greenAvg / chunkItemCounter)
		blueList.append(blueAvg / chunkItemCounter)

		# Add the chunk
		chunks.append(chunk)

		# Reset
		lamp1avg = 0
		lamp2avg = 0
		lamp3avg = 0
		luxAvg = 0
		colorTemperatureAvg = 0
		redAvg = 0
		greenAvg = 0
		blueAvg = 0
		chunkItemCounter = 0

	prevMinute = thisMinute

# Timestamp, X, Y, mood
energyLevel = df4["y"]
energyTimestamps = df4["Timestamp"]
sunsetTimestamps = []
minBefores = []
energyLevels = []


for i in range(len(energyTimestamps)):
	energyTimestamp = energyTimestamps[i]
	date = datetime.datetime.fromtimestamp(energyTimestamps[i] / 1e3)
	thisMinute = int(date.strftime("%M"))
	thisHour = int(date.strftime("%H"))

	if(thisHour < 14): # ratings before 11.00
		sunsetTi = int((thisHour * 60 + thisMinute + 3 * 60 + 13))
		print(energyTimestamps[i] - sunsetTi * 60 * 1000)

		minBefores.append(int((thisHour * 60 + thisMinute + 3 * 60 + 13) / 5))
		#timeSinceSunset = (thisHour * 60 + thisMinute + 3 * 60 + 13) * 60 * 1000

		#sunsetTimestamp = df['Timestamp'][i] - timeSinceSunset

		sunsetTimestamps.append(energyTimestamp)
		energyLevels.append(energyLevel[i])
		#sunsetDate = datetime.datetime.fromtimestamp(sunsetTimestamp / 1e3)


		# accumulate blue light from sunset (Sunset at 20.47) and 5 hours forward:

# make nice plot:

# Get indexes in dataset:

sunsetIndexes = []

# print(minBefores)

for i in range(len(sunsetTimestamps)):
	minDist = 99999999999
	minDistindex = -1
	for j in range(len(timestampList)):
		dist = abs(timestampList[j] - sunsetTimestamps[i])
		if dist < minDist:
			minDist = dist
			minDistindex = j
	sunsetIndexes.append(minDistindex)

# print(sunsetIndexes) # [57, 345, 633, 1209, 1498, 1785, 2361, 3513, 3514, 3801]

# get accumulated blue
sampleLength = int((5 * 60) / 5)
accBluesList = []

test = []

for i in range(len(sunsetIndexes)):
	accBlue = 0
	test = []
	for j in range(sampleLength):
		idx = sunsetIndexes[i] + j - minBefores[i]
		accBlue = accBlue + blueList[idx]
		test.append(blueList[idx])
	accBluesList.append(accBlue)

print(accBluesList)


def reverse(n): 
  return 160 - n

energyLevels = map(reverse, energyLevels)

enBefore = []
enAfter = []
accBlueBefore = []
accBlueAfter = []

slope, intercept, r_value, p_value, std_err = stats.linregress(accBluesList, energyLevels)
print("slope", slope)
print("intercept", intercept)
print("r_value", r_value)
print("p_value", p_value)
print("std_err", std_err)
print "r-squared:", r_value**2

# ('slope', -0.05143532690235725)
# ('intercept', 116.94431256356295)
# ('r_value', -0.38729297041396255)
# ('p_value', 0.23927949609850968)
# ('std_err', 0.04081418790776249)
# r-squared: 0.14999584493207047

# From 0 to 160
area = np.pi*5

# Plot
#plt.xscale("log")
plt.grid(color='#00000010', alpha=0.1, linestyle='-', linewidth=1)

plt.scatter(accBluesList, energyLevels, s=area, color="#0000ff", label="Energy")

mymodel = np.poly1d(np.polyfit(accBluesList, energyLevels, 1))
print(mymodel) # -0.05144 x + 116.9
myline = np.linspace(0, 600, 100)

plt.plot(myline, mymodel(myline), color="#000000", label="Linear regression")

plt.title('Energy level in the morning vs. accumulated blue light in the evening before')
plt.ylabel('Energy level')
plt.xlabel('Accumulated blue light after sunset (relative unit)')
plt.ylim(0, 160)
#plt.xlim(0, 1000)
plt.legend()
plt.show()

"""
plt.plot(test, color='#ff0000', linewidth=1)

plt.legend(['Red','Green','Blue'], loc='upper left')
plt.title('Average light during a day (After solution implemented)')
plt.xlabel('Time in intervals of 5 minutes')
plt.ylabel('Relative brightness')

plt.grid()
plt.yscale("log")

plt.show()
"""