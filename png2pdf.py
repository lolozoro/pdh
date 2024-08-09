import fitz  # PyMuPDF
import re
import os
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

pytesseract.pytesseract.tesseract_cmd = r'D:/shix_2024/ocr/tesseract.exe'

def preprocess_image(image_path):
    image = Image.open(image_path)
    # 转换为灰度图像
    image = image.convert('L')
    # 增强对比度
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)
    # 调整二值化阈值
    image = image.point(lambda x: 0 if x < 150 else 255, '1')
    # 去噪
    image = image.filter(ImageFilter.MedianFilter())
    return image

def extract_text_from_image(image_path):
    # 预处理图片
    image = preprocess_image(image_path)
    # 使用Tesseract OCR从图片中提取文本
    text = pytesseract.image_to_string(image, lang='chi_sim', config='--psm 6')
    return text

def insert_markers_in_pdf(pdf_path, output_pdf_path):
    # 打开 PDF 文件
    pdf_document = fitz.open(pdf_path)

    # 创建一个新的 PDF 文档
    output_pdf_document = fitz.open()

    # 遍历每一页
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        new_page = output_pdf_document.new_page(width=page.rect.width, height=page.rect.height)

        # 提取图片中的文本
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_path = f"image_{page_num}_{img_index}.{image_ext}"
            with open(image_path, "wb") as img_file:
                img_file.write(image_bytes)
            image_text = extract_text_from_image(image_path)
            os.remove(image_path)  # 删除临时图片文件

            # 将提取的文本添加到新页面
            text_box = fitz.Rect(50, 50, page.rect.width - 50, page.rect.height - 50)
            new_page.insert_textbox(text_box, image_text, fontsize=12, color=(0, 0, 0))

    # 保存新的 PDF 文件
    output_pdf_document.save(output_pdf_path)

# 使用示例
pdf_path = 'D:/shix_2024/公司规章制度/信息公司管理制度1/信息公司管理制度/01管理制度（截至2023年末）/人力资源部/1.北信司文〔2021〕3号关于印发《北大荒信息有限公司高层次和急需紧缺专业人才引进管理的实施方案（试行）》的通知.pdf'
output_pdf_path = 'D:/shix_2024/公司规章制度/划分段落/信息公司管理制度/01管理制度（截至2023年末）/招聘数据/output.pdf'
insert_markers_in_pdf(pdf_path, output_pdf_path)
