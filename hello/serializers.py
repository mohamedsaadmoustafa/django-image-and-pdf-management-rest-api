from rest_framework import serializers
from .models import *
from base64 import b64encode

class ImageSerializer(serializers.ModelSerializer):
    file = serializers.FileField(read_only=True)

    class Meta:
        model = Image
        fields = ('id', 'file', 'width', 'height', 'channels')

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['file'] = b64encode(instance.file.read()).decode('utf-8')
    #     return representation

class PdfSerializer(serializers.ModelSerializer):
    file = serializers.FileField(read_only=True)

    class Meta:
        model = Pdf
        fields = ('id', 'file', 'title', 'author', 'num_pages', 'page_width', 'page_height')

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['file'] = b64encode(instance.file.read()).decode('utf-8')
    #     return representation