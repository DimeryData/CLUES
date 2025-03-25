#pip install usb --break-system-packages




from escpos.printer import Usb
import escpos
# Update this with the output from USBDev.py
vendor_id = 0x0485
product_id = 0x5741
printer = Usb(vendor_id, product_id)

#printer.set(align='center', font='b', width=2, height=2)
#printer._raw(b'\x1b\x21\x1e')
# Set alignment and font size (if needed)
printer.set(align='center', font='b', width=2, height=2)
#printer._raw(b'\xb1\x40')
printer.text("Hey There")

printer.cut()
