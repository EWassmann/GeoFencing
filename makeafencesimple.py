# from re import X
from shapely.geometry import Polygon, Point
import multiprocessing as mp
import serial
from ublox_gps import UbloxGps
import threading
import time
port1 = serial.Serial('/dev/ttyACM1', baudrate=38400, timeout=1)
gps = UbloxGps(port1)
counter = 0
Geofencecoordinates = list()

arduino = serial.Serial(
port = '/dev/ttyACM0',
baudrate = 2000000, #perhaps make this lower need to do research
bytesize = serial.EIGHTBITS,
parity = serial.PARITY_NONE,
stopbits = serial.STOPBITS_ONE,
timeout = 5,
xonxoff = False,
rtscts = False,
dsrdtr = False,
writeTimeout = 2
)

#----------------Functions---------------------------
def Left():
    arduino.write("1".encode()) 
    global b
    b = 1
def Forward():
    arduino.write("0".encode())
    global b
    b = 0
def Right():
    arduino.write("2".encode())
    global b
    b = 2
def Stop():
    arduino.write("4".encode())
    global b
    b = 4
def Back():
    arduino.write("3".encode())
    global b
    b = 3
def Search():
    arduino.write("5".encode())
    global b
    b = 5
def track(stop):
    print("Beginning to track")
    while True:
        try:
            global counter
            global Geofencecoordinates
            global geo
            geo = gps.geo_coords()
            x = geo.lon
            #print(x)
            y = geo.lat
            #print(y)
            Geofencecoordinates.insert(counter, (x,y))
            
            counter = counter + 1
        except (ValueError, IOError) as err:
            print(err)
        if stop():
            break
stop_threads = False
t1 = threading.Thread(target = track, args = (lambda: stop_threads, ))
t1.start()

def track2(stop2):
    print("Beginning to track")
    while True:
        try:
            
            global a
            global b
            #geo = gps.geo_coords()
            a = geo.lon
            #print(a)
            b = geo.lat
            #print(b)   
        except (ValueError, IOError) as err:
            print(err)
        if stop2():
            break
stop_threads2 = False
t2 = threading.Thread(target = track2, args = (lambda: stop_threads2, )) 

while True:
    
        
    

    print("Use WASD to move, q to end program")


    directions = input()


    if directions == "w":
        Forward()
    if directions == "a":
        Left()
    if directions =="d":
        Right()
    if directions == "s":
        Stop()
    if directions == "ss":
        Back() 
    if directions== "q":
        stop_threads = True
        Geofencecoordinates.insert(counter, Geofencecoordinates[0])
        #print(Geofencecoordinates)
        GeoFence = Polygon(Geofencecoordinates)
        cent = (GeoFence.centroid)
        print(cent)
        break

t2.start()
while True:
    directions = input()
    RobotCoord = Point(a,b)
    if GeoFence.contains(RobotCoord) == True:
        if directions == "w":
            Forward()
        if directions == "a":
            Left()
        if directions =="d":
            Right()
        if directions == "s":
            Stop()
        if directions == "ss":
            Back() 
    else:
        Back()
        time.sleep(4)
    
    if directions == "q":
            stop_threads2 = True
            break   
    
    # if GeoFence.contains(RobotCoord) == True:
    #     print("inside")
    # else:
    #     print("outside")




