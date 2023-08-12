import PIL

def extract_image_details(image):
        img = PIL.Image.open(image)
        width, height = img.size
        channels = img.mode
        return {
                "width": width,
                "height": height,
                "channels": channels
        }