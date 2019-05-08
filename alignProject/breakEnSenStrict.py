import os
import re
import nltk

nltk.download('punkt')


def breakEnSen(en_org_path, en_sen_path):
    """
    使用nltk对英文断句
    通过nltk，将英文txt大段文本断句，写入到sen.en中
    :param en_org_path: 英文txt大段文本文件路径
    :param en_sen_path: sen.en文件路径
    :return:
    """
    EP = re.compile(r'[:."?!。？：！”]$')
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    with open(en_org_path, 'r', encoding='utf-8') as infile, open(en_sen_path, 'w', encoding='utf-8') as outfile:
        sen_str = infile.read()
        sen_str = sen_str.replace('et al.', ' ').replace('i.e.', 'illustrate')
        ########## 断句 ##########
        sens = tokenizer.tokenize(sen_str)
        sens = '\n'.join(sens)
        sens = sens.splitlines()
        #########################
        line_list = []
        break_num = 0
        for i, line in enumerate(sens):
            if break_num != 0:
                continue
            line = line.strip()
            if not line:
                continue
            line = re.sub(r'\[[0-9;]*?\]', r' ', line)  # [;;;]
            line = re.sub(r'\s{2,}', r' ', line)  # 多个空白
            line = re.sub(r' ', r' ', line)  # 不知名的空格
            line = line.replace('\t', ' ')  # tab
            line = line.replace('•', '')
            if re.search(r'([0-9a-zA-Z])\1{3,}', line):  # aaa，aTTT
                print(repr("[ if re.search(r'([0-9a-zA-Z])\1{3,}', line): ]"), '-->', line)
                continue
            line_len = len(line)
            if line_len < 20:  # 单行小于20
                print(repr("[ 单行小于20 ]"), '-->', line)
                continue
            big_len = len(re.findall(r'[A-Z]', line))
            if big_len / line_len > 0.7:  # 大写占比70%且总长度小于20
                print(repr("[ 大写占比70%且总长度小于20 ]"), '-->', line)
                continue
            if len(re.findall(r'[0-9.\[\];\s]', line)) == line_len:  # 2.2，...， 2222
                print(repr("[ 行中全部是<数字.[];不知名空白> ]"), '-->', line)
                continue
            if re.findall(r'\d{2} [A-Z][a-z]+ \d{4}- \d{2} [A-Z][a-z]+ \d{4}', line):  # 22 Asabs 2222- 22 Asg 3333
                print(repr("[ re.findall(r'\d{2} [A-Z][a-z]+ \d{4}- \d{2} [A-Z][a-z]+ \d{4}', line): ]"), '-->', line)
                continue

            if 'References' == line:
                break_num = i
                continue
            if re.findall(r'[0-9.]+\s+References$', line):
                break_num = i
                continue

            if (not EP.search(line)) and (line_len < 30):  # 行中没有标点并且字数小于60字
                print(repr("[ 非标点结束并且长度小于30 ]"), '-->', line)
                continue

            line_list.append(line)
        lines = '\n'.join(line_list)
        outfile.write(lines)
        print('en break over')
