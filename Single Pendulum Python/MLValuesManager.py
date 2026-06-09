#!/usr/bin/env python3

import tkinter as tk
import MLValue as mlv
class ValuesManager:
	def __init__(self, values: list = None):
		self.values = values if values is not None else []
	def append(self, value):
		self.values.append(value)
	def display(self, parent):
		frame = tk.Frame(parent, bg="yellow", bd=2, relief = "raised")
		frame.columnconfigure(0, weight=1)
		frame.columnconfigure(1, weight=1)
		frame.pack(anchor="w", padx=10, pady=5)
		# Ligne : label + champ de saisie
		for row, value in enumerate(self.values):
			value.display(frame,row)

parameters: list = [
	mlv.Value("ka", 220, 1, 0x20),
	mlv.Value("kad", 22, 1, 0x21),
	mlv.Value("kx", 177, 1, 0x22),
	mlv.Value("kxd", 62, 1, 0x23),
	mlv.Value("Current max [A]", 0.65, 1, 0x03),
	mlv.Value("Magnitude max [mm]", 245, 1000, 0x05),
	mlv.Value("Speed max [mm/s]", 3000, 1000, 0x06),
	mlv.Value("Acceleration max [m/s2]", 18, 1, 0x07),
	mlv.Value("position 1 [mm]", 131, 1000, 0x11),
	mlv.Value("Acceleration 1 [m/s2]", 2.7, 1, 0x12),
	mlv.Value("position 2 [mm]", -210, 1000, 0x13),
	mlv.Value("Acceleration 2 [m/s2]", 18, 1, 0x14),
	mlv.Value("position 3 [mm]", 0, 1000, 0x15),
	mlv.Value("Acceleration 3 [m/s2]", 18, 1, 0x16),
	mlv.Value("Threshold [deg]", 112, 57.295, 0x17),
	mlv.Value("Looping pulse [mm]", 8, 1000, 0x32),
	mlv.Value("Balance down pulse [mm]", 10, 1000, 0x33),
	mlv.Value("Balance down threshold [deg]", 150, 57.295, 0x34),
	mlv.Value("Position [mm]", 0, 1000, 0x35),
]

readings: list = [
	mlv.Value("Angle [deg]", 0, 57.295, 0x40),
	mlv.Value("Angular velocity [rad/s]", 0, 1, 0x41),
	mlv.Value("Position [mm]", 0, 1000, 0x42),
	mlv.Value("Velocity [mm/s]", 0, 1000, 0x43),
	#mlv.Value("cycle time [us]", 0, 1000000, 0x44),
	#mlv.Value("phase", 0, 1, 0x45),
]