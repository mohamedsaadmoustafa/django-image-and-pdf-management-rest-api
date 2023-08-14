import logging

from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import InMemoryUploadedFile

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status

from .models import Image, Pdf
from .serializers import ImageSerializer, PdfSerializer

from utils.extract_details import *
from utils.file_converter import *
from utils.validation import *


# Get an instance of a logger
logger = logging.getLogger(__name__)

class UploadView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        data = request.POST
        base64_string = data.get("base64_string")

        file, file_extension, data_string = decode_base64_string(base64_string)

        if file_extension.lower() in ["jpg", "jpeg", "png"]:
            image_details = extract_image_details(file)

            image = Image(file=base64_string, **image_details)
            image.save()
            serializer = ImageSerializer(image)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif file_extension == 'pdf':
            pdf_details = extract_pdf_details(file)

            pdf = Pdf(file=base64_string, **pdf_details)
            pdf.save()
            serializer = PdfSerializer(pdf)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response('Invalid file type.', status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

class ImageView(APIView):
    def get(self, request, format=None):
        image = Image.objects.all()
        serializer = ImageSerializer(image, many=True)
        return Response(serializer.data)


class PdfView(APIView):
    def get(self, request, format=None):
        pdf = Pdf.objects.all()
        serializer = PdfSerializer(pdf, many=True)
        return Response(serializer.data)


class ImageDetailsView(APIView):
    def get(self, request, pk, format=None):
        try:
            image = Image.objects.get(pk=pk)
            serializer = ImageSerializer(image)
            return Response(serializer.data)
        except Image.DoesNotExist:
            return Response('Image not found.', status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        try:
            image = Image.objects.get(pk=pk)
            # image_path = image.file.path
            image.delete()

            # # Delete the file from media storage
            # if default_storage.exists(image_path):
            #     default_storage.delete(image_path)

            return Response('Image deleted successfully.', status=status.HTTP_204_NO_CONTENT)
        except Image.DoesNotExist:
            return Response('Image not found.', status=status.HTTP_404_NOT_FOUND)

class PdfDetailsView(APIView):
    def get(self, request, pk, format=None):
        try:
            pdf = Pdf.objects.get(pk=pk)
            serializer = PdfSerializer(pdf)
            return Response(serializer.data)
        except Pdf.DoesNotExist:
            return Response('Pdf not found.', status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        try:
            pdf = Pdf.objects.get(pk=pk)
            # pdf_path = pdf.file.path
            pdf.delete()

            # # Delete the file from media storage
            # if default_storage.exists(pdf_path):
            #     default_storage.delete(pdf_path)

            return Response('Pdf deleted successfully.', status=status.HTTP_204_NO_CONTENT)
        except Pdf.DoesNotExist:
            return Response('Pdf not found.', status=status.HTTP_404_NOT_FOUND)


class ImageRotationView(APIView):
    def post(self, request, format=None):
        id = request.POST.get('id')
        degree = request.POST.get('rotation_angle')
        if not id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            degree = int(degree)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        image_row = Image.objects.get(pk=id)
        if not image_row:
            return Response(status=status.HTTP_404_NOT_FOUND)

        base64_string = image_row.file
        image = decode_base64_string(base64_string)[0]
        image = PIL.Image.open(image)
        rotated_image = image.rotate(degree)
        return Response(PostImage(rotated_image))



class PdfToImageView(APIView):
    def post(self, request, format=None):
        id = request.POST.get('id')
        if not id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        pdf_file = Pdf.objects.get(pk=id)
        if not pdf_file:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            pdf_base64_string = pdf_file.file
            pdf_file, file_extension, data_string = decode_base64_string(pdf_base64_string)
            pdf_images = pdf_bytes_to_image(pdf_file)
        except Exception as e:
            err = f"Unable to convert PDF to image.\n {e}"
            return Response(err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if pdf_images:
            image = pdf_images[0]
            base64_encoded = PostImage(image)
            return Response(base64_encoded)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)