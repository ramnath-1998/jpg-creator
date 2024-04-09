import os
from pdf2image import convert_from_path
import uuid
from PIL import Image
from io import BytesIO
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image as ReportLabImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"File removed successfully. - {file_path}")
    else:
        print("The file does not exist.")


def create_heading_jpg(main_content, heading, image_identifier):

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
        page.save(f'{image_identifier}-o.jpg', 'JPEG')

    delete_file("./"+image_identifier+".pdf")
    delete_file("./"+image_identifier+".jpg")


def create_data_jpg(main_content, image_identifier):

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
        page.save(f'{image_identifier}-o.jpg', 'JPEG')

    delete_file("./"+image_identifier+".pdf")
    delete_file("./"+image_identifier+".jpg")




def crop_center(image, crop_width, crop_height):
    ratio = crop_width / float(image.size[0])
    height = int(float(image.size[1]) * float(ratio))
    resized_img = image.resize((crop_width, height), Image.LANCZOS)
    width, height = resized_img.size
    left = (width - crop_width) // 2
    top = (height - crop_height) // 2
    right = (width + crop_width) // 2
    bottom = (height + crop_height) // 2
    return resized_img.crop((left, top, right, bottom))





def save_bytes_as_image(image_bytes):
    img = Image.open(BytesIO(image_bytes))
    img = crop_center(img,1080,540)
    global image_identifier
    image_identifier = str(uuid.uuid4())
    img.save(image_identifier+".jpg")
    return image_identifier

def handle_create_image(post_type, content, heading, image_identifier):
    if post_type == "Post with content only":
        create_data_jpg(content, image_identifier)
    elif post_type == "Post with heading and content":
        create_heading_jpg(content,heading, image_identifier)

def main():
    st.set_page_config("Create a Post | Whatsaround UPSC")
    st.header("Create the Insta Post")
    post_type = st.selectbox("Select the type of Post", ("Post with content only","Post with heading and content"))
    content = ""
    heading = ""
    if post_type == "Post with content only":
        content = st.text_area("Enter the Content here")
    elif post_type == "Post with heading and content":
        heading = st.text_area("Enter the heading here")
        content = st.text_area("Enter the content here")
    image = st.file_uploader("Upload the image file", accept_multiple_files=False)
    image_identifier = ""
    if image is not None:
        image_bytes = image.getvalue()
        image_identifier = save_bytes_as_image(image_bytes)
        if st.button("Create Image", on_click=handle_create_image(post_type, content,heading, image_identifier)):
            print(image_identifier)
            with st.spinner("Creating image..."):    
                with open(f"./{image_identifier}-o.jpg", "rb") as file:
                    st.download_button(
                        label="Download image",
                        data=file,
                        file_name=f"{image_identifier}-o.jpg",
                        mime="image/jpg"
                    )
                st.success("Done")
    
    delete_file(f"./{image_identifier}-o.jpg")
    st.empty()

if __name__ == "__main__":
    main()