import re, os

from extractWordDocx2txt import docx2text
from breakEnSenStrict import breakEnSen
from breakZhSenStrict import breakZhSen
from alignCTK import alignCTK
from lineWriteExcel import toExcel


def addDir(file, bdir):
    if not os.path.exists(bdir):
        os.makedirs(bdir)
    return os.path.join(bdir, file)


def subIllegal(file):
    r = re.compile(r'[^-\u4e00-\u9fa5A-Za-z0-9_/]')
    all = os.path.splitext(file)
    return r.sub(r'-', all[0])


sdir = '/home/wande/文档/docx/source'
mdir = '/home/wande/文档/docx/middle'
rdir = '/home/wande/文档/docx/result'
en_doc = 'IB BAY 1101042_V4.0.docx'  # 文件名称（带后缀）
cn_doc = 'IB BAY 1101042_V4.0-CN.docx'
en_name = subIllegal(en_doc)
cn_name = subIllegal(cn_doc)
en_org = en_name + '-org.en'
cn_org = cn_name + '-org.cn'
en_sen = en_name + '-sen.en'
cn_sen = cn_name + '-sen.cn'

# 从doc到txt
en_org_path = addDir(en_org, mdir)
cn_org_path = addDir(cn_org, mdir)
docx2text(addDir(en_doc, sdir), en_org_path)
docx2text(addDir(cn_doc, sdir), cn_org_path)
# 从txt到breakSen
en_sen_path = addDir(en_sen, mdir)
cn_sen_path = addDir(cn_sen, mdir)
breakEnSen(en_org_path, en_sen_path)
breakZhSen(cn_org_path, cn_sen_path)
# 从sen到align
align_label_path = addDir(en_name + '-align-label.txt', mdir)
alignCTK(en_sen_path, cn_sen_path, align_label_path)
# 从align-label到excel
excel_path = addDir(en_name + '.xls', rdir)
toExcel(align_label_path, en_sen_path, cn_sen_path, excel_path)
