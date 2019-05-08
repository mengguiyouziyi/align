import os, sys, time
from pprint import pprint

from extractWordDocx2txt import docx2text
from breakEnSenStrict import breakEnSen
from breakZhSenStrict import breakZhSen
from alignCTK import alignCTK
from lineWriteExcel import toExcel

"""
doc_path:
    en_doc_path 
    zh_doc_path
txt_org_path:
    en_org_path
    zh_org_path
en_sen_path
zh_sen_path
align_label_path
excel_path
"""


def iter_files(rootDir):
    for root, dirs, files in os.walk(rootDir):
        for file in files:
            file_name = os.path.join(root, file)
            yield file_name
        for dirname in dirs:
            iter_files(dirname)


def main(rootDir):
    for root, dirs, files in os.walk(rootDir):
        for dir in dirs:
            print(dir)
            en_list = []
            cn_list = []
            for unno_dir in os.listdir(os.path.join(root, dir)):
                unno_dir = os.path.join(root, dir, unno_dir)
                for f in iter_files(unno_dir):
                    if '-CN' in f:
                        cn_list.append(f)
                    else:
                        en_list.append(f)

            yield en_list, cn_list


if __name__ == '__main__':
    rootDir = r'/home/wande/文档/罗氏/英译中/英译中'
    resultDir = r'/home/wande/文档/alignFile'
    for en_list, cn_list in main(rootDir):
        file_en_list = [os.path.basename(p) for p in en_list]
        file_cn_list = [os.path.basename(p) for p in cn_list]
        pprint(file_en_list)
        pprint(file_cn_list)
        if len(en_list) != len(cn_list):
            continue
        for en_file, cn_file in zip(en_list, cn_list):
            if not en_file.endswith('.docx'):
                continue
            if not cn_file.endswith('.docx'):
                continue
            en_doc_path = en_file
            zh_doc_path = cn_file
            en_doc_file = os.path.basename(en_doc_path)
            zh_doc_file = os.path.basename(zh_doc_path)
            en_doc_dir = os.path.dirname(en_doc_path)
            zh_doc_dir = os.path.dirname(zh_doc_path)
            en_doc_name = os.path.splitext(en_doc_path)[0].replace(rootDir, resultDir)
            zh_doc_name = os.path.splitext(zh_doc_path)[0].replace(rootDir, resultDir)
            if en_doc_name not in zh_doc_name:
                print(en_doc_name, zh_doc_name)
                continue
            # 从doc到txt
            en_org_path = en_doc_name + '-org.en'
            zh_org_path = zh_doc_name + '-org.zh'
            docx2text(en_doc_path, en_org_path)
            docx2text(zh_doc_path, zh_org_path)
            # 从txt到breakSen
            en_sen_path = en_doc_name + '-sen.en'
            zh_sen_path = zh_doc_name + '-sen.zh'
            breakEnSen(en_org_path, en_sen_path)
            breakZhSen(zh_org_path, zh_sen_path)
            # 从sen到align
            align_label_path = en_doc_name + '-align-label.txt'
            alignCTK(en_sen_path, zh_sen_path, align_label_path)
            # 从align-label到excel
            excel_path = en_doc_name + '.xls'
            toExcel(align_label_path, en_sen_path, zh_sen_path, excel_path)

        time.sleep(1)
        print('=====================================')
