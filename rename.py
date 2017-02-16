# _*_ coding: utf-8 -*-
"""
    本脚本用于对指定目录下的图片集进行重命名，功能包括
    1. 补零               @leftpad
    2. 扁平化图片集       @flatten
    3. 通过对译表重命名   @renamemap
"""

import os
import re


def main():
    """ 默认运行的主函数 """
    print("""
        请通过 main.py 进行调用。本模块包括以下三个方法：

        .leftpadall(path) :
            为 path 中所有图片文件名补零。

        .flatten(path) :
            分析 path 下有多少个子目录，为子目录中所有图片补零，
            并添加上文件夹名前缀，提出到父目录。

        .renamemap(path, map_file_name='map') :
            通过对译表重命名 path 下所有图片文件。""")


def image_pat():
    return re.compile(r'(.*)\.(jpg|png)')


def parseimgs(path):
    """ 分析 path 中有多少图片，返回图片 list """
    files = next(os.walk(path))[2]
    images = [f for f in files if image_pat().match(f)]
    if len(images) == 0:
        print("错误：没有图片")
        return "err"
    return images


def leftpad(src, length):
    """ 根据 length 为 src 左方补零 """
    name = image_pat().match(src).group(1)
    suffix = image_pat().match(src).group(2)
    return name.rjust(length, '0') + '.' + suffix


def padnum(arr):
    """ 计算需补零的个数
        (计算长度 (转为str (数组的长度，等同于最大的数)))"""
    return len(str(len(arr)))


def leftpadall(path):
    """ 把 arr 中所有文件补零 """
    images = parseimgs(path)
    img_count = len(images)
    length = padnum(images)
    if images != "err":
        for src in images:
            dst = leftpad(src, length)
            os.replace(src, dst)
    print("完成。\n共处理 " + str(img_count) + " 张图片")


def flatten(path):
    """ 分析 path 下有多少个子目录，
        为子目录中所有图片补零，并添加上文件夹名前缀，
        提出到父目录 """
    dirs = next(os.walk(path))[1]

    dir_count = len(dirs)
    img_count = 0

    for folder in dirs:
        imgs = parseimgs(folder)
        for img in imgs:
            dst = folder + '-' + leftpad(img, padnum(imgs))
            os.replace(folder + '/' + img, dst)
            img_count += 1

    print("完成。\n共处理 " + str(dir_count) + "个目录，" + str(img_count) + " 张图片。")


def renamemap(path, map_file_name='map'):
    """ 通过对译表重命名
        对译表默认名称为 map，是一个无扩展名的纯文本文件
        对译表每行为一个命名对，通过空格分隔（不包括行号）：
        1  src1 dst1
        2  src2 dst2
    """

    try:
        with open(map_file_name, 'r') as file_content:
            map_content = file_content.read()
    except FileNotFoundError:
        print('无法打开文件\n' +
              '请使用默认对译表名称`map`\n' +
              '或正确指定文件名： -m <map_file_name>')

    try:
        src_dst_list = map_content.split('\n')

        map_images = [x.split(' ')[0] for x in src_dst_list]
        dir_images = parseimgs(path)

        if set(map_images) == set(dir_images):
            for src_dst in src_dst_list:
                src = src_dst.split(' ')[0]
                dst = src_dst.split(' ')[1]
                os.replace(src, dst)
            print("共处理 " + str(rename_count) + " 条记录")
        # 磁盘和对译表内容不匹配
        else:
            # 磁盘和对译表内容不匹配
            print(map_dir_compare(map_images, dir_images, map_file_name))
            return

    except Exception as err:
        print(err)
        print("出错了，检查 `" + map_file_name + "` 文件的格式是否正确")
        print("`" + map_file_name + "` 应为纯文本文件")
        print("对译表每行为一个命名对，通过空格分隔（不包括行号）：\n" +
              "1  src1 dst1\n" +
              "2  src2 dst2")


def main(path='.'):
    """ 默认运行的主函数 """
    renamemap(path)
def map_dir_compare(map_list, dir_list, map_file_name):
    in_dir = list(set(dir_list) - set(map_list))
    in_map = list(set(map_list) - set(dir_list))

    map_file = map_file_name

    only_dir_file_count = len(in_dir)
    only_map_file_count = len(in_map)

    only_dir_files = "    " + "\n    ".join(in_dir) + '\n'
    only_map_files = "    " + "\n    ".join(in_map) + '\n'

    if in_map == []:
        err_msg = (
            "\n[错误]\n" +
            "以下 " + str(only_dir_file_count) + " 个文件在磁盘中 *存在* ，" +
            "但 *未在* `" + map_file + "` 中，\n" +
            "请检查你的 `" + map_file + "` 文件：\n\n" +
            only_dir_files
        )
    elif in_dir == []:
        err_msg = (
            "\n[错误]\n" +
            "以下 " + str(only_map_file_count) + " 个文件在磁盘中 *不存在* ，" +
            "但 *记录在* `" + map_file + "` 中，\n" +
            "请确保你下载完了全部的文件，"
            "或检查你的 `" + map_file + "` 文件：\n\n" +
            only_map_files
        )
    else:
        err_msg = (
            "\n[错误]\n" +
            "以下 " + str(only_map_file_count) + " 个文件在磁盘中 *不存在*，" +
            "但 *出现* 在 `" + map_file + "` 文件中：\n" +
            only_map_files + "\n" +
            "以下 " + str(only_dir_file_count) + " 个文件在磁盘中 *存在*，" +
            "但 *不在* `" + map_file + "` 文件中：\n\n" +
            only_dir_files + "\n" +
            "请确保你下载完了全部的文件，" +
            "或检查你的 `" + map_file + "` 文件：\n\n"
        )

    return err_msg

if __name__ == '__main__':
    main()
