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
    ''' 默认运行的主函数 '''
    print("""
        请通过 main.py 进行调用。本模块包括以下三个方法：

        .leftpadall(path) :
            为 path 中所有图片文件名补零。

        .flatten(path) :
            分析 path 下有多少个子目录，为子目录中所有图片补零，
            并添加上文件夹名前缀，提出到父目录。

        .renamemap(path, map_file_name='map') :
            通过对译表重命名 path 下所有图片文件。""")


def img_pat():
    ''' 返回图片后缀名
    img_pat()['dot'] = ('.jpg','.png',...)
    img_pat()['nodot'] = ('jpg','png',...)
    '''
    return{
        "dot": ('.jpg', '.jpeg', '.png', '.bmp', '.tif'),
        "nodot": ('jpg', 'jpeg', 'png', 'bmp', 'tif')
    }


def is_img(file_name):
    ''' 判断文件是否图片，返回 True 或 False '''
    return file_name.endswith(img_pat()['dot'])


def parseimgs(path):
    ''' 分析 path 中有多少图片，返回图片 list '''
    files = next(os.walk(path))[2]
    images = [f for f in files if is_img(f)]
    if len(images) == 0:
        print("错误：没有图片")
        return "err"
    return images


def leftpad(src, length):
    name = image_pat().match(src).group(1)
    suffix = image_pat().match(src).group(2)
    ''' 根据 length 为 src 左方补零 '''
    return name.rjust(length, '0') + '.' + suffix


def padnum(arr):
    """ 计算需补零的个数
        (计算长度 (转为str (数组的长度，等同于最大的数)))"""
    return len(str(len(arr)))


def leftpadall(path):
    """ 为 path 中所有图片文件名补零 """
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
    """ 通过对译表重命名 """

    try:
        with open(map_file_name, 'r') as file_content:
            map_content = file_content.read()
    except FileNotFoundError:
        print("\n    [错误]\n" +
              "    无法打开文件\n" +
              "    请使用默认对译表名称`map`\n" +
              "    或正确指定文件名：-m <map_file_name>")
        return

    try:
        src_dst_list = map_content.split('\n')[:-1]  # 忽略末尾换行

        if check_map_format(src_dst_list) == 'ok':
            map_images = [x.split(' ')[0] for x in src_dst_list]
            dir_images = parseimgs(path)
        else:
            print(
                "\n[格式错误]\n" +
                "对译表每行为一个命名对，通过空格分隔（不包括行号）：\n" +
                "1  src1.jpg dst1.jpg\n" +
                "2  src2.png dst2.png\n\n" +
                "以下行格式存在问题：\n\n    " +
                "\n    ".join(check_map_format(src_dst_list))
            )
            return

        if set(map_images) == set(dir_images):
            for src_dst in src_dst_list:
                src = src_dst.split(' ')[0]
                dst = src_dst.split(' ')[1]
                os.replace(src, dst)
            print("共处理 " + str(len(dir_images)) + " 条记录")
        else:
            # 磁盘和对译表内容不匹配
            print(map_dir_compare(map_images, dir_images, map_file_name))
            return

    except FileNotFoundError as err:
        print(err)
        print("出错了，检查 `" + map_file_name + "` 文件的格式是否正确")
        print("`" + map_file_name + "` 应为纯文本文件")


def map_dir_compare(map_list, dir_list, map_file_name):
    ''' 列出两个列表不一致的部分 '''
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


def check_map_format(map_lines_list):
    map_pattern = re.compile(r"^.*?\.(jpg|png) .*?\1$")
    ''' 检查对译表格式是否正确 '''

    err_line_content = []
    lines_count = len(map_lines_list)

    for i in range(lines_count):
        line = map_lines_list[i]
        if not map_pattern.match(line):
            err_msg = str(i + 1).rjust(len(str(lines_count))) + " | " + line
            err_line_content.append(err_msg)

    if len(err_line_content) == 0:
        return 'ok'
    else:
        return err_line_content

if __name__ == '__main__':
    main()
