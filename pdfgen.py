import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from pdf2image import convert_from_path
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image as ReportLabImage, PageTemplate,Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print("File removed successfully.")
    else:
        print("The file does not exist.")


def create_heading_jpg(main_content, heading, image_identifier, post_type):

    pdfmetrics.registerFont(TTFont('Montserrat', './fonts/Montserrat-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('Roboto-Light', './fonts/Roboto-Medium.ttf'))
    image_path = "./"+ image_identifier+".jpg"
    styles = getSampleStyleSheet()
    heading_style = ParagraphStyle(
        'HeadingStyle',
        parent=styles['Normal'],  
        fontSize=46,  
        fontName='Roboto-Light',
        leading=30
    )

    content_style = ParagraphStyle(
        'ContentStyle',
        parent=styles['Normal'],  
        fontSize=34,  
        fontName='Montserrat',
        leading=40
    )
    footer_style = ParagraphStyle(
        'ContentStyle',
        parent=styles['Normal'],  
        fontSize=25,  
        fontName='Montserrat',
        leading=25
    )
    
    doc = SimpleDocTemplate("./"+image_identifier+".pdf", pagesize=(1080,1080))
    
    flowables = []

    img = ReportLabImage(image_path, width=940, height=540)  # Adjust width and height as needed
    flowables.append(img)
    flowables.append(Paragraph("<br/><br/>", heading_style))

    p = Paragraph(heading, style=heading_style)
    flowables.append(p)
    flowables.append(Paragraph("<br/><br/>", heading_style))

    p = Paragraph(main_content, style=content_style)   
    flowables.append(p)
    flowables.append(Paragraph("<br/><br/>", content_style))
    
    p = Paragraph("@whatsaroundUPSC", style=footer_style)   
    flowables.append(p)
    doc.build(flowables)

    pages = convert_from_path("./"+image_identifier+".pdf", 500)
    for count, page in enumerate(pages):
        page.save(f'{image_identifier}-created.jpg', 'JPEG')



def create_data_jpg(main_content, heading, image_identifier, post_type):

    pdfmetrics.registerFont(TTFont('Montserrat', './fonts/Montserrat-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('Roboto-Light', './fonts/Roboto-Medium.ttf'))
    image_path = "./"+ image_identifier+".jpg"
    styles = getSampleStyleSheet()

    content_style = ParagraphStyle(
        'ContentStyle',
        parent=styles['Normal'],  
        fontSize=34,  
        fontName='Montserrat',
        leading=40
    )
    footer_style = ParagraphStyle(
        'ContentStyle',
        parent=styles['Normal'],  
        fontSize=25,  
        fontName='Montserrat',
        leading=10
    )
    
    doc = SimpleDocTemplate("./"+image_identifier+".pdf", pagesize=(1080,1080))
    
    flowables = []

    img = ReportLabImage(image_path, width=940, height=540)  # Adjust width and height as needed
    flowables.append(img)
    flowables.append(Paragraph("<br/><br/>", content_style))

    p = Paragraph(main_content, style=content_style)   
    flowables.append(p)
    flowables.append(Paragraph("<br/><br/>", content_style))
    
    p = Paragraph("@whatsaroundUPSC", style=footer_style)   
    flowables.append(p)
    doc.build(flowables)

    pages = convert_from_path("./"+image_identifier+".pdf", 500)
    for count, page in enumerate(pages):
        page.save(f'{image_identifier}-created.jpg', 'JPEG')






def crop_center(image, crop_width, crop_height):
    ratio = crop_width / float(img.size[0])
    height = int(float(img.size[1]) * float(ratio))
    resized_img = img.resize((crop_width, height), Image.LANCZOS)
    width, height = resized_img.size
    left = (width - crop_width) // 2
    top = (height - crop_height) // 2
    right = (width + crop_width) // 2
    bottom = (height + crop_height) // 2
    return resized_img.crop((left, top, right, bottom))

img = Image.open("./2399ef54-1407-4160-b8e6-9b6ee67750as.jpg")
img = crop_center(img,1080,540)
global image_identifier
image_identifier = "2399ef54-1407-4160-b8e6-9b6ee67750as"
img.save(image_identifier+".jpg")
# main_content = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
main_content = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s."

heading = "Sample Heading Lorem Ipsum"
create_data_jpg(main_content,heading,image_identifier,"")