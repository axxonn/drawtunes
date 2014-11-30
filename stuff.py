import sys
#import and init pygame
import pygame
from pygame import *
init() 

#create the screen
window = display.set_mode((640, 480)) 

#draw a line - see http://www.pygame.org/docs/ref/draw.html for more 
draw.line(window, (255, 255, 255), (0, 0), (30, 50))

#draw it to the screen
display.flip() 

#input handling (somewhat boilerplate code):
while True: 
   for event in pygame.event.get(): 
      if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit(0) 
      else:
          draw.line(window, (255, 255, 255), (0, 0), mouse.get_pos())
          print event 
          
          
#          
#import sys
##import and init pygame
#import pygame
#pygame.init() 
#
##create the screen
#window = pygame.display.set_mode((640, 480)) 
#
##draw a line - see http://www.pygame.org/docs/ref/draw.html for more 
#pygame.draw.line(window, (255, 255, 255), (0, 0), (30, 50))
#
##draw it to the screen
#pygame.display.flip() 
#
##input handling (somewhat boilerplate code):
#while True: 
#   for event in pygame.event.get(): 
#      if event.type == pygame.QUIT:
#          pygame.quit()
#          sys.exit(0) 
#      else:
#          pygame.draw.line(window, (255, 255, 255), (0, 0), mouse.get_pos())
#          print event 


from pygame import *
init()
screen = display.set_mode((1000,720))
for e in iter(event.wait, event.Event(QUIT)):
    col = {(1, 0, 0): 'white', (0, 0, 1): 'black'}.get(mouse.get_pressed())
    if col and e.type in (MOUSEBUTTONDOWN, MOUSEMOTION):
        display.update(screen.fill(Color(col), Rect(mouse.get_pos(), (1, 1))))
quit()










from Tkinter import *

class PaintBox( Frame ):
   def __init__( self ):
      Frame.__init__( self )
      self.pack( expand = YES, fill = BOTH )
      self.master.title( "A simple paint program" )
      self.master.geometry( "300x150" )

      self.message = Label( self, text = "Drag the mouse to draw" )
      self.message.pack( side = BOTTOM )
      
      # create Canvas component
      self.myCanvas = Canvas( self )
      self.myCanvas.pack( expand = YES, fill = BOTH )

      # bind mouse dragging event to Canvas
      self.myCanvas.bind( "<B1-Motion>", self.paint )

   def paint( self, event ):
      x1, y1 = ( event.x - 4 ), ( event.y - 4 )
      x2, y2 = ( event.x + 4 ), ( event.y + 4 )
      self.myCanvas.create_oval( x1, y1, x2, y2, fill = "black" )
   
def main():
   PaintBox().mainloop()

if __name__ == "__main__":
   main()
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
from PIL import Image, ImageFilter

def roll(image, delta):
    "Roll an image sideways"

    xsize, ysize = image.size

    delta = delta % xsize
    if delta == 0: return image

    part1 = image.crop((0, 0, delta, ysize))
    part2 = image.crop((delta, 0, xsize, ysize))
    image.paste(part2, (0, 0, xsize-delta, ysize))
    image.paste(part1, (xsize-delta, 0, xsize, ysize))

    return image

original = Image.open("input.png") # load an image from the hard drive
blurred = original.filter(ImageFilter.BLUR) # blur the image
 
roll(blurred, 1000).save('output.png')

import webbrowser
webbrowser.open('output.png')

