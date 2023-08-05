# Author: Sergio Caponi
# A Python module for the Raspberry Pi to interface with the 
# MCP342x series of I²C Analogue-to-Digital Converters.
#
# v0.1



class MCP342x(object):

	# --- Define configuration bits ---

	_continous_mode = {0: 0b00000000,
					   1: 0b00010000}

	_channels = {1: 0b0000000, 
				 2: 0b0100000, 
				 3: 0b1000000, 
				 4: 0b1100000}

	_resolutions = {12: 0b0000,
					14: 0b0100,
					16: 0b1000,
					18: 0b1100}

	_gains = 	{1: 0b00,
				 2: 0b01,
				 4: 0b10,
				 8: 0b11}

	_conversion_times = {12: 1.0/240,
						 14: 1.0/60,
						 16: 1.0/15,
						 18: 1.0/3.75}

	_resolution_to_lsb = {12: 1000,
						  14: 250,
						  16: 62.5,
						  18: 15.625}

	# ---------------------------------

	# --- Default configuration -------

	contMode = 1
	ch = 1
	res = 12
	gain = 1 

	# ---------------------------------



	def __init__(self, bus, addr, smbuslib):
		self.bus = bus
		self.smbuslib = smbuslib
		self.addr = addr

	def write_config(self):
		""" Write configuration byte to the device """

		# Combine individual bits into single config byte using config bit definitions
		config = self._continous_mode[self.contMode] | self._channels[self.ch] | self._resolutions[self.res] | self._gains[self.gain]
		
		# Write config to device
		self.bus.write_byte(self.addr, config)


	def set_channel(self, channel, configureNow=False):
		""" Set the channel of the device"""

		if channel not in self._channels:
			raise Exception('Unknown channel')
		
		self.ch = channel

		if configureNow == True:
			self.write_config()
			
	def set_resolution(self, resolution, configureNow=False):
		""" Set the resolution of the device"""

		if resolution not in self._resolutions:
			raise Exception('Unknown resolution')
		
		self.res = resolution

		if configureNow == True:
			self.write_config()

	def set_gain(self, gain, configureNow=False):
		""" Set the PGA gain of the device"""

		if gain not in self._gains:
			raise Exception('Unknown gain')
		
		self.gain = gain

		if configureNow == True:
			self.write_config()

	def read(self):
		""" Read the current analogue to digital conversion stored in the device. This will either
		be the value converted within the last 1/SPS second timeframe in continuous mode or the value
		converted right after config. byte writing with RDY bit in one-shot mode. """


		# Set the received buffer length depending on whether the device is operating in 18-bit 
		# resolution mode or not. The buffer will be 3 bytes in 18-bit mode and 2 bytes in other modes
		# (see datasheet and documentation for details)
		buf_length = 3 if self.res == 18 else 2

		# Create the i2c message object using the smbus2 library. 
		# Add 1 to the buffer length to get the config byte as well.
		# This will be useful to check the RDY bit and to check 
		# whether the config is what we expected (functionalities to be added later)
		message = self.smbuslib.i2c_msg.read(self.addr, buf_length+1)

		# The actual read operation. The function uses pointers to save the
		# received buffer into message.buf[]
		self.bus.i2c_rdwr(message)
		raw_bytes = message.buf[:buf_length]

		#print(message.buf[buf_length]) # Debugging - print the config byte, which is the last byte of the buffer

		# Get value from the buffer bytes. "big" is used as the bytes 
		# are encoded with MSB at the start. The conversion is encoded
		# in two's complement, so we use "signed=True"
		conversion = int.from_bytes(raw_bytes, "big", signed=True)

		# Calculate voltage from the coded conversion using datsheet formula:
		# V[in uV] = code * (LSB_voltage / gain)
		voltage = conversion * self._resolution_to_lsb[self.res] / self.gain / 1000

		return voltage



