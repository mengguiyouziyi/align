import subprocess


def alignCTK(en_sen_path, zh_sen_path, align_label_path, cham_path):
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
    print(return_code)
