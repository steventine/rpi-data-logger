from sense_hat import SenseHat
from picamera import PiCamera
from time import sleep
from time import time
from csv import writer
import math
import logging

def LED(Brightness):
    e = [Brightness, Brightness, Brightness]
    image = [
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e
    ]
    sense.set_pixels(image)

def LED_Indications(Color):
    sense.set_pixel(0,0, Color) #light up the top-right pixel to green, blue, or red to indicate success/failures

GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
NONE = (0, 0, 0)
REC_TIME_SEC = 60
SAMPLES_PER_SEC = 120
sense = SenseHat()
camera = PiCamera()
camera.rotation = 270

curr_time = time()

LED(255)
camera.resolution = (1280,720)
camera.framerate = 60  #15ms frames
camera.start_preview()
#Use this to convert to MP4 ffmpeg -framerate 60 -i video.h264  -c copy video5.mp4
try:
    camera.start_recording(f'video/{curr_time:.0f}.h264',format='h264',bitrate=2000000)
    LED_Indications(GREEN) #if the recording works, show green
except PiCameraError:
    LED_Indications(RED) #if the recording fails, show red


while True: #change conditional latter *****************
    start_time = time()
    end_time = start_time + REC_TIME_SEC
    blink_timer = 0

    with open(f'data/{curr_time:.0f}_data.csv', 'w', newline='') as f:
        data_writer = writer(f)
        data_writer.writerow(['Time','Accel X','Accel Y','Accel Z'])

        while (curr_time < end_time):
            #camera.annotate_text = "annotation #%s" % i
            raw = sense.get_accelerometer_raw()
            curr_time = time()
            camera.annotate_text = "Sec:{sec:.3f}".format(sec = (curr_time-start_time)) + " x: {x:.2f}, y: {y:.2f}, z: {z:.2f}".format(**raw)
            data_writer.writerow([round((curr_time-start_time), 3), round(raw["x"], 2), round(raw["y"], 2), round(raw["z"], 2)])
            if blink_timer >= 5:
                LED_Indications(GREEN)
                blink_timer = 0 #every five readings, blink a green LED
            else:
                LED_Indications(NONE) #turn off the green LED unless it is the fith reading
                blink_timer += 1
        camera.split_recording(f'video/{curr_time:.0f}.h264') #start recording in a new file
    
camera.stop_recording()
camera.stop_preview()
LED(0)