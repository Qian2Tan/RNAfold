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
    site_data.fillna('', inplace=True)

    site_data['sequence'] = site_data['sequence'] + '<br>' + site_data['RNAfold']

    def combine_columns(row):
    # 如果 sequence_modi_prune 是 "special case"，則返回原值
        if row['sequence_modi_prune'] == 'special case' or row['sequence_modi_prune'] == 'no modified':
            return row['sequence_modi_prune']
        else:
            # 否則合併 sequence_modi_prune 和 rnafold_modi_prune
            return row['sequence_modi_prune'] + '<br>' + row['rnafold_modi_prune']

    # 使用 apply 函式將 combine_columns 函式應用到 DataFrame 的每一行
    site_data['sequence_modi_prune'] = site_data.apply(lambda row: combine_columns(row), axis=1)

    if version == 'up45down9':
        site_data['TTS_sequence(include_8nt_of_each_flank_sequence)'] = pd.DataFrame(site_data['TTS_sequence(include_8nt_of_each_flank_sequence)'] +'<br>'+ site_data['predicted_RNA_fold_structure'])


    print(site_data)
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
