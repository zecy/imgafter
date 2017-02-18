#图片集后期处理

## 这是
一系列用于对图片文件集（典型如漫画）进行处理的脚本

## 你通过
`imgafter.py` 来使用它们：

```
{存放 imgafter.py 的目录}/imgafter.py <命令名> [-m <对译表名称>] [-d <目标路径>]
```

## 它们是
- `leftpad`

    对当前目录下的图片文件名补零。

- `flatten` 
    
    为当前目录下子文件夹中图片添加子文件夹名称为前缀，并提到当前目录。

- `map`

    依据对译表对当前目录下的图片文件进行重命名。

- `zip`
    
    打包当前目录下所有图片，并把压缩包移到上一级目录。压缩包名称为目录名称。

- `zipall`
    
    分别打包当前目录下的纯图片文件夹，每个文件夹为一个压缩包，压缩包名成为文件夹名称。

## 它们还有一些参数

- `-m`

    文件名对译表，默认为 `map` ，一个无后缀名的纯文本文件
- `-d`

    目标文件夹，默认为当前名录

默认情况下不需要设置上面两个参数

## 通过 `alias` 让的你生活美好一些

```
alias img='python3 {存放 imgafter.py 的目录}/imgafter.py'
alias leftpad='python3 {存放 imgafter.py 的目录}/imgafter.py leftpad'
```

## 使用它们你需要
- py3