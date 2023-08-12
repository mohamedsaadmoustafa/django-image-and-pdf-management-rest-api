from django.urls import path
from . import views


urlpatterns = [
    path('upload/', views.UploadView.as_view()),

    path('images/', views.ImageView.as_view()),
    path('images/<int:pk>/', views.ImageDetailsView.as_view()),

    path('pdfs/', views.PdfView.as_view()),
    path('pdfs/<int:pk>/', views.PdfDetailsView.as_view()),

    path('images/<int:pk>/delete/', views.ImageDeleteView.as_view()),
    path('pdfs/<int:pk>/delete/', views.PdfDeleteView.as_view()),

    path('rotate/', views.ImageRotationView.as_view()),
    path('convert-pdf-to-image/', views.PdfToImageView.as_view()),
]