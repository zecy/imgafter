# _*_ coding: utf-8 -*-
"""
    本脚本用于对 ** 当前 ** 目录下的图片集进行重命名，功能包括
    1. 补零               @leftpad      DONE
    2. 扁平化图片集       @flatten      DONE
    3. 通过对译表重命名   @renamemap    TODO
"""

import os
import re

image_pat = re.compile(r'(.*)\.(jpg|png)')


def parseimgs(path):
    """ 分析 path 中有多少图片，返回图片 list """
    files = next(os.walk(path))[2]
    images = [f for f in files if image_pat.match(f)]
    return images


def leftpad(src, length):
    """ 根据 length 为 src 左方补零 """
    name = image_pat.match(src).group(1)
    suffix = image_pat.match(src).group(2)
    return name.rjust(length, '0') + '.' + suffix


def padnum(arr):
    """ 计算需补零的个数
        (计算长度 (转为str (数组的长度，等同于最大的数)))"""
    return len(str(len(arr)))


def leftpadall(arr):
    """ 把 arr 中所有文件补零 """
    for src in arr:
        dst = leftpad(src, padnum(arr))
        os.replace(src, dst)


def flatten(path):
    """ 分析 path 下有多少个子目录，
        为子目录中所有图片补零，并添加上文件夹名前缀，
        提出到父目录 """
    dirs = next(os.walk(path))[1]
    for folder in dirs:
        imgs = parseimgs(folder)
        for img in imgs:
            dst = folder + '-' + leftpad(img, padnum(imgs))
            os.replace(folder + '/' + img, dst)


def renamemap(path, mapfilename='map'):
    """ 通过对译表重命名
        对译表默认名称为 map，是一个无扩展名的纯文本文件
        对译表每行为一个命名对，通过空格分隔（不包括行号）：
        1  src1 dst1
        2  src2 dst2
    """
    mapcontent = []

    try:
        with open(mapfilename, 'r') as file_content:
            mapcontent = file_content.readlines()
    except FileNotFoundError:
        print('无法打开文件\n' +
              '请使用默认对译表名称`map`\n' +
              '或正确指定文件名： -m <map_file_name>')

    print(mapcontent)


def main(path='.'):
    """ 默认运行的主函数 """
    flatten(path)

if __name__ == '__main__':
    main()
