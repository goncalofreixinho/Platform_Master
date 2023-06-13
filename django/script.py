from typing import Tuple

from django.shortcuts import render
from django.http import JsonResponse

import torch
from django.views.decorators.csrf import csrf_exempt
import torchvision.transforms as transforms
from PIL import Image
from transformers import ViTFeatureExtractor, ViTForImageClassification


from transformers import pipeline
from typing import Tuple, List
import torch


def init():

   # Load the pre-trained template for text classification
    model = pipeline(
        "text-classification",
        model="distilbert-base-uncased-finetuned-sst-2-english",

    )
    # Return the loaded model
    return model


def inference(text: str, model) -> Tuple[int, List[float]]:
    # Pass the input through the model to obtain the probabilities for all classes
    result = model(text)[0]
    predicted_class = result['label']
    probs = result['score']

    # Return the predicted class e and its probability
    return predicted_class, probs
