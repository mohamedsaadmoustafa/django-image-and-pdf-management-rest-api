import PIL
import pdfplumber
import datetime


def extract_pdf_details(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        try:
            title = pdf.metadata['Title']
        except:
            title = ""
        try:
            author = pdf.metadata['Author']
        except:
            author = ""
        num_pages = len(pdf.pages)
        page_width = pdf.pages[0].width
        page_height = pdf.pages[0].height

        return {
            'title': title,
            'author': author,
            'num_pages': num_pages,
            'page_width': page_width,
            'page_height': page_height,
        }


def extract_image_details(image):
        img = PIL.Image.open(image)
        width, height = img.size
        channels = img.mode
        return {
                "width": width,
                "height": height,
                "channels": channels
        }