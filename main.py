# _*_ coding: utf-8 -*-
""" 入口函数 """

import sys
import getopt
import rename


def script_name():
    return sys.argv[0].split('/')[-1]  # 本脚本的文件名


def working_dir(path='.'):
    return path  # 脚本工作路径，默认为调用本脚本的文件夹


def error_message():
    return "参数错误，通过`" + script_name() + " -h` 获取帮助"

def main(argv):
    """ 主函数 """
    try:
        if len(argv) == 2:
            exe_command = argv[1]
            print(exe_command)
            if not "-" in exe_command:
                print("this is command")
            else:
                print('this is opt')
def help_message():
    return ("用法：" + script_name() + " <命令名> [-m <对译表名称>] [-d <目标路径>]\n" +
            "      -m : 文件名对译表，默认为 `map` ，一个无后缀名的纯文本文件\n" +
            "      -d : 目标文件夹，默认为当前名录\n" +
            "      默认情况下不需要设置上面两个参数")
        else:
            print_error()

        opts, args = getopt.getopt(argv[2:], "m:d:")
        if opts == []:
            opts = [('-h', '')]
    except getopt.GetoptError:
        print_error()

    for opt, arg in opts:
        if opt == "-h":
            print_help()
            break

        if opt == "-m":
            print("-m " + arg)

        if opt == "-d":
            print("-d " + arg)

    # rename.renamemap(path, mapname)

if __name__ == '__main__':
    main(sys.argv)
