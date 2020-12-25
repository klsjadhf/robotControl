# module to send commands and receive data to robot via tcp

import socket
import math

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP_ADDR = "127.0.0.1"
TCP_PORT = 5005

debug = False   # put true to print debug message

def connect(ip="127.0.0.1", port=5005):
    if debug:
        print("connecting to", ip, ", port", port)
    s.settimeout(2) 
    try:
        s.connect((ip, port))
    except Exception as e:
        print("error connecting to ip", e)

def disconnect():
    if debug:
        print("disconnecting")
    s.close()

def receive(buf_Size=1024):
    try:
        data = s.recv(buf_Size)
        if debug:
            print("received", data)
        return data
    except:
        print("receive error")

def move(dir="stop", speed=0):
    # connect(IP_ADDR, TCP_PORT)
    if debug:
        print("dir:", dir, "\nspeed:", speed)

    #send movement or other commands
    if dir == "stop":
        s.send(b"S")
    elif dir == "fwd":
        s.send(b"F")
    elif dir == "back":
        s.send(b"B")
    elif dir == "left":
        s.send(b"L")
    elif dir == "right":
        s.send(b"R")
    else:
        s.send(dir.encode())
        
    receive()
    
    # s.send(str(speed).encode()) #change movement speed

    # disconnect()

def get_sensor(sensor):
    # connect(IP_ADDR, TCP_PORT)
    if debug:
        print("send", sensor.encode())
    s.send(sensor.encode())
    data = receive()
    # disconnect()
    return data

# returns sensor that detected collision
def col():
    sensor_array = ["front left", "front", "front right", "back"] #arrangement of sensors
    dir = get_sensor("C").decode().split()
    if debug:
        print("collision data:", dir)
    for i in zip(dir, sensor_array):
        if i[0] == '0':     # collision is 0, no collision is 1
            return i[1]
    return "none"

mag_x_max = 0
mag_x_min = 0
mag_y_max = 0
mag_y_min = 0

# larger is towards north
def angle():    # return degrees relative to north clockwise
    mag = get_sensor("M").decode().split()
    if debug:
        print(mag)
    x_ang = int(mag[0]) # x axis data
    x_ang = ((x_ang - mag_x_min)/(mag_x_max - mag_x_min) - 0.5)*2
    y_ang = int(mag[1]) # x axis data
    y_ang = ((y_ang - mag_y_min)/(mag_y_max - mag_y_min) - 0.5)*2
    ang = (math.atan2(y_ang,x_ang)*180/math.pi)
    if debug:
        print(x_ang,y_ang, ang)
    if y_ang < 0:
        return -ang
    else:
        return 360 - ang

# calibrate magnetnometer 
def cal_mag():
    global mag_x_max
    global mag_x_min
    global mag_y_max
    global mag_y_min
    mag = get_sensor("M").decode().split()
    mag_x_max = mag_x_min = int(mag[0])
    mag_y_max = mag_y_min = int(mag[1])
    for i in range(100):
        mag = get_sensor("M").decode().split()
        move("left")
        move("stop")
        if int(mag[0]) > mag_x_max:
            mag_x_max = int(mag[0])
        elif int(mag[0]) < mag_x_min:
            mag_x_min = int(mag[0])
        if int(mag[1]) > mag_y_max:
            mag_y_max = int(mag[1])
        elif int(mag[1]) < mag_y_min:
            mag_y_min = int(mag[1])
    if debug:
        print(mag_x_max, mag_x_min, mag_y_max, mag_y_min)

# turn number of degrees using gyro
# - is turn left, + is turn right
def turn(angle):
    s.send(b"q")    # clear turn angle
    receive()
    if angle < 0:
        while float(get_sensor("Q").decode()) > angle:
            if debug:
                print("sensor:", float(get_sensor("Q").decode()), "angle:", angle)
            move("left")
            move("stop")
    else:
        while float(get_sensor("Q").decode()) < angle:
            if debug:
                print("sensor:", float(get_sensor("Q").decode()), "angle:", angle)
            move("right")
            move("stop")

# move distance in meters + is foward - is backward
def travel(dist):
    s.send(b"d")    # clear distance
    receive()
    if dist < 0:
        while float(get_sensor("D").decode()) > dist:
            if debug:
                print("sensor:", float(get_sensor("D").decode()), "dist:", dist)
            move("back")
    else:
        while float(get_sensor("D").decode()) < dist:
            if debug:
                print("sensor:", float(get_sensor("D").decode()), "dist:", dist)
            move("fwd")
    move("stop")