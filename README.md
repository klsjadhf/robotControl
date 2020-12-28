# robotControl
some random python module to control my robot
# contents
* [usage](#usage)
* [movement controls](#movement-controls)
* [sensors](#sensors)
  * [switches](#switches)
  * [accelerometer](#accelerometer)
  * [gyroscope](#gyroscope)
  * [magnometer](#magnometer)

# usage
1. connect to server: `robotControl.connect(IP_ADDR, TCP_PORT)`
1. do stuff (move, read sensors, etc)
1. disconnect `robotControl.disconnect()`

# movement controls
`robotControl.move()`
input is string with one of the values: 
* "stop"
* "fwd"
* "back"
* "left"
* "right"  

no return value

`robotControl.turn()`
input is number of degrees to turn (float)  
positive is turn right, negative is turn left  
no return value  

`robotControl.travel()`
input is meters to move (float)    
positive is move foward, negative is move backwards  
no return value  

# sensors
`robotControl.get_sensor(sensor)`
input | sensor
------|-------
"A" | accelerometer
"T" | gyroscope
"M" | magnometer
"C" | switches  

returns byte array containing space seperated sensor values
## switches
`robotControl.col()`
no input
returns str with switch that detected collision
* "front left"
* "front"
* "front right"
* "back"
* "none"
## accelerometer
`robotControl.get_sensor("A")`
send "A" to `get_sensor()` method  
returns byte array b"x_data y_data z_data" 
## gyroscope
`robotControl.get_sensor("T")`
send "T" to `get_sensor()` method  
returns byte array b"x_data y_data z_data" 
## magnometer
calibrate magnometer first `robotControl.cal_mag()`
robot will turn about 2 times and get max and min values for gyro data  
use `robotControl.angle()` to get azimuth  
no input  
returns angle from north clockwise in degrees (north is 0, east is 90, south is 180, west is 270)  
