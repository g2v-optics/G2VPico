#!/usr/bin/env python3

import time
from g2vpico import G2VPico

PICO_ID = "00000000c2ca735f"

PICO_IP_ADDRESS = "192.168.1.70"

if __name__=="__main__":
    ## Create an instance of the G2VPico
    pico = G2VPico(PICO_IP_ADDRESS, PICO_ID)

    ## if the pico is already on, turn it off
    if pico.is_fixture_on():
        pico.turn_off()

    ## Go through each channel and set the value to 0
    for channel in pico.channel_list:
        pico.set_channel_value(channel, 0)

    ## Ensure that the gloabl intensity is set to 100%
    pico.set_global_intensity(100.0)

    ## Enable the light
    pico.turn_on()

    ## Go through each channel and change the value until the limit is reached
    ## Sleep for 10 ms between each change
    for channel in pico.channel_list:

        value = 0
        channel_limit = pico.get_channel_limit(channel)

        while value < channel_limit and value >= 0:
            pico.set_channel_value(channel, value)
            value += 1
            time.sleep(0.01)

        pico.set_channel_value(channel, 0)
