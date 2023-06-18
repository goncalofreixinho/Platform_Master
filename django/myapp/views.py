from typing import List, Tuple, get_type_hints, Dict, Union
from myapp.models import Feedback
import base64
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
import torch
import datetime
from PIL import Image
import torchvision.transforms as transforms
from transformers import ViTFeatureExtractor, ViTForImageClassification
from TeseProjeto import settings
from transformers import pipeline

from typing import Dict, Union
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

try:
    from script import init
except ImportError:
    pass

try:
    from script import inference
except ImportError:
    pass

import importlib

# Import script.py as a module
script_module = importlib.import_module('script')

# Check if the init() function exists in the script module
if hasattr(script_module, 'init'):
    model = script_module.init()
else:
    # If the init() function does not exist, Model inside Inference is None
    model = None


@csrf_exempt
def api(request):
    global model

    if request.method == 'POST':
        # Check which input type is being used
        if 'image' in request.FILES:
            # Get image from HTTP request
            image = request.FILES['image']
            image_bytes = image.read()

            # Call the inference function and give the output (predicted class)
            result = inference(image)

            # Return the predicted class as a JSON object
            return JsonResponse({'class': result}, safe=False)

        elif 'image_bytes' in request.FILES:
            # Get image from HTTP request
            image = request.FILES['image_bytes']
            # Convert InMemoryUploadedFile image to bytes
            image_bytes = image.read()

            # Call the inference function and give the output (predicted class)
            result = inference(image_bytes)

            # Return the predicted class as a JSON object
            return JsonResponse({'class': result}, safe=False)

        elif 'context' in request.POST and 'question' in request.POST:
            # Get user input text from HTTP request
            context = request.POST.get('context', '')
            question = request.POST.get('question', '')

            # Call the inference function and give the output (answer)
            result = inference(context, question)

            # Add the custom keys to the result dictionary
            result = {'answer': result['answer'], 'score': result['score']}

            # Return the results as a JSON object
            return JsonResponse(result)

        elif 'text' in request.POST:
            current_time = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
            print(f"[{current_time}] THE REQUEST WAS SENT HERE!")
            # Get the text of the input
            text = request.POST.get('text')

            if model is None:
                predicted_class, probs = inference(text)
            else:  # Call the inference function and get the predicted class and probabilities
                predicted_class, probs = inference(text, model)

            # Return the predicted class and probabilities as a JSON object
            return JsonResponse({'predicted_class': predicted_class, 'probs': [probs]}, safe=False)

        elif 'prompt' in request.POST:
            prompt = request.POST.get('prompt')

            if model is None:
                text_generated = inference(prompt)
            else:
                text_generated = inference(prompt, model)

            # Return the predicted class  as a JSON object
            return JsonResponse({'text_generated': text_generated}, safe=False)

        else:
            # Return an error if no input type is found
            return JsonResponse({'error': 'Invalid input type'}, status=400)
    else:
        # Obtain the type of input and output of the inference function
        input_type = get_type_hints(inference).get('image') or get_type_hints(inference).get(
            'image_bytes') or get_type_hints(inference).get('text') or \
                     get_type_hints(inference).get('context' and 'question') or get_type_hints(inference).get('prompt')

        
        input_name = list(get_type_hints(inference).keys())[0]

        output_type = get_type_hints(inference).get('return')

        # Check the input and output type of the inference function to render the corresponding HTML page

        if input_name == 'image' and input_type == bytes and output_type == Tuple[str, float] or input_type == List[
            Tuple
            [str, List[float]]]:
            return render(request, 'Image_Classification.html')

        elif input_name == 'image_bytes' and input_type == bytes and output_type == List[
            Tuple[str, float, List[float]]]:
            return render(request, 'Object_Detection.html')

        elif input_type == str and output_type == Tuple[int, List[float]] or input_type == str and output_type == Tuple[
            str, List[float]] or input_type == str and output_type == Dict[str, Union[str, float]]:
            return render(request, 'Text_Classification.html')

        elif input_name == 'prompt' and input_type == str and output_type == str:
            return render(request, 'Text_Generator.html')

        elif input_type == str and output_type == str or input_type == str and output_type == dict[str]:
            return render(request, 'Translation.html')

        elif input_type == str and output_type == Dict[str, str] or input_type == str and output_type == Dict[str, str]:
            return render(request, 'QA.html')
        else:
            return render(request, 'error.html')


@csrf_exempt
def feedback_view(request):
    if request.method == 'POST':

        # Get the feedback text, rating, input and output
        feedback_text = request.POST.get('feedback_text')
        rating = request.POST.get('rating')
        user_input = request.POST.get('user_input')
        output = request.POST.get('output')
        user_input_image = request.POST.get('user_input_image')
        output_image = request.POST.get('output_image')

        # Saving the feedback and the values of the input and outputs in the database
        if feedback_text and rating and user_input and output:
            feedback = Feedback(model_type='Test Model', input_data=user_input, output_data=output,
                                feedback_text=feedback_text, rating=rating)

            feedback.save()

            return JsonResponse({'status': 'success'}, safe=False)

        elif feedback_text and rating and user_input_image and output_image:
            base64_image = user_input_image.split(',')[1]  # remove the prefix 'data:image/jpeg;base64,'
            image_bytes = base64.b64decode(base64_image)
            feedback = Feedback(model_type='Test Model', image_data=image_bytes, output_data=output_image,
                                feedback_text=feedback_text, rating=rating)
            feedback.save()

            return JsonResponse({'status': 'success'}, safe=False)
        else:
            return JsonResponse({'status': 'error', 'message': 'Feedback_text, rating, input and output are required'},
                                status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


def feedback_list(request, token):
    # Checks if the token is valid
    if token != settings.TOKEN_SECRET:
        return HttpResponseForbidden('Token inválido!')

    feedback_list = Feedback.objects.all()
    for feedback in feedback_list:
        if feedback.image_data:
            encoded_image = base64.b64encode(feedback.image_data).decode('utf-8')
            feedback.image_data = encoded_image
    return render(request, 'feedback_list.html', {'feedback_list': feedback_list})
