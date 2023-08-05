pi-MCP4725
================

A Python module for the Raspberry Pi to interface with the [MCP4725](https://ww1.microchip.com/downloads/en/devicedoc/22039d.pdf) I²C Digital-to-Analogue Converter.

# Installation

## Compatibility

Tested on Python 3.9 on a Raspberry Pi Zero W v1.1, but should be compatible with most Raspberry Pi models running the latest version of Python.

Module works with Microchip's MCP4725 DAC.

## Pre-requisites

- `smbus2` library

	The MCP4725 module uses the Raspberry Pi's built-in I²C driver to communicate with the chip. This is done on Python using the SMBus protocol. However, due to SMBus incorporating only a subset of I²C features, it is not fully compatible with I²C commands. This is fixed by using `smbus2`, a drop-in replacement of the `smbus` module with extra functionality permitting the extra I²C features. It can be imported as `smbus` to be backward compatible. See below for more details.

	The module must be imported within the main code (it is not imported within the module).

## Install

The MCP4725 module can be installed by cloning the files into your project folder.

TO-DO: Add the module to PiPy for easier installation with pip.


# Usage Example

## Initialisation

The library and its pre-requisites must be imported first, and an SMBus object is created:

```python
import MCP4725
import smbus2 as smbus

BUS_No = 1

bus = smbus.SMBus(BUS_No)
```

A DAC can now be initialised using the MCP4725 class:

```python
# Default address for the MCP4725. Change as needed accordingly.
ADDRESS = 0X67

# Initialise MCP4725 object, providing the bus instance, device address and smbus module
dac = MCP4725.MCP4725(bus, ADDRESS, smbus)
```

(Note that the SMBus module is sent to the init. function as one of its structure classes is needed by the module)

## Setting the output voltage

To set the output voltage:

```python
V_DD = 5 		# Supply voltage of the chip

v_out = 2.5		# Desired output voltage (must be between 0 and V_DD)

dac_value = 4095 * v_out/V_DD	# The value must be between 0 and 4095 (i.e. 12 bits)

MCP4725.write(dac_value)		# Set the DAC output voltage
```

## Saving value to EEPROM

The DAC features an integrated EEPROM so that the requested voltage output persists through power cycles. To write to EEPROM:

```python
MCP4725.write(dac_value, True)
```

## Power down mode

The MCP4725 also features a power-down mode, which will disable the output voltage and instead connect the output to ground through a pre-set resistance. The available resistances are 1kOhm, 100kOhm and 500kOhm (see datasheet). To power up the device, simple write a voltage to it.

To power down the device:

```python
RESISTANCE = 100	# Set power down resistance to 100kOhm

# Power down the device
MCP4725.write(power_down=RESISTANCE)

# Power down device, and retain powered-down state through power cycles:
MCP4725.write(write_to_EEPROM=True, power_down=RESISTANCE)
```

Note that in both cases, a voltage value can be sent, but will have no effect given that the device will be powered down.

# To-do:

- [ ] Add module to PyPi
- [ ] Add logging to the library
- [ ] Add exception catching and set function to return a success flag
- [ ] Document I2C interface details