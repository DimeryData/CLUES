from escpos.printer import Usb
import escpos
# Update this with the output from USBDev.py
# Constants for the printer
CONTROL_MODE = "Epson"
BAUD_RATE = 9600
DATA_BITS = 8
STOP_BITS = 1
PARITY = 'N'
vendor_id = 0x0485
product_id = 0x5741

printer = Usb(vendor_id, product_id)


ALIGNMENT = 'center'
FONT = 'b'
WIDTH = 8
HEIGHT = 8


printer.set(align=ALIGNMENT, font=FONT, width=WIDTH, height=HEIGHT)


printer.text("SUP DUDE?")


printer.cut()
