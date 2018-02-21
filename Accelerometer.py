# Hackathon 2017 Accelerometer Test Code
# Telerover Test Program
# SparkFun Triple Axis Accelerometer Breakout - MMA8452Q
# https://www.sparkfun.com/products/12756
# Steven Griset 09/13/2017


import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# MMA8452Q address, 0x1D(29)
# Select Control register, 0x2A(42)
#		0x00(00)	StandBy mode
bus.write_byte_data(0x1D, 0x2A, 0x00)
# MMA8452Q address, 0x1D(29)
# Select Control register, 0x2A(42)
#		0x01(01)	Active mode
bus.write_byte_data(0x1D, 0x2A, 0x01)
# MMA8452Q address, 0x1D(29)
# Select Configuration register, 0x0E(14)
#		0x00(00)	Set range to +/- 2g
bus.write_byte_data(0x1D, 0x0E, 0x00)

time.sleep(0.5)

# MMA8452Q address, 0x1D(29)
# Read data back from 0x00(0), 7 bytes
# Status register, X-Axis MSB, X-Axis LSB, Y-Axis MSB, Y-Axis LSB, Z-Axis MSB, Z-Axis LSB
data = bus.read_i2c_block_data(0x1D, 0x00, 7)

# Convert the data
xAccl = (data[1] * 256 + data[2]) / 16
if xAccl > 2047 :
	xAccl -= 4096

yAccl = (data[3] * 256 + data[4]) / 16
if yAccl > 2047 :
	yAccl -= 4096

zAccl = (data[5] * 256 + data[6]) / 16
if zAccl > 2047 :
	zAccl -= 4096

# Output data to screen
print "Acceleration in X-Axis : %d" %xAccl
print "Acceleration in Y-Axis : %d" %yAccl
print "Acceleration in Z-Axis : %d" %zAccl
