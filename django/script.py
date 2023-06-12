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

   # Carregar o modelo pré-treinado para classificação de texto
    model = pipeline(
        "text-classification",
        model="distilbert-base-uncased-finetuned-sst-2-english",

    )
    # Retornar o modelo carregado
    return model


def inference(text: str, model) -> Tuple[int, List[float]]:
    # Passar o input pelo modelo para obter as probabilidades para todas as classes
    result = model(text)[0]
    predicted_class = result['label']
    probs = result['score']

    # Retornar a classe prevista e e a sua probabilidade
    return predicted_class, probs

