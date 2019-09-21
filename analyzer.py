from google_images_download import google_images_download   #importing the library

def stuff(keyword):
    response = google_images_download.googleimagesdownload()   #class instantiation
    arguments = {"keywords":keyword,"limit":20,"no_download":True,"metadata":True}   #creating list of arguments
    paths = response.download(arguments)   #passing the arguments to the function

    for i in paths[0][keyword]:
        print(i)

stuff("music")