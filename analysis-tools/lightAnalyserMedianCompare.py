

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

#for i in range(25150): # Goes through all elements in dataset
for i in range(25150, len(df)): # Goes through all elements in dataset
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

# Accumulated blue light after sunset:
accBlue = 0
for j in range(int(1247 / 5), len(dayAvgBlue)):
  accBlue = accBlue + dayAvgBlue[j]

# Before: ('AccBlue', 206)
# After: ('AccBlue', 85)

q2before = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 5.0, 10.0, 20.0, 33.0, 51.0, 67.0, 86.0, 106.0, 142.0, 178.0, 239.0, 794.0, 1011.0, 1095.0, 1157.0, 1257.0, 1326.0, 1441.0, 1813.0, 2190.0, 2465.0, 2707.0, 2730.0, 2958.0, 2628.0, 2723.0, 2797.0, 2887.0, 3119.0, 3389.0, 3399.0, 3485.0, 3655.0, 3767.0, 3966.0, 3867.0, 3889.0, 4000.0, 4199.0, 4185.0, 4297.0, 4492.0, 4966.0, 5241.0, 5500.0, 5633.0, 5664.0, 5585.0, 5072.0, 5075.0, 5021.0, 5338.0, 5284.0, 5226.0, 5168.0, 5106.0, 5057.0, 5046.0, 4776.0, 4890.0, 4844.0, 4697.0, 4924.0, 4748.0, 4492.0, 4231.0, 4566.0, 4453.0, 4308.0, 4172.0, 4036.0, 3901.0, 3587.0, 3288.0, 3056.0, 2876.0, 2772.0, 2707.0, 2612.0, 2525.0, 2440.0, 2350.0, 2272.0, 2208.0, 2153.0, 1913.0, 1833.0, 2047.0, 1843.0, 1644.0, 1573.0, 1448.0, 1363.0, 1311.0, 1268.0, 1233.0, 1209.0, 1177.0, 1155.0, 1193.0, 1309.0, 1250.0, 1141.0, 1113.0, 1085.0, 1083.0, 1047.0, 1046.0, 1043.0, 1030.0, 1011.0, 1002.0, 980.0, 978.0, 1001.0, 1008.0, 975.0, 934.0, 982.0, 976.0, 912.0, 903.0, 894.0, 857.0, 922.0, 912.0, 893.0, 888.0, 884.0, 872.0, 862.0, 855.0, 847.0, 839.0, 831.0, 796.0, 768.0, 763.0, 756.0, 749.0, 742.0, 702.0, 728.0, 710.0, 674.0, 697.0, 687.0, 633.0, 623.0, 614.0, 663.0, 654.0, 644.0, 633.0, 624.0, 612.0, 599.0, 587.0, 554.0, 528.5, 515.5, 497.5, 441.0, 433.5, 408.0, 388.0, 366.0, 332.0, 307.0, 292.0, 269.0, 240.0, 193.0, 165.0, 138.0, 108.0, 84.0, 60.0, 41.0, 37.0, 34.0, 32.0, 21.0, 18.0, 16.0, 12.0, 10.0, 9.0, 9.0, 8.0, 8.0, 8.0, 8.0, 6.0, 6.0, 3.0, 1.0, 1.0, 2.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
q2after = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 5.0, 11.0, 20.0, 31.0, 47.0, 74.0, 98.0, 126.0, 164.0, 205.0, 245.0, 300.0, 572.0, 412.0, 572.0, 872.0, 1953.0, 1275.0, 967.0, 1236.0, 2065.0, 2495.0, 2198.0, 2770.0, 2900.0, 2929.0, 2895.0, 2923.0, 2835.0, 2838.0, 3103.0, 3025.0, 3404.0, 3410.0, 3407.0, 3426.0, 3604.0, 3749.0, 3898.0, 3713.0, 3842.0, 4044.0, 4243.0, 4277.0, 4253.0, 4293.0, 4418.0, 4510.0, 4465.0, 4430.0, 4426.0, 4468.0, 4414.0, 4386.0, 4617.0, 4600.0, 4521.0, 4297.0, 4490.0, 5158.0, 4073.0, 3676.0, 3833.0, 3737.0, 2817.0, 3416.0, 3550.0, 3535.0, 3503.0, 3412.0, 3458.0, 3439.0, 3294.0, 3414.0, 2234.0, 2147.0, 2553.0, 1946.0, 2949.0, 2840.0, 2706.0, 2616.0, 2187.0, 2372.0, 2294.0, 2245.0, 2369.0, 2129.0, 1839.0, 1751.0, 1668.0, 1694.0, 1639.0, 1644.0, 1766.0, 1741.0, 1674.5, 1615.5, 1612.0, 1612.5, 1565.0, 1558.0, 1500.0, 1461.5, 1422.0, 1400.5, 1342.0, 1303.5, 1270.0, 1231.0, 1136.0, 1164.5, 1102.5, 1213.5, 1169.0, 1189.5, 1242.5, 1156.0, 1068.0, 1160.5, 1150.0, 1202.0, 1180.0, 1173.0, 1144.0, 1150.0, 1117.0, 1017.5, 955.0, 988.5, 1002.5, 1008.5, 1011.0, 1003.0, 1028.0, 994.0, 920.5, 940.0, 989.5, 924.0, 914.0, 870.0, 826.5, 774.0, 736.5, 730.0, 695.5, 732.0, 626.0, 615.0, 601.0, 550.5, 537.0, 570.5, 562.0, 559.5, 542.5, 562.0, 560.5, 548.5, 568.0, 560.0, 543.0, 527.0, 509.0, 503.0, 485.0, 448.0, 439.0, 415.0, 372.0, 344.0, 314.0, 285.0, 255.0, 230.0, 188.0, 154.0, 123.0, 99.0, 75.0, 53.0, 46.0, 34.0, 22.0, 13.0, 8.0, 4.0, 3.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
q2compare = []

for bent in range(249, 288):
  first = 0
  if(q2before[bent] != 0):
    first = math.log(abs(q2before[bent]))

  second = 0
  if(q2after[bent] != 0):
    first = math.log(abs(q2after[bent]))

  q2compare.append(q2before[bent] - q2after[bent])

if(shouldPlot):
  plt.plot(q2compare, color='#000000', linewidth=1)

  plt.legend(['Min'], loc='upper left')
  plt.title('Quantile - adjusted for Q2')
  plt.xlabel('Time in intervals of 5 minutes')
  plt.ylabel('Difference from Q2')

  plt.grid()

  plt.show()