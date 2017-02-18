# -*- coding: utf-8 -*-
"""
本模块提供基础方法，需通过 import 调用：
    @img_pat()：
        return type：dict
        统一返回图片后缀名集，方便灵活使用判别方法。

    @is_img(file_name)：
        reutrn type：boolean
        判断一个文件名是否为图片文件名。

    @parseimgs(path)：
        return type：list
        分析 path 中有多少图片，返回图片 list

    @all_imgs(path):
        reutrn type：boolean
        输入路径，检查是否为纯图片文件夹。
"""

import os


def main():
    print(__doc__)


def img_pat():
    """
    返回图片后缀名
        img_pat()['dot'] = ('.jpg','.png',...)
        img_pat()['nodot'] = ('jpg','png',...)
    """
    return{
        "dot": ('.jpg', '.jpeg', '.png', '.bmp', '.tif'),
        "nodot": ('jpg', 'jpeg', 'png', 'bmp', 'tif')
    }


def is_img(file_name):
    """ 判断 `file_name` 是否图片，返回 boolean """
    return file_name.endswith(img_pat()['dot'])


def parseimgs(path):
    """ 分析 path 中有多少图片，返回图片 list """
    files = next(os.walk(path))[2]
    images = [f for f in files if is_img(f)]
    if len(images) == 0:
        print("错误：没有图片")
        return "err"
    return images


def all_imgs(path):
    """ 输入路径，检查是否为纯图片文件夹。 """
    dir_contents = next(os.walk(path))[1:3]

    dir_sub_folder = dir_contents[0]

    if len(dir_sub_folder) > 0:
        # 存在子文件夹，返回 False
        return False

    dir_files = dir_contents[1]

    if len(dir_files) == 0:
        # 文件夹为空，返回 False
        return False

    for dir_file in dir_files:
        # 如果有一个文件不是图片，马上返回 False
        if not is_img(dir_file):
            return False

    return True


if __name__ == '__main__':
    main()
