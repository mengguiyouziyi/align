import docx2txt


def doc2txt_docx2txt(doc_path, txt_org_path):
    """
        使用docx2txt包，将docx中的中英文文本提取到txt文件中
    :param doc_path: docx文件路径
    :param txt_org_path: txt文件路径
    :return:
    """
    text = docx2txt.process(doc_path)
    with open(txt_org_path, 'w', encoding='utf-8') as f:
        f.write(text)
