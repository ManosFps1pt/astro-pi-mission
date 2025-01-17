import pandas as pd
import math
from datetime import datetime as dt
import matplotlib.pyplot as plt


data_path = "iss-data.csv"
data_set = pd.read_csv(data_path)
print(f"Row Count = {len(data_set):5d}")
#print("Row Count = {:5d}".format(len(data_set)))
earth_rad = 3440.1 # nautical miles

haversine_velocity_list = []
pythagorean_velocity_list = []
latitude_list = []
longitude_list = []
times_list = []
inaccuracy_rate = []
iss_speed = 7.66
i = 0

def covert_degrees_radians(degrees):
    return degrees*math.pi/180

def haversine_formula(long1: float, lat1: float, long2: float, lat2: float) -> float:
    return (
        3440.1
        * math.acos (
            (
                math.sin (
                    lat1
                ) * math.sin (
                    lat2
                )
            ) + math.cos (
                    lat1
                ) * math.cos (
                    lat2
                ) * math.cos (
                long1 - long2
            )
        )
    )

def hf(radLongA, radLatA, radLongB, radLatB):
    distance = earth_rad * math.acos((math.sin(radLatA) * math.sin(radLatB)) +
                                     math.cos(radLatA) * math.cos(radLatB) * math.cos(radLongA - radLongB))
    return distance


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

    latA_radians = covert_degrees_radians(latA)
    latB_radians = covert_degrees_radians(latB)
    longA_radians = covert_degrees_radians(longA)
    longB_radians = covert_degrees_radians(longB)

    y_difference = (abs(latB) - abs(latA)) * 111_111   #To convert degrees to meters we multiply by 111111#
    x_difference = (abs(longB) - abs(longA)) * 111_111 #To convert degrees to meters we multiply by 111111#
    haversine_distance = hf(longA_radians, latA_radians, longB_radians, latB_radians)
    pythagorean_distance = math.hypot(x_difference, y_difference)
    haversine_velocity_km_per_sec = ((haversine_distance * 1.853) + (1670/3600) * deltaT)  / deltaT
    pythagorean_velocity_km_per_sec = pythagorean_distance / deltaT / 1000

    haversine_velocity_list.append(haversine_velocity_km_per_sec)
    latitude_list.append(latA)
    times_list.append(timeA)
    longitude_list.append(longA)
    inaccuracy_rate.append(abs(haversine_velocity_km_per_sec - iss_speed))
    pythagorean_velocity_list.append(pythagorean_velocity_km_per_sec)
    i += 1
    # print(f"latitudeA = {latA:.3f} degrees longitudeA = {longA:.3f} degrees")
    # print("latitudeB = {:.3f} degrees longitudeB = {:.3f} degrees".format(latB, longB))
    # print(f"timeA = {timeA} timeB = {timeB} DeltaT = {deltaT} seconds")
    # print(f"velocity = {velocity_km_per_sec:.2f} km/sec")
print(f"median speed = {haversine_velocity_list[len(haversine_velocity_list) // 2]:.2f} km/sec")
print(f"average speed = {sum(haversine_velocity_list)/len(haversine_velocity_list):.2f} km/sec")
print(max(latitude_list))
plt.plot(times_list, latitude_list, c="red", label="latitude", linewidth=.5)
plt.plot(times_list, haversine_velocity_list, c="green", label="haversine velocity estimation", linewidth=.5)
plt.plot(times_list, longitude_list, c="blue", label="longitude", linewidth=.5)
plt.plot(times_list, [iss_speed for _ in range(len(times_list))], c="black", label="iss velocity", linewidth=2)
plt.plot(times_list, pythagorean_velocity_list, c="purple", label="Pythagorean velocity estimation", linewidth=.5)
# plt.plot(times_list, inaccuracy_rate, c="yellow", label="inaccuracy rate", linewidth=.5)
plt.ylabel("latitude-longitude-speed")
plt.xlabel("time")
plt.title("data visualization")
plt.legend()
plt.show()

