# This work is licensed under the MIT license.
# Copyright (c) 2013-2023 OpenMV LLC. All rights reserved.
# https://github.com/openmv/openmv/blob/master/LICENSE
#
# AprilTags Example
#
# This example shows the power of the OpenMV Cam to detect April Tags
# on the OpenMV Cam M7. The M4 versions cannot detect April Tags.

import sensor
import time
import math
from machine import PWM, Pin

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
clock = time.clock()


########################### OUTPUT SETUP ############################
pwm = PWM('P7', freq=50, duty_u16=8192)  # create a PWM object on a pin
rightEN = Pin('P8', Pin.OUT)
leftEN = Pin('P9', Pin.OUT)
#####################################################################

# c_x is the image x center position in pixels.
# c_y is the image y center position in pixels.

f_x = (2.8 / 3.984) * 160  # find_apriltags defaults to this if not set
f_y = (2.8 / 2.952) * 120  # find_apriltags defaults to this if not set
c_x = 160 * 0.5  # find_apriltags defaults to this if not set (the image.w * 0.5)
c_y = 120 * 0.5  # find_apriltags defaults to this if not set (the image.h * 0.5)




def degrees(radians):
    return (180 * radians) / math.pi


Kp = 65535 / 20     # Control Constant
Kd = 65535 / 30

motorControl = 0
error = 0
prevError = 0
reset = 0

while True:
    clock.tick()
    img = sensor.snapshot()

    reset += 1

    if reset >= 10:
        motorControl = max(0, motorControl - 1000)
    
    # Loop if tag is detected
    for tag in img.find_apriltags(fx=f_x, fy=f_y, cx=c_x, cy=c_y):  # defaults to TAG36H11
        
        reset = 0
        
        img.draw_rectangle(tag.rect, color=(255, 0, 0))
        img.draw_cross(tag.cx, tag.cy, color=(0, 255, 0))
        print_args = (
            tag.x_translation,
            tag.y_translation,
            tag.z_translation,
            degrees(tag.x_rotation),
            degrees(tag.y_rotation),
            degrees(tag.z_rotation),
        )
        # Translation units are unknown. Rotation units are in degrees.
        # print("Tx: %f, Ty %f, Tz %f, Rx %f, Ry %f, Rz %f" % print_args)
        print(f'Z coordinate: {tag.z_translation}')
        
        # prevError = error
        error = 0 - tag.z_translation

        # derivative = error - prevError

        # motorControl = abs(int(Kp * error + Kd * derivative))
        motorControl = abs(int(Kp * error))
        
        if error >= 0:
            leftEN.on()
            rightEN.off()
        elif error <= 0:
            leftEN.off()
            rightEN.on()
        
    pwm.duty_u16(motorControl)
    
    print(motorControl)

    # print(clock.fps())