import threading
import requests
from config import *
from bs4 import BeautifulSoup
import re
import os
from queue import Queue


class Ip_Address:
    def __init__(self, T):
        # url
        self.__url = url
        self._threader_count = int(T)
        self._threader = []
        self._result = []
        self._queue = Queue()

    def _request_url(self):
        '''
        请求单个网页
        :return:
        '''
        responce = requests.get(url=self.__url, headers=head)
        html = responce.content.decode('gb2312')
        # 关闭爬虫体，减少系统资源的占用以及服务器的压力
        responce.close()
        # 将所有的url进行分离
        soup = BeautifulSoup(html, 'lxml')
        a_list = soup.find_all(name='a', attrs={'href': re.compile(r'^/areaindex_\w+/1.html')})
        # 判断文件是否存在
        if os.path.exists(fr'./url/{url_name_file}'):
            os.remove(fr'./url/{url_name_file}')
        # 写文件操作
        for i in a_list:
            self._write_url(i['href'])

    def _write_url(self, temp):
        '''
        写爬取到的url 地址到文件中方便读取
        '''
        f = open(rf'./url/{url_name_file}', mode='a+', encoding='utf-8')
        f.write(f'http://www.66ip.cn{temp}\n')
        f.close()

    def _init_queue(self):
        with open(f'./url/{url_name_file}') as f:
            for u in f:
                self._queue.put(u.rstrip())

    class Ip_spider_run(threading.Thread):
        def __init__(self, quere):
            super().__init__()
            self._quere = quere
            self._result = []

        def run(self):
            while not self._quere.empty():
                res = requests.get(self._quere.get(), headers=head)
                html = res.content.decode('gb2312')
                res.close()
                soup = BeautifulSoup(html, 'lxml')
                table = soup.find('table', bordercolor='#6699ff')
                # 再找 tr
                trs = table.find_all('tr')
                del (trs[0])
                for tr in trs:
                    tds = tr.find_all('td')
                    url = r'http://httpbin.org/ip'
                    proxy = {
                        'http': 'http://' + tds[0].text + ':' + tds[1].text,
                        'https': 'http://' + tds[0].text + ':' + tds[1].text
                    }
                    try:
                        res = requests.get(url, headers=head, proxies=proxy, timeout=3)
                        res.close()
                        if res.status_code == 200:
                            print(f'已经成功：{proxy}')
                            #     写入结果集
                            self._result.append(tds[0].text + ':' + tds[1].text + '\n')
                    except Exception as e:
                        pass
            self._result = list(set(self._result))
            for i in self._result:
                f = open(f'./url/{ip_name_file}', mode='a+', encoding='utf-8')
                f.write(i)
                f.close()

    def start(self):
        '''
        执行类的所有方法
        '''
        # 爬取全部的url地址
        self._request_url()
        # 准备队列
        self._init_queue()
        if os.path.exists(f'./url/{ip_name_file}'):
            os.remove(f'./url/{ip_name_file}')
        # 准备线程
        for i in range(self._threader_count):
            self._threader.append(self.Ip_spider_run(self._queue))
        # 启动线程
        for i in self._threader:
            i.start()
        # 等待子线程结束
        for i in self._threader:
            i.join()

        print('已经全部完成')
