# _*_ coding: utf-8 _*_

import zipfile
import rename


def main():
    cur_images('.')


def cur_images(path):
    print(rename.parseimgs(path))


if __name__ == '__main__':
    main()
