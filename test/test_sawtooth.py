#!/usr/bin/env python3

import unittest
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
		self._actions.append("turn_on")

	def turn_off(self):
		self._turned_on = False
		self._actions.append("turn_off")

	def set_global_intensity(self, intensity):
		self._global_intensity = intensity
		self._actions.append(("set_global_intensity", intensity))

	def clear_channels(self):
		self._actions.append("clear_channels")

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


if __name__ == "__main__":
	unittest.main()
