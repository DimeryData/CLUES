# sudo pip3 intall python-escpos --break-system-packages
from PIL import Image
from escpos.printer import Usb
vendor_id = 0x0485
product_id = 0x5741
printer = Usb(vendor_id, product_id)

def print_image(image_path):
	img = Image.open(image_path)
	
	img = img.convert("1")
	
	

	# print image
	printer.image(img)
	

print_image("pig.jpeg")
