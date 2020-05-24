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

def reverse(n): 
  return 160 - n

# Timestamp, X, Y, mood
happinessesBefore = df["x"]
energyLevelsBefore = df["y"]
energyLevelsBefore = map(reverse, energyLevelsBefore)

avgEnergyB = 0
for i in range(len(energyLevelsBefore)):
  avgEnergyB = avgEnergyB + energyLevelsBefore[i]
avgEnergyB = int(avgEnergyB / len(energyLevelsBefore))

avgHappyB = 0
for i in range(len(happinessesBefore)):
  avgHappyB = avgHappyB + happinessesBefore[i]
avgHappyB = int(avgHappyB / len(happinessesBefore))

happinessesAfter = df2after["x"]
energyLevelsAfter = df2after["y"]
energyLevelsAfter = map(reverse, energyLevelsAfter)

avgEnergyA = 0
for i in range(len(energyLevelsAfter)):
  avgEnergyA = avgEnergyA + energyLevelsAfter[i]
avgEnergyA = int(avgEnergyA / len(energyLevelsAfter))

avgHappyA = 0
for i in range(len(happinessesAfter)):
  avgHappyA = avgHappyA + happinessesAfter[i]
avgHappyA = int(avgHappyA / len(happinessesAfter))



# From 0 to 160
area = np.pi*5

# Plot
plt.grid(color='#00000010', alpha=0.1, linestyle='-', linewidth=1)
plt.scatter(happinessesBefore, energyLevelsBefore, s=area, color="#ff9999", label="Before")
plt.scatter(happinessesAfter, energyLevelsAfter, s=area, color="#9999ff", label="After")


plt.scatter(avgHappyB, avgEnergyB, s=area, color="#ff0000", label="Before AVG")
plt.scatter(avgHappyA, avgEnergyA, s=area, color="#0000ff", label="After AVG")


plt.title('Mood scatter')
plt.xlabel('Happiness')
plt.ylabel('Energy level')
plt.ylim(0, 160)
plt.xlim(0, 160)
plt.legend()
plt.show()
