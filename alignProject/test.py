import re, os

from extractWordDocx2txt import docx2text
from breakEnSenStrict import breakEnSen
from breakZhSenStrict import breakZhSen
from alignCTK import alignCTK
from lineWriteExcel import toExcel


def addDir(file, bdir):
    return os.path.join(bdir, file)


bdir = '/home/wande/文档/docx'
en_file = 'IB BAY 1101042_V4.0.docx'
cn_file = 'IB BAY 1101042_V4.0-CN.docx'
en_doc_name = os.path.splitext(en_file)[0]
zh_doc_name = os.path.splitext(en_file)[0]
en_file = addDir(en_file, bdir)
cn_file = addDir(cn_file, bdir)
en_doc_name = addDir(en_doc_name, bdir)
zh_doc_name = addDir(zh_doc_name, bdir)

r = re.compile(r'[^-\u4e00-\u9fa5A-Za-z0-9_/]')
en_doc_path = r.sub('-', en_file.replace('.docx', '')) + '.docx'
zh_doc_path = r.sub('-', cn_file.replace('.docx', '')) + '.docx'
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
