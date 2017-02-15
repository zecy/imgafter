#! _*_ coding: utf-8 -*-
#! /Usr/local/bin/python3
""" 入口函数 """

import rename


def main():
    """ 主函数 """
    imgs = rename.parseimgs('.')
    rename.leftpadall(imgs)

if __name__ == '__main__':
    main()
