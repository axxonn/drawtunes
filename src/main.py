from PIL import Image
from midiutil.MidiFile import MIDIFile
import webbrowser

def get_pixels(filename):
    """Returns: a 2D list that contains the RGB values of each pixel, represented as a tuple
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
            # value = pixels[j * width + i][0]
            # # change as necessary to support different effects
            # # for different colors
            # if value == 255:
            #     pixel_cols[i].append(0)
            # else:
            #     pixel_cols[i].append(1)
    
    for i in xrange(len(pixel_cols)):
       for j in xrange(len(pixel_cols[0])):
           print pixel_cols[i][j],
       print '\n'
    
    return pixel_cols

def convert_to_music(pixels):
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
                MyMIDI.addNote(0, 0, 100 - j, time, duration * (1 + temp), 100)
        time += duration
    
    return MyMIDI


def get_colors(pixellist):
    """Returns: a list of colors from an array of RBG values that correspond with pixels
    Precondition: pixellist is a 2D list containing tuples that correspond to RGB values"""
    pass



def create_masterlist(colorlist, pixellist):
    """Returns: a list of 2D lists, each of which contains information for one color
    Precondition: colorlist is a list of colors """
    # loop through colorlist
    # for each color, loop through file
        # append to masterlist
    pass



def main():
    filename = raw_input('Please enter the name of your image file (don\'t include .png): ')
    pixels = get_pixels(filename + '.png')
    colors = get_colors(pixels)
    masterlist = create_masterlist(colors, pixels) # list of 2D lists which contain 
    midi = convert_to_music(pixels)
    binfile = open(filename + ".mid", 'wb')
    midi.writeFile(binfile)
    binfile.close() # no idea if this is necessary or not
    webbrowser.open(filename + '.mid')

main()