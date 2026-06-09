#!/usr/bin/env python3

import struct
import tkinter as tk
from tkinter import font as tkfont

class Value:
	def __init__(self, label: str, value: float = 0.0, unit_ratio = 1.0, address: int = 0xFF):
		self.label = label
		self.value = value
		self.unit_ratio = unit_ratio
		self.address = address
		self.var = None
		
	def display(self, parent, row):
		# Label
		if self.var is None:
			self.var = tk.StringVar(value=str(self.value))  # ← créé seulement ici
		bg=parent.cget("bg")
		font    = tkfont.Font(family="Avenir", size=10)
		label = tk.Label(parent, text=self.label, bg=parent.cget("bg"), font = font, anchor="w")
		
		label.grid(row=row, column=0, padx=5, pady=0, sticky="e")		
		# Entry (TextField)
		entry = tk.Entry(
			parent,
			textvariable=self.var,
			font=font,
			width=7,
			relief="flat",
			bd=0,
			highlightthickness=0,
			insertborderwidth=0
		)
		entry.grid(row=row, column=1, padx=5, pady=0, sticky="w")
	
	def get_value(self) -> float:
		"""Retourne la valeur float actuelle du champ"""
		try:
			return float(self.var.get())
		except ValueError:
			return 0.0  
		
	def set_value(self, value: float):
		# Update the value and the displayed text
		self.value = value * self.unit_ratio
		self.var.set(str(self.value))

	def get_data_to_send(self) -> bytes:
		# convert the value to the raw bytes to be sent to the microcontroller
		value_to_send = struct.pack('<f', self.get_value() / self.unit_ratio)
		address = bytes([self.address])
		return address + value_to_send