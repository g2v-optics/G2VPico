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
