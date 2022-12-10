# coding=utf-8
import os
import sys
import re
#  引入配置文件
from config import *


def get_config():
    '''
    获取当前系统的配置信息
    '''
    # 判断是否已经读取了配置文件
    if not os.path.exists(f'{two_file_path_save}'):
        # 读取配置的信息
        os.system(f'secedit /export /cfg {first_file_path_save}')
        # 文件转码(注意必要的操作)
        os.system(f'type {first_file_path_save} > {two_file_path_save}')
        # 删除转码前的文件
        os.remove(first_file_path_save)
    # 如果已经有文件就读取本身配置的信息
    else:
        if not os.path.exists(two_file_path_save):
            print('未检测到系统文件')
            sys.exit('-1')
    print('读取系统配置成功')


def read_config():
    '''
    读取配置文件
    '''
    # 读取获取到的配置文件
    f = open(f'{two_file_path_save}', mode='r')
    for i in f.readlines():
        # 将遍历的数据存入临时列表中方便查询
        temp_cst.append(i.strip('\n'))
    #  文件关闭操作
    f.close()


def write_rule(string):
    '''
    写入信息到文件中
    :param string: 传入文本
    '''
    f = open(file_rule, mode='a+', encoding='gbk')
    f.write(string)
    f.close()


def rule():
    '''
    这里是判断是否满足规则的位置
    '''
    # 初始化总条目变量
    total_all = 0
    # 初始化正确条目变量
    total_t = 0
    # 初始化错误条目变量
    total_f = 0
    # 初始化需要手工检查变量
    total_m = 0
    # 文件如果存在就删除
    if os.path.exists(file_rule):
        os.remove(file_rule)
    # 存放规则队列
    rules = [password_timeout(), passwords_sizeof(), password_history(),
             user_locktime(), user_locknum(), user_lockconum(),
             user_remote_line()]
    # 执行规则
    for i in rules:
        all, t, f, m = i
        total_all += all
        total_t += t
        total_f += f
        total_m += m
    # 打印检测数据
    rule_result = rf'''
        <__________检测结果如下__________>
        <___总检测条目:{total_all}_______________>
        <_____正确条目:{total_t}_______________>
        <_____错误条目:{total_f}_______________>
        <____手工检查条目:{total_m}_______________>
    '''
    # 打印结果
    print(rule_result)


def password_timeout():
    '''
        判断windows策略的时间是否合乎规则
    '''
    r1 = []

    for i in temp_cst:
        # 读取条件规则
        if i.find('MaximumPasswordAge') != -1:
            r1.append(i)
    # 数据处理
    temp = r1[0].split('=')
    temp = int(temp[1].strip())
    # 进行与定义的规则判断
    rule_str = ''
    all, t, f, m = 0, 0, 0, 0
    if temp >= rule_passwords_timeout:
        # 错误条目次数
        f += 1
        # 需要手工设置条目
        m += 1
        # 总检查条目
        all += 1
        # 追加文本的内容
        rule_str += f'1--windows系统的密码过期时间超过了设置，建议设置在{rule_passwords_timeout}天之下'
        print(rule_str)
        # 写入文件
        write_rule(string=rule_str + '\n')
    else:
        # 正确条目
        t += 1
        all += 1
    # 返回处理结果
    return all, t, f, m


def passwords_sizeof():
    '''
       检查是否已配置密码长度最小值
    '''
    r1 = []
    all, t, f, m = 0, 0, 0, 0
    for i in temp_cst:
        # 读取条件规则
        if i.find('MinimumPasswordLength') != -1:
            r1.append(i)
    # 数据处理
    # print(r1)
    temp = r1[0].split('=')
    temp = int(temp[1].strip())
    # 进行与定义的规则判断
    rule_str = ''
    if temp <= rule_passwords_timeout:
        # 错误条目次数
        f += 1
        # 需要手工设置条目
        m += 1
        # 总检查条目
        all += 1
        # 追加文本的内容
        rule_str += f'2--windows系统密码设置长度不满足条件，建议设置在{rule_password_sizeof}位之上'
        print(rule_str)
        # 写入文件
        write_rule(string=rule_str + '\n')
    else:
        # 正确条目
        t += 1
        all += 1
    # 返回处理结果
    return all, t, f, m


def password_history():
    '''
       检查是否已正确配置强制密码历史
       注意本条可能很大程度不存在
    '''
    r1 = []
    all, t, f, m = 0, 0, 0, 0
    for i in temp_cst:
        # 读取条件规则
        if i.find('PasswordHistorySize') != -1:
            r1.append(i)
    # 数据处理
    # print(r1)
    # 判断是否为空如果为空就返回不存在
    try:
        temp = r1[0].split('=')
    except Exception as e:
        all, t, f, m = 0, 0, 0, 0
        print('3--未发现windows账户强制密码历史选项，请配置后重新尝试')
        # 返回处理结果
        return all, t, f, m
    temp = int(temp[1].strip())
    # 进行与定义的规则判断
    rule_str = ''
    if temp <= rule_password_history:
        # 错误条目次数
        f += 1
        # 需要手工设置条目
        m += 1
        # 总检查条目
        all += 1
        # 追加文本的内容
        rule_str += f'3--windows系统强密码历史过少，建议设置在{rule_password_history}次以上'
        print(rule_str)
        # 写入文件
        write_rule(string=rule_str + '\n')
    else:
        # 正确条目
        t += 1
        all += 1
    # 返回处理结果
    return all, t, f, m


