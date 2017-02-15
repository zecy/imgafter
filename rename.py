#! _*_ coding: utf8 -*-
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

def parseimgs():
    filenames = next(os.walk('.'))[2]
    print(filenames)

def main():
    parseimgs()

if __name__ == '__main__':
    main()
