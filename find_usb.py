import usb.core
import usb.util

# Finding all connected USB devices

devices = usb.core.find(find_all=True)

for device in devices:
print(f"Device: {device}")
print(f"Vendor ID: {hex(device.idVendor)}")
print(f"Product ID {hex(device.idProduct)}")
