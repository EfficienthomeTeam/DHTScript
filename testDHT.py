import serial
import requests
import json
from time import sleep

ser = serial.Serial('/dev/ttyACM0', 9600)
url = 'http://ec2-52-59-230-221.eu-central-1.compute.amazonaws.com:3000/data'
headers = {'Content-Type': 'application/json'}
state = 'off'

while True:
    #Get mode
    try:
        rawCmd = requests.get(url).text
        cmds = [s for s in rawCmd.split()]
        mode = cmds[0]
        maxT = float(cmds[1])
        trgT = float(cmds[2])
        dltT = float(cmds[3])
    except:
        print("No connection on GET")
        mode = 'all'
        maxT = 30.0
        trgT = 10.0
        dltT = 2.0    
    #Get sensor data
    try:
        raw = ser.readline()
        sensors = [float(x) for x in raw.split()]
        internal = sensors[1:]
    except:
        print("Serial port error")
        continue
        
    #On/off heater    
    try:
        if mode == 'all':
            if all( [t <= trgT - dltT for t in internal] ):
                state = 'on'
            elif all ( [t >= trgT + dltT for t in internal] ):
                state = 'off'
            
        elif mode == '1' or '2' or '3':
            ind = int(mode)
            if (sensors[ind] <= trgT - dltT):
                state = 'on'
            elif (sensors[ind] >= trgT + dltT):
                state = 'off'
            
            #Safety check
            if any ( [t >= maxT for t in sensors] ):
                state = 'off'
                
            if state == 'on':
                ser.write('+'.encode())
            else:
                ser.write('-'.encode())
                
    except:
        print("Problem with temperature values")
            
    #Send data to server
    payload = {"data" : '"' + str(sensors) + ' ' + state + '"'}
    try:
        requests.post(url, data=json.dumps(payload), headers=headers)
    except:
        print("No connection on POST")

    try:
        print('')
        print('switch ',state)
        print('mode: ',mode)
        print('external temp: ', sensors[0])
        print('near water temp: ', sensors[1])
        print('on arduino temp: ', sensors[2])
        print('near top temp: ', sensors[3])
    except:
        print('problem to print status')

    sleep(10)