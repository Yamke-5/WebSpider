# coding=utf-8
from config import *
from User_Agent_random import *
import sys
import requests
import re
import os


class Scanphp:
    def __init__(self, filename, url):
        # 判断是否输入了正确的文件版本号
        if filename not in version:
            sys.stdout.write('输入的文件版本不对')
            sys.exit(-1)
        self.__filepath = filepath + '/' + str(filename)
        self.__url = url.strip('/')
        #     检测临时文件是否存在
        if os.path.exists(tmp):
            os.remove(tmp)

    # 读取Payload到url并且写出成功的结果集
    def __read_file(self, file):
        with open(file, mode='r', encoding='utf-8') as f:
            for line in f:
                a, b = line.split(':')
                if self.__request_url(urls=self.__url + b):
                    print(f'存在{a}漏洞,写入数据到{tmp}文件中')
                    file = open(tmp, mode='a+', encoding='utf-8')
                    file.write(f'{a}\n{self.__url + b}')
                else:
                    print(rf'抱歉未扫描出漏洞')

    # 爬虫体
    def __request_url(self, urls):
        ua = UserAgent()
        head = {
            'User-Agent': ua.randoms()
        }
        res = requests.get(url=urls, headers=head)
        html = res.text
        res.close()

        # 找里面是否有关键字。如果有就返回真，没有就返回假
        if re.findall('phpinfo', html):
            return True
        return False

    # 定义执行的方法
    def start(self):
        self.__read_file(self.__filepath)
