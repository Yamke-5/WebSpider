import requests

from config import *
import os
import sys
from queue import Queue
import threading


class Scan:
    def __init__(self, dict_address, url, threads_counts):
        # 判断字典是否存在
        if not os.path.exists(dict_address):
            print('字典不存在')
            sys.exit(-1)
        self._dict_name = dict_address
        self._url = self._filter_url(urls=url)
        # 准备队列
        self._queue = Queue()
        # 准备线程数量
        self._threads = int(threads_counts)
        self._threads_list = []
        self._queue_total = 0

    def _read_dict(self):
        '''
        读取字典并且返回值
        '''
        with open(self._dict_name, mode='r', encoding=dict_type) as f:
            for d in f:
                # 将拼接好的url放进队列
                self._queue.put('http://' + self._url + '/' + d)
                self._queue.put('https://' + self._url + '/' + d)
            # 存储队列的总数
            self._queue_total = self._queue.qsize()

    def _filter_url(self, urls):
        '''
        对url进行处理
        :param urls: 传入网址
        :return: 返回处理后的纯净url
        '''
        temp = ''
        if 'http://' in urls:
            temp = urls.split('http://')
            temp = temp[1].rstrip('/')
        if 'https://' in urls:
            temp = url.split('https://')
            temp = temp[1].rstrip('/')
        return temp

    class Dir_scan(threading.Thread):
        def __init__(self, queue, total):
            super().__init__()
            self._queue = queue
            self._queue_total = total

        def run(self):
            while not self._queue.empty():
                scan_url = self._queue.get().rstrip()
                # 打印进度信息
                self._message(self._queue.qsize())
                try:
                    res = requests.get(url=scan_url, headers=head, timeout=2)
                    res.close()
                    if res.status_code == 200:
                        self._write_file(scan_url)
                except Exception as e:
                    pass

        def _message(self, last_count):
            line = round(100 - ((last_count / self._queue_total) * 100), 2)
            sys.stdout.write(f'\r当前进度：{line}%' + '=' * int(line // 2) + '>')

        def _write_file(self, u):
            with open(ip_address, mode='a+', encoding='utf-8') as f:
                f.write(u + '\n')

    def start(self):
        '''
        执行类的所有方法
        '''
        self._read_dict()
        if os.path.exists(ip_address):
            os.remove(ip_address)
        # 准备线程
        for i in range(self._threads):
            self._threads_list.append(self.Dir_scan(self._queue, self._queue_total))

        # 启动线程
        for i in self._threads_list:
            i.start()
        # 等待子线程结束
        for i in self._threads_list:
            i.join()
