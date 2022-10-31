import argparse
from code import *

if __name__ == '__main__':
    # 配置命令行参数
    parser = argparse.ArgumentParser(description='这是个爬取IP地址的工具，ip地址仅限http类型')
    parser.add_argument('-t', help='输入线程数量')
    # 获取参数
    args = parser.parse_args()
    ipaddress = Ip_Address(T=args.t)
    ipaddress.start()
