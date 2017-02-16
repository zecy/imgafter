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


def help_message():
    return ("用法：" + script_name() + " <命令名> [-m <对译表名称>] [-d <目标路径>]\n" +
            "      -m : 文件名对译表，默认为 `map` ，一个无后缀名的纯文本文件\n" +
            "      -d : 目标文件夹，默认为当前名录\n" +
            "      默认情况下不需要设置上面两个参数")


def command_getter(argv):
    opt_status = len(argv)

    command_name = ''
    command_mapname = ''
    command_dir = working_dir()

    if opt_status == 1:
        print(help_message())
    elif opt_status == 2:
        command_name = argv[1]
        if not "-" in command_name:
            pass
        else:
            print(error_message())
    elif opt_status > 2:
        command_name = argv[1]
        opts = getopt.getopt(argv[2:], "hm:d:")[0]
        for opt, arg in opts:
            if opt == "-m":
                command_mapname = arg
            elif opt == "-d":
                command_dir = arg
            else:
                return error_message()
    else:
        return error_message()

    return {
        'command_name': command_name,
        'command_mapname': command_mapname,
        'command_dir': command_dir
    }


def command_switcher(command_bundle):
    command_name = command_bundle['command_name']
    command_mapname = command_bundle['command_mapname']
    command_dir = command_bundle['command_dir']

    if command_name == "leftpad":
        rename.leftpadall(command_dir)
    if command_name == "flatten":
        rename.flatten(command_dir)


def exe_command(argv):
    command_bundle = command_getter(argv)
    command_switcher(command_bundle)


def main(argv):
    """ 主函数 """
    try:
        exe_command(argv)
    except getopt.GetoptError:
        print(error_message())

    # rename.renamemap(path, mapname)

if __name__ == '__main__':
    main(sys.argv)
