# -*- coding: utf-8 -*-
"""
用法：imgafter <命令名> [-m <对译表名称>] [-d <目标路径>]

      [命令]

      leftpad 对当前目录下的图片文件名补零。

      flatten 为当前目录下子文件夹中图片添加子文件夹名称为前缀，
              并提到当前目录。

      map     依据对译表对当前目录下的图片文件进行重命名。

      zip     打包当前目录下所有图片，并把压缩包移到上一级目录。
              压缩包名称为目录名称。

      [参数]

      -m : 文件名对译表，默认为 `map` ，一个无后缀名的纯文本文件
      -d : 目标文件夹，默认为当前名录

     默认情况下不需要设置上面两个参数
"""

import sys
import getopt
import rename
import zipimgs


def script_name():
    """
    本脚本的文件名

    return: str

    返回本脚本的名字，方便调用。
    """
    return sys.argv[0].split('/')[-1]


def working_dir(path='.'):
    """
    脚本工作路径

    return: str

    返回本脚本的工作路径，默认为调用本脚本的文件夹。
    """

    return path


def error_message():
    """
    错误信息

    return: str

    返回错误信息文本，方便调用。
    """

    return "参数错误，通过`" + script_name() + " -h` 获取帮助"


def help_message():
    """
    帮助信息

    return: str

    返回帮助信息文本，方便调用。内容为本脚本的说明文档。
    """

    return __doc__


def command_getter(argv):
    """
    获取命令

    reutrn: dict
        {
            'command_name': command_name,
            'command_mapname': command_mapname,
            'command_dir': command_dir
        }

    ``command_name``      type: str  命令的名称，对应的命令通过 -h 查看。
    ``command_mapname``   type: str  对译表名称。
    ``command_dir``       type: str  执行命令的目录。
    """
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
    """
    命令切换器

    根据 ``command_bundle`` 执行各个命令。命令用途通过 -h 查看。

    ``command_bundle``  ``command_getter``的返回值。
    """
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
    if command_name == "zip":
        zipimgs.zip_cur_imgs()


def exe_command(argv):
    """
    根据参数执行命令

    控制函数，用于同一调用 ``command_getter`` 和 ``command_switcher`` 两个方法。
    """
    command_bundle = command_getter(argv)
    command_switcher(command_bundle)


def main(argv):
    """
    主函数

    默认执行的函数，用于接受命令行参数并调用 ``exe_command``，参数有问题时抛出错误。
    """
    try:
        exe_command(argv)
    except getopt.GetoptError:
        print(error_message())

if __name__ == '__main__':
    main(sys.argv)
