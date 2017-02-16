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
    return ("\n用法：" + script_name() + " <命令名> [-m <对译表名称>] [-d <目标路径>]\n\n" +
            "      <命令>\n\n" +
            "      leftpad ：对当前目录下的图片文件名补零。\n\n" +
            "      flatten ：为当前目录下子文件夹中图片添加子文件夹名称为前缀，\n" +
            "                并提到当前目录。\n\n" +
            "      map     ：依据对译表对当前目录下的图片文件进行重命名。\n\n" +
            "      <参数>\n\n" +
            "      -m : 文件名对译表，默认为 `map` ，一个无后缀名的纯文本文件\n" +
            "      -d : 目标文件夹，默认为当前名录\n\n" +
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
    if command_name == "map":
        print(command_mapname)
        if command_mapname == "":
            rename.renamemap(command_dir)
        else:
            rename.renamemap(command_dir, command_mapname)


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
