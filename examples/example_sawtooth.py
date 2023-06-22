#!/usr/bin/env python3

'''
This example script shows how to control the pico to produce a
sawtooth output
'''

import datetime as dt
import json
import sys
import warnings
import os

from g2vpico import G2VPico

PICO_ID                 = "00000000c2ca735f"
PICO_IP_ADDRESS         = "192.168.1.69"

class TimestepWarning(UserWarning):
    pass

class IntensityWarning(UserWarning):
    pass

class SawtoothWaveform():
    ''' class to run a sawtooth on a pico '''

    def __init__(self, picoobj):

        self._waveform_minimum_step = 0.25  # minimum dwell time

        self._period = None
        self._cycles = None
        self._steps = None
        self._peak = None
        self._trough = None

        self._timestep = None
        self._intensitystep = None

        self._verboseFlag = False

        self.cycle_count = 1
        self.step_count = 0

        self.pico = picoobj
        
    @property
    def period(self):
        return self._period

    @period.setter
    def period(self, value):
        try:
            value = float(value)
        except (ValueError, TypeError) as e:
            raise ValueError("Peak must be a numerical value.") from e

        if value <= 0:
            raise ValueError("Period must be greater than zero.")
        self._period = value
        
    @property
    def cycles(self):
        return self._cycles

    @cycles.setter
    def cycles(self, value):
        if not isinstance(value, int):
            raise ValueError("Cycles must be an integer.")
        if value <= 0:
            raise ValueError("Cycles must be greater than zero.")
        self._cycles = value

    @property
    def steps(self):
        return self._steps

    @steps.setter
    def steps(self, value):
        if not isinstance(value, int):
            raise ValueError("Steps must be an integer.")
        if value <= 0:
            raise ValueError("Steps must be greater than zero.")
        self._steps = value

    @property
    def peak(self):
        return self._peak

    @peak.setter
    def peak(self, value):
        try:
            value = float(value)
        except (ValueError, TypeError) as e:
            raise ValueError("Peak must be a numerical value.") from e

        if value < 0 or value > 100:
            raise ValueError("Peak must be between 0 and 100.")
        if self._trough is not None and value <= self._trough:
            raise ValueError("Peak must be greater than trough.")
        self._peak = value

    @property
    def trough(self):
        return self._trough

    @trough.setter
    def trough(self, value):
        try:
            value = float(value)
        except (ValueError, TypeError) as e:
            raise ValueError("Peak must be a numerical value.") from e

        if value < 0 or value > 100:
            raise ValueError("Trough must be between 0 and 100.")
        if self._peak is not None and value >= self._peak:
            raise ValueError("Trough must be less than peak.")
        self._trough = value

    @property
    def timestep(self):
        return self._timestep

    @property
    def verboseFlag(self):
        return self._verboseFlag

    @verboseFlag.setter
    def verboseFlag(self, value):
        if isinstance(value, bool):
            self._verboseFlag = value
        else:
            raise ValueError("verboseFlag must be a boolean value.")
    
    def calculate_timestep(self):
        ''' method to calculate timestep '''
        if self._steps is None:
            raise ValueError("Cannot calculate timestep as number of steps is not defined.")
        if self._period is None:
            raise ValueError("Cannot calculate timestep as period is not defined.")

        timestep = self._period / self._steps
        self._timestep = max(timestep, self._waveform_minimum_step)

        if self._timestep == self._waveform_minimum_step:
            warnings.warn("The minimum waveform step is being used as the timestep.", TimestepWarning)

    def calculate_intensitystep(self):
        if self._steps is None:
            raise ValueError("Cannot calculate intensity step as number of steps is not defined.")
        if self._peak is None:
            raise ValueError("Cannot calculate intensity step as waveform peak is not defined.")
        if self._trough is None:
            raise ValueError("Cannot calculate intensity step as waveform trough is not defined.")

        intensity_range = self._peak - self._trough
        self._intensitystep = intensity_range / self._steps

    def run_sawtooth(self):
        if self._steps is None:
            raise ValueError("Cannot run sawtooth waveform as number of steps is not defined.")
        if self._peak is None:
            raise ValueError("Cannot run sawtooth waveform as waveform peak is not defined.")
        if self._trough is None:
            raise ValueError("Cannot run sawtooth waveform as waveform trough is not defined.")
        if self._period is None:
            raise ValueError("Cannot run sawtooth waveform as waveform period is not defined.")

        # make sure parameters are up to date
        self.calculate_timestep()
        self.calculate_intensitystep()

        self.pico.turn_on()
        self.pico.set_global_intensity(self._trough)
        if self.verboseFlag: 
            print(f"Setting Pico global intensity to {self._trough}")
        
        t0 = dt.datetime.now()

        try:
            time_next_action = t0 + dt.timedelta(seconds=self._timestep)

            while True:
                if dt.datetime.now() >= time_next_action:
                    time_next_action = time_next_action + dt.timedelta(seconds=self._timestep)

                    if self.step_count > (self._steps - 1):
                        if self.verboseFlag:
                            print(f"Cycle {self.cycle_count} completed")
                        self.cycle_count += 1
                        if self.cycle_count > self._cycles:
                            break
                        self.step_count = 0
                    else:
                        self.step_count += 1

                    next_intensity = self._trough + self.step_count * self._intensitystep
                    if next_intensity > 100:
                        warnings.warn("Sawtooth tried to write global intensity above 100.", IntensityWarning)
                        next_intensity = 100

                    self.pico.set_global_intensity(next_intensity)
                    if self.verboseFlag:
                        print(f"Time: {dt.datetime.now()} Cycle: {self.cycle_count} Step: {self.step_count} Next Intensity: {next_intensity}")

        except KeyboardInterrupt:
            print("Keyboard Interrupt Caught - Exiting script")
        except Exception as e:
            print(f"Unknown exception occurred - {e}")
        finally:
            if self.verboseFlag:
                print("Setting Pico to zero spectrum")
            self.pico.turn_off()
            self.pico.clear_channels()

if __name__=="__main__":

    # create a pico object, make sure it is turned off
    pico = G2VPico(PICO_IP_ADDRESS, PICO_ID)
    pico.turn_off()
    pico.clear_channels()

    if os.path.isfile("test_spectrum.json") is False:
        print("ERROR: Could not find test_spectrum.json file")
        print("Exiting script")
    else:
        with open("test_spectrum.json", 'r') as infile:
            new_spectrum = json.load(infile)

        print("Setting Pico to use test spectrum")
        pico.set_spectrum(new_spectrum)

        waveformgenerator = SawtoothWaveform(pico)      # create sawtooth generator with pico object
        waveformgenerator.verboseFlag = True

        # Adjust these paramters to change waveform
        waveformgenerator.period = 5                    # period of waveform in seconds         
        waveformgenerator.cycles = 5                    # number of cycles to perform
        waveformgenerator.steps = 5                     # number of steps per cycle 
        waveformgenerator.trough = 60                   # trough of waveform, in % global intensity
        waveformgenerator.peak = 90                     # peak of waveform, in % global intensity

        waveformgenerator.run_sawtooth()

    sys.exit(0)
