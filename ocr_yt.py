import pytesseract
import cv2 
import os 
import glob
import pandas as pd
from PIL import Image
import tabula
import fitz
pytesseract.pytesseract.tesseract_cmd="C:/Program Files/Tesseract-OCR/tesseract.exe"
from pdf2image import convert_from_path


pdf_file="Q1FY22 Result Note.pdf"

images = convert_from_path('Q1FY22 Result Note.pdf')
print(type(images))

def create_pages():
    #images = convert_from_path('E:/pdf-to-text-ocr/Q4FY21 Result Note.pdf')
    if not os.path.exists("pages"):
        os.mkdir("pages")
    else:
        print("Directory already exists.")
    for i in range(len(images)):
        images[i].save('pages/page'+ str(i) +'.jpg', 'JPEG')
create_pages()


def extract_text(image):
    #with Image.open(image_path) as img:
    text = pytesseract.image_to_string(image)
    return text


def combined_text():
    text_list = []
    for img in images:
        text = extract_text(img)
        text_list.append(text)

    all_text = "\n".join(text_list) 
    return all_text
text = combined_text()

def create_csv_text():
    df=pd.DataFrame({'text':text.split('\n')})
    df.to_csv('extracted_text.csv', index=False)
    file = open('extracted.txt', 'w')
    file.write(text)
    file.close()
create_csv_text() 


file_path = 'deepstream.pdf'
def get_images():
    pdf_file = fitz.open(file_path)
    if not os.path.exists("extracted_images"):
        os.mkdir("extracted_images")
    else:
        print("Directory already exists.")
    images_path = 'extracted_images/'
    page_nums = len(pdf_file)
    images_list = []
    for page_num in range(page_nums):
        page_content = pdf_file[page_num]
        images_list.extend(page_content.get_images())
    if len(images_list)==0:
        raise ValueError(f'No images found in {file_path}')
    
    for i, image in enumerate(images_list, start=1):
        xref = image[0]
        base_image = pdf_file.extract_image(xref)
        image_bytes = base_image['image']
        image_ext = base_image['ext']
        image_name = str(i) + '.' + image_ext
        with open(os.path.join(images_path, image_name) , 'wb') as image_file:
            image_file.write(image_bytes)
            image_file.close()
get_images()  


def extract_tables(pdf_file,output_dir):
    if not os.path.exists("extracted_tables"):
        os.mkdir("extracted_tables")
    dfs = tabula.read_pdf(pdf_file, pages='all')
    # print(dfs)
    # print(len(dfs))
    for i in range(len(dfs)):
        dfs[i].to_csv(f"extracted_tables/table_{i}.csv",index=False)
         
extract_tables(pdf_file,output_dir=extract_tables)