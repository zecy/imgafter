# _*_ coding: utf-8 _*_
"""
对图片集进行打包，通过 ``imgafter.py`` 调用。

包含方法：

    @zip_cur_imgs()
        打包当前目录下所有图片，并把压缩包移到上级目录，压缩包名称为目录名称。

    @zip_sub_dir_imgs(path=".")
        打包 `path` 下所有纯图片文件夹。
        纯图片文件夹条件：
            1.不为空；
            2.文件全部为图片；
            3.不包含子文件夹。
"""

import zipfile
import os
import basefunc


def main():
    print(__doc__)


def cur_images(path):
    """返回 path 下的所有图片"""
    return basefunc.parseimgs(path)


def cur_dir_name():
    """返回当前目录的名称"""
    return os.getcwd().split('/')[-1]


def parent_dir_name():
    """返回当父目录的名称"""
    return os.getcwd().split('/')[-2]


def zip_cur_imgs(path="."):
    """ 打包当前目录下所有图片，并把压缩包移到上级目录，压缩包名称为目录名称。 """
    os.chdir(path)
    zip_file_name = cur_dir_name() + '.zip'
    cur_imgs = cur_images(".")
    try:
        with zipfile.ZipFile(zip_file_name, "w", zipfile.ZIP_STORED) as zf:
            for img in cur_imgs:
                zf.write(img)
        os.rename(zip_file_name, "../" + zip_file_name)
        print("\n`" + zip_file_name + "` 压缩完成，" +
              "并已移动到 `" + parent_dir_name() + "` 目录下。")
    except zipfile.BadZipfile as err:
        print("压缩文件错误：\n    ", err)


def zip_sub_dir_imgs(path="."):
    """ 把目录下的子目录各自进行打包，压缩包名称为目录名称。"""

    sub_dirs = next(os.walk(path))[1]

    img_dirs = []
    no_img_dirs = []
    dir_already_zip = []
    zip_count = 0

    for sub_dir in sub_dirs:
        if basefunc.all_imgs(sub_dir):
            img_dirs.append(sub_dir)
        else:
            no_img_dirs.append(sub_dir)

    for img_dir in img_dirs:
        try:
            if not os.path.exists(img_dir + ".zip"):
                os.chdir(img_dir)
                zip_cur_imgs()
                os.chdir("..")
                zip_count += 1
            else:
                dir_already_zip.append(img_dir + " ==> " + img_dir + ".zip")
        except FileNotFoundError:
            print("找不到目录：\n    ", img_dir)

    print("\n[压缩结果]\n\n" +
          "    共 " + str(len(sub_dirs)) + " 个文件夹，成功压缩 " + str(zip_count) + " 个文件夹。\n")

    if len(no_img_dirs) > 0:
        print("[未处理文件夹]\n\n" +
              "    本命令只支持纯图片文件夹，因此以下文件夹未被压缩，如果它们是目标文件夹，请检查：\n\n" +
              "        " + "\n        ".join(no_img_dirs) + "\n\n" +
              "    纯图片文件夹条件：\n\n" +
              "        1.不为空；2.文件全部为图片；3.不包含子文件夹。\n")

    if len(dir_already_zip) > 0:
        print("[忽略文件夹]\n\n"
              "    以下文件夹已经被压缩，因此未被处理。如果你希望重新压缩，请先删除原同名压缩包：\n\n" +
              "        " + "\n        ".join(dir_already_zip))

if __name__ == '__main__':
    main()
