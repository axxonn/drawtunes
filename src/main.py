import sys
from PIL import Image
from midiutil.MidiFile import MIDIFile
import webbrowser

def get_pixels(filename):
    """Returns: a 2D list that contains ints (that represent hue)
    Precondition: filename is a string that corresponds to a png file"""
    im = Image.open(filename)
    
    pixels = list(im.getdata())
    width, height = im.size
    # partition into columns
    pixel_cols = []
    for i in xrange(width):
        pixel_cols.append([])
        for j in xrange(height):
            value = pixels[j * width + i]
            pixel_cols[i].append(value)
    
    # for i in xrange(len(pixel_cols)):
    #    for j in xrange(len(pixel_cols[0])):
    #        print pixel_cols[i][j],
    #    print '\n'
    
    return pixel_cols

def convert_to_music(midi, pixels, track, length = 0.5):
    """Writes the given pixels to the midi on the given track.
    #May specify duration of notes."""
    MyMIDI = midi
    
    # Tracks are numbered from zero. Times are measured in beats.
    #track = 0   
    time = 0
    
    # Add track name and tempo.
    #MyMIDI.addTrackName(track,time,"Sample Track")
    MyMIDI.addTempo(track,time,120)
    
    duration = length
    
    width = len(pixels)
    height = len(pixels[0])
    for i in xrange(width):
        for j in xrange(height):
            # check to make sure note is not already accounted for
            if pixels[i][j] == 1 and not (i > 0 and pixels[i-1][j] == 1):
                # extend duration as necessary
                temp = 0
                while i + temp + 1 < width and pixels[i + temp + 1][j] == 1:
                    temp += 1
                # parameters: track, channel, pitch, time, duration, volume
                MyMIDI.addNote(track, track, 100 - j, time, duration * (1 + temp), 100)
        time += duration
    
    #return MyMIDI


def get_colors(pixellist):
    """Returns: a dictionary of colors (key is the color)
    Precondition: pixellist is a 2D list containing tuples (RGB values)"""
    colorlist = {}
    for column in pixellist:
        for pixelcolor in column:
            if not pixelcolor in colorlist and pixelcolor[:3] != (255, 255, 255) :
                colorlist[pixelcolor] = 0
    return colorlist


def create_masterlist(color, pixellist):
    """Returns: a 2D list which contains 1 or 0 depending on if that color is at that pixel
    Precondition: color is a tuple of RGB values, pixellist is a 2D list of tuples (RGB values)"""
    masterlist = []
    for column in pixellist:
        columnlist = []
        for row in column:
            if row == color:
                columnlist.append(1)
            else:
                columnlist.append(0)
        masterlist.append(columnlist)
    return masterlist


def rgb_to_hue(color):
    """Returns: float that represents the hue
    Preconditions: color is a tuple that contains RGB values"""
    red = color[0] / 255.0
    green = color[1] / 255.0
    blue = color[2] / 255.0
    maxValue = max(red, green, blue)
    minValue = min(red, green, blue)
    if maxValue == minValue:
       hue = 0
    elif maxValue == red and green >= blue:
       hue = 60.0 * (green - blue)/(maxValue - minValue)
    elif maxValue == red and green < blue:
       hue = 60.0 * (green - blue)/(maxValue - minValue) + 360.0
    elif maxValue == green:
       hue = 60.0 * (blue - red)/(maxValue - minValue) + 120.0
    elif maxValue == blue:
       hue = 60.0 * (red - green)/(maxValue - minValue) + 240.0
    return hue


def main():
    filename = raw_input('Please enter the name of your image file (don\'t include .png): ')
    pixels = get_pixels(filename + '.png')
    colors = get_colors(pixels)
    while len(colors) > 15:
        sys.stdout.write('This image has too many colors.')
        filename = raw_input('Please enter the name of your image file (don\'t include .png): ')
        pixels = get_pixels(filename + '.png')
        colors = get_colors(pixels)
    print colors
    track = 0
    # Create the MIDIFile Object with 1 track
    midi = MIDIFile(len(colors))
    for color in colors:
        midi.addProgramChange(track, track, 0, track * 15)
        colors[color] = create_masterlist(color, pixels)
        convert_to_music(midi, colors[color], track)
        track += 1
    binfile = open(filename + ".mid", 'wb')
    midi.writeFile(binfile)
    binfile.close() # no idea if this is necessary or not
    webbrowser.open(filename + '.mid')

if __name__ == '__main__':
    main()