# _*_ coding: utf-8 _*_

import zipfile
import os
import rename


def main():
    print("通过外部调用")


def cur_images(path):
    return rename.parseimgs(path)


def cur_dir_name():
    return os.getcwd().split('/')[-1]


def zip_cur_imgs():
    ''' 打包当前目录下所有图片，并把压缩包移到上级目录，压缩包名称为目录名称。 '''
    zip_file_name = cur_dir_name() + '.zip'
    cur_imgs = cur_images('.')
    try:
        with zipfile.ZipFile(zip_file_name, "w", zipfile.ZIP_STORED) as zf:
            for img in cur_imgs:
                zf.write(img)
        os.rename(zip_file_name, "../" + zip_file_name)
        print("`" + zip_file_name + "` 压缩完成，" +
              "并已移动到 `" + parent_dir_name() + "` 目录下。")
    except zipfile.BadZipfile as err:
        print("压缩文件错误：\n    ", err)


if __name__ == '__main__':
    main()
