import logging, os

from django.http import HttpResponse
from django.core.files.storage import default_storage

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from pdf2image import convert_from_path, convert_from_bytes
from PIL import Image as PILImage

from .models import Image, Pdf
from .serializers import ImageSerializer, PdfSerializer
from utils.extract_details import *
from utils.base64_encoded_image import base64_encoded_image
from utils.validation import *


# Get an instance of a logger
logger = logging.getLogger(__name__)

class UploadView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        file = request.FILES.get('file')
        if not file:
            logger.warning("No file specified for upload request")
            return Response('No file specified for upload request', status=status.HTTP_400_BAD_REQUEST)

        if not validate_file_type(file):
            logger.warning("Invalid file type.")
            return Response('Invalid file type.', status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

        if not validate_file_size(file):
            logger.warning("File size is too large.")
            return Response('File size is too large.', status=status.HTTP_413_PAYLOAD_TOO_LARGE)

        if file.content_type.startswith('image'):
            # Check if image is already present
            image_exists = Image.objects.filter(file=file).exists()
            # ToDo: fix -> check if image exists
            if image_exists:
                logger.warning("Image with the same file already exists")
                return Response('Image with the same file already exists', status=status.HTTP_400_BAD_REQUEST)

            image_details = extract_image_details(file)

            # Validate image dimensions
            if not validate_image_dimensions(image_details):
                err = f"Image dimensions must be less than 1000x1000.\nImage dimensions: {image_details}"
                logger.warning(err)
                return Response(err, status=status.HTTP_400_BAD_REQUEST)

            image = Image(file=file, **image_details)
            image.save()
            logger.info(f"Image with name {file} saves successfully")
            serializer = ImageSerializer(image)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif file.content_type.startswith('application/pdf'):
            # Check if pdf is already present
            pdf_exists = Image.objects.filter(file=file).exists()

            # ToDo: fix -> check if pdf exists
            if pdf_exists:
                logger.warning("Pdf with the same file already exists")
                return Response('Pdf with the same file already exists', status=status.HTTP_400_BAD_REQUEST)
            pdf_details = extract_pdf_details(file)

            pdf = Pdf(file=file, **pdf_details)
            pdf.save()
            logger.info(f"Pdf with name {file} saves successfully")
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
            image_path = image.file.path
            image.delete()

            # Delete the file from media storage
            if default_storage.exists(image_path):
                default_storage.delete(image_path)

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
            pdf_path = pdf.file.path
            pdf.delete()

            # Delete the file from media storage
            if default_storage.exists(pdf_path):
                default_storage.delete(pdf_path)

            return Response('Pdf deleted successfully.', status=status.HTTP_204_NO_CONTENT)
        except Pdf.DoesNotExist:
            return Response('Pdf not found.', status=status.HTTP_404_NOT_FOUND)


class ImageRotationView(APIView):
    def post(self, request, format=None):
        id = request.POST.get('id')
        degree = request.POST.get('rotation_angle')
        image_file = Image.objects.get(pk=id).file

        image = PILImage.open(image_file)
        rotated_image = image.rotate(int(degree))
        base64_encoded = base64_encoded_image(rotated_image)
        response = HttpResponse(base64_encoded, content_type='image/png')
        return response


class PdfToImageView(APIView):
    def post(self, request, format=None):
        id = request.POST.get('id')
        pdf_file = Pdf.objects.get(pk=id)
        pdf_file_bytes = pdf_file.file.read()

        try:
            pdf_images = convert_from_bytes(pdf_file_bytes)
            image = pdf_images[0]
            base64_encoded = base64_encoded_image(image)
            return Response(base64_encoded, content_type='image/png')

        except Exception as e:
            err = f"Unable to convert PDF to image.\n {e}"
            return Response(err, status=status.HTTP_400_BAD_REQUEST)