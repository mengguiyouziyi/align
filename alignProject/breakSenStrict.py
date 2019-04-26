import os
import re
import nltk


def breakEnSen(path1, path2):
    """
    使用nltk对英文断句
    通过nltk，将英文txt大段文本断句，写入到sen.en中
    :param path1: 英文txt大段文本文件路径
    :param path2: sen.en文件路径
    :return:
    """
    EP = re.compile(r'[:."?!。？：！”]$')
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    with open(path1, 'r', encoding='utf-8') as infile, open(path2, 'w', encoding='utf-8') as outfile:
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
                print(repr("if re.search(r'([0-9a-zA-Z])\1{3,}', line):"), '~~~~~~~~~~~', line)
                continue
            line_len = len(line)
            if line_len < 10:  # 单行小于2
                print(repr("if line_len < 2:"), '~~~~~~~~~~~', line)
                continue
            big_len = len(re.findall(r'[A-Z]', line))
            if (big_len / line_len > 0.7) and (line_len < 10):  # 大写占比70%且总长度小于10
                print(repr("if (big_len / line_len > 0.7) and line_len < 10"), '~~~~~~~~~~~', line)
                continue
            if len(re.findall(r'[0-9.\[\];\s]', line)) == line_len:  # 2.2，...， 2222
                print(repr("if len(re.findall(r'[0-9.\[\]]', line)) == line_len:"), '~~~~~~~~~~~', line)
                continue
            if re.findall(r'\d{2} [A-Z][a-z]+ \d{4}- \d{2} [A-Z][a-z]+ \d{4}', line):
                print(repr("re.findall(r'\d{2} [A-Z][a-z]+ \d{4}-\s*\d{2} [A-Z][a-z]+ \d{4}'"), '~~~~~~~~~~~', line)
                continue

            if 'References' == line:
                break_num = i
                continue
            if re.findall(r'[0-9.]+\s+References$', line):
                break_num = i
                continue

            if (not EP.search(line)) and (line_len < 60):
                print(repr("EP: "), '~~~~~~~~~~~', line)
                continue

            line_list.append(line)
        lines = '\n'.join(line_list)
        outfile.write(lines)
        print('en break over')


def breakZhSen(path1, path2):
    """
    自定义中文断句。
    通过自定义规则，将txt文件中中文大段文本断句，写入到sen.zh文件中
    :param path1: 中文txt大段文本文件路径
    :param path2: sen.zh文件路径
    :return:
    """
    cncomp = re.compile(r'[\u4e00-\u9fa5]')
    EP = re.compile(r'[:."?!。？：！”]$')
    with open(path1, 'r', encoding='utf-8') as infile, open(path2, 'w', encoding='utf-8') as outfile:
        para = infile.read()
        para = re.sub('([。！？\?])([^”’])', r"\1\n\2", para)  # 单字符断句符
        para = re.sub('(\.{6})([^”’])', r"\1\n\2", para)  # 英文省略号
        para = re.sub('(\…{2})([^”’])', r"\1\n\2", para)  # 中文省略号
        para = re.sub('([。！？\?][”’])([^，。！？\?])', r'\1\n\2', para)
        # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
        para = para.rstrip()  # 段尾如果有多余的\n就去掉它
        # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
        para = para.splitlines()
        para_list = []
        break_num = 0
        for i, line in enumerate(para):
            if break_num != 0:
                continue
            line = re.sub(r'\[[0-9;]*?\]', r'', line)  # [;;;]
            line = re.sub(r'\s{2,}', r'', line)  # 多个空白
            line = re.sub(r' ', r'', line)  # 不知名的空格
            line = line.replace('•', '')
            line = line.replace('\t', '')  # tab
            line = line.strip()
            if not line:
                continue
            if re.search(r'([0-9a-zA-Z])\1{3,}', line):  # aaa，aTTT
                print(repr("if re.search(r'([0-9a-zA-Z])\1{3,}', line):"), '~~~~~~~~~~~', line)
                continue
            line_len = len(line)
            if line_len < 5:  # 单行小于2
                print(repr("if line_len < 5:"), '~~~~~~~~~~~', line)
                continue
            big_len = len(re.findall(r'[A-Z]', line))
            if (big_len / line_len > 0.7) and line_len < 10:  # 大写占比70%且总长度小于10
                print(repr("if (big_len / line_len > 0.7) and line_len < 10"), '~~~~~~~~~~~', line)
                continue
            if len(re.findall(r'[0-9.\[\];\s]', line)) == line_len:  # 2.2，...， 2222
                print(repr("if len(re.findall(r'[0-9.\[\]];\s]', line)) == line_len:"), '~~~~~~~~~~~', line)
                continue

            if len(cncomp.findall(line)) / line_len < 0.3:
                print(repr("cncomp.findall(line) / line_len < 0.3"), '~~~~~~~~~~~', line)
                continue
            if '参考文献' == line:
                break_num = i
                continue
            if re.findall(r'[0-9.]+\s+参考文献$', line):
                break_num = i
                continue

            if (not EP.search(line)) and (line_len < 30):
                print(repr("EP: "), '~~~~~~~~~~~', line)
                continue
            para_list.append(line)
        para = '\n'.join(para_list)
        outfile.write(para)
        print('zh break over')
