import os
import sys
libPath = 'C:\\Users\\user\\AppData\\Local\\Temp\\.astro_pi_replay'
if not libPath in sys.path: sys.path.append(libPath)
import pandas as pd
import math
from datetime import datetime as dt
# import matplotlib.pyplot as plt
import numpy as np
from picamzero import Camera
from orbit import ISS
from time import sleep

def covert_degrees_radians(degrees):
    return degrees*math.pi/180

def get_gps_coordinates(iss):
    point = iss.coordinates()
    return (point.latitude.signed_dms(), point.longitude.signed_dms())

earth_rad = 3440.1 #miles
pythLst = [0]
harvLst = [0]
wait_time = 5 #seconds
velocityList =[]
iss = ISS()
cam = Camera()
#for i in range(len(data_set)-1):
for i in range(10):
    cam.take_photo(f"image {i + 1}.jpg")
    location = ISS().coordinates()
    print(f'LongitudeA degrees = {location.longitude.degrees}')
    print(f'LatitudeA degrees = {location.latitude.degrees}')
    #print(f'LongitudeA radians = {location.longitude.radians}')
    #print(f'LatitudeA radians = {location.latitude.radians}')
    radLongA = location.longitude.radians
    radLatA = location.latitude.radians
    elevA = location.elevation.km
    sleep(wait_time)
    location = ISS().coordinates()
    print(f'LongitudeB degress = {location.longitude.degrees}')
    print(f'LatitudeB degrees = {location.latitude.degrees}')
    #print(f'LongitudeB radians = {location.longitude.radians}')
    #print(f'LatitudeB radians = {location.latitude.radians}')
    radLongB = location.longitude.radians
    radLatB = location.latitude.radians
    elevB = location.elevation.km
    distance = (earth_rad)*math.acos((math.sin(radLatA)*math.sin(radLatB))+
                                math.cos(radLatA)*math.cos(radLatB)*math.cos(radLongA-radLongB))
    distance = distance*1.853 + (1670/3600) * wait_time  + abs(elevB-elevA)
    velocity = distance / wait_time
    print("distance =  %2.2f km, velocity =  %.5f km/sec latB - latA = %.5f" %(distance, velocity, (radLatB - radLatA)))
    velocityList.append(velocity)
    print("====================================================================")

with open("output.txt", "w") as file:
    for i in velocityList:
        file.write(str(i))
velocityList.sort()
estimate_kmps = velocityList[len(velocityList)//2]
print(f'Estimates Velocity = {estimate_kmps:.5f} km/sec')
with open("result.txt", "w") as file:
    file.write(str(estimate_kmps))

    