def user_locktime():
    '''
    检查是否已正确配置帐户锁定时间
    注意本条可能很大程度不存在
    '''
    r1 = []
    all, t, f, m = 0, 0, 0, 0
    for i in temp_cst:
        # 读取条件规则
        if i.find('ResetLockoutCount') != -1:
            r1.append(i)
    # 数据处理
    # print(r1)
    # 判断是否为空如果为空就返回不存在
    try:
        temp = r1[0].split('=')
    except Exception as e:
        all, t, f, m = 0, 0, 0, 0
        print('4--未发现windows账户锁定时间选项，请配置后重新尝试')
        # 返回处理结果
        return all, t, f, m
    temp = int(temp[1].strip())
    # 进行与定义的规则判断
    rule_str = ''
    if temp >= rule_user_locktime:
        # 错误条目次数
        f += 1
        # 需要手工设置条目
        m += 1
        # 总检查条目
        all += 1
        # 追加文本的内容
        rule_str += f'4--windows系统强锁定时间过短，建议设置在{rule_user_locktime}以上'
        print(rule_str)
        # 写入文件
        write_rule(string=rule_str + '\n')
    else:
        # 正确条目
        t += 1
        all += 1
    # 返回处理结果
    return all, t, f, m


def user_locknum():
    '''
       检查是否已正确配置帐户锁定阈值
       注意本条可能很大程度不存在
       '''
    r1 = []
    all, t, f, m = 0, 0, 0, 0
    for i in temp_cst:
        # 读取条件规则
        if i.find('LockoutBadCount') != -1:
            r1.append(i)
    # 数据处理
    # print(r1)
    # 判断是否为空如果为空就返回不存在
    try:
        temp = r1[0].split('=')
    except Exception as e:
        all, t, f, m = 0, 0, 0, 0
        print('5--未发现windows帐户锁定阈值选项，请配置后重新尝试')
        # 返回处理结果
        return all, t, f, m
    temp = int(temp[1].strip())
    # 进行与定义的规则判断
    rule_str = ''
    if temp >= rule_user_lockNum:
        # 错误条目次数
        f += 1
        # 需要手工设置条目
        m += 1
        # 总检查条目
        all += 1
        # 追加文本的内容
        rule_str += f'5--windows系统帐户锁定阈值次数过少，建议设置在{rule_user_lockNum}次以上'
        print(rule_str)
        # 写入文件
        write_rule(string=rule_str + '\n')
    else:
        # 正确条目
        t += 1
        all += 1
    # 返回处理结果
    return all, t, f, m


def user_lockconum():
    '''
           检查是否已正确配置复位帐户锁定计数器
           注意本条可能很大程度不存在
           '''
    r1 = []
    all, t, f, m = 0, 0, 0, 0
    for i in temp_cst:
        # 读取条件规则
        if i.find('LockoutDuration') != -1:
            r1.append(i)
    # 数据处理
    # print(r1)
    # 判断是否为空如果为空就返回不存在
    try:
        temp = r1[0].split('=')
    except Exception as e:
        all, t, f, m = 0, 0, 0, 0
        print('6--未发现windows复位帐户锁定计数器选项，请配置后重新尝试')
        # 返回处理结果
        return all, t, f, m
    temp = int(temp[1].strip())
    # 进行与定义的规则判断
    rule_str = ''
    if temp <= rule_user_lockNum:
        # 错误条目次数
        f += 1
        # 需要手工设置条目
        m += 1
        # 总检查条目
        all += 1
        # 追加文本的内容
        rule_str += f'6--indows复位帐户锁定计数器次数过多，建议设置在{rule_user_lockNum}次以下'
        print(rule_str)
        # 写入文件
        write_rule(string=rule_str + '\n')
    else:
        # 正确条目
        t += 1
        all += 1
    # 返回处理结果
    return all, t, f, m


def user_remote_line():
    '''
               检查是否已删除可远程访问的注册表路径和子路径
               注意本条可能很大程度不存在
    '''
    r1 = []
    all, t, f, m = 0, 0, 0, 0
    for i in temp_cst:
        # 读取条件规则
        if i.find('MACHINE\System\CurrentControlSet\Control\SecurePipeServers\Winreg\AllowedExactPaths\Machine') != -1:
            r1.append(i)
    # 数据处理
    # print(r1)
    try:
        temp = r1[0].split(',')
    except Exception as e:
        all, t, f, m = 0, 0, 0, 0
        print('7--未发现windows可远程访问的注册表路径和子路经，请配置后重新尝试')
        # 返回处理结果
        return all, t, f, m
    # 进行与定义的规则判断
    rule_str = ''
    if len(temp[1]) != 0:
        # 错误条目次数
        f += 1
        # 需要手工设置条目
        m += 1
        # 总检查条目
        all += 1
        # 追加文本的内容
        rule_str += f'7--windows可远程访问的注册表路径和子路经未删除，建议删除路径'
        print(rule_str)
        # 写入文件
        write_rule(string=rule_str + '\n')
    else:
        # 正确条目
        t += 1
        all += 1
    # 返回处理结果
    return all, t, f, m


def run():
    '''
    系统执行的方法，外部调用即可
    '''
    # 读取配置信息
    get_config()
    # 整合数据
    read_config()
    # 规则判断
    rule()
