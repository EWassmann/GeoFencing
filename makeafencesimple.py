# importing all of the needed packages
from shapely.geometry import Polygon, Point
import multiprocessing as mp
import serial
from ublox_gps import UbloxGps
import threading
import time
#setting up the port and baudrate for the gps (serial communications), baudrate is what sparkfun reccomended on github
port1 = serial.Serial('/dev/ttyACM1', baudrate=38400, timeout=1)
gps = UbloxGps(port1)
#initalizing the counter for the Geofence coordinats list as well as the Geofence coordinates list
counter = 0
Geofencecoordinates = list()

#setting up the serial communications with the arduino
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
#these are all the functions that write to the arduino that tell it to move, the numbers are sent as a 
#string and the arduino will decode them on that side
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
#this is the inital thread it is used to store the gps coordinates of a track the robot takes, and assighn them to a list containing tuples that 
#shapely can use
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
            #this breaks out of the function
        if stop():
            break
#starting the thread for creating the fence
stop_threads = False
t1 = threading.Thread(target = track, args = (lambda: stop_threads, ))
t1.start()
#this is the second thread it just keeps track of the robots positon so part two of the code can see if it is in or out of the fence

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
#loop for making the fence
while True:
    
        
    

    print("Use WASD to move, q to end program")


    directions = input()
    #stuff below is from keyboard controll it is looking for the inputs to run themovement functions from the top


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
    #q is gonna set the last point to the first point (shapely wants this) end the first thread and determine the center of the fence
    #center of the fence isnt used here but may be used in later iterations of this code
    if directions== "q":
        stop_threads = True
        Geofencecoordinates.insert(counter, Geofencecoordinates[0])
        #print(Geofencecoordinates)
        GeoFence = Polygon(Geofencecoordinates)
        cent = (GeoFence.centroid)
        print(cent)
        break
#starting the second thread
t2.start()
while True:
    #this allows  you to drive the robot around using wasd untill you exit the fence
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
        Stop()
    #this ends the threads and closes out the port
    if directions == "q":
            stop_threads2 = True
            port1.close()
            break   
    
    # if GeoFence.contains(RobotCoord) == True:
    #     print("inside")
    # else:
    #     print("outside")




