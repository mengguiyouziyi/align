import subprocess


def alignCTK(en_sen_path, zh_sen_path, align_label_path, cham_path=r'/home/wande/align/champollion-1.2/'):
    """
        /search/odin/meng/xingzong/champollion-1.2/
        /home/wande/align/champollion-1.2/
    :param en_sen_path:
    :param zh_sen_path:
    :param align_label_path:
    :param cham_path:
    :return:
    """
    return_code = subprocess.call(f"""
        export PATH={cham_path}bin:$PATH && export CTK={cham_path} &&
        champollion.EC_utf8 {en_sen_path} {zh_sen_path} {align_label_path}
    """, shell=True)
    print(f"""
        export PATH={cham_path}bin:$PATH && export CTK={cham_path} &&
        champollion.EC_utf8 {en_sen_path} {zh_sen_path} {align_label_path}
    """)
    print(return_code)


if __name__ == '__main__':
    en_sen_path = r'/home/wande/文档/alignFile/罗氏-20180102（Anny Zhao）-英中/翻译原文/MO39171 ICF V3 22DEC2017 FINAL-sen.en'
    zh_sen_path = r'/home/wande/文档/alignFile/罗氏-20180102（Anny Zhao）-英中/发送稿/MO39171 ICF V3 22DEC2017 FINAL-CN-sen.zh'
    align_label_path = r'/home/wande/文档/alignFile/罗氏-20180102（Anny Zhao）-英中/翻译原文/MO39171 ICF V3 22DEC2017 FINAL-align-label.txt'
    alignCTK(en_sen_path, zh_sen_path, align_label_path)
