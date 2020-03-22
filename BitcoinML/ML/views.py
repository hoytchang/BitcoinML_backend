from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
import os
import json
from ML.Predict import Model

def index(request):
    return HttpResponse("Hello, world.")

def read_json(name):
    # Read in json files
    # TODO: read from db instead of json file
    # TODO: populate db with data
    filename = os.path.join(os.getcwd(),"ML")
    filename = os.path.join(filename,"data")
    filename = os.path.join(filename,name+'.json')
    with open(filename, 'r') as openfile:
        json_object = json.load(openfile)
    return json_object

@api_view()
def price(request):
    return JsonResponse(read_json('market-price'))

@api_view()
def hashRate(request):
    return JsonResponse(read_json('hash-rate'))

@api_view()
def nTransactions(request):
    return JsonResponse(read_json('n-transactions'))

@api_view()
def nUniqueAddresses(request):
    return JsonResponse(read_json('n-unique-addresses'))

@api_view()
def predict(request, model_settings):
    model = Model(model_settings)
    model.build_model()
    prediction = model.predict()
    return HttpResponse("predict = " + str(prediction))