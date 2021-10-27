#!/usr/bin/env python3

'''

This example demonstrates how to loop through all channels in a Pico and increment
the channel value from 0 to the maximum limit of the channel.


'''

import time
from g2vpico import G2VPico

PICO_ID = "00000000c2ca735f"

PICO_IP_ADDRESS = "192.168.1.69"

def main():
    ## Create an instance of the G2VPico
    pico = G2VPico(PICO_IP_ADDRESS, PICO_ID)

    print(str(pico))

    ## if the pico is already on, turn it off
    if pico.is_fixture_on():
        print("Turning off Pico")
        pico.turn_off()

    ## Go through each channel and set the value to 0
    pico.clear_channels()

    print("Pico channels all set to 0")

    ## Ensure that the gloabl intensity is set to 100%
    pico.set_global_intensity(100.0)
    print("Pico global intensity set to 100.0%")

    ## Enable the light
    pico.turn_on()

    ## Go through each channel and change the value until the limit is reached
    ## Sleep for 10 ms between each change
    for channel in pico.channel_list:
        value = 0
        channel_limit = pico.get_channel_limit(channel)

        while value <= channel_limit and value >= 0:
            pico.set_channel_value(channel, value)
            print("Changing Pico channel {c} to value {v}".format(c=channel, v=value), end="\r")
            value += 10
            time.sleep(0.01)

        pico.set_channel_value(channel, 0)
        print("Finished going through channel {c}".format(c=channel))

    pico.turn_off()
    print("Turning off the Pico")

if __name__=="__main__":
    main()
