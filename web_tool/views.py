from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import pandas as pd
import os
import base64

def web(request):
    return (render(request, "RNAfold.html"))

@csrf_exempt
def read_csv(request):
    version = request.POST['version']

    path = f"/home/xiangwei/chien/rnafold/static/csv_result/{version}.csv"
    site_data = pd.read_csv(path)
    print(site_data)
    site_data['sequence'] = site_data['sequence'] + '<br>' + site_data['RNAfold']
    dict_site_data = site_data.to_dict(orient='records')

    response={
        "site_data": dict_site_data,
    }
    return JsonResponse(response)

def get_picture(request):
    version = request.POST['version']
    picture_index = request.POST['index']
    print(picture_index)

    file_name = f"{picture_index}_ss_1.png"
    path = f"/home/xiangwei/chien/rnafold/static/picture/{version}_pictures_png/{file_name}"
    with open(path, 'rb') as f:
        image_data = f.read()
    encoded_image = base64.b64encode(image_data).decode('utf-8')

    response = {
        'error': '',
        'image': encoded_image
    }

    return JsonResponse(response)
