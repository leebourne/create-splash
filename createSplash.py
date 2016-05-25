#!/usr/bin/python
'''
Created on Oct 30, 2013

@author: Lee Khan-Bourne

Utility to create multiple splash screens from one source image
Source image is resized without distortion and can be annotated

Usage:
    python createSplash.py screens.xml
    
Prerequisites:
    PIL module, the easiest way to install this is using: pip install Pillow
    You'll also need some external libraries, see: https://pypi.python.org/pypi/Pillow/2.1.0  
    
'''

from PIL import Image, ImageDraw, ImageFont
from xml.dom.minidom import parseString
import sys, os

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)
        
def toRGB(colour):
    if len(colour) < 3:
        return None
    
    if len(colour) > 5:
        colour = colour[-6:]
    else:
        shortColour = colour[-3:]
        colour = shortColour[0:1]*2 + shortColour[1:2]*2 + shortColour[2:3]*2

    rgb = (int(colour[0:2], 16), int(colour[2:4], 16), int(colour[4:6], 16))
        
    return rgb 

if len(sys.argv) > 1:
    xmlFileName = sys.argv[1]
else:
    xmlFileName = 'screens.xml'

# Open the screens xml file
try:
    xmlFile = open(xmlFileName, 'r')
except:
    print "Can't open " + xmlFileName
    quit()
    
# Read the xml file into a string:
data = xmlFile.read()
xmlFile.close()

# Parse the xml screens file
dom = parseString(data)

domTag = dom.getElementsByTagName('source')
if domTag:
    source = domTag[0].firstChild.data
else:
    print "No source image defined"
    quit()
    
domTag = dom.getElementsByTagName('fill')
if domTag:
    fillColour = domTag[0].firstChild.data
else:
    fillColour = None

domTag = dom.getElementsByTagName('transparency')
if domTag:
    transparency = domTag[0].firstChild.data
else:
    transparency = None

try: 
    im = Image.open(source)
except:
    print "Can't open " + source
    quit()
    
srcWidth  = float(im.size[0])
srcHeight = float(im.size[1])
srcRatio  = srcWidth / srcHeight

screens     = dom.getElementsByTagName('screen')
annotations = dom.getElementsByTagName('annotations')

#iterate through each screen in the file
for screen in screens:
    destWidth  = int(screen.getElementsByTagName('width')[0].firstChild.data)
    destHeight = int(screen.getElementsByTagName('height')[0].firstChild.data)
    destination = screen.getElementsByTagName('destination')[0].firstChild.data
    
    if srcRatio > (float(destWidth) / float(destHeight)):
        newSize = destWidth, int(srcHeight * (float(destWidth) / srcWidth))
    else:
        newSize = int(srcWidth * (float(destHeight) / srcHeight)), destHeight
        
    try:
        newImage = im.resize(newSize, Image.ANTIALIAS)
    except:
        print "Could not resize " + destination
        quit()
        
    try:
        finalImage = Image.new("RGB", (destWidth,destHeight), fillColour)
        x = (destWidth - newSize[0]) / 2
        y = (destHeight - newSize[1]) / 2
        finalImage.paste(newImage, (x, y, x + newSize[0], y + newSize[1]))
        del newImage
    except:
        print "Could not expand canvas for " + destination
        quit()
       
    if transparency:
        try:        
            rgb = toRGB(transparency)
            if rgb:
                finalImage = finalImage.convert("RGBA")
                datas = finalImage.getdata()
            
                newData = list()
                for item in datas:
                    if item[0] == rgb[0] and item[1] == rgb[1] and item[2] == rgb[2]:
                        newData.append((rgb[0], rgb[1], rgb[2], 0))
                    else:
                        newData.append(item)
            
                finalImage.putdata(newData)
        except:
            print "Couldn't apply transparency for " + destination
            quit()                
        
    for annotation in annotations:
        annoText = annotation.getElementsByTagName('text')
        if annoText:
            ''' Defaults '''
            fontFace   = ''
            fontColour = 'black'
            fontSize   = 36
            hAlign     = 'center'
            vAlign     = 'center'

            annoText = annoText[0].firstChild.data
     
            ''' Check to see if any of the defaults have been overridden ''' 
            domTag = annotation.getElementsByTagName('color')
            if domTag:
                fontColour = domTag[0].firstChild.data
            
            domTag = annotation.getElementsByTagName('size')
            if domTag:
                fontSize = int(domTag[0].firstChild.data)
                
            domTag = annotation.getElementsByTagName('align')
            if domTag:
                hAlign = domTag[0].firstChild.data
            
            domTag = annotation.getElementsByTagName('valign')
            if domTag:
                vAlign = domTag[0].firstChild.data
            
            domTag = annotation.getElementsByTagName('font')
            if domTag:
                fontFace = domTag[0].firstChild.data
            
            if fontFace > '':    
                font = ImageFont.truetype(fontFace, fontSize)
            else:
                font = ImageFont.load_default()
                                
            ''' Work out where to place the text top=5%, bottom=95%, left=5%, right=95% 
                Use getsize to work out the size of the text
            '''
            textSize = font.getsize(annoText)
            if hAlign == 'left':
                textLeft = destWidth / 20
            elif hAlign == 'right':
                textLeft = destWidth - (destWidth / 20) - textSize[0]
            else:
                textLeft = (destWidth - textSize[0]) / 2                
            if vAlign == 'top':
                textTop = destHeight / 20
            elif vAlign == 'bottom':
                textTop = destHeight - (destHeight / 20) - textSize[1]
            else:
                textTop = (destHeight - textSize[1]) / 2                
                
            draw = ImageDraw.Draw(finalImage)
            draw.text((textLeft, textTop), annoText, font=font, fill=fontColour)
            del draw
     
    try:
        ensure_dir(destination)
        domTag = screen.getElementsByTagName('dpi')
        if domTag:
            dpi = int(domTag[0].firstChild.data)
            finalImage.save(destination, dpi=(dpi, dpi))
        else:
            finalImage.save(destination)
        print "Created " + destination
        del finalImage
    except:
        print "Could not save " + destination
        quit()
        
del im
