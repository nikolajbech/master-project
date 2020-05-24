

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

for i in range(25150): # Goes through all elements in dataset
#for i in range(25150, len(df)): # Goes through all elements in dataset
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

  i = i + 1

print("i", i) # 25150

prevHour = -1

dayAvgRed = [] # size 24 * 12 = 288
dayAvgGreen = []
dayAvgBlue = []

dayAvgRedCounter = [] # size 24 * 12 = 288
dayAvgGreenCounter = []
dayAvgBlueCounter = []

allIntervals = []

for brian in range(288):
  valuesInInterval = []
  allIntervals.append(valuesInInterval)

for lars in range(289):
  dayAvgRed.append(0)
  dayAvgGreen.append(0)
  dayAvgBlue.append(0)
  dayAvgRedCounter.append(0)
  dayAvgGreenCounter.append(0)
  dayAvgBlueCounter.append(0)

for iddx in range(len(chunks)):

  # Time:
  date = datetime.datetime.fromtimestamp(chunks[iddx]['time'] / 1e3)
  thisMinute = int(date.strftime("%M"))
  thisHour = int(date.strftime("%H"))
  idx = (thisHour * 60 + thisMinute) / chunkSize

  dayAvgRed[idx] = dayAvgRed[idx] + chunks[iddx]['red']
  dayAvgRedCounter[idx] = dayAvgRedCounter[idx] + 1

  dayAvgGreen[idx] = dayAvgGreen[idx] + chunks[iddx]['green']
  dayAvgGreenCounter[idx] = dayAvgGreenCounter[idx] + 1

  dayAvgBlue[idx] = dayAvgBlue[idx] +chunks[iddx]['blue']
  dayAvgBlueCounter[idx] = dayAvgBlueCounter[idx] + 1


  #Special thing for blue:
  allIntervals[idx].append(chunks[iddx]['blue'])

print(pandas.Series(allIntervals[200]).quantile([0.00, 0.25,0.5,0.75, 1.00])[0])

mins = []
q1s = []
q2s = []
q3s = []
maxs = []

for jens in range(0, 288):
  jeeens = pandas.Series(allIntervals[jens]).quantile([0.00, 0.25,0.5,0.75, 1.00])
  mins.append(float(jeeens[0]))
  q1s.append(float(jeeens[0.25]))
  q2s.append(float(jeeens[0.50]))
  q3s.append(float(jeeens[0.75]))
  maxs.append(float(jeeens[1.00]))

for idddx in range(288):
  dayAvgRed[idddx] = int(dayAvgRed[idddx] / dayAvgRedCounter[idddx])
  dayAvgGreen[idddx] = int(dayAvgGreen[idddx] / dayAvgGreenCounter[idddx])
  dayAvgBlue[idddx] = int(dayAvgBlue[idddx] / dayAvgBlueCounter[idddx])

accMedianBluelight = 0
for brian in range(249, 288):
  accMedianBluelight = accMedianBluelight + q2s[brian]

accMedianBluelight = accMedianBluelight / (288 - 249)

print("accMedianBluelight", accMedianBluelight)

# Accumulated blue light after sunset:
accBlue = 0
for j in range(int(1247 / 5), len(dayAvgBlue)):
  accBlue = accBlue + dayAvgBlue[j]

print("AccBlue", accBlue)
# Before: ('AccBlue', 206)
# After: ('AccBlue', 85)

print(q2s)

if(shouldPlot):
  plt.plot(mins, color='#DEDEDE', linewidth=1)
  plt.plot(q1s, color='#7E7E7E', linewidth=1)
  plt.plot(q2s, color='#000000', linewidth=1)
  plt.plot(q3s, color='#7E7E7E', linewidth=1)
  plt.plot(maxs, color='#DEDEDE', linewidth=1)

  plt.legend(['Min','Q1','Q2', 'Q3', 'Max'], loc='upper left')
  plt.title('Blue light (before)')
  plt.xlabel('Time in intervals of 5 minutes')
  plt.ylabel('Light intensity')

  plt.grid()
  plt.yscale("log")

  plt.axvline(int(326 / 5)) # Sunrise at 05.26
  plt.axvline(int(1247 / 5)) # Sunset at 20.47
  plt.text(int(326 / 5) - 3, 150, 'Sunrise', horizontalalignment='right')
  plt.text(int(1247 / 5) + 3, 150, 'Sunset', horizontalalignment='left')

  plt.show()