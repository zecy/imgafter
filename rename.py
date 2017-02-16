# _*_ coding: utf-8 -*-
"""
    本脚本用于对 ** 当前 ** 目录下的图片集进行重命名，功能包括
    1. 补零               @leftpad      DONE
    2. 扁平化图片集       @flatten      DONE
    3. 通过对译表重命名   @renamemap    TODO
"""

import os
import re


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

        # 磁盘和对译表内容不匹配
        else:
            in_dir = list(set(dir_images) - set(map_images))
            in_map = list(set(map_images) - set(dir_images))

            only_dir = "    " + "\n    ".join(in_dir) + '\n'
            only_map = "    " + "\n    ".join(in_map) + '\n'

            if in_map == []:
                print("以下文件在磁盘中 *存在* ，" +
                      "但 *未在* `" + map_file_name + "` 中，\n" +
                      "请检查你的 `" + map_file_name + "` 文件：\n\n" +
                      only_dir)
            elif in_dir == []:
                print("以下文件在磁盘中 *不存在* ，" +
                      "但 *记录在* `" + map_file_name + "` 中，\n" +
                      "请确保你下载完了全部的文件，"
                      "或检查你的 `" + map_file_name + "` 文件：\n\n" +
                      only_map)
            else:
                print("以下文件在磁盘中 *不存在*，" +
                      "但 *出现* 在 `" + map_file_name + "` 文件中：\n" +
                      only_map + '\n' +
                      "以下文件在磁盘中 *存在*，" +
                      "但 *不在* `" + map_file_name + "` 文件中：\n\n" +
                      only_dir +
                      "请确保你下载完了全部的文件，" +
                      "或检查你的 `" + map_file_name + "` 文件：\n\n"
                      )
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

if __name__ == '__main__':
    main()
