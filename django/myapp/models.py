from django.db import models


class Feedback(models.Model):
    model_type = models.CharField(max_length=255)
    input_data = models.TextField(null=True, blank=True)
    image_data = models.BinaryField(null=True, blank=True)
    output_data = models.TextField()
    feedback_text = models.TextField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(null=True, blank=True)
