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


<main>

<article id="content">

<header>

# Module G2VPico

</header>

<nav id="sidebar">

# Index

*   ### [Classes](#header-classes)

    *   #### [G2VPico](#g2vpico.G2VPico "g2vpico.G2VPico")

        *   [channel_count](#g2vpico.G2VPico.channel_count "g2vpico.G2VPico.channel_count")
        *   [channel_list](#g2vpico.G2VPico.channel_list "g2vpico.G2VPico.channel_list")
        *   [clear_channels](#g2vpico.G2VPico.clear_channels "g2vpico.G2VPico.clear_channels")
        *   [get_channel_limit](#g2vpico.G2VPico.get_channel_limit "g2vpico.G2VPico.get_channel_limit")
        *   [get_channel_value](#g2vpico.G2VPico.get_channel_value "g2vpico.G2VPico.get_channel_value")
        *   [get_channel_wavelength_range](#g2vpico.G2VPico.get_channel_wavelength_range "g2vpico.G2VPico.get_channel_wavelength_range")
        *   [get_global_intensity](#g2vpico.G2VPico.get_global_intensity "g2vpico.G2VPico.get_global_intensity")
        *   [get_spectrum](#g2vpico.G2VPico.get_spectrum "g2vpico.G2VPico.get_spectrum")
        *   [id](#g2vpico.G2VPico.id "g2vpico.G2VPico.id")
        *   [is_fixture_on](#g2vpico.G2VPico.is_fixture_on "g2vpico.G2VPico.is_fixture_on")
        *   [set_channel_value](#g2vpico.G2VPico.set_channel_value "g2vpico.G2VPico.set_channel_value")
        *   [set_global_intensity](#g2vpico.G2VPico.set_global_intensity "g2vpico.G2VPico.set_global_intensity")
        *   [set_spectrum](#g2vpico.G2VPico.set_spectrum "g2vpico.G2VPico.set_spectrum")
        *   [turn_off](#g2vpico.G2VPico.turn_off "g2vpico.G2VPico.turn_off")
        *   [turn_on](#g2vpico.G2VPico.turn_on "g2vpico.G2VPico.turn_on")

</nav>

<section>

## Classes

<dl>

<dt id="G2VPico.G2VPico"><span>class <span class="ident">G2VPico</span></span> <span>(</span><span>ip_address, pico_id)</span></dt>

<dd>

<div class="desc">

A class used to represent a G2V Pico

## Parameters

<dl>

<dt>ip_addres : str</dt>

<dd>The IP address of the Pico on the network</dd>

<dt>pico_id : str</dt>

<dd>The 16 character ID of the Pico</dd>

</dl>

</div>

### Instance variables

<dl>

<dt id="g2vpico.G2VPico.channel_count">var <span class="ident">channel_count</span></dt>

<dd>

<div class="desc">

The number of channels available in the Pico

</div>

</dd>

<dt id="g2vpico.G2VPico.channel_list">var <span class="ident">channel_list</span></dt>

<dd>

<div class="desc">

A list of the available channels in the Pico

</div>

</dd>

<dt id="g2vpico.G2VPico.id">var <span class="ident">id</span></dt>

<dd>

<div class="desc">

The ID of the Pico used to intialize the object

</div>

</dd>

</dl>

### Methods

<dl>

<dt id="g2vpico.G2VPico.clear_channels"><span>def <span class="ident">clear_channels</span></span>(<span>self)</span></dt>

<dd>

<div class="desc">

Set all channels in the Pico to a value of 0

## Returns

<dl>

<dt>bool</dt>

<dd>True when all channels have been set to 0</dd>

</dl>

</div>

</dd>

<dt id="g2vpico.G2VPico.get_channel_limit"><span>def <span class="ident">get_channel_limit</span></span>(<span>self, channel)</span></dt>

<dd>

<div class="desc">

Returns the maximum limit [0-4096] of the channel.

This limit is the maximum value that can be used when setting The channel value.

## Parameters

<dl>

<dt>channel : str, int</dt>

<dd>The channel number in the range [1, channel_count]</dd>

</dl>

## Returns

<dl>

<dt>int</dt>

<dd>The maximum limit of the channel in the range [0, 4096]</dd>

</dl>

## Exceptions

ValueError Raised when the channel parameter is an invalid type

ValueError Raised when the channel is not in the range [0, channel_count]

</div>

</dd>

<dt id="g2vpico.G2VPico.get_channel_value"><span>def <span class="ident">get_channel_value</span></span>(<span>self, channel)</span></dt>

<dd>

<div class="desc">

Returns the current PWM value of the channel

## Parameters

<dl>

<dt>channel : str, int</dt>

<dd>The channel number in the range [1, channel_count]</dd>

</dl>

## Returns

<dl>

<dt>int</dt>

<dd>The current value of the channel in the range [0, 4096]</dd>

</dl>

## Exceptions

ValueError Raised when the channel parameter is an invalid type

</div>

</dd>

<dt id="g2vpico.G2VPico.get_channel_wavelength_range"><span>def <span class="ident">get_channel_wavelength_range</span></span>(<span>self, channel)</span></dt>

<dd>

<div class="desc">

Returns the minimum and maximum wavelength values for a channel in nm

## Parameters

<dl>

<dt>channel : str, int</dt>

<dd>The channel number in the range [1, channel_count]</dd>

</dl>

## Returns

[] A list where index 0 is the minimum wavelength and index 1 is the maximum wavelength Units are nm

## Exceptions

ValueError Raised when the channel parameter is an invalid type

ValueError Raised when the channel is not in the range [0, channel_count]

</div>

</dd>

<dt id="g2vpico.G2VPico.get_global_intensity"><span>def <span class="ident">get_global_intensity</span></span>(<span>self)</span></dt>

<dd>

<div class="desc">

Returns the global intensity that is applied to all channels

## Returns

<dl>

<dt>float</dt>

<dd>A value between 0.0 and 100.0 where 100.0 means all channels are fully on and a value of 0.0 means all channels are 0.</dd>

</dl>

</div>

</dd>

<dt id="g2vpico.G2VPico.get_spectrum"><span>def <span class="ident">get_spectrum</span></span>(<span>self)</span></dt>

<dd>

<div class="desc">

Get the current spectrum as a JSON string

## Returns

<dl>

<dt>str</dt>

<dd>A JSON formatted string containing channel and value information forming the current spectrum in the Pico.</dd>

</dl>

</div>

</dd>

<dt id="g2vpico.G2VPico.is_fixture_on"><span>def <span class="ident">is_fixture_on</span></span>(<span>self)</span></dt>

<dd>

<div class="desc">

Returns whether the fixture is on or off

## Returns

<dl>

<dt>bool</dt>

<dd>True if the fixture is on False if the fixture is off</dd>

</dl>

</div>

</dd>

<dt id="g2vpico.G2VPico.set_channel_value"><span>def <span class="ident">set_channel_value</span></span>(<span>self, channel, value)</span></dt>

<dd>

<div class="desc">

Sets the chosen channel to the specified value.

## Parameters

<dl>

<dt>channel : str, int</dt>

<dd>The channel number in the range [1, channel_count]</dd>

<dt>value : str, int, float</dt>

<dd>The value to set the chosen channel to in the range [0, channel_limit]</dd>

</dl>

## Returns

<dl>

<dt>bool</dt>

<dd>True if the channel has been set to the new value False if the channel has not been changed</dd>

</dl>

## Exceptions

ValueError Raised when the channel parameter is an invalid type

ValueError Raised when the channel is not in the range [0, channel_count]

ValueError Raised when the value parameter is an invalid type

</div>

</dd>

<dt id="g2vpico.G2VPico.set_global_intensity"><span>def <span class="ident">set_global_intensity</span></span>(<span>self, value)</span></dt>

<dd>

<div class="desc">

Sets the global intensity that is applied to all channels. Note that the new global intensity will take effect immediately.

## Parameters

<dl>

<dt>value : float</dt>

<dd>The value of the new global intensity in the range [0.0, 100.0]</dd>

</dl>

## Returns

<dl>

<dt>bool</dt>

<dd>True if the global intensity has been set successfully False if the global intensity was not changed</dd>

</dl>

</div>

</dd>

<dt id="g2vpico.G2VPico.set_spectrum"><span>def <span class="ident">set_spectrum</span></span>(<span>self, channel_list)</span></dt>

<dd>

<div class="desc">

Load in a spectrum either as a json string or a dictionary

## Parameters

<dl>

<dt>channel_list : str, list</dt>

<dd>str - A JSON formatted string contain channels and their corresponding values list - A list of dict objects containing 'channel' and 'value' keys</dd>

</dl>

## Returns

<dl>

<dt>bool</dt>

<dd>True if the new spectrum has been loaded</dd>

</dl>

## Exceptions

ValueError If the spectrum data in channel_list is invalid when of str type

ValueError If the type of channel_list is invalid

ValueError Raised when the channel value is an invalid type

ValueError Raised when the channel is not in the range [0, channel_count]

</div>

</dd>

<dt id="g2vpico.G2VPico.turn_off"><span>def <span class="ident">turn_off</span></span>(<span>self)</span></dt>

<dd>

<div class="desc">

Turns the fixture off while preserving channel values

## Returns

<dl>

<dt>bool</dt>

<dd>True if the fixture was turned off False if the fixture failed to turn off</dd>

</dl>

</div>

</dd>

<dt id="g2vpico.G2VPico.turn_on"><span>def <span class="ident">turn_on</span></span>(<span>self)</span></dt>

<dd>

<div class="desc">

Turns the fixture on with previously stored spectrum

## Returns

<dl>

<dt>bool</dt>

<dd>True if the fixture was turned on and channels set to their value False if the fixture failed to turn on</dd>

</dl>

</div>

</dd>

</dl>

</dd>

</dl>

</section>

</article>


</main>
