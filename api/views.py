from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser, JSONParser
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
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

    def post(self, request, *args, **kwargs):
        # Getting Image and filter name
        request_data = QueryDict.dict(request.data)
        filter_name = int(request_data['filter_name'])
        image = request.FILES['file']
        # imageName = request_data.get('name')
        path = default_storage.save("inputs/upload/" + str(image), ContentFile(image.read()))

        save_restore_path = inference("media/"+path)

        # Adding Filter to image
        img = Image.open(save_restore_path)

        if filter_name == 1:
            filtered_img = img
        elif filter_name == 2:
            filtered_img = img
        elif filter_name == 3:
            filtered_img = img
        elif filter_name == 4:
            filtered_img = img
        else:
            filtered_img = img

        model_instance = FilterImg()

        # Saving the filtered image for download
        f = BytesIO()
        try:
            filtered_img.save(f, format='png')
            model_instance.image.save(str(random.random())+'.png',
                                        ContentFile(f.getvalue()))
            model_instance.save()
        finally:
            f.close()

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