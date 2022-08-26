# -*- coding: utf-8 -*-

# 按照大小分割文件

import os

filename = "../logs/HDFS/HDFS.log"  # 需要进行分割的文件，请修改文件名
size = 1073741824  # 分割大小约80K


def mk_SubFile(srcName, sub, buf):
    [des_filename, extname] = os.path.splitext(srcName)
    filename = des_filename + '_' + str(sub) + extname
    print('正在生成子文件: %s' % filename)
    with open(filename, 'wb') as fout:
        fout.write(buf)
        return sub + 1


def split_By_size(filename, size):
    with open(filename, 'rb') as fin:
        buf = fin.read(size)
        sub = 1
        while len(buf) > 0:
            sub = mk_SubFile(filename, sub, buf)
            buf = fin.read(size)
            break
    print("ok")


if __name__ == "__main__":
    split_By_size(filename, size)

# coding:utf-8
# 将大文本文件分割成多个小文本文件
import os

sourceFileName = "wm.txt"  # 定义要分割的文件


def cutFile():
    print("正在读取文件...")
    sourceFileData = open(sourceFileName, 'r', encoding='utf-8')
    ListOfLine = sourceFileData.read().splitlines()  # 将读取的文件内容按行分割，然后存到一个列表中
    n = len(ListOfLine)
    print("文件共有" + str(n) + "行")
    print("请输入需要将文件分割的个数:")
    m = int(input(""))  # 定义分割的文件个数
    p = n // m + 1
    print("需要将文件分成" + str(m) + "个子文件")
    print("每个文件最多有" + str(p) + "行")
    print("开始进行分割···")
    for i in range(m):
        print("正在生成第" + str(i + 1) + "个子文件")
        destFileName = os.path.splitext(sourceFileName)[0] + "_part" + str(i) + ".log"  # 定义分割后新生成的文件
        destFileData = open(destFileName, "w", encoding='utf-8')
        if (i == m - 1):
            for line in ListOfLine[i * p:]:
                destFileData.write(line + '\n')
        else:
            for line in ListOfLine[i * p:(i + 1) * p]:
                destFileData.write(line + '\n')
        destFileData.close()
    print("分割完成")


cutFile()