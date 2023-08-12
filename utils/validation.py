def validate_file_type(file):
    return file.content_type.startswith('image') or file.content_type.startswith('application/pdf')


def validate_file_size(file):
    return file.size < 10000000


def validate_image_dimensions(image_details):
    return image_details['width'] < 1000 or image_details['height'] < 1000