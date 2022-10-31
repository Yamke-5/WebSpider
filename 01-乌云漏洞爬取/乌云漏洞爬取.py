# coding=utf-8
import requests
import re
# 调用多线程函数
import threading
import time
from User_Agent_random import UserAgent


# 爬虫主体
def split(search):
    # 随机请求头
    ua = UserAgent()
    head = {
        'User-Agent': ua.randoms(),
        'referer': 'https://wy.zone.ci/',
    }
    # 设置代理
    # proxy = {
    #     'http': 'http://223.82.60.202:8060',
    #     'https': 'https://223.82.60.202:8060'
    # }
    url = rf'https://wy.zone.ci/searchbug.php?q={search}&page=1'
    # 爬虫体
    res = requests.get(url=url, headers=head)
    # 处理页数
    page_nums = result_num(res.text)
    # 处理文件函数调用
    flag = page_message(res.text)
    # 关闭当前爬虫
    res.close()
    # 写入文件
    organize(flag)
    print('已经处理完成第1页')
    return page_nums


def result_num(value):
    req = r'page=\w+'
    page_nums = re.findall(req, value)
    page_nums = page_nums[3]
    page_nums = int(page_nums[5:])
    return page_nums


# 洗出网页数据
def page_message(value):
    restext = r'bug_detail.php\?wybug_id=wooyun-\w+-\w+">\w+'
    page_news = re.findall(restext, value)
    page_message = []
    for i in page_news:
        page_message += tuple(re.split('">', i))
    return page_message


# 文件写入
def organize(value):
    f = open('list.txt', mode='a+', encoding='utf-8')
    title = 0
    for i in value:
        title += 1
        if title % 2 == 0:
            f.write('名字:' + i + '\n')
        else:
            f.write('网址：https://wy.zone.ci/' + i + '\n')
    f.close()


# 处理其他页面的参数
def num_pages(value1, value2):
    for i in range(value1, value2 + 1):
        # 创建遍历的其他链接
        ua = UserAgent()
        head = {
            'User-Agent': ua.randoms(),
            'referer': 'https://wy.zone.ci/',
        }
        urls = rf'https://wy.zone.ci/searchbug.php?q={search}&page={i}'
        # 构建爬虫体
        resq = requests.get(url=urls, headers=head)
        # 处理文件函数
        more_message = page_message(resq.text)
        # 关闭当前爬虫
        resq.close()
        # 写入文件
        organize(more_message)
        print(rf'已经处理完成第{i}页')


if __name__ == '__main__':
    # 网址
    search = input('请输入要搜索的漏洞名称')
    # 传入值到爬虫,返回总的页数
    page_nums = split(search=search)
    # 输入线程数量
    th_nums = int(input('请输入线程数'))
    # 动态创建线程
    th_list = []
    new_page = page_nums // th_nums
    for i in range(1, th_nums + 1):
        if th_nums == 1:
            a = threading.Thread(target=num_pages, kwargs={'value1': 2, 'value2': page_nums})
            th_list.append(a)
        else:
            if i == 1:
                a = threading.Thread(target=num_pages, kwargs={'value1': 2, 'value2': new_page})
                th_list.append(a)
            elif i == th_nums:
                a = threading.Thread(target=num_pages,
                                     kwargs={'value1': int(new_page * (i - 1) + 1), 'value2': page_nums})
                th_list.append(a)
            else:
                a = threading.Thread(target=num_pages,
                                     kwargs={'value1': int(new_page * (i - 1) + 1), 'value2': new_page * i})
                th_list.append(a)
    # 动态调用线程
    for i in th_list:
        i.start()
