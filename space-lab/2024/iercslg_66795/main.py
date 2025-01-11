""""
                SPEED ESTIMATION OF ISS
    IERCSLG of 3rd GYMNASIUM OF IERAPETRA CRETE GREECE
    
To estimate the speed of ISS we use geographic coordinates to measure the distance in kms between two points (A, B) on the
surface of the earth, within time intervals of 1 second, i.e.
we take the position of ISS "now" and retake its position after 1 sec.
Then we devide the distance travelled by the time interval to calculate
the speed, in our case since time interval equals 1 sec, speed equals the travalled distance.

In order calculate the distance between any two points we use the Harvesine formula as explained in: https://www.youtube.com/watch?v=HaGj0DjX8W8.
We use time intervals of 1 second because according to our experiments it results to a better estimation, however
our program is general enough to allow any time interval by changing appropriately the value of "wait_time" variable.

We collect plenty such pair of points with each point pair resulting in a different speed estimation.
As the final speed estimation we take the median of the collected values.

In the mean time we collect various sensor values such as temprature, humidity, pressure, latitude, longitude etc.
which are saved in a .csv file, while intermediate results are kept in the output.txt file. The fianl result of speed
estimation is saved in the result.txt file.

"""

#Iporting libraries
import os
import sys
import csv
from sense_hat import SenseHat
from pathlib import Path
from orbit import ISS
from picamera import PiCamera
import time
import math
from datetime import datetime as dt, timedelta
from time import sleep

#initalize "constants"
base_folder = Path(__file__).parent.resolve()
out_file = open(base_folder / "output.txt", "w") #File for writing intermediate results
earth_rad = 3440.1 #miles
running_time = 10 #minutes
wait_time = 1 #seconds
cam = PiCamera()
cam.resolution = (4056, 3040)
seperator = "="

# Set up Sense Hat
sense = SenseHat()

def create_csv_file(data_file):
    """Create a new CSV file and add the header row"""
    with open(data_file, 'w', newline='') as f:
        writer = csv.writer(f)
        header = ("Counter", "Date/time", "Latitude", "Longitude", "Temperature", "Humidity", "Pressure", "Compass")
        writer.writerow(header)

def add_csv_data(data_file, data):
    """Add a row of data to the data_file CSV"""
    with open(data_file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data)

def convert(angle):
    # Convert a `skyfield` Angle to an Exif-appropriate
    # representation (positive rationals)
    # e.g. 98° 34' 58.7 to "98/1,34/1,587/10"
    # Return a tuple containing a Boolean and the converted angle,
    # with the Boolean indicating if the angle is negative
    sign, degrees, minutes, seconds = angle.signed_dms()
    exif_angle = f'{degrees:.0f}/1,{minutes:.0f}/1,{seconds*10:.0f}/10'
    return sign < 0, exif_angle

def custom_capture(iss, camera, base_folder, image):
    # Use `camera` to capture an `image` file with lat/long Exif data
    point = iss.coordinates()
    # Convert the latitude and longitude to Exif-appropriate
    # representations
    south, exif_latitude = convert(point.latitude)
    west, exif_longitude = convert(point.longitude)
    # Set the Exif tags specifying the current location
    camera.exif_tags['GPS.GPSLatitude'] = exif_latitude
    camera.exif_tags['GPS.GPSLatitudeRef'] = "S" if south else "N"
    camera.exif_tags['GPS.GPSLongitude'] = exif_longitude
    camera.exif_tags['GPS.GPSLongitudeRef'] = "W" if west else "E"
    
    # Capture the image
    camera.capture(str(base_folder) + "/" + image)

def covert_degrees_radians(degrees):
    return degrees*math.pi/180

#Create a list to keep the speed estimated in each iteration
velocityList = []

# Create a variable to store the start time
start_time = dt.now()

# Create a variable to store the current time
# (these will be almost the same at the start)
now_time = dt.now()

# Initialise the CSV file
data_file = base_folder/"data.csv"
create_csv_file(data_file)

