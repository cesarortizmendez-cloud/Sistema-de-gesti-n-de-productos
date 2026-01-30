from PIL import Image

img = Image.open("assets/icon.png")  # tu imagen base
img.save("assets/icon.ico", sizes=[(16,16),(32,32),(48,48),(256,256)])
