# Program to control a single inverted pendulum
# using a GUI built with tkinter, 
# and communicating with a microcontroller via serial port
# Author: Magdi Laoun
# Date: 8th of June 2026
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
import MLValue as mlv
import MLValuesManager as mlvm
import MLCustomButton as mlcb
import serial
import MLSerial as mlse
import struct

# ── Main window ─────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("Single inverted pendulum")
root.geometry("800x600")
parameters_manager = mlvm.ValuesManager(values=mlvm.parameters)
results_manager = mlvm.ValuesManager(values=mlvm.readings)
ser = mlse.get_serial_port() # open the serial port (or None if not found)
# ── Fonts ─────────────────────────────────────────────────────────────────
font_title     = tkfont.Font(family="Avenir", size=22)
font_sub_title = tkfont.Font(family="Avenir", size=16)
font_footer = tkfont.Font(family="Avenir", size=12)
font_resultat  = tkfont.Font(family="Courier New", size=15, weight="bold")
# ── Frames ──────────────────────────────────────────────────────────────────
frame_title      = tk.Frame(root)
frame_central    = tk.Frame(root, bg="#ffffff", relief="flat")
frame_parameters = tk.Frame(frame_central, bg="#5272DA", bd=0, relief="flat")
frame_controls    = tk.Frame(frame_central, bg="#999999", relief="flat")
frame_result     = tk.Frame(frame_controls, bg="#DA6452", relief="flat")
frame_footer     = tk.Frame(root, bg="#CECECE", relief="flat")
# ── Layout ──────────────────────────────────────────────────────────────────
frame_title.pack()
frame_central.pack(fill="both", expand=True)
frame_parameters.pack(side="left", anchor = "nw", padx=10, pady=10)
frame_controls.pack(anchor = "nw", padx=10, pady=10)
frame_result.pack(anchor = "n", padx=5, pady=5)
frame_footer.pack(fill="x", side="bottom")
# ── Title ────────────────────────────────────────────────────────────────────
label_title = tk.Label(
    frame_title,
    text="Single pendulum, command",
    font=font_title
)
label_title.pack()
# ── Frame parameters ────────────────────────────────────────────────────────────
def display():
    for value in parameters_manager.values:
        x = value.get_data_to_send()
        try:
            if ser is None:
                return
            ser.write(x)
        except serial.SerialException as e:
            print(f"Error sending parameters: {e}")
label = tk.Label(frame_parameters, text = "Parameters", font = font_sub_title, bg="#5272DA", fg="white")
label.pack(pady=0)
parameters_manager.display(frame_parameters) # display the parameters to be sent to the controller in the parameters frame
btn = mlcb.CustomButton(frame_parameters, text = "Update", command =lambda: display(), bg = "#2E8F4B", fg = "white")
btn.pack(anchor="center", pady=0) # button to send the parameters to the controller
# ── Controls ──────────────────────────────────────────────────────────────────
label = tk.Label(frame_result, text = "Reading values", font = font_sub_title, bg=frame_result.cget("bg"), fg="white")
label.pack(pady=0)
results_manager.display(frame_result) # display the readings from the controller in the result frame
def send_command(address, value):
    value_to_send = bytes([address]) + struct.pack('<f', value)
    try:
        if ser is None:
            return
        ser.write(value_to_send)
    except serial.SerialException as e:
        print(f"Error sending command: {e}")
buttons = [ #list of buttons to send commands to the controller (address + value)
    ("Reset encoder", 0x02, 0.0),
    ("Reset driver",  0x01, 0.0),
    ("Stop",          0x00, 0.0),
    ("Swing-up",      0x00, 1.0),
    #("Balance-up",    0x00, 2.0),
    ("Damping",       0x00, 3.0),
    ("Looping left",  0x00, 4.0),
    ("Looping right", 0x00, 5.0),
]
for text, addr, val in buttons:
    mlcb.CustomButton(
        frame_controls, text=text,
        command=lambda a=addr, v=val: send_command(a, v),
        bg="red", fg="white"
    ).pack(anchor="center", pady=2)

# ── Footer ──────────────────────────────────────────────────────────────
label_footer = tk.Label(
    frame_footer,
    text="Magdi Laoun, 8th of June 2026",
    font=font_footer,
    bg=frame_footer.cget("bg"),
    fg="#2a4a5e"
)
label_footer.pack(side="bottom", pady=16)
display()
def on_packet_received(values): # callback function called when data is received from the controller
    f1, f2, f3, f4, f5, f6 = values
    results_manager.values[0].set_value(f1)  # Angle
    results_manager.values[1].set_value(f2)  # Angular velocity
    results_manager.values[2].set_value(f3)  # Position
    results_manager.values[3].set_value(f4)  # Velocity
    #results_manager.values[4].set_value(f5)  # Cycle time
    #results_manager.values[5].set_value(f6)  # Phase

reader = mlse.SerialReader(ser)  # ser = instance of serial.Serial or None if no port found
reader.start(callback=on_packet_received)

root.mainloop()

reader.stop()  # when closing the application, stop the serial reader thread and close the serial port