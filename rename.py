#! _*_ coding: utf-8 -*-
#! /Usr/local/bin/python3
"""
    本脚本用于对图片集进行重命名包括
    1. 统一编号 @numberic
    2. 添加目录前缀 @dirprefix
    3. 通过对译表重命名 @renamemap
"""

import os
import sys
import re

suffix = re.compile('.*\.(jpg|png)')

def parseimgs(path):
    files  = next(os.walk(path))[2]
    images = [f for f in files if suffix.match(f)]
    return images

def main(path):
    print(parseimgs(path))

if __name__ == '__main__':
    main('.')
