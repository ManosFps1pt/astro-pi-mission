import pandas as pd
import math
from datetime import datetime as dt
import matplotlib.pyplot as plt

data_path = "iss-data.csv"
data_set = pd.read_csv(data_path)
print(f"Row Count = {len(data_set):5d}")
#print("Row Count = {:5d}".format(len(data_set)))
earth_rad = 3440.1 #miles
velocity_list = []
latitude_list = []
longitude_list = []
times_list = []
i = 0
while i < len(data_set) - 1: 
    print(f"----- ITERATION {i} -----")
    latA = data_set.iloc[i,1]
    longA = data_set.iloc[i,2]
    latB = data_set.iloc[i+1,1]
    longB = data_set.iloc[i+1,2]
    timeA = data_set.iloc[i,0]
    timeB = data_set.iloc[i+1,0]

    timeA = dt.strptime(timeA, '%Y-%m-%d %H:%M:%S')
    timeB = dt.strptime(timeB, '%Y-%m-%d %H:%M:%S')
    deltaT = (timeB-timeA).seconds

    y_difference = (latB - latA) * 111_111   #To convert degrees to meters we multiply by 111111#
    x_difference = (longB - longA) * 111_111 #To convert degrees to meters we multiply by 111111#
    distance = math.hypot(x_difference, y_difference)
    velocity_km_per_sec = distance/deltaT/1000

    velocity_list.append(velocity_km_per_sec)
    latitude_list.append(latA)
    times_list.append(timeA)
    longitude_list.append(longA)
    i += 1
    # print(f"latitudeA = {latA:.3f} degress longitudeA = {longA:.3f} degrees")
    # print("latituteB = {:.3f} degrees longitudeB = {:.3f} degrees".format(latB, longB))
    # print(f"timeA = {timeA} timeB = {timeB} DeltaT = {deltaT} seconds")
    # print(f"velocity = {velocity_km_per_sec:.2f} km/sec")
plt.plot(times_list, latitude_list, c="red", label="latitude", linewidth=.5)
plt.plot(times_list, velocity_list, c="green", label="velocity", linewidth=.5)
plt.plot(times_list, longitude_list, c="blue", label="longitude", linewidth=.5)
plt.ylabel("lattitude-longitude-speed")
plt.xlabel("time")
plt.title("data visualization")
plt.legend()
plt.show()
print(f"median speed = {velocity_list[len(velocity_list)//2]:.2f} km/sec")