idx = 1
while (now_time < start_time + timedelta(minutes = running_time - 0.35)):
    try: 
        loop_start_time = dt.now()
        out_file.write(f"Iterarion = {idx}\n")
        
        #capturing the coordinates of current ISS location (A)
        location = ISS().coordinates()
        
        #Taking measurements from the sensors
        humidity = round(sense.humidity, 1)
        temperature = round(sense.temperature, 1)
        pressure = round(sense.pressure, 1)
        compass = round(sense.compass, 1)
        
        #Writting location data of point A to output.txt file
        out_file.write(f"{location} \n")
        out_file.write(f'LatitudeA in degrees: {location.latitude.degrees}\n')
        out_file.write(f'LongitudeA in degrees: {location.longitude.degrees}\n')
        out_file.write(f'ElevationA in Km: {location.elevation.km}\n')
        
        #Keep latitude and longitude of point A in degrees
        latA = location.latitude.degrees
        longA = location.longitude.degrees
        
        #Take elevation of point A as well
        elevA = location.elevation.km
        
        #Add total data collected for point A to the data.csv file
        data = idx, dt.now(), latA, longA, temperature, humidity, pressure, compass
        add_csv_data(data_file, data)
        
        sleep(wait_time) #wait for wait_time seconds until the next gps position
        
        #capturing the coordinates of current ISS location (B)
        location = ISS().coordinates()
        
        #Taking measurements from the sensors
        humidity = round(sense.humidity, 1)
        temperature = round(sense.temperature, 1)
        pressure = round(sense.pressure, 1)
        compass = round(sense.compass, 1)
        
        #Writting location data of point B to output.txt file
        out_file.write(f"{location} \n")
        out_file.write(f'LatitudeB in degress: {location.latitude.degrees}\n')
        out_file.write(f'LongitudeB in degrees: {location.longitude.degrees}\n')
        out_file.write(f'ElevationB in Km: {location.elevation.km}\n')
        
        #Keep latitude and longitude of point B in degrees
        latB = location.latitude.degrees
        longB = location.longitude.degrees
        
        #Take elevation of point B as well
        elevB = location.elevation.km
        
        #Convert degress to radians for point A and point B
        radLatA = covert_degrees_radians(latA)
        radLongA = covert_degrees_radians(longA)
        radLatB = covert_degrees_radians(latB)
        radLongB = covert_degrees_radians(longB)
        
        #Write the position of ISS in the output.txt file in radians
        out_file.write(f"LatitudeA in Radians: {radLatA}, LongitudeA in Radians = {radLongA}\n")
        out_file.write(f"LatitudeB in Radians: {radLatB}, LongitudeB in Radians = {radLongB}\n")

        #Add total data collected for point A to the data.csv file
        data = idx, dt.now(), latB, longB, temperature, humidity, pressure, compass
        add_csv_data(data_file, data)

        #Measure the distance between points A and B in nautical miles using the harvesine formula:
        #informatin taken from https://www.youtube.com/watch?v=HaGj0DjX8W8
        distance = earth_rad*math.acos((math.sin(radLatA)*math.sin(radLatB))+
                                math.cos(radLatA)*math.cos(radLatB)*math.cos(radLongA-radLongB))
        
        #Convert nautical miles into km 
        #also take into consideration that earth rotates in the same direction with ISS
        #with the speed of 1670 km/hour
        distance = distance*1.853+abs(elevB-elevA)+(1670/3600)*wait_time
        
        #Estimate the speed my dividing distance interval with time interval (wait_time)
        #update the variable velocity and append the value to the velocityList
        velocity = distance/wait_time
        velocityList.append(velocity)
        
        #write the (intermediate) result to the output file
        out_file.write("distance =  %2.2f, velocity =  %2.2f\n" %(distance, velocity))
        
        #Capturing photo taking into consideration the limit of 42 pictures
        if (idx <= 42):
            custom_capture(ISS(), cam, base_folder, f"image{idx}.jpg")
            out_file.write(f"photo: image{idx}.jpg\n")
        idx += 1
        
        #capturing loop time and print the result to output.txt file
        now_time = dt.now()
        out_file.write(f"loop time = {now_time - loop_start_time}\n")
        out_file.write(f"{seperator * 60}\n")
        now_time = dt.now() #update the time
    except:
        out_file.write("An exception occured :( \n")
        now_time = dt.now() #update the time in case of an except occured to avoid an infinite loop
        
#sorting the velocityList and take the median by accessing the central element of the list
velocityList.sort()
estimate_kmps = velocityList[len(velocityList)//2]

#Write the result to the intermediate results output.txt file
out_file.write(f"Median Speed = {estimate_kmps}\n")

#Format the estimate speed value to 5 decimal places
estimate_kmps_formatted = "{:.5f}".format(estimate_kmps)

#Create a string to write to the file
velocity_string = estimate_kmps_formatted

#Set the result_file to "result.txt"
result_file = base_folder / "result.txt"

#Write the result to the result.txt file
with open(result_file, 'w') as file:
    file.write(f"{velocity_string}\n")

#Write the same result to the intermediate results output.txt file
out_file.write(f"Estimates Speed = {velocity_string}\n")

#Print the final message
print("Data written to", result_file)

#Write total execution time to the intermediate results output.txt file
out_file.write(f"total execution time: {dt.now() - start_time}")

#Close files: output.txt and result.txt
out_file.close()
file.close()

