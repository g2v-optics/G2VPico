#!/usr/bin/env python3

'''
This example script shows how to get the current spectrum values of the Pico,
save the spectrum values into a file called example.json and then load in a
new test spectrum.
'''

import os
import time
import json
from g2vpico import G2VPico

PICO_ID = "00000000c2ca735f"

PICO_IP_ADDRESS = "192.168.1.69"

def main():
    ## Create an instance of the G2VPico
    pico = G2VPico(PICO_IP_ADDRESS, PICO_ID)

    print(str(pico))

    ## Ensure that the Pico is turned off
    pico.turn_off()

    ## Read out a list containing dict items corresponding to the spectrum
    spectrum_data = pico.get_spectrum()
    print("Current spectrum of Pico is {sd}".format(sd=spectrum_data))

    with open("example.json", 'w') as outfile:
        json.dump(spectrum_data, outfile, indent=4)
        print("Current spectrum saved to example.json")

    ## Open up example test spectrum
    if os.path.isfile("test_spectrum.json"):
        print("Loading in test spectrum")

        with open("test_spectrum.json", 'r') as infile:
            new_spectrum = json.load(infile)

    ## Load the spectrum into the Pico
    pico.set_spectrum(new_spectrum)
   

if __name__=="__main__":
    main()
