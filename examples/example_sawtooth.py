#!/usr/bin/env python3

'''
This example script shows how to control the pico to produce a
sawtooth output
'''

import os
import json
import datetime as dt
from g2vpico import G2VPico

PICO_ID = "00000000c2ca735f"

PICO_IP_ADDRESS = "192.168.1.69"

WAVEFORM_PERIOD_SEC     = 5
WAVEFORM_CYCLES         = 5         # number of cycles to perform
WAVEFORM_STEPS          = 10        # number of steps per cycle

WAVEFORM_MIN_STEP       = 0.25      # minimum dwell time, seconds

WAVEFORM_MIN            = 60        # trough of waveform
WAVEFORM_MAX            = 90        # peak of waveform

def sawtooth(pico):
	''' function to run a sawtooth output on pico '''

	# calculate size of time step in seconds
	timestep = WAVEFORM_PERIOD_SEC/WAVEFORM_STEPS
	if timestep < WAVEFORM_MIN_STEP:
		timestep = WAVEFORM_MIN_STEP

	# calculate intensity rise per timestep
	delta_intensity = (WAVEFORM_MAX - WAVEFORM_MIN)/(WAVEFORM_STEPS)

	# turn on pico, set starting intensity
	pico.turn_on()
	print("Setting Pico global intensity to WAVEFORM_MIN: {0}".format(str(WAVEFORM_MIN)))
	pico.set_global_intensity(WAVEFORM_MIN)

	t0 = dt.datetime.now()

	verboseFlag = True

	try:
		# setup variables to track the loop
		cycle_count = 1
		step_count = 0
		time_next_action = t0 + dt.timedelta(seconds=timestep)		# set time to take next action

		# main loop code to change pico output
		while True:
			if (dt.datetime.now() >= time_next_action):
				# update time for next action
				time_next_action = time_next_action + dt.timedelta(seconds=timestep)

				if step_count > WAVEFORM_STEPS:
					cycle_count = cycle_count + 1
					if cycle_count > WAVEFORM_CYCLES:
						break
					step_count = 0
				else:
					step_count = step_count + 1

				next_intensity = WAVEFORM_MIN + step_count*delta_intensity
				pico.set_global_intensity(next_intensity)

				if verboseFlag:
					print("Time: {0} Cycle: {1} Step: {2} Next Intensity {3}".format(str(dt.datetime.now()), int(cycle_count), int(step_count), float(next_intensity)))

	except KeyboardInterrupt:
		print("Exiting script")
	except Exception as e:
		print("Unknown exception occurred - {e}".format(e=e))
	finally:
		print("Turning off the Pico")
		pico.turn_off()
		pico.clear_channels()

def main():
	## Create an instance of the G2VPico
	pico = G2VPico(PICO_IP_ADDRESS, PICO_ID)

	print(str(pico))

	pico.turn_off()

	if os.path.isfile("test_spectrum.json") is False:
		print("ERROR: Could not fine test_spectrum.json file")
		print("Exiting script")
	else:
		with open("test_spectrum.json", 'r') as infile:
			new_spectrum = json.load(infile)

		print("Setting Pico to use test spectrum")
		pico.set_spectrum(new_spectrum)
		
		sawtooth(pico)
		
  

if __name__=="__main__":
	main()