import os
import xlwt


def toExcel(align_label_path, en_sen_path, zh_sen_path, excel_path):
    """
        根据对齐文件 1 <-> 1，在英中断句文件中找到相对应的句子，写入到excel中
    :param align_label_path: 对齐文件路径
    :param en_sen_path: 英文断句文件路径
    :param zh_sen_path: 中文断句文件路径
    :param excel_path: 导出的excel文件路径
    :return:
    """

    # 筛选对应行号，入 xxx_num_list
    align = open(align_label_path, 'r', encoding='utf-8')
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
    src_sen_file = open(en_sen_path, 'r', encoding='utf-8')
    tgt_sen_file = open(zh_sen_path, 'r', encoding='utf-8')
    src_sen_list = src_sen_file.readlines()
    src_list = [src_sen_list[int(i) - 1] for i in src_num_list]
    tgt_sen_list = tgt_sen_file.readlines()
    tgt_list = [tgt_sen_list[int(i) - 1] for i in tgt_num_list]
    # 将对照文本写入文件
    excel_path_file = excel_path
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('align')
    for i, en, zh in zip(range(len(src_list)), src_list, tgt_list):
        worksheet.write(i, 0, en.strip())
        worksheet.write(i, 1, zh.strip())
    workbook.save(excel_path_file)

    align.close()
    src_sen_file.close()
    tgt_sen_file.close()
