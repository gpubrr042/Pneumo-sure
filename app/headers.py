from flask import *
import os
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
from app import app



prediction_key = "1382241948aa47e49236b0f499eb8c5c"
publish_iteration_name = "Pneumonia"
ENDPOINT = "https://southeastasia.api.cognitive.microsoft.com/"
projectId = "f57285e6-1023-486e-8e20-8f582abca681"
# prediction_key = "your-prediction key"
# publish_iteration_name = "classifyModel"
# ENDPOINT = "your-endpoint"
# projectId = "your project id"
