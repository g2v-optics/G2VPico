#!/usr/bin/env python3

import os
import time
import json
import datetime as dt
from g2vpico import G2VPico

PICO_ID = "00000000c2ca735f"

PICO_IP_ADDRESS = "192.168.1.69"

SPECTRUM_PERIOD_SEC = 5

def main():
    ## Create an instance of the G2VPico
    pico = G2VPico(PICO_IP_ADDRESS, PICO_ID)

    print(str(pico))

    spectrum_check_time = dt.datetime.now()

    pico.turn_off()

    if os.path.isfile("am1.5.json") is False:
        print("ERROR: Could not fine am1.5.json file")
        print("Exiting script")
    else:
        with open("am1.5.json", 'r') as infile:
            new_spectrum = json.load(infile)

        print("Setting Pico to use am1.5 spectrum")
        pico.set_spectrum(new_spectrum)
        
        print("Setting Pico global intensity to 100.0%")
        pico.set_global_intensity(100.0)

        try:
            while True:
                if (dt.datetime.now() >= (spectrum_check_time + dt.timedelta(seconds=SPECTRUM_PERIOD_SEC))):
                    spectrum_check_time = dt.datetime.now()
                    if pico.is_fixture_on():
                        print("{dt} Turning Pico Off".format(dt=spectrum_check_time))
                        pico.turn_off()
                    else:
                        print("{dt} Turning Pico On".format(dt=spectrum_check_time))
                        pico.turn_on()

        except KeyboardInterrupt:
            print("Exiting script")
        except Exception as e:
            print("Unknown exception occurred - {e}".format(e=e))
        finally:
            print("Turning off the Pico")
            pico.turn_off()
            pico.clear_channels()
  

if __name__=="__main__":
    main()
