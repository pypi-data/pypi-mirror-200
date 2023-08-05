pi-MCP342x
================

A Python module for the Raspberry Pi to interface with the MCP342x series of I²C Analogue-to-Digital Converters. Currently only supports reading from the device in continuous conversion mode.

# Installation

## Compatibility

Tested on Python 3.9 on a Raspberry Pi Zero W v1.1, but should be compatible with most Raspberry Pi models running the latest version of Python.

### Compatible devices

Module works with all models the [MCP3422/3/4](https://ww1.microchip.com/downloads/en/devicedoc/22088c.pdf), 18-bit ADC series. Compatibility with the MCP3426/7/8 series is yet to be established.

Full list of compatible devices:

- MCP3422 (2 input channels)
- MCP3423 (2 input channels with address selection pins)
- MCP3424 (4 input channels with address selection pins)

## Pre-requisites

- `smbus2` library

	The MCP342x module uses the Raspberry Pi's built-in I²C driver to communicate with the chip. This is done on Python using the SMBus protocol. However, due to SMBus incorporating only a subset of I²C features, it is not fully compatible with the MCP342x series of devices. This module differs from other similar modules in its usage of the `smbus2`, a drop-in replacement of the `smbus` module with extra functionality permitting extra I²C features. It can be imported as `smbus` to be backward compatible. See below for more details.

	The module must be imported within the main code (it is not imported within the module).

## Install

The MCP342x module can be installed by cloning the files into your project folder.

TO-DO: Add the module to PiPy for easier installation with pip.


# Usage Example

## Initialisation

The library and its pre-requisites must be imported first, and an SMBus object is created:

```python
import MCP342x
import smbus2 as smbus

BUS_No = 1

bus = smbus.SMBus(BUS_No)
```

An ADC can now be initialised using the MCP342x class:

```python
# Default address for the MCP3422/3/4. Change as needed according to configuration pins.
ADDRESS = 0X68

# Initialise MCP342x object, providing the bus instance, device address and smbus module
adc = MCP342x.MCP342x(bus, ADDRESS, smbus)
```

(Note that the SMBus module is sent to the init. function as one of its structure classes is needed by the module)

## Configuring the ADC

The ADC can now be configured using the function below. Configuration bit details will be provided further down, but these are all managed by the module.

| Function									| Description											| Available parameters	|
| ---										| ---													| ---					|
| `set_channel(channel, configNow=False)`	| Set the channel to be read							| `1, 2` and for MCP3424 `3, 4`
| `set_resolution(res, configNow=False)`	| Set the sampling resolution (and thus sampling speed)	| `12, 14, 16, 18`			|
| `set_gain(gain, configNow=False)`			| Set the PGA gain										| `1, 2, 4, 8`			|
| `write_config()`							| Write the current configuration to the device			| N/A					|

The `configureNow` flag can be used to directly write the configuration to the ADC. By default, however, setting a config value will only save it in memory and the module will wait for the `send_config()` function to be called to write the config to the device itself.

### Examples:

To set adc to read from channel 4, with an 18-bit resolution and a gain of 2:

```python
adc.set_channel(2)
adc.set_resolution(18)
adc.set_gain(2)
adc.write_config()
```

To change the channel to 1 and gain to 8, while keeping an 18-bit res:

```python
adc.set_channel(1)
adc.set_gain(1, True)
# Setting the configNow flag to True here immediately 
# writes all previously set config values to the device
```

## Reading the analogue value

The MCP342x has a sample rate (samples per second, SPS) dependent on the resolution:

| Resolution	| Sample rate	|
| ---			| ---			|
| 12 bits		| 240 SPS		|
| 14 bits		| 60 SPS		|
| 16 bits		| 15 SPS		|
| 18 bits		| 3.75 SPS		|

Once the configuration is set, the user must thus wait 1/SPS seconds before reading from the device. In continuous conversion mode, the device will repeatedly sample at this frequency, updating its register every time.

To read the analogue output saved in the register, use the `read()` function:

```python
# Read analogue voltage input on channel 1,
# with a gain of 1 and resolution of 18 bits (Resolution of 15.625uV).
# The module handles all conversion and will divide by the amplification 
# to return the true input voltage.
voltage_in_mV = adc.read()

print(voltage_in_mV)
```

# To-do:

- [ ] Add module to PyPi
- [ ] Add logging  to the library
- [ ] Add exception catching and set functions to return a success flag
- [ ] Document I2C interface details
- [ ] Add RDY bit checking when reading analogue input
- [ ] Add code examples for reading multiple channels
- [ ] Check compatibility with MCP3426/7/8 series
- [ ] Add one-shot reading capability