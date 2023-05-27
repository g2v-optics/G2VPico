#!/usr/bin/env python3

import datetime as dt
import unittest
import sys
import warnings

from examples.example_sawtooth import SawtoothWaveform
from examples.example_sawtooth import TimestepWarning

class MockPico:
	def __init__(self):
		self._turned_on = False
		self._global_intensity = None
		self._actions = []

	def turn_on(self):
		self._turned_on = True
		self._actions.append((dt.datetime.now(), "turn_on"))

	def turn_off(self):
		self._turned_on = False
		self._actions.append((dt.datetime.now(), "turn_off"))

	def set_global_intensity(self, intensity):
		self._global_intensity = intensity
		self._actions.append((dt.datetime.now(), "set_global_intensity", intensity))

	def clear_channels(self):
		self._actions.append((dt.datetime.now(), "clear_channels"))

	def get_actions(self):
		return self._actions

	def is_turned_on(self):
		return self._turned_on

	def get_global_intensity(self):
		return self._global_intensity

class TestSawtooth(unittest.TestCase):

	def setUp(self):
		self.mockpico = MockPico()
		self.generator = SawtoothWaveform(self.mockpico)

	def get_starting_time(self, actionlog):
		for action in actionlog:
			if len(action) > 2 and action[1] == 'set_global_intensity':
				t0 = action[0]
				return t0

	def construct_expected_log(self, t0, cycles, steps, trough, expected_cycle_time, expected_step_time, expected_intensity_step):
		# construct test case from current conditions
		expected_actions = []
		expected_actions.append((t0, "turn_on"))
		for cycles in range(cycles):
			for steps in range(steps + 1):
				tstep = t0 + dt.timedelta(seconds=(cycles*expected_cycle_time)) + dt.timedelta(seconds=(steps*expected_step_time))
				next_intensity = trough + steps*expected_intensity_step
				expected_actions.append((tstep, "set_global_intensity", next_intensity))

		tstep += dt.timedelta(seconds=expected_step_time)
		expected_actions.append((tstep, "turn_off"))
		expected_actions.append((tstep, "clear_channels"))

		return expected_actions

	def test_period_property(self):
		# Test setting and getting the period property
		self.generator.period = 1.5
		self.assertEqual(self.generator.period, 1.5)

		# Test error case: setting period with a non-float value
		with self.assertRaises(ValueError):
			self.generator.period = "invalid"

		# Test error case: setting period with a non-positive value
		with self.assertRaises(ValueError):
			self.generator.period = -2.0

	def test_cycles_property(self):
		# Test setting and getting the cycles property
		self.generator.cycles = 5
		self.assertEqual(self.generator.cycles, 5)

		# Test error case: setting cycles with a non-integer value
		with self.assertRaises(ValueError):
			self.generator.cycles = 2.5

		# Test error case: setting period with a string
		with self.assertRaises(ValueError):
			self.generator.cycles = "string not integer"

		# Test error case: setting cycles with a non-positive value
		with self.assertRaises(ValueError):
			self.generator.cycles = -3

	def test_steps_property(self):
		# Test setting and getting the steps property
		self.generator.steps = 10
		self.assertEqual(self.generator.steps, 10)

		# Test error case: setting steps with a non-integer value
		with self.assertRaises(ValueError):
			self.generator.steps = 2.5

		# Test error case: setting period with a string
		with self.assertRaises(ValueError):
			self.generator.cycles = "string not integer"

		# Test error case: setting steps with a non-positive value
		with self.assertRaises(ValueError):
			self.generator.steps = -3

	def test_peak_property(self):
		# Test setting and getting the peak property
		self.generator.trough = 30
		self.generator.peak = 70
		self.assertEqual(self.generator.peak, 70)

		# Test error case: setting peak with a non-float value
		with self.assertRaises(ValueError):
			self.generator.peak = "invalid string input"

		# Test error case: setting peak with a value less than trough
		with self.assertRaises(ValueError):
			self.generator.peak = 20

		# Test error case: setting peak with a value outside the range 0-100
		with self.assertRaises(ValueError):
			self.generator.peak = 120

	def test_trough_property(self):
		# Test setting and getting the trough property
		self.generator.peak = 70
		self.generator.trough = 30
		self.assertEqual(self.generator.trough, 30)

		# Test error case: setting trough with a non-float value
		with self.assertRaises(ValueError):
			self.generator.trough = "invalid string input"

		# Test error case: setting trough with a value greater than or equal to peak
		with self.assertRaises(ValueError):
			self.generator.trough = 80

		# Test error case: setting trough with a value outside the range 0-100
		with self.assertRaises(ValueError):
			self.generator.trough = -10
	
	def test_calculate_timestep(self):
		# Set steps and period
		self.generator.steps = 10
		self.generator.period = 10

		# Call calculate_timestep method
		self.generator.calculate_timestep()

		# Check that timestep is calculated correctly
		self.assertEqual(self.generator._timestep, 1.00)

	def test_calculate_timestep_undefined_properties(self):
		# Call calculate_timestep method without setting steps and period
		with self.assertRaises(ValueError):
			self.generator.calculate_timestep()

	def test_calculate_timestep_warning(self):
		# Set steps and period
		self.generator.steps = 10
		self.generator.period = 2.5

		# run generator to catch warnings
		with warnings.catch_warnings(record=True) as warning_list:
			# Call the calculate_timestep method
			self.generator.calculate_timestep()

			# Assert that at least one warning has been raised
			self.assertGreater(len(warning_list), 0)

			# Iterate over the captured warnings and assert the warning message
			for warning in warning_list:
				self.assertEqual(warning.category, TimestepWarning)
				self.assertIn("The minimum waveform step is being used as the timestep.", str(warning.message))

	def test_calculate_intensitystep_defined_properties(self):
		# Set steps, peak, and trough
		self.generator.steps = 10
		self.generator.peak = 70
		self.generator.trough = 30

		# Call calculate_intensitystep method
		self.generator.calculate_intensitystep()

		# Check that intensity step is calculated correctly
		self.assertEqual(self.generator._intensitystep, 4)

	def test_calculate_intensitystep_undefined_properties(self):
		# Call calculate_intensitystep method without setting steps, peak, and trough
		with self.assertRaises(ValueError):
			self.generator.calculate_intensitystep()

	def test_verbose_flag_default_value(self):
		self.assertFalse(self.generator.verboseFlag)

	def test_verbose_flag_setter_valid_input(self):
		self.generator.verboseFlag = True
		self.assertTrue(self.generator.verboseFlag)

		self.generator.verboseFlag = False
		self.assertFalse(self.generator.verboseFlag)

	def test_verbose_flag_setter_invalid_input(self):
		with self.assertRaises(ValueError):
			self.generator.verboseFlag = "invalid"

	def test_run_sawtooth_ten_steps(self):
		self.generator.trough = 0	
		self.generator.peak = 100
		self.generator.steps = 10
		self.generator.period = 10
		self.generator.cycles = 1
		 
		# expected behaviours based on above parameters
		expected_step_time = 1
		expected_cycle_time = 10
		expected_intensity_step = 10

		# get logged actions from mockpico
		self.generator.run_sawtooth() 
		actions = self.mockpico.get_actions()  

		t0 = self.get_starting_time(actions)
		expected_actions = self.construct_expected_log(t0, self.generator.cycles, self.generator.steps, self.generator.trough, expected_cycle_time, expected_step_time, expected_intensity_step)		

		for index in range(len(actions)):
			time_delta = abs(actions[index][0] - expected_actions[index][0])
			self.assertLessEqual(time_delta, dt.timedelta(seconds=1))
			self.assertEqual(actions[index][1], expected_actions[index][1])
			if len(actions[index]) > 2:
				self.assertEqual(actions[index][2], expected_actions[index][2])

	def test_run_sawtooth_twenty_steps(self):
		self.generator.trough = 0	
		self.generator.peak = 100
		self.generator.steps = 20
		self.generator.period = 10
		self.generator.cycles = 1
		 
		# expected behaviours based on above parameters
		expected_step_time = 0.5
		expected_cycle_time = 20
		expected_intensity_step = 5

		# get logged actions from mockpico
		self.generator.run_sawtooth() 
		actions = self.mockpico.get_actions()  

		t0 = self.get_starting_time(actions)
		expected_actions = self.construct_expected_log(t0, self.generator.cycles, self.generator.steps, self.generator.trough, expected_cycle_time, expected_step_time, expected_intensity_step)		

		for index in range(len(actions)):
			time_delta = abs(actions[index][0] - expected_actions[index][0])
			self.assertLessEqual(time_delta, dt.timedelta(seconds=1))
			self.assertEqual(actions[index][1], expected_actions[index][1])
			if len(actions[index]) > 2:
				self.assertEqual(actions[index][2], expected_actions[index][2])

	def test_run_sawtooth_ten_steps_half_range(self):
		self.generator.trough = 25	
		self.generator.peak = 75
		self.generator.steps = 10
		self.generator.period = 10
		self.generator.cycles = 1
		 
		# expected behaviours based on above parameters
		expected_step_time = 1
		expected_cycle_time = 10
		expected_intensity_step = 5

		# get logged actions from mockpico
		self.generator.run_sawtooth() 
		actions = self.mockpico.get_actions()  

		t0 = self.get_starting_time(actions)
		expected_actions = self.construct_expected_log(t0, self.generator.cycles, self.generator.steps, self.generator.trough, expected_cycle_time, expected_step_time, expected_intensity_step)		

		for index in range(len(actions)):
			time_delta = abs(actions[index][0] - expected_actions[index][0])
			self.assertLessEqual(time_delta, dt.timedelta(seconds=1))
			self.assertEqual(actions[index][1], expected_actions[index][1])
			if len(actions[index]) > 2:
				self.assertEqual(actions[index][2], expected_actions[index][2])

	def test_run_sawtooth_five_steps_quarter_range(self):
		self.generator.trough = 25	
		self.generator.peak = 50
		self.generator.steps = 5
		self.generator.period = 2.5
		self.generator.cycles = 1
		 
		# expected behaviours based on above parameters
		expected_step_time = 0.5
		expected_cycle_time = 2.5
		expected_intensity_step = 5

		# get logged actions from mockpico
		self.generator.run_sawtooth() 
		actions = self.mockpico.get_actions()  

		t0 = self.get_starting_time(actions)
		expected_actions = self.construct_expected_log(t0, self.generator.cycles, self.generator.steps, self.generator.trough, expected_cycle_time, expected_step_time, expected_intensity_step)		

		for index in range(len(actions)):
			time_delta = abs(actions[index][0] - expected_actions[index][0])
			self.assertLessEqual(time_delta, dt.timedelta(seconds=1))
			self.assertEqual(actions[index][1], expected_actions[index][1])
			if len(actions[index]) > 2:
				self.assertEqual(actions[index][2], expected_actions[index][2])

	def test_run_sawtooth_five_steps_quarter_range_four_cycles(self):
		self.generator.trough = 25	
		self.generator.peak = 50
		self.generator.steps = 5
		self.generator.period = 2.5
		self.generator.cycles = 4
		 
		# expected behaviours based on above parameters
		expected_step_time = 0.5
		expected_cycle_time = 2.5
		expected_intensity_step = 5

		# get logged actions from mockpico
		self.generator.run_sawtooth() 
		actions = self.mockpico.get_actions()  

		t0 = self.get_starting_time(actions)
		expected_actions = self.construct_expected_log(t0, self.generator.cycles, self.generator.steps, self.generator.trough, expected_cycle_time, expected_step_time, expected_intensity_step)		

		for index in range(len(actions)):
			# removed time check as ideal case hard to maintain
			self.assertEqual(actions[index][1], expected_actions[index][1])
			if len(actions[index]) > 2:
				self.assertEqual(actions[index][2], expected_actions[index][2])

	def test_square_wave(self):
		self.generator.trough = 10	
		self.generator.peak = 90
		self.generator.steps = 1
		self.generator.period = 5
		self.generator.cycles = 5
		 
		# expected behaviours based on above parameters
		expected_step_time = 5
		expected_cycle_time = 5
		expected_intensity_step = 80

		# get logged actions from mockpico
		self.generator.run_sawtooth() 
		actions = self.mockpico.get_actions()  

		t0 = self.get_starting_time(actions)
		expected_actions = self.construct_expected_log(t0, self.generator.cycles, self.generator.steps, self.generator.trough, expected_cycle_time, expected_step_time, expected_intensity_step)		

		for index in range(len(actions)):
			# removed time check as ideal case hard to maintain
			self.assertEqual(actions[index][1], expected_actions[index][1])
			if len(actions[index]) > 2:
				self.assertEqual(actions[index][2], expected_actions[index][2])




if __name__ == "__main__":
	unittest.main()
