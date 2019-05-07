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
    # cn_list = []
    # en_list = []
    # for fname in iter_files(rootDir):
    #     if '-CN' in fname:
    #         cn_list.append(fname)
    #     else:
    #         en_list.append(fname)
    # return cn_list, en_list
    return iter_files(rootDir)


if __name__ == '__main__':
    bpath = r'/home/wande/文档'
    rootDir = r'罗氏/英译中/英译中'
    for root, dirs, files in os.walk(os.path.join(bpath, rootDir)):
        # print(root, dirs, files)
        en_list = []
        cn_list = []
        for dir in dirs:
            for unno_dir in os.listdir(os.path.join(root, dir)):
                unno_dir = os.path.join(root, dir, unno_dir)
                for f in iter_files(unno_dir):
                    if '-CN' in f:
                        cn_list.append(f)
                    else:
                        en_list.append(f)
            pprint(cn_list)
            pprint(en_list)
            time.sleep(1)
            print('=====================================')
