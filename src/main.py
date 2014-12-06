import sys
import os
import webbrowser
import argparse
from PIL import Image
from midiutil.MidiFile import MIDIFile

def get_pixels(filename):
    """Returns: a 2D list that contains tuples (RBG values)
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

def convert_to_music(midi, pixels, instrument, tempo = 120):
    """Writes the given pixels to the midi on the given track.
    #May specify duration of notes."""
    MyMIDI = midi

    # Tracks are numbered from zero. Times are measured in beats.
    #track = 0
    time = 0

    # Add track name and tempo.
    #MyMIDI.addTrackName(track,time,"Sample Track")
    MyMIDI.addTempo(instrument,time,tempo)

    duration = 0.5

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
                pitch = (88 - j) + 21 # int((height-j)/float(height) * 88) + 21
                # parameters: track, channel, pitch, time, duration, volume
                MyMIDI.addNote(instrument, instrument, pitch, time, duration * (1 + temp), 100)
        time += duration

    #return MyMIDI


def normalize_height(pixellist):
    """Returns: a 2D list of height 88 that contains tuples (RGB values)
    Precondition: pixellist is a 2D list of random height and width"""
    pixel88list = []
    for column in range(len(pixellist)):
        newcolumn = []
        for row in range(88): # creates columns of 88 white pixels
            newcolumn.append((255, 255, 255)) # appends a white pixel
        pixel88list.append(newcolumn) # adds column to new 2D list
    for column in range(len(pixellist)):
        for row in range(len(pixellist[column])):
            if pixellist[column][row][:3] != (255, 255, 255):
                height = int((row*1.0)/len(pixellist[column]) * 88)
                pixel88list[column][height] = pixellist[column][row]
    return pixel88list

def fix_chords(pixel88list):
    """Returns: a beautiful version of pixel88list. Notes are shifted so that they do not clash within chords."""
    # This implementation is slightly inefficient in that it redundantly checks some known whitespaces for clashes
    # after shifting a note, but we keep it to simplify the loop mechanics.
    for column in range(len(pixel88list)):
        notes = {} # set of pitches in a given column
        for row in range(len(pixel88list[column]))[:-1]:
            pixel = pixel88list[column][row][:3]
            if pixel != (255, 255, 255):
                pitch = 88 - row
                index = row # index for keeping track of shifted note
                for i in notes:
                    while is_clashing(i, pitch):
                        if index + 1 >= len(pixel88list[column]):
                            # print 'oh no'
                            break
                        pitch -= 1
                        pixel88list[column][index+1] = pixel
                        pixel88list[column][index] = (255, 255, 255)
                        index += 1
                notes[pitch] = 0  # 0 is placeholder value, just need key
    return pixel88list

def is_clashing(note1, note2):
    """Returns: whether note1 and note2 clash, i.e. whether they are one or two half-steps away from each other
    Precondition: note1, note2 are pitches, 0-88 (correspond to piano keyboard)"""
    distance = min((note1-note2)%12,(note2-note1)%12)
    return 0 < distance < 3  # 1 or 2 half-steps


def get_colors(pixellist):
    """Returns: a dictionary of colors (key is the color)
    Precondition: pixellist is a 2D list containing tuples (RGB values)"""
    colorlist = {}
    for column in pixellist:
        for pixelcolor in column:
            pixelcolor3 = pixelcolor[:3]
            if pixelcolor3 != (255, 255, 255) and not pixelcolor3 in colorlist:
                colorlist[pixelcolor3] = 0
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

class ColorException(Exception):
    pass

def main():
    os.chdir(os.getcwd() + '\\..\\sandbox')  # first requires working directory to be "../final"
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='the name of the image file')
    args = parser.parse_args()
    filename = args.filename
    while filename != 'quit()':
        try:
            pixels = get_pixels(filename + '.png')
            pixels88 = normalize_height(pixels)
            colors = get_colors(pixels88)
            if len(colors) > 15:
                raise ColorException()
            break
        except IOError:
            print 'File not found. Please enter a valid filename.'
            filename = raw_input(
                'Please enter the name of your image file (don\'t include .png) \nor type \'quit()\' to quit: ')
        except ColorException:
            print 'This image has too many colors.'
            filename = raw_input(
                'Please enter the name of your image file (don\'t include .png) \nor type \'quit()\' to quit: ')
    if filename == 'quit()':
        return

    midi = MIDIFile(len(colors))
    track = 0
    for color in colors:
        instrument = int((color[0]*100+color[1]*10+color[2]) / (28305/127))
        midi.addProgramChange(track, track, 0, instrument)
        colors[color] = create_masterlist(color, pixels88)
        convert_to_music(midi, colors[color], track, tempo=240)
        track += 1
        print `color` + ': ' + `instrument`
    filename = 'beautiful_' + filename
    binfile = open(filename + ".mid", 'wb')
    midi.writeFile(binfile)
    binfile.close()  # no idea if this is necessary or not
    webbrowser.open(filename + '.mid')

if __name__ == '__main__':
    main()