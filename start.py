import argparse
from code import *
import exrex

if __name__ == '__main__':
    # 定义命令集
    parser = argparse.ArgumentParser(description='密码字典生成器')
    parser.add_argument('-u', help='用于分析的url连接')

    # 获取参数
    args = parser.parse_args()
    # print(args.u)
    # print(args.t)
    url_dict = Url_Dict(url=args.u)
    url_dict.start()
    print('字典生成完成')
