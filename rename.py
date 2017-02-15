#! _*_ coding: utf-8 -*-
#! /Usr/local/bin/python3
"""
    本脚本用于对图片集进行重命名包括
    1. 补零 @leftpad
    2. 添加目录前缀 @dirprefix
    3. 通过对译表重命名 @renamemap
"""

import os
import re

image = re.compile(r'(.*)\.(jpg|png)')


def parseimgs(path):
    files = next(os.walk(path))[2]
    images = [f for f in files if image.match(f)]
    return images


def leftpad(arr):
    length = len(str(len(arr)))  # (计算长度 (转为str (数组的长度，等同于最大的数)))
    for src in arr:
        name = image.match(src).group(1)
        suffix = image.match(src).group(2)
        dst = name.rjust(length, '0') + '.' + suffix
        os.replace(src, dst)


def main(path):
    imgs = parseimgs(path)
    leftpad(imgs)

if __name__ == '__main__':
    main('.')
