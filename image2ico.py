from PIL import Image

png_path = "pdf.jpg"
ico_path = "icona.ico"

img = Image.open(png_path)
img.save(ico_path, format="ICO")
