# Imports the Google Cloud client library
from google.cloud import vision
import os


def run_quickstart():
    image = "gs://cloud-samples-data/vision/label/wakeupcat.jpg"
    return detect_image(image)


def detect_image(image_file) -> vision.EntityAnnotation:
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = image_file

    response = client.label_detection(image=image)
    labels = response.label_annotations
    output = []
    for label in labels:
        output.append(label.description)
    return output