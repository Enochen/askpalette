import io
import os
import urllib.request
from google_images_download import google_images_download
from google.cloud import vision, storage
from google.cloud.vision import types
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

class Color:
    def __init__(self, red, green, blue, score):
        self.red = float(red)
        self.green = float(green)
        self.blue = float(blue)
        self.score = float(score)

    def diff(self, other):
        color1_rgb = sRGBColor(self.red/255, self.green/255, self.blue/255)
        color2_rgb = sRGBColor(other.red/255, other.green/255, other.blue/255)
        color1_lab = convert_color(color1_rgb, LabColor)
        color2_lab = convert_color(color2_rgb, LabColor)
        return delta_e_cie2000(color1_lab, color2_lab)
    
    def toRGB(self):
        return "RGB(" + str(self.red) + ", " + str(self.green) + ", " + str(self.blue) + ")"
    
    def __str__(self):
        return "{},{},{},{}".format(str(self.red), str(self.green), str(self.blue), str(self.score))

    def relativeWidth(self, list):
        sumScore = sum(item.score for item in list)
        return self.score/sumScore * 300

    def toHex(self):
        return '#%02x%02x%02x' % (int(self.red), int(self.green), int(self.blue))


def __average(color1, color2):
    weight = color1.score / color2.score;
    newRed = (color1.red * weight + color2.red)/(weight+1)
    newGreen = (color1.green * weight + color2.green)/(weight+1)
    newBlue = (color1.blue * weight + color2.blue)/(weight+1)
    return Color(newRed, newGreen, newBlue, color1.score + color2.score)

def __tooBig(url):
    try:
        usock = urllib.request.urlopen(url)
        size =  usock.info().get('Content-Length')
        if size is None:
            size = 0
        return float(size) > 10000000
    except:
        return True;
    

def stuff(keyword):
    ColorList = []
    file = "cache/" + keyword.lower()
    storageClient = storage.Client()
    bucket = storageClient.get_bucket('askpalette.appspot.com')
    blob = bucket.blob(file)
    exists = storage.Blob(bucket=bucket, name=file).exists(storageClient)

    if exists:
        file = blob.download_as_string()
        if file:
            lines = file.decode().splitlines()
            for line in lines:
                list = line.split(",")
                ColorList.append(Color(list[0],list[1],list[2],list[3]))
            return ColorList

    try:
        response = google_images_download.googleimagesdownload()   #class instantiation
        arguments = {"keywords":keyword,"limit":3,"silent_mode":True, "no_numbering":True,"no_download":True}
        #arguments = {"keywords":keyword,"limit":5,"no_numbering":True}   #creating list of arguments
        paths = response.download(arguments)   #passing the arguments to the function

        while paths[0][keyword].__len__() < 1:
            paths = response.download(arguments)

        for uri in paths[0][keyword]:
            # Loads the image into memory
            if(__tooBig(uri)):
                 continue
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
                    if existing.diff(color) < 10:
                        existing = __average(existing, color)
                        merged = True
                        break
                if not merged:
                    ColorList.append(color)
        ColorList2 = ColorList.copy()
        for existing in ColorList:
            for existing2 in ColorList2:
                threshold = 18
                if ColorList.__len__() < 7:
                    threshold = 5
                if existing != existing2 and existing.diff(existing2) < threshold:
                    existing = __average(existing, existing2)
                    ColorList.remove(existing2)
                    ColorList2.remove(existing2)

        ColorList.sort(key=lambda color: color.score, reverse=True)

        uploadStr = ""
        for color in ColorList:
            uploadStr += (color.__str__() + '\n')
        
        storageClient = storage.Client()    
        bucket = storageClient.get_bucket('askpalette.appspot.com')
        blob = bucket.blob(file)
        blob.upload_from_string(uploadStr)
    except:
        return None

    return ColorList
#stuff("music")
# print(Color(6,17,71,0).diff(Color(6,9,36,1)))