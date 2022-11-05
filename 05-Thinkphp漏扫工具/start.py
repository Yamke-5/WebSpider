# coding=utf-8
from code import *
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ThinkPHP漏洞扫描工具')
    sys.stdout.write(f'请输入以下的版本号:{version}和url即可')
    parser.add_argument('-f', help='请输入文件名称')
    parser.add_argument('-u', help='请输入网址')
    args = parser.parse_args()
    sys.stdout.write(f'\r')
    scan = Scanphp(args.f, args.u)
    scan.start()
