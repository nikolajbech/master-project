import pandas
import matplotlib.pyplot as plt
import numpy as np
import math
import cv2
from PIL import Image
import datetime

# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = "Circadian", "Reading", "Productivity", "Relax", "Pause"
sizes = [431446254,	7709944,	51029881,	551499,	42960646]

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()