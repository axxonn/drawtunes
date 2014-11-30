#Import the library

from PIL import Image
from midiutil.MidiFile import MIDIFile
import webbrowser

im = Image.open('input.png')

pixels = list(im.getdata())
width, height = im.size
# partition into columns
pixel_cols = []
for i in xrange(width):
    pixel_cols.append([])
    for j in xrange(height):
        value = pixels[j * width + i][0]
        if value == 255:
            pixel_cols[i].append(0)
        else:
            pixel_cols[i].append(1)

for i in xrange(len(pixel_cols)):
    for j in xrange(len(pixel_cols[0])):
        print pixel_cols[i][j],
    print '\n'

# Create the MIDIFile Object with 1 track
MyMIDI = MIDIFile(1)

# Tracks are numbered from zero. Times are measured in beats.
track = 0   
time = 0

# Add track name and tempo.
MyMIDI.addTrackName(track,time,"Sample Track")
MyMIDI.addTempo(track,time,120)

track = 0
channel = 0
pitch = 0
time = 0
duration = 0.5
volume = 100

for i in xrange(width):
    for j in xrange(height):
        temp = 0
        if pixel_cols[i][j] == 1:
            MyMIDI.addNote(0, 0, 100 - j, time, duration, 100)
    time += duration

#for i in xrange(width):
#    for j in xrange(height):
#        temp = 0
#        if pixel_cols[i][j] == 1 and not (i > 0 and pixel_cols[i-1][j] == 1):
#            while i + temp + 1 < width and pixel_cols[i + temp + 1][j] == 1:
#                temp += 1
#            MyMIDI.addNote(0, 0, 100 - j, time, duration * (1 + temp), 100)
#    time += duration

binfile = open("output2.mid", 'wb')
MyMIDI.writeFile(binfile)
binfile.close()
webbrowser.open('output2.mid')