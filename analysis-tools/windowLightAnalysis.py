import pandas
import matplotlib.pyplot as plt
import numpy as np
import math
import cv2
from PIL import Image
import datetime

df = pandas.read_csv('../data/SensorData.csv')

# Variables:
chunkSize = 10 #minutes
shouldPlot = True

# Initialize:
luxAvg = 0
colorTemperatureAvg = 0
redAvg = 0
greenAvg = 0
blueAvg = 0

chunkItemCounter = 0
prevMinute = -1
chunks = []

timestampList = []
luxList = []
colorTemperatureList = []
redList = []
greenList = []
blueList = []

print("Data size:", len(df))

#Timestamp,Temperature,Lux,R,G,B,C,,Timestamp2,temperature2,Lux2,R2,G2,B2,C2

dayCounter = 0
prevDay = 0

for i in range(len(df)): # Goes through all elements in dataset

	# Date stuff:
	date = datetime.datetime.fromtimestamp(df['Timestamp'][i] / 1e3)
	thisMinute = int(date.strftime("%M"))
	day = int(date.strftime("%d"))
	thisMinute = round(thisMinute / 2) * 2

	if(prevDay != day):
		prevDay = day
		print(dayCounter)
		dayCounter = 0
	else:
		dayCounter = dayCounter + 1

	# Add values:
	luxAvg = luxAvg + df['Lux2'][i]
	colorTemperatureAvg = colorTemperatureAvg + df['temperature2'][i]
	redAvg = redAvg + df['R2'][i]
	greenAvg = greenAvg + df['G2'][i]
	blueAvg = blueAvg + df['B2'][i]

	chunkItemCounter += 1

	#print(thisMinute, chunkSize, thisMinute % chunkSize == 0)
	#print(thisMinute != prevMinute)

	#if (thisMinute % chunkSize == 0 and thisMinute != prevMinute):

	chunk = {
		"time": df['Timestamp'][i],
		"lux": luxAvg / chunkItemCounter,
		"colorTemperature": colorTemperatureAvg / chunkItemCounter,
		"red": redAvg / chunkItemCounter,
		"green": greenAvg / chunkItemCounter,
		"blue": blueAvg / chunkItemCounter
	}

	timestampList.append(df['Timestamp'][i])
	luxList.append(luxAvg / chunkItemCounter)
	colorTemperatureList.append(colorTemperatureAvg / chunkItemCounter)
	redList.append(redAvg / chunkItemCounter)
	greenList.append(greenAvg / chunkItemCounter)
	blueList.append(blueAvg / chunkItemCounter)

	# Add the chunk
	chunks.append(chunk)

	# Reset
	luxAvg = 0
	colorTemperatureAvg = 0
	redAvg = 0
	greenAvg = 0
	blueAvg = 0
	chunkItemCounter = 0

	prevMinute = thisMinute

if(shouldPlot):
	#plt.plot(dataA, color='#FF4F31', linewidth=1)
	plt.plot(redList, color='#ff0000', linewidth=1)
	plt.plot(greenList, color='#00ff00', linewidth=1)
	plt.plot(blueList, color='#0000ff', linewidth=1)

	plt.legend(['Red','Green','Blue'], loc='upper left')

	plt.xlabel('Time')
	plt.ylabel('Light intensity')

	plt.grid()
	plt.yscale("log")
	plt.show()

def TwoFiveFiveLog(val):
	try:
		calVal = int(val)
		logVal = math.log10(calVal)
		adjust = int((logVal / 4.8) * 255)
		limited = max(0, min(255, adjust))
		return limited
	except ValueError:
		return 0

def addZeros(data, amount):
	newArray = []
	for num in range(amount):
		newArray.append(0)
	for dat in data:
		newArray.append(dat)
	return newArray

rykLigeLidt = 220

data1 = addZeros(redList, rykLigeLidt)
data2 = addZeros(greenList, rykLigeLidt)
data3 = addZeros(blueList, rykLigeLidt)

imageWidth =  711 #One for each 5 min of a day
imageHeight = 40 * 5

data = np.zeros((imageHeight, imageWidth, 3), dtype=np.uint8)

y = 0
offset = 0
for row in range(imageHeight):
	val = 0
	
	if row % 40 == 0:
			offset = offset + 1

	for col in range(imageWidth):

		val = col + (offset * imageWidth)

		if val > len(redList) - 1:
			val = 0

		red = TwoFiveFiveLog(data1[val])
		green = TwoFiveFiveLog(data2[val])
		blue = TwoFiveFiveLog(data3[val])
		data[row, col] = [red, green, blue]

img = Image.fromarray(data, 'RGB')
img.save('windowSensorLight.png')
img.show()