from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser, JSONParser
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
# Import required image modules
from PIL import Image, ImageFilter

# Import all the enhancement filter from pillow
# Can import and use filters according to your self
from PIL.ImageFilter import (
   CONTOUR, DETAIL, EDGE_ENHANCE,EMBOSS
)

from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

import random
import os

from inference_gfpgan import inference
from .models import *

from django.conf import settings

from django.http import QueryDict

class Filter(APIView):
    parser_classes = (JSONParser, MultiPartParser, FileUploadParser, FormParser, )

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        # Getting Image and filter name
        request_data = QueryDict.dict(request.data)
        filter_name = int(request_data['filter_name'])
        image = request.FILES['img_name']
        print("///////////////////////:", image)
        # imageName = request_data.get('name')

        # Adding Filter to image
        img = Image.open(image)

        if filter_name == 1:
            filtered_img = img.filter(CONTOUR)
        elif filter_name == 2:
            filtered_img = img.filter(DETAIL)
        elif filter_name == 3:
            filtered_img = img.filter(EDGE_ENHANCE)
        elif filter_name == 4:
            filtered_img = img.filter(EMBOSS)
        else:
            filtered_img = img.filter(DETAIL)


        print("**************************", filtered_img)

        model_instance = FilterImg()

        print("teeeeeeeeeeeeeeeeeeeeeeeest 1")
        # Saving the filtered image for download
        f = BytesIO()
        print("teeeeeeeeeeeeeeeeeeeeeeeest 2")
        try:
            filtered_img.save(f, format='png')
            print("teeeeeeeeeeeeeeeeeeeeeeeest 3")
            model_instance.image.save(str(random.random())+'.png',
                                        ContentFile(f.getvalue()))
            print("teeeeeeeeeeeeeeeeeeeeeeeest 4")
            model_instance.save()
            print("teeeeeeeeeeeeeeeeeeeeeeeest 5")
        finally:
            f.close()

        print("teeeeeeeeeeeeeeeeeeeeeeeest 6")

        print("Response(str(model_instance.image.url)) : ", Response(str(model_instance.image.url)))
        return Response(str(model_instance.image.url))

# View to clear database objects and images in folders
@api_view(['GET'])
def clear(request):
    for file in os.listdir(f'{settings.BASE_DIR}/media/images'):
        if file.endswith('.png'):
            os.remove(f'{settings.BASE_DIR}/media/images/{file}')

    FilterImg.objects.all().delete()

    for file in os.listdir(f'{settings.BASE_DIR}/inputs/upload'):
        if file.endswith('.png'):
            os.remove(f'{settings.BASE_DIR}/inputs/upload/{file}')

    FilterImg.objects.all().delete()

    return Response("Data Cleared")