import docx2txt


def doc2txt_docx2txt(path1, path2):
    """
    使用docx2txt包，将docx中的中英文文本提取到txt文件中
    :param path1: docx文件路径
    :param path2: txt文件路径
    :return:
    """
    text = docx2txt.process(path1)
    with open(path2, 'w', encoding='utf-8') as f:
        f.write(text)