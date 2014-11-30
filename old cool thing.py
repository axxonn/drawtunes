from PIL import Image

im = Image.open('input333.png')

# splitting pixels: http://stackoverflow.com/a/1109747
pixels = list(im.getdata())
width, height = im.size
pixels = [pixels[i * height: (i + 1) * height] for i in xrange(width)]


#for rows in pixels:
#    for i in rows:
#        print 1 if i[0] == 255 else 0,
        
import webbrowser
#webbrowser.open('input.png')

im2 = Image.new("RGB", (width, height), "white")
pixels2 = im2.load()
for i in range(width):
    for j in range(height):
        pixels2[i, j] = pixels[i][j]
im2.save("output2.png")
#webbrowser.open('input.png')
webbrowser.open('output2.png')