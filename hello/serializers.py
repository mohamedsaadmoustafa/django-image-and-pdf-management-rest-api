from rest_framework import serializers
from .models import *

class ImageSerializer(serializers.ModelSerializer):
    file = serializers.FileField(read_only=True)

    class Meta:
        model = Image
        fields = ('id', 'file', 'width', 'height', 'channels')


class PdfSerializer(serializers.ModelSerializer):
    file = serializers.FileField(read_only=True)

    class Meta:
        model = Pdf
        fields = ('id', 'file', 'title', 'author', 'num_pages', 'page_width', 'page_height')
