import os, sys, time, re
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
        print(dirs)
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
    # rootDir = r'/home/wande/文档/罗氏/英译中/英译中'
    rootDir = r'/home/wande/文档/docx'
    resultDir = r'/home/wande/文档/alignFile'
    r = re.compile(r'[^-\u4e00-\u9fa5A-Za-z0-9_/]')
    for i, (en_list, cn_list) in enumerate(main(rootDir)):
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
            # en_doc_path = en_file.replace(' ', '-').replace('\xa0', '-').replace('（', '-').replace('）', '-').replace(
            #     '(', '-').replace(')', '-')
            # zh_doc_path = cn_file.replace(' ', '-').replace('\xa0', '-').replace('（', '-').replace('）', '-').replace(
            #     '(', '-').replace(')', '-')
            en_doc_path = r.sub('-', en_file.replace('.docx', '')) + '.docx'
            zh_doc_path = r.sub('-', cn_file.replace('.docx', '')) + '.docx'
            en_doc_file = os.path.basename(en_doc_path)
            zh_doc_file = os.path.basename(zh_doc_path)
            en_doc_dir = os.path.dirname(en_doc_path).replace(rootDir, resultDir)
            zh_doc_dir = os.path.dirname(zh_doc_path).replace(rootDir, resultDir)
            en_doc_name = os.path.splitext(en_doc_path)[0].replace(rootDir, resultDir)
            zh_doc_name = os.path.splitext(zh_doc_path)[0].replace(rootDir, resultDir)
            en_doc_file_name = os.path.splitext(en_doc_file)[0]
            zh_doc_file_name = os.path.splitext(zh_doc_file)[0]
            if en_doc_file_name not in zh_doc_file_name:
                print(en_doc_file_name, zh_doc_file_name)
                continue
            if not os.path.exists(en_doc_dir):
                os.makedirs(en_doc_dir)
            if not os.path.exists(zh_doc_dir):
                os.makedirs(zh_doc_dir)
            # 从doc到txt
            en_org_path = en_doc_name + '-org.en'
            zh_org_path = zh_doc_name + '-org.zh'
            docx2text(en_file, en_org_path)
            docx2text(cn_file, zh_org_path)
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
            # exit()
