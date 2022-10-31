from config import *
import os
import exrex


class Url_Dict:
    def __init__(self, url):
        self._url = url
        self._filiter_url = []

    def _url_filiter_url(self):
        '''
        用于过滤网址里面的关键字
        :return: 返回过滤后的关键字
        '''
        url = self._url
        url = url.rstrip('/')
        # 分割http协议
        if '://' in url:
            temp = url.split('://')
            url = temp[1]
        # 对点进行分割操作
        urls = url.split('.')
        # 过滤黑名单
        lists = []
        for i in urls:
            if i not in black_list_url:
                lists.append(i)
        # 假如有斜杠需要去掉最后面的斜杠
        return lists

    def _random_list(self):
        self._filiter_url = self._url_filiter_url()
        # 判断字典文件是否存在,存在就删除
        if os.path.exists('./dicts/dict.txt'):
            os.remove('./dicts/dict.txt')
        # 调用过滤后的关键字
        for d in self._filiter_url:
            # 调用配置文件
            for p in passwd_m_list:
                # 正则表达式，关系到生成的字典的配置
                re_dict = d + password_re + p
                # 根据正则的规则生成字典
                with open(rf'./dicts/dict.txt', mode='a+', encoding='utf-8') as f:
                    for i in list(exrex.generate(re_dict)):
                        f.write(i + '\n')

    def start(self):
        '''
        外部调用的开始方法
        '''
        self._random_list()
