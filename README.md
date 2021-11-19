# G2VPico
Python API library for interaction with G2V Optics Pico

## Installation
```bash
pip install git+https://git@github.com/g2v-optics/G2VPico.git@main
```
## Examples
Example scripts are available in the _examples_ directory.  
Please note that the _examples_ directory will not be installed with the setup but can be downloaded through GitHub.

## Simple Demo
```python
from g2vpico import G2VPico
# Create a Pico instance using the IP address and the Pico ID assigned to the Pico

pico = G2VPico('192.168.1.70', '00000000c2ca735f')

# Get the number of channels avaialble
num_channels = pico.channel_count

# Turn channel 1 to a value of 50
pico.set_channel_value(1, 50)

# Read out the value of channel 5
pico.get_channel_value(5)
```

## g2vpico.MainClass module

### class g2vpico.MainClass.G2VPico(ip_address, pico_id)
Bases: `object`

A class used to represent a G2V Pico


### \__init__(ip_address, pico_id)
##### ARGS:
- `ip_address`: The IP address of the Pico on the network
- `pico_id`: The 16 character ID of the Pico

## PROPERTIES
### channel_count
The number of channels available in the Pico
##### RETURNS:
- `int`: The number of channels available
____

### channel_list
A list of the available channels in the Pico
##### RETURNS:
- `list`: List of channels with type `int`
____
### id
The ID of the Pico used to intialize the object
##### RETURNS:
- `str`: The ID of the Pico
____
## METHODS
### clear_channels()
Set all channels in the Pico to a value of 0
##### RETURNS:
- `bool`: True when all channels have been set to 0
____
### get_channel_limit(channel)
Returns the maximum limit [0-4096] of the channel.  This limit is the
maximum value that can be used when setting the channel value.
##### ARGS:
- `channel`: The channel number in the range [1, channel_count]

##### RETURNS:
- `int`: The maximum limit of the channel in the range [0, 4096]

##### EXCPETIONS:
- `ValueError`: Raised when the channel parameter is an invalid type
- `ValueError`: Raised when the channel is not in the range [0, channel_count]
____

### get_channel_value(channel)
Returns the current PWM value of the channel
##### ARGS:
- `channel`: The channel number in the range [1, channel_count]

##### RETURNS:
- `int`: The current value of the channel in the range [0, 4096]

##### EXCEPTIONS:
- `ValueError`: Raised when the channel parameter is an invalid type
____

### get_channel_wavelength_range(channel)
Returns the minimum and maximum wavelength values for a channel in nm
##### ARGS:
- `channel`: The channel number in the range [1, channel_count]

##### RETURNS:
- `list`: A list where index 0 is the minimum wavelength and index 1 is the maximum wavelength
    Units are nm

##### EXCEPTIONS:
- `ValueError`: Raised when the channel parameter is an invalid type
- `ValueError`: Raised when the channel is not in the range [0, channel_count]
____

### get_global_intensity()
Returns the global intensity that is applied to all channels
##### RETURNS:
- `float`: A value between 0.0 and 100.0 where 100.0 means all channels are fully on
    and a value of 0.0 means all channels are 0.
_____

### get_spectrum()
Get the current spectrum as a list of dict itmes
##### RETURNS:
- `list`: A list of dict items channel and value keys forming
    the current spectrum in the Pico.
____


### is_fixture_on()
Returns whether the fixture is on or off
##### RETURNS:
- `bool`: True if the fixture is on and False if the fixture is off
_____

### set_channel_value(channel, value)
Sets the chosen channel to the specified value.
##### ARGS:
- `channel`: The channel number in the range [1, channel_count]
- `value`: The value to set the chosen channel to in the range [0, channel_limit]

##### RETURNS:
- `bool`: True if the channel has been set to the new value and False if it has not changed

##### EXCEPTIONS:
- `ValueError`: Raised when the channel parameter is an invalid type
- `ValueError`: Raised when the channel is not in the range [0, channel_count]
- `ValueError`: Raised when the value parameter is an invalid type
_____

### set_global_intensity(value)
Sets the global intensity that is applied to all channels.
Note that the new global intensity will take effect immediately.
##### ARGS:
- `value`: The value of the new global intensity in the range [0.0, 100.0]

##### RETURNS:
- `bool`: True if the global intensity has been set successfully and False if not
_____

### set_spectrum(channel_list)
Load in a spectrum either as a json string or a dictionary.
Channels are changed individually so operation is not instantaneous.
##### ARGS:
- `channel_list`:
    - `str` - A JSON formatted string contain channels and their corresponding values
    - `list` - A list of dict objects containing ‘channel’ and ‘value’ keys

##### RETURNS:
- `bool`: True if the new spectrum has been loaded and False if not

##### EXCEPTIONS
- `ValueError`: If the spectrum data in channel_list is invalid when of str type
- `ValueError`: If the type of channel_list is invalid
- `ValueError`: Raised when the channel value is an invalid type
- `ValueError`: Raised when the channel is not in the range [0, channel_count]
_____

### turn_off()
Turns the fixture off while preserving channel values
##### RETURNS:
- `bool`: True if the fixture was turned off and False if the fixture failed to turn off
_____

### turn_on()
Turns the fixture on with previously stored spectrum
##### RETURNS:
- `bool`: True if the fixture was turned on and False if the fixture failed to turn on
_____
