import argparse
from code import *
from config import *

if __name__ == '__main__':
    # 配置命令行参数
    parser = argparse.ArgumentParser(description='目录扫描工具')
    parser.add_argument('-dic', help='字典存放位置', default=dict_name)
    parser.add_argument('-u', help='网站的域名')
    parser.add_argument('-t', help='运行线程的数量', default=5)
    args = parser.parse_args()
    scan = Scan(args.dic, args.u, args.t)
    scan.start()
