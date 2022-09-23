
'''
该文件对之前所有create文件做了统一规范，方便使用
(1)使用该文件时将所有文档打包成一个文件夹置于file_data文件夹中，并将文件夹命名为你想建立的ES数据库索引名称，同时将每个文件对应的文件链接放在file_data文件夹下;
文件链接对应名称应为path：存放文件名称和文件链接对应的excel文件，此excel文件第一行应为两个title,即fileName和path，后缀为.xlsx
(2)该方法会自动读取所有文件生成json文件并在ES数据库中建立与文件夹同名索引
(3)会在data_file文件夹下生成同名json文件，请使用curl命令将其导入你的ES数据库
(4)使用此文件前请前往同目录下Index_create文件将ES数据库链接和账户信息修改成自己的ES数据库信息
(5)请注意在linux系统下和windows系统文件路径表示会有不同，在此使用的是windows系统下的路径
'''
import os
from test import write_json
from Index_create import index_create
from Link_replace import link_replace


def json_create():
        old_path = 'file_data\\'
        dir_list = os.listdir(old_path)
        index_name = dir_list[0]
        path = 'file_data\\' + index_name + '\\'     #打开文件夹目录
        fileList = os.listdir(path)          #保存各个文件名字
        n = len(fileList)

        TypeList = []     #用于存储各个文本内容
        #利用excel文件替换链接进入PathList
        link_path = 'file_data\\' + index_name + '.xlsx'
        PathList = link_replace(link_path, fileList)     #用于存储各个文件的链接/路径
        print(PathList)
        print(len(PathList))
        ##################################
        for i in range(0, n):
            a = open(path + fileList[i], "r", encoding='utf-8')
            out = str(a.readlines())    #逐行读取文本
            str_out = ""
            for x in out:
                str_out += x           #将整个文本组成一个字符串
            TypeList.append(str_out)   #加入文本列表


        number = 1
        ju_1 = ''
        ju_2 = ''

        # print(ju_1)
        k = 0
        for x in TypeList:
            res_1 = ju_1 + str(fileList[k])   #构建文本id
            h1 = {"_index": index_name, "_id": res_1}
            h2 = {"index": h1}                #构建指引头部index
            print(res_1)
            #a = open(r"r1.6.json", "a", encoding='UTF-8')
            #a.write(res_1)
            write_json('..\data_file\\' + index_name + '.json', h2)      #写入json文件

            res_2 = ju_2 + x
            print(res_2)
            hashmap2 = {"file_link": PathList[k], "text_entry": res_2}
            write_json('..\data_file\\' + index_name + '.json', hashmap2)        #写入json文件
            k += 1
            number += 1
            # a = open(r'out1.7.json', "a", encoding='UTF-8')
            # a.write(res_2)
        print(index_name)
        index_create(index_name)

if __name__ == '__main__':
    json_create()
