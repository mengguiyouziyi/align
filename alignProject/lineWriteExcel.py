import os
import xlwt


def toExcel(file_align, en_sen, zh_sen, xlsx):
    """
    根据对齐文件 1 <-> 1，在英中断句文件中找到相对应的句子，写入到excel中
    :param file_align: 对齐文件路径
    :param en_sen: 英文断句文件路径
    :param zh_sen: 中文断句文件路径
    :param xlsx: 导出的excel文件路径
    :return:
    """
    current_path = os.getcwd()
    # 筛选对应行号，入 xxx_num_list
    align = open(os.path.join(current_path, '../file', file_align), 'r', encoding='utf-8')
    src_num_list = []
    tgt_num_list = []
    for line in align.readlines():
        if 'omitted' in line or ',' in line:
            continue
        line = line.strip()
        src_num, tgt_num = line.split(' <=> ')
        src_num_list.append(src_num)
        tgt_num_list.append(tgt_num)
    # 根据行号提取对照文本，入 xxx_list
    src_sen_file = open(os.path.join(current_path, '../file', en_sen), 'r', encoding='utf-8')
    tgt_sen_file = open(os.path.join(current_path, '../file', zh_sen), 'r', encoding='utf-8')
    src_sen_list = src_sen_file.readlines()
    src_list = [src_sen_list[int(i) - 1] for i in src_num_list]
    tgt_sen_list = tgt_sen_file.readlines()
    tgt_list = [tgt_sen_list[int(i) - 1] for i in tgt_num_list]
    # 将对照文本写入文件
    xlsx_file = os.path.join(current_path, '../file', xlsx)
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('align')
    for i, en, zh in zip(range(len(src_list)), src_list, tgt_list):
        worksheet.write(i, 0, en.strip())
        worksheet.write(i, 1, zh.strip())
    workbook.save(xlsx_file)

    align.close()
    src_sen_file.close()
    tgt_sen_file.close()
