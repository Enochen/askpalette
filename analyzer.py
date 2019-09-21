import io
import os
from google_images_download import google_images_download
from google.cloud import vision
from google.cloud.vision import types

class Color:
    def __init__(self, red, green, blue, score):
        self.red = red
        self.green = green
        self.blue = blue
        self.score = score

    def diff(self, other):
        diffRed = abs(self.red - other.red)/255
        diffGreen = abs(self.green - other.green)/255
        diffBlue = abs(self.blue - other.blue)/255
        return (diffRed + diffGreen + diffBlue) / 3 * 100
    
    def toRGB(self):
        return "rgb(" + str(self.red) + ", " + str(self.green) + ", " + str(self.blue) + ")"
    
    def __str__(self):
        return "Red: " + str(self.red) + " Green: " + str(self.green) + " Blue: " + str(self.blue) + " Score: " + str(self.score);

    def score(self):
        return self.score

def __average(color1, color2):
    weight = color1.score / color2.score;
    newRed = (color1.red * weight + color2.red)/(weight+1)
    newGreen = (color1.green * weight + color2.green)/(weight+1)
    newBlue = (color1.blue * weight + color2.blue)/(weight+1)
    return Color(newRed, newGreen, newBlue, color1.score + color2.score)

def stuff(keyword):
    response = google_images_download.googleimagesdownload()   #class instantiation
    arguments = {"keywords":keyword,"limit":3,"silent_mode":True, "no_numbering":True,"no_download":True, "size":"medium"}   #creating list of arguments
    paths = response.download(arguments)   #passing the arguments to the function

    ColorList = []

    for uri in paths[0][keyword]:
        # Loads the image into memory
        print(uri)
        client = vision.ImageAnnotatorClient()
        image = vision.types.Image()
        image.source.image_uri = uri

        response = client.image_properties(image=image)
        props = response.image_properties_annotation
        #print('Properties:')

        #print(response)


        for colorData in props.dominant_colors.colors:
            color = Color(colorData.color.red, colorData.color.green, colorData.color.blue, colorData.score)
            
            merged = False;
            for existing in ColorList:
                if color.diff(existing) < 30:
                    existing = __average(existing, color)
                    merged = True
                    break
            if not merged:
                ColorList.append(color)

            # print('frac: {}'.format(color.pixel_fraction))
            # print('\tr: {}'.format(color.color.red))
            # print('\tg: {}'.format(color.color.green))
            # print('\tb: {}'.format(color.color.blue))
            # print('\ta: {}'.format(color.color.alpha))
    return ColorList
#stuff("music")