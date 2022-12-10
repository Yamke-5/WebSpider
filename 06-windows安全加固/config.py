# coding=utf-8

'''
程序配置项
'''
# 读取配置文件的默认存放路径
first_file_path_save = r'1.txt'
two_file_path_save = r'2.txt'
# 临时存放读取到的系统配置
temp_cst = []

# 文件写入位置
file_rule = r'rule.csv'

'''
系统判定的规则
'''
# windows密码最长的过期时间
rule_passwords_timeout = 90
# windows是否已配置密码长度最小值
rule_password_sizeof = 8
# windows强制密码历史
rule_password_history = 2
# windows帐户锁定时间
rule_user_locktime = 1
# windows帐户锁定阈值
rule_user_lockNum = 5
# windows 帐户锁定计数器
rule_user_lockCoNum = 5
