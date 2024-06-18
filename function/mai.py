
from google.cloud import vision
import pandas as pd
import validators

def detect_web(uri):
    """Detects web annotations given an image."""
    url = []
    if validators.url(uri):
        client = vision.ImageAnnotatorClient()
        image = vision.Image()
        image.source.image_uri = uri
    else:
        try:
            client = vision.ImageAnnotatorClient()
            with open(uri, "rb") as image_file:
                content = image_file.read()
            image = vision.Image(content=content)
        except:
            return 'Invalid Url'

    response = client.web_detection(image=image)
    annotations = response.web_detection

    for image in annotations.visually_similar_images:
        url.append(image.url)
    return url

def objects_detection(path):
    n=[]
    
    if validators.url(path):
        client = vision.ImageAnnotatorClient()
        image = vision.Image()
        image.source.image_uri = path
    else:
        try:
            client = vision.ImageAnnotatorClient()
            with open(path, "rb") as image_file:
                content = image_file.read()
            image = vision.Image(content=content)
        except:
            return 'Invalid Url'

    objects = client.object_localization(image=image).localized_object_annotations
    for obj in objects:
        naam=obj.name
        n.append(naam)
    return n

def label_detection(path):
    labels = []
    
    if validators.url(path):
        client = vision.ImageAnnotatorClient()
        image = vision.Image()
        image.source.image_uri = path
    else:
        try:
            client = vision.ImageAnnotatorClient()
            with open(path, "rb") as image_file:
                content = image_file.read()
            image = vision.Image(content=content)
        except:
            return 'Invalid Url'

    response = client.label_detection(image=image)
    for label in response.label_annotations:
        labels.append(label.description)
    return labels


def logo_detection(path):
    logos = []
    
    if validators.url(path):
        client = vision.ImageAnnotatorClient()
        image = vision.Image()
        image.source.image_uri = path
    else:
        try:
            client = vision.ImageAnnotatorClient()
            with open(path, "rb") as image_file:
                content = image_file.read()
            image = vision.Image(content=content)
        except:
            return 'Invalid Url'

    response = client.logo_detection(image=image)
    for logo in response.logo_annotations:
        logos.append(logo.description)
    return logos
