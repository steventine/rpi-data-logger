# rpi-data-logger
Project to record acceleration (using the Sense HAT) and video (using the Pi Camera)

To start at boot time, add the content in the rc.local file to the end of /etc/rc.local on the pi

The rc.local service looks to be configured out of the box. To validate run:

`systemctl list-units |grep rc`

output should look like: 
 `rc-local.service                         
    loaded active exited    /etc/rc.local Compatibility`


Some key info on recording the Pi Camera to a file is available [here](https://picamera.readthedocs.io/en/release-1.13/recipes1.html#recording-video-to-a-file)
