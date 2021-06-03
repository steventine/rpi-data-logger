from sense_hat import SenseHat
from picamera import PiCamera
from time import sleep
from time import time
from csv import writer
import math

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


REC_TIME_SEC = 20
SAMPLES_PER_SEC = 120
sense = SenseHat()
camera = PiCamera()
camera.rotation = 270

with open('data.csv', 'w', newline='') as f:
    data_writer = writer(f)
    data_writer.writerow(['Time','Accel X','Accel Y','Accel Z'])

    LED(255)
    camera.resolution = (1280,720)
    camera.framerate = 60  #15ms frames
    camera.start_preview()
    #Use this to convert to MP4 ffmpeg -framerate 60 -i video.h264  -c copy video5.mp4
    camera.start_recording('/home/pi/Desktop/video.h264',format='h264',bitrate=2000000)
    start_time = time()
    end_time = start_time + REC_TIME_SEC
    curr_time = 0
    while (curr_time < end_time):
        #camera.annotate_text = "annotation #%s" % i
        raw = sense.get_accelerometer_raw()
        curr_time = time()
        camera.annotate_text = "Sec:{sec:.3f}".format(sec = (curr_time-start_time)) + " x: {x:.2f}, y: {y:.2f}, z: {z:.2f}".format(**raw)
        stephen = raw["x"]
        data_writer.writerow([round((curr_time-start_time), 3), round(raw["x"], 2), round(raw["y"], 2), round(raw["z"], 2)])
    camera.stop_recording()
    camera.stop_preview()
    LED(0)