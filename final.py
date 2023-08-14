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

pdf_path=input("Enter a pdf file path: ")

def create_folder():
    pdf_name=os.path.splitext(os.path.basename(pdf_path))[0] 

    new_folder_path = os.path.join(os.path.dirname(pdf_path),pdf_name)
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
        print(f"Created a new folder '{pdf_name}' at '{new_folder_path}'")
    else:
        print(f"Folder '{pdf_name}' already exists at '{new_folder_path}'")

    images_path = os.path.join(new_folder_path, "Pages")
    print("image path is...",images_path)
    Extracted_data = os.path.join(new_folder_path, "Extracted_data")
    print("path to extracted data: ",Extracted_data)
    Extracted_images = os.path.join(new_folder_path,"Extracted_images")
    if not os.path.exists(Extracted_images):
        os.makedirs(Extracted_images)
    if not os.path.exists(images_path ):
        os.makedirs(images_path)
    if not os.path.exists(Extracted_data):
        os.makedirs(Extracted_data)
    print(f"Created two folders under '{pdf_name}' folder: '{images_path}' and '{ Extracted_data}'")
   
    
    create_pages(pdf_path, images_path, pdf_name,Extracted_data,Extracted_images)

def create_pages(pdf_path,images_path,pdf_name,Extracted_data,Extracted_images):
    images = convert_from_path(pdf_path)
    for i,page in enumerate(images):
        image_path = os.path.join(images_path,f"{pdf_name}_page{i+1}.jpg")
        page.save(image_path,"JPEG")
        print(image_path,"image path is")
        print(f"Saved page {i+1} as '{image_path}'")

    extract_text(images,Extracted_data,pdf_name,Extracted_images)
def extract_text(images,Extracted_data,pdf_name,Extracted_images):
    text_list = []
    for img in images:
        text = pytesseract.image_to_string(img)
        text_list.append(text)
    
    all_text = "\n".join(text_list)
    # print(all_text)
    with open(os.path.join(Extracted_data,"Extracted.txt"),"w") as file:
        file.write(all_text)

    
    extract_table(pdf_path,Extracted_data,pdf_name,Extracted_images)
def extract_table(pdf_path,Extracted_data,pdf_name,Extracted_images):
    dfs = tabula.read_pdf(pdf_path, pages='all')
    for i,df in enumerate(dfs):
        table_path = os.path.join(Extracted_data,f"{pdf_name}_table_{i+1}.csv")
        df.to_csv(table_path,index=False) #, {pdf_name}_{i}.csv,index=False)
   
    get_images(pdf_path,Extracted_images)
def get_images(pdf_path,Extracted_images):
    pdf_file = fitz.open(pdf_path)
    page_nums = len(pdf_file)
    images_list = []
    for page_num in range(page_nums):
        page_content = pdf_file[page_num]
        images_list.extend(page_content.get_images())
    if len(images_list)==0:
        raise ValueError(f'No images found in {pdf_path}')
    
    for i, image in enumerate(images_list, start=1):
        xref = image[0]
        base_image = pdf_file.extract_image(xref)
        image_bytes = base_image['image']
        image_ext = base_image['ext']
        image_name = str(i) + '.' + image_ext
        images_path = os.path.join(Extracted_images,image_name)
        with open((images_path) , 'wb') as image_file:
            image_file.write(image_bytes)
            image_file.close()

create_folder() 
