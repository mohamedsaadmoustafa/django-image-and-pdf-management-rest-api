from django.urls import path
from .views import *


urlpatterns = [
    path('upload/', UploadView.as_view(), name='upload'),

    path('images/', ImageView.as_view(), name='image-list'),
    path('pdfs/', PdfView.as_view(), name='pdf-list'),

    path('images/<int:pk>/', ImageDetailsView.as_view(), name='image-details'),
    path('pdfs/<int:pk>/', PdfDetailsView.as_view(), name='pdf-details'),

    path('images/<int:pk>/', ImageDetailsView.as_view(), name='image-delete'),
    path('pdfs/<int:pk>/', PdfDetailsView.as_view(), name='pdf-delete'),

    path('rotate/', ImageRotationView.as_view(), name='image-rotate'),
    path('convert-pdf-to-image/', PdfToImageView.as_view(), name='pdf-to-image'),
]
