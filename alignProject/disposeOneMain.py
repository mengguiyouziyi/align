import re, os

from extractWordDocx2txt import docx2text
from breakEnSenStrict import breakEnSen
from breakZhSenStrict import breakZhSen
from alignCTK import alignCTK
from lineWriteExcel import toExcel

import argparse

parse = argparse.ArgumentParser()
parse.description = '''python disposeOne.py -s sourceDir -m middleDir -r resultDir -e enFile -c cnFile'''
parse.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
parse.add_argument("-S", '--sourceDir', dest='sourceDir', default='/home/wande/文档/docx/source', help="""将要处理文件所在的目录""")
parse.add_argument("-M", '--middleDir', dest='middleDir', default='/home/wande/文档/docx/middle',
                   help="""处理过程中产生的中间文件所在的目录""")
parse.add_argument("-R", '--resultDir', dest='resultDir', default='/home/wande/文档/docx/result', help="""处理结果所在的目录""")
parse.add_argument("-s", '--srcFile', dest='srcFile', default='1 summary-clin-efficacy-hemophilia-a-cn-final.docx', help="""要处理的源文件""")
parse.add_argument("-t", '--tgtFile', dest='tgtFile', default='IB BAY 1101042_V4.0-CN.docx', help="""要处理的目标文件""")
parse.add_argument("-l", '--lang2lang', dest='lang2lang', choices=['cn2en', 'en2cn'], default='en2cn', help="""语言对""")
parse.add_argument("-f", '--srcSuffix', dest='srcSuffix', choices=['docx', 'doc', 'pdf', 'txt'], default='docx',
                   help="""要处理的源文件后缀""")
parse.add_argument("-F", '--tgtSuffix', dest='tgtSuffix', choices=['docx', 'doc', 'pdf', 'txt'], default='docx',
                   help="""要处理的源文件后缀""")

args = parse.parse_args()
print(args)
sdir = args.sourceDir
mdir = args.middleDir
rdir = args.resultDir
lang2lang = args.lang2lang
if lang2lang == 'en2cn':
    en_doc = args.srcFile  # 文件名称（带后缀）
    cn_doc = args.tgtFile
elif lang2lang == 'cn2en':
    en_doc = args.tgtFile
    cn_doc = args.srcFile
else:
    en_doc = args.srcFile  # 文件名称（带后缀）
    cn_doc = args.tgtFile


def addDir(file, bdir):
    if not os.path.exists(bdir):
        os.makedirs(bdir)
    return os.path.join(bdir, file)


def subIllegal(file):
    """
        替换文件名中的非法字符，并返回文件名
    :param file: a b.txt
    :return: a_b
    """
    r = re.compile(r'[^-\u4e00-\u9fa5A-Za-z0-9_/]')
    all = os.path.splitext(file)
    return r.sub(r'-', all[0])


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
