import pandas
import matplotlib.pyplot as plt
import numpy as np
import math
import cv2
from PIL import Image
import datetime

df = pandas.read_csv('../data/finalData.csv')

# Variables:
chunkSize = 5 #minutes
shouldPlot = False

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

for i in range(len(df)): # Goes through all elements in dataset

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

print("Chunks size:", len(chunks))

if(shouldPlot):
	#plt.plot(dataA, color='#FF4F31', linewidth=1)
	plt.plot(redList, color='#ff0000', linewidth=1)
	plt.plot(greenList, color='#00ff00', linewidth=1)
	plt.plot(blueList, color='#0000ff', linewidth=1)

	plt.legend(['Red','Green','Blue'], loc='upper left')

	plt.xlabel('xLabel')
	plt.ylabel('yLabel')

	plt.grid()
	plt.yscale("log")
	plt.show()

def TwoFiveFiveLog(val):
	try:
		calVal = int(val)
		logVal = math.log10(calVal)
		adjust = int((logVal / 4) * 255)
		limited = max(0, min(255, adjust))
		return int((logVal / 4) * 255)
	except ValueError:
		return 0

def addZeros(data, amount):
	newArray = []
	for num in range(amount):
		newArray.append(0)
	for dat in data:
		newArray.append(dat)
	return newArray

rykLigeLidt = 210

data1 = addZeros(redList, rykLigeLidt)
data2 = addZeros(greenList, rykLigeLidt)
data3 = addZeros(blueList, rykLigeLidt)

imageWidth = 288 #One for each 5 min of a day
imageHeight = 800

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
		#print("writing to", [x, wid], "samplesADay", int(samplesADay))
		data[row, col] = [red, green, blue]

img = Image.fromarray(data, 'RGB')
img.save('my.png')
img.show()