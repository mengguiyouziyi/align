import subprocess


def alignCTK(path1, path2, align, cham):
    """
    /search/odin/meng/xingzong/champollion-1.2/
    :param path1:
    :param path2:
    :param align:
    :return:
    """
    return_code = subprocess.call(f"""
        export PATH={cham}bin:$PATH && export CTK={cham} &&
        champollion.EC_utf8 {path1} {path2} {align}
    """, shell=True)
    print(return_code)
