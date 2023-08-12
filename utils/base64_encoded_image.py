from io import BytesIO
from base64 import b64encode


def base64_encoded_image(image, format='PNG'):
    # Convert the image to base64-encoded string
    buffered = BytesIO()
    image.save(buffered, format=format)
    base64_encoded = b64encode(buffered.getvalue()).decode()
    return base64_encoded