# G2VPico
Python API library for interaction with G2V Optics Pico

## Install
```bash
pip install git+ssh://git@github.com/g2v-optics/G2VPico.git@dev
```

## Simple Demo
```python
from g2vpico import G2VPico
# Create a Pico instance using the Pico ID and the IP address assigned to the Pico

pico = G2VPico('192.168.1.70', '00000000c2ca735f')

# Get the number of channels avaialble
pico.channel_count

# Turn channel 1 to a value of 50
pico.set_channel_value(1, 50)

# Read out the value of channel 5
pico.get_channel_value(5)
```

More demo scripts are available under the `Examples` directory.

## g2vpico.MainClass module

### class g2vpico.MainClass.G2VPico(ip_address, pico_id)
Bases: `object`

A class used to represent a G2V Pico


#### \__init__(ip_address, pico_id)
ip_address

    The IP address of the Pico on the network

pico_id

    The 16 character ID of the Pico


#### property channel_count()
The number of channels available in the Pico


#### property channel_list()
A list of the available channels in the Pico


#### clear_channels()
Set all channels in the Pico to a value of 0

bool

    True when all channels have been set to 0


#### get_channel_limit(channel)
Returns the maximum limit [0-4096] of the channel.

This limit is the maximum value that can be used when setting
The channel value.

channel

    The channel number in the range [1, channel_count]

int

    The maximum limit of the channel in the range [0, 4096]

ValueError

    Raised when the channel parameter is an invalid type

ValueError

    Raised when the channel is not in the range [0, channel_count]


#### get_channel_value(channel)
Returns the current PWM value of the channel

channel

    The channel number in the range [1, channel_count]

int

    The current value of the channel in the range [0, 4096]

ValueError

    Raised when the channel parameter is an invalid type


#### get_channel_wavelength_range(channel)
Returns the minimum and maximum wavelength values for a channel in nm

channel

    The channel number in the range [1, channel_count]

list

    A list where index 0 is the minimum wavelength and index 1 is the maximum wavelength
    Units are nm

ValueError

    Raised when the channel parameter is an invalid type

ValueError

    Raised when the channel is not in the range [0, channel_count]


#### get_global_intensity()
Returns the global intensity that is applied to all channels

float

    A value between 0.0 and 100.0 where 100.0 means all channels are fully on
    and a value of 0.0 means all channels are 0.


#### get_spectrum()
Get the current spectrum as a list of dict itmes

list

    A list of dict items channel and value keys forming
    the current spectrum in the Pico.


#### property id()
The ID of the Pico used to intialize the object


#### is_fixture_on()
Returns whether the fixture is on or off

bool :

    True if the fixture is on
    False if the fixture is off


#### set_channel_value(channel, value)
Sets the chosen channel to the specified value.

channel

    The channel number in the range [1, channel_count]

value

    The value to set the chosen channel to in the range [0, channel_limit]

bool

    True if the channel has been set to the new value
    False if the channel has not been changed

ValueError

    Raised when the channel parameter is an invalid type

ValueError

    Raised when the channel is not in the range [0, channel_count]

ValueError

    Raised when the value parameter is an invalid type


#### set_global_intensity(value)
Sets the global intensity that is applied to all channels.
Note that the new global intensity will take effect immediately.

value

    The value of the new global intensity in the range [0.0, 100.0]

bool

    True if the global intensity has been set successfully
    False if the global intensity was not changed


#### set_spectrum(channel_list)
Load in a spectrum either as a json string or a dictionary

channel_list

    str - A JSON formatted string contain channels and their corresponding values
    list - A list of dict objects containing ‘channel’ and ‘value’ keys

bool

    True if the new spectrum has been loaded

ValueError

    If the spectrum data in channel_list is invalid when of str type

ValueError

    If the type of channel_list is invalid

ValueError

    Raised when the channel value is an invalid type

ValueError

    Raised when the channel is not in the range [0, channel_count]


#### turn_off()
Turns the fixture off while preserving channel values

bool

    True if the fixture was turned off
    False if the fixture failed to turn off


#### turn_on()
Turns the fixture on with previously stored spectrum

bool

    True if the fixture was turned on and channels set to their value
    False if the fixture failed to turn on

## Module contents
