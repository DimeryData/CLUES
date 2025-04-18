import tkinter as tk
from tkinter import messagebox
import threading
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import time

from escpos.printer import Usb

# === USB Printer Settings ===
VENDOR_ID = 0x0485       # Replace with your printer's Vendor ID
PRODUCT_ID = 0x5741      # Replace with your printer's Product ID

# Initialize printer
printer = Usb(VENDOR_ID, PRODUCT_ID)

# === Text Formatting Options ===
ALIGNMENT = 'center'     # Options: 'left', 'center', 'right'
FONT = 'b'               # Font style: 'a' or 'b'
WIDTH = 1                # Max width scale (1-8)
HEIGHT = 1               # Max height scale (1-8)

# Apply settings
printer.set(
    align=ALIGNMENT,
    font=FONT,
    width=WIDTH,
    height=HEIGHT
)

# === App Logic ===

# List of allowed names (must match RFID tag text exactly)
people = ["Andrew Dimery", "Big Car;"]
person_count = 1
group_count = 1

def printer_print(name, person, group):
    printer.text(f"Welcome : {name} \n\n")
    printer.text(f"You are part of group {group} \n")
    printer.text(f"Number {person}")
    printer.cut()

def read_rfid():
    reader = SimpleMFRC522()
    print("Hold a tag near the reader...")
    id, text = reader.read()
    cleaned_text = text.strip()
    print("Tag UID:", id)
    print("Tag text:", cleaned_text)
    print("Raw tag text:", repr(text))
    return cleaned_text

class RFIDLoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RFID Login")

        self.label = tk.Label(root, text="Please scan your RFID card", font=("Arial", 14))
        self.label.pack(pady=20)

        self.status = tk.Label(root, text="Waiting for RFID...", font=("Arial", 12), fg="blue")
        self.status.pack(pady=10)

        # Start background thread for continuous scanning
        threading.Thread(target=self.scan_loop, daemon=True).start()

    def scan_loop(self):
        global person_count, group_count
        while True:
            try:
                self.set_status("Waiting for RFID...", "blue")
                tag_text = read_rfid()

                if tag_text.strip() == "":
                    self.set_status("Scan Error: Empty tag", "orange")
                    self.root.after(0, lambda: messagebox.showwarning("Scan Error", "Could not read card properly."))
                elif tag_text in people:
                    message = f"Welcome, {tag_text}!\nYou are person {person_count}, Group {group_count}"
                    self.set_status(message, "green")
                    printer_print(tag_text, person_count, group_count)

                    person_count += 1
                    if person_count == 5:
                        person_count = 1
                        group_count += 1
                else:
                    self.set_status("Access Denied", "red")
                    self.root.after(0, lambda: messagebox.showerror("Error", f"'{tag_text}' is not authorized."))

            except Exception as e:
                print("Error during RFID read:", e)
                self.root.after(0, lambda: messagebox.showerror("RFID Error", str(e)))

            # Wait before scanning again
            time.sleep(5)

    def set_status(self, message, color):
        self.root.after(0, lambda: self.status.config(text=message, fg=color))

def on_closing():
    print("Cleaning up GPIO...")
    GPIO.cleanup()
    root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = RFIDLoginApp(root)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
