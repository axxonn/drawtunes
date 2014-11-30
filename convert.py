from PIL import Image
import webbrowser

im = Image.open('input.png')

pixels = im.load()
width, height = im.size
# partition into columns
pixel_cols = []
for i in xrange(width):
    pixel_cols.append([])
    for j in xrange(height):
        pixel_cols[i].append(pixels[j * width + i])
print pixels

#for i in xrange(len(pixel_cols)):
#    for j in xrange(len(pixel_cols[0])):
#        print 0 if pixel_cols[i][j][0] == 255 else 1,
#    print '\n'

# the following is all just testing for validity
im2 = Image.new("RGB", (width * 2, height), "#00FF00")
pixels2 = im2.load()
for i in range(width):
    for j in range(height):
        pixels2[i * 2, j] = pixel_cols[i][j]
im2.save("output3.png")
webbrowser.open('output3.png')