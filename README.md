# robotControl
some random python module to control my robot
# contents
* [usage](./README.md#usage)
* [movement controls](./README.md#movement-controls)
* [sensors](./README.md#sensors)
  * [switches](./README.md#switches)
  * [accelerometer](./README.md#accelerometer)
  * [gyroscope](./README.md#gyroscope)
  * [magnometer](./README.md#magnometer)

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
