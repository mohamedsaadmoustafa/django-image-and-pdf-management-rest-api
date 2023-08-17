#  Image and PDF Upload REST API
This Django project provides a REST API for uploading, retrieving, and deleting images and PDF files.

Endpoints
```
POST /api/upload/: Accepts image and PDF files in base64 format and saves them to the server.
GET /api/images/: Returns a list of all uploaded images.
GET /api/pdfs/: Returns a list of all uploaded PDFs.
GET /api/images/{id}/: Returns the details of a specific image, like the location, width, height, number of channels.
GET /api/pdfs/{id}/: Returns the details of a specific PDF, like the location, number of pages, page width, page height.
DELETE /api/images/{id}/: Deletes a specific image.
DELETE /api/pdfs/{id}/: Deletes a specific PDF.
POST /api/rotate/: Accepts an image ID and rotation angle, rotates the image, and returns the rotated image.
POST /api/convert-pdf-to-image/: Accepts a PDF ID, converts the PDF to an image, and returns the image.
```

### Models
The following models are used to store the images and PDF files:
  ```
  Image: Stores the image data, location, and other metadata.
  PDF: Stores the PDF data, location, and other metadata.
  ```
### Serializers
The following serializers are used to convert the models to JSON:
```
  ImageSerializer: Converts Image objects to JSON.
  PDFSerializer: Converts PDF objects to JSON.
  ```
### Views
The following views are used to handle the API endpoints:
  ```
  UploadView: Handles the POST /api/upload/ endpoint.
  ImagesView: Handles the GET /api/images/ and GET /api/images/{id}/ endpoints.
  PDFsView: Handles the GET /api/pdfs/ and GET /api/pdfs/{id}/ endpoints.
  DeleteImageView: Handles the DELETE /api/images/{id}/ endpoint.
  DeletePDFView: Handles the DELETE /api/pdfs/{id}/ endpoint.
  RotateImageView: Handles the POST /api/rotate/ endpoint.
  ConvertPDFToImageView: Handles the POST /api/convert-pdf-to-image/ endpoint.
```
  
### URLs
The following URLs are used to access the API endpoints:
```
  /api/upload/: POST
  /api/images/: GET
  /api/images/{id}/: GET
  /api/pdfs/: GET
  /api/pdfs/{id}/: GET
  /api/images/{id}/: DELETE
  /api/pdfs/{id}/: DELETE
  /api/rotate/: POST
  /api/convert-pdf-to-image/: POST
  ```


### Build the Docker image:
```
  docker build --tag django-image-and-pdf-management-rest-api .
  docker run --publish 8000:8000 django-image-and-pdf-management-rest-api
```

The API will be available at http://localhost:8000/api/.
