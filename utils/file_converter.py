import base64
import pdf2image
import PIL
import io
import base64
from django.core.files.base import ContentFile


def decode_base64_string(base64_string):
    """Decodes a base64 string.
    Args:
        base64_string: The base64 string to decode.
    Returns:
        The file, file extension, data string
    """
    data_format, data_string = base64_string.split(';base64,')
    details = data_format.split('/')
    file_extension = details[-1]
    #content_type = details[0].split(':')[-1]
    file = ContentFile(
      base64.b64decode(data_string),
      name='temp.' + file_extension
    )
    return file, file_extension, data_string


def file_to_base64(file):
  """Converts a file to a Base64 string.
  Args:
    uploaded file: The file to convert.
  Returns:
    The Base64 string.
  """
  bytes_io =io.BytesIO(file.read())
  base64_string = base64.b64encode(bytes_io.getvalue()).decode('utf-8')
  return base64_string


def pdf_bytes_to_image(pdf_data):
  """Converts a PDF to images.
  Args:
    pdf_data: The PDF data to convert.
  Returns:
    A list of images.
  """
  images = pdf2image.convert_from_bytes(pdf_data.read())
  return images


def base64_encoded_image(image, format='PNG'):
  """Converts an image to a base64-encoded string.
  Args:
    image: The image to convert.
    format: The format of the image to convert.
  Returns:
    The base64-encoded string of the image.
  """
  buffered = io.BytesIO()
  image.save(buffered, format=format)
  base64_encoded = base64.b64encode(buffered.getvalue()).decode()
  return base64_encoded


def PostImage(image, format='PNG'):
  """Converts an image to a base64-encoded string and returns it as a POST request.
  Args:
    image: The image to convert.
    format: The format of the image to convert.
  Returns:
    The base64-encoded string of the image as a POST request.
  """
  rawBytes = io.BytesIO()
  image.save(rawBytes, "JPEG")
  rawBytes.seek(0)
  img_base64 = base64.b64encode(rawBytes.getvalue()).decode('ascii')
  mime = "image/jpeg"
  return "data:%s;base64,%s" % (mime, img_base64)