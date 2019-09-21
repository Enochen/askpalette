from google_images_download import google_images_download   #importing the library

response = google_images_download.googleimagesdownload()   #class instantiation

keyword = "music"
arguments = {"keywords":keyword,"limit":20,"no_download":True,"metadata":True}   #creating list of arguments
paths = response.download(arguments)   #passing the arguments to the function