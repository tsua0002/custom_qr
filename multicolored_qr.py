import qrcode
import random
from PIL import Image, ImageDraw, ImageFont

# Create base image
img_size = 500
img = Image.new('RGB', (img_size, img_size), 'white')

# Top rectangle
d = ImageDraw.Draw(img)
d.rectangle([0, 0, img_size, img_size//4], fill=(66, 133, 244))

# Left rectangle 
d.rectangle([0, 0, img_size//4, img_size], fill=(234, 67, 53))

# Right rectangle
d.rectangle([img_size - img_size//4, 0, img_size, img_size], fill=(251, 188, 5)) 

# Bottom rectangle
d.rectangle([0, img_size - img_size//4, img_size, img_size], fill=(52, 168, 83))

# Generate QR code
qr = qrcode.QRCode()
qr.add_data("https://maps.app.goo.gl/rWyqEFdX4WyLJmuT7?g_st=ic")
qr.make(fit=True)
qr_img = qr.make_image(fill_color=(66, 133, 244), back_color="white")
# Scale and overlay QR code on image
qr_size = 250
qr_img = qr_img.resize((qr_size, qr_size))
pos = ((img_size - qr_size) // 2, (img_size - qr_size) // 2)
img.paste(qr_img, pos)

# Add google text
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("fonts/CaviarDreams.ttf", 40)
draw.text((10,10), "The PubCrawlCompany", font=font, fill=(255,255,255))

font_review = ImageFont.truetype("fonts/ORGANICAL.ttf",50)
draw.text((20,90), "Review", font=font_review, fill=(0,0,0))

draw.text((60,390), "Thomas", font=font, fill=(255,255,255))

img.save('multicolor_qr.png')
