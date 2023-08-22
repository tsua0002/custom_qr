import qrcode
import PIL
from PIL import Image, ImageDraw, ImageFont

# Generate QR code
qr = qrcode.QRCode(version=1, box_size=12, border=2)
qr.add_data('https://thepubcrawlcompany.com/be/brussels/producto/pubcrawls/')
qr.make(fit=True)
img = qr.make_image(fill_color=(0, 0, 0), back_color="white")

# Create blank image with google colors 
size = img.size[0] + 90
google_img = Image.new('RGB', (int(size*(3/2)), int(size*(3/2))), (251, 188, 5))

# Paste QR code in the center
google_img.paste(img, (size//3,size//3)) 

# Add google text
draw = ImageDraw.Draw(google_img)
font = ImageFont.truetype("fonts/CaviarDreams.ttf", 60)
draw.text((10,10), "The PubCrawlCompany", font=font, fill=(255,255,255))

font_small = ImageFont.truetype("fonts/CaviarDreams_italic.ttf", 35)
draw.text((10,105), "Buy Ticket for La Troupe Grand Place", font=font_small, fill=(255,255,255))

draw.text((30,690), "Made with <3 by Thomas.", font=font, fill=(255,255,255))

google_img.save('outputs/payment_qr.png')

