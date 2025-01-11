# Import the libraries
#https://missions.astro-pi.org/mz/code_submissions/new
from sense_hat import SenseHat
from time import sleep
sleeping_time = 0.5
# Set up the Sense HAT
sense = SenseHat()
sense.set_rotation(270, False)

# Set up the colour sensor
sense.color.gain = 60 # Set the sensitivity of the sensor
sense.color.integration_cycles = 64 # The interval at which the reading will be taken

# Add colour variables and image
def hex(string):
    if string[0] == "#":
        return (int(string[1:3], base = 16), int(string[3:5], base = 16), int(string[5:], base = 16))
        
gray = hex("#333333")
bg = hex("#87ceeb")
g = hex("#00aa00")
b = hex("#9b7653")
y = hex("#fbf719")
w = hex("#cccccc")
org = hex("#FF7400")
face_color = hex("#ffe536")
color_class = sense.color

color_rgb = (color_class.red, color_class.green, color_class.blue)
base_frame = [org, bg, bg, bg, bg, bg, bg, bg,
           bg, bg, bg, bg, bg, bg, bg, bg,
           bg, bg, bg, bg, bg, bg, bg, bg,
           bg, bg, bg, bg, bg, bg, bg, bg,
           bg, bg, bg, bg, bg, bg, bg, bg,
           bg, bg, bg, bg, bg, bg, bg, bg,
           bg, bg, bg, bg, bg, bg, bg, bg,
           b, b, b, b, b, b, b, b
          ]
face = [2, 2, 1, 1, 1, 1, 2, 2,
        2, 1, 1, 1, 1, 1, 1, 2,
        1, 1, 0, 1, 1, 0, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 0, 1, 1, 0, 1, 1,
        1, 1, 1, 0, 0, 1, 1, 1,
        2, 1, 1, 1, 1, 1, 1, 2,
        2, 2, 1, 1, 1, 1, 2, 2]


sense.set_pixels(base_frame)
sleep(sleeping_time)

frame = base_frame[:]


#----| 1 |--------------
frame[1] = org
frame[8] = org
frame[52] = g
sense.set_pixels(frame)
sleep(sleeping_time)

#-----| 2 |---------------------
frame[2] = org
frame[9] = org
frame[16] = org
frame[44] = g
sense.set_pixels(frame)
sleep(sleeping_time)

#-----| 3 |---------------
frame[8] = bg
frame[16] = bg
frame[43] = g
sense.set_pixels(frame)
sleep(sleeping_time)

#-----| 4 |-------------------
frame[3] = org
frame[10] = org
frame[18] = bg
frame[0] = bg
frame[9] = bg
frame[36] = g
sense.set_pixels(frame)
sleep(sleeping_time)

#-----| 5 |---------------------
frame[1] = bg
frame[4] = org
frame[10] = bg
frame[11] = org
frame[37] = g
sense.set_pixels(frame)
sleep(sleeping_time)

#-----| 6 |------------------
frame[5] = org
frame[11] = bg
frame[12] = org
frame[2] = bg
frame[10] = bg
frame[28] = g
sense.set_pixels(frame)
sleep(sleeping_time)

#-----| 7 |-------------------------
frame[6] = org
frame[3] = bg
frame[12] = bg
frame[13] = org
frame[20] = y
sense.set_pixels(frame)
sleep(sleeping_time)


#-----| 8 |---------------------------
frame[2] = bg
frame[11] = bg
frame[17] = bg
frame[4] = bg
frame[7] = org
frame[13] = bg
frame[14] = org
frame[20] = color_rgb # change color
frame[21] = y
frame[12] = y
frame[19] = y
frame[28] = y
sense.set_pixels(frame)
sleep(sleeping_time)


#-----| 9 |--------------------------------
frame[15] = org
frame[23] = org
frame[11] = y
frame[13] = y
frame[27] = y
frame[29] = y
sense.set_pixels(frame)
sleep(sleeping_time)

#-----| 10 |---------------------------
frame[5] = bg
frame[14] = bg
frame[23] = bg
frame[36] = y
frame[18] = y
frame[4] = y
frame[22] = y
sense.set_pixels(frame)
sleep(sleeping_time)


#-----| 11 |----------------------------
frame[6] = bg
frame[15] = bg
sense.set_pixels(frame)
sleep(sleeping_time)

#-----| 12 |-------------------------
frame[7] = bg
sense.set_pixels(frame)
sleep(sleeping_time)

#-----| 13 |--------------------------------
for idx, val in enumerate(frame):
    if val == bg:
        frame[idx] = gray
sense.set_pixels(frame)
sleep(sleeping_time)

#-----| 14 | ------------
frame = [gray for _ in range(64)]
    
sense.set_pixels(frame)
sleep(sleeping_time)

#-----| 15 |----------------
for idx, val in enumerate(face):
    if val == 0:
        frame[idx] = gray
    if val == 1:
        frame[idx] = face_color
    if val == 2:
        frame[idx] = bg

sense.set_pixels(frame)
sleep(sleeping_time)
