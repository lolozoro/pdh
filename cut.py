import fitz  # PyMuPDF
import re
import os

def insert_markers_in_pdf(pdf_path, txt_path):
    # 打开 PDF 文件
    pdf_document = fitz.open(pdf_path)

    # 初始化一个空的文本字符串
    text_content = ""

    # 遍历每一页
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text = page.get_text("text")

        # 在每个章节前插入标识符 <<<
        # 这里假设每个章节以“第一章”、“第二章”等形式开头
        text = re.sub(r'第[一二三四五六七八九十百千]+章', r'<<<\n\g<0>', text)

        text_content += text

    # 检查文本内容中是否包含“第几章”
    if '第' in text_content and '章' in text_content:
        # 如果包含“第几章”，则不在一二等标题前加 <<<
        pass
    else:
        # 如果不包含“第几章”，则在一二等标题前加 <<<
        text_content = re.sub(r'([一二三四五六七八九十百千]+、)', r'<<<\n\g<0>', text_content)

    # 确保输出路径存在，如果不存在则创建
    output_dir = os.path.dirname(txt_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 将处理后的文本写入 TXT 文件
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text_content)

def process_pdfs_in_directory(pdf_dir, txt_dir):
    # 确保输出目录存在，如果不存在则创建
    if not os.path.exists(txt_dir):
        os.makedirs(txt_dir)

    # 遍历 PDF 目录中的所有文件
    for filename in os.listdir(pdf_dir):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(pdf_dir, filename)
            txt_path = os.path.join(txt_dir, filename.replace('.pdf', '.txt'))
            insert_markers_in_pdf(pdf_path, txt_path)

# 使用示例
pdf_dir = "D:/shix_2024/公司规章制度/信息公司管理制度1/信息公司管理制度/新制度"
txt_dir = 'D:/shix_2024/农业知识/划分段落/信息公司管理制度/新制度'
process_pdfs_in_directory(pdf_dir, txt_dir)

# pdf_path = 'D:/shix_2024/农业知识问题整理/2023年建三江分公司寒地绿色水稻优质高产高效生产技术规程问答.pdf'
# txt_path = 'D:/shix_2024/农业知识/划分段落/2023年建三江分公司寒地绿色水稻优质高产高效生产技术规程问答.txt'
# insert_markers_in_pdf(pdf_path, txt_path)