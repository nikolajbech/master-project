import pandas
import matplotlib.pyplot as plt
import numpy as np
import math
import cv2
from PIL import Image
import datetime

df = pandas.read_csv('../data/moodLogFinal.csv')
df2after = pandas.read_csv('../data/moodLogFinalAfter.csv')

# 22. april 16.46 shift from no light control to light control

getEnergy = True

def reverse(n): 
  return 160 - n

timestamps = df["Timestamp"]

if(getEnergy):
  energyLevel = df["y"]
  energyLevel = map(reverse, energyLevel)
else:
  energyLevel = df["x"]
minutes = []

timestampsAfter = df2after["Timestamp"]

if(getEnergy):
  energyLevelAfter = df2after["y"]
  energyLevelAfter = map(reverse, energyLevelAfter)
else:
  energyLevelAfter = df2after["x"]

minutesAfter = []

for i in range(len(df)):
  date = datetime.datetime.fromtimestamp(df['Timestamp'][i] / 1e3)
  thisMinute = int(date.strftime("%M"))
  thisHour = int(date.strftime("%H"))
  minute = thisHour * 60 + thisMinute
  minutes.append(minute)

for i in range(len(df2after)):
  date = datetime.datetime.fromtimestamp(df['Timestamp'][i] / 1e3)
  thisMinute = int(date.strftime("%M"))
  thisHour = int(date.strftime("%H"))
  minute = thisHour * 60 + thisMinute
  minutesAfter.append(minute)

# AVG morning before
avgMorningBefore = 0
avgMorningBeforeEnergy = 0
counter = 0
counter2 = 0
while(counter < len(minutes)):
  if(minutes[counter] < 800):
    avgMorningBefore = avgMorningBefore + minutes[counter]
    avgMorningBeforeEnergy = avgMorningBeforeEnergy + energyLevel[counter]
    counter2 = counter2 + 1
  counter = counter + 1

avgMorningBefore = avgMorningBefore / counter2
avgMorningBeforeEnergy = avgMorningBeforeEnergy / counter2

# AVG evening before
avgEveningBefore = 0
avgEveningBeforeEnergy = 0
counter = 0
counter2 = 0
while(counter < len(minutes)):
  if(minutes[counter] > 800):
    avgEveningBefore = avgEveningBefore + minutes[counter]
    avgEveningBeforeEnergy = avgEveningBeforeEnergy + energyLevel[counter]
    counter2 = counter2 + 1
  counter = counter + 1

  print(counter2)

avgEveningBefore = avgEveningBefore / counter2
avgEveningBeforeEnergy = avgEveningBeforeEnergy / counter2

print(avgMorningBefore, avgMorningBeforeEnergy)
  

# AVG morning after
avgMorningAfter = 0
avgMorningAfterEnergy = 0
counter = 0
counter2 = 0
while(counter < len(minutesAfter)):
  if(minutes[counter] < 800):
    avgMorningAfter = avgMorningAfter + minutesAfter[counter]
    avgMorningAfterEnergy = avgMorningAfterEnergy + energyLevelAfter[counter]
    counter2 = counter2 + 1
  counter = counter + 1

avgMorningAfter = avgMorningAfter / counter2
avgMorningAfterEnergy = avgMorningAfterEnergy / counter2

# AVG evening after
avgEveningAfter = 0
avgEveningAfterEnergy = 0
counter = 0
counter2 = 0
while(counter < len(minutesAfter)):
  if(minutes[counter] > 800):
    avgEveningAfter = avgEveningAfter + minutesAfter[counter]
    avgEveningAfterEnergy = avgEveningAfterEnergy + energyLevelAfter[counter]
    counter2 = counter2 + 1
  counter = counter + 1

avgEveningAfter = avgEveningAfter / counter2
avgEveningAfterEnergy = avgEveningAfterEnergy / counter2


# From 0 to 160
area = np.pi*5

# Plot
plt.grid(color='#eeeeee', linestyle='-', linewidth=1)
plt.scatter(minutes, energyLevel, s=area, color="#ff4040", label="Before")
plt.scatter(minutesAfter, energyLevelAfter, s=area, color="#4040ff", label="After")


#plt.scatter(avgMorningBefore, avgMorningBeforeEnergy, s=area, color="#00ff00", label="Before avg")
#plt.scatter(avgEveningBefore, avgEveningBeforeEnergy, s=area, color="#00ff00", label="Before avg")

#plt.scatter(avgMorningAfter, avgMorningAfterEnergy, s=area, color="#ffff00", label="After avg")
#plt.scatter(avgEveningAfter, avgEveningAfterEnergy, s=area, color="#ffff00", label="After avg")

plt.plot([avgMorningBefore, avgEveningBefore], [avgMorningBeforeEnergy, avgEveningBeforeEnergy], color="#ff4040", label="Before (avg)")
plt.plot([avgMorningAfter, avgEveningAfter], [avgMorningAfterEnergy, avgEveningAfterEnergy], color="#4040ff", label="After (avg)")

plt.title('Time of mood rating and energy level')
plt.xlabel('Time of day in minutes')
if(getEnergy):
  plt.ylabel('Energy level')
else:
  plt.ylabel('Happiness')
plt.ylim(0, 160)

plt.legend()
plt.show() 