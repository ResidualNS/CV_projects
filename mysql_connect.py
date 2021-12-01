# -*- coding: utf-8 -*-
# __author__:YZY
# 2021/5/11 17:13
'''
将表格数据添加数据库
'''
import pymysql

def insert_db(data):
    # 打开数据库连接，不需要指定数据库，因为需要创建数据库
    db = pymysql.connect('localhost', user = "yzy", passwd = "123456")
    # 获取游标
    cursor = db.cursor()
    # 创建pythonBD数据库
    cursor.execute('CREATE DATABASE IF NOT EXISTS pythondb DEFAULT CHARSET utf8 COLLATE utf8_general_ci;')

    sql = """INSERT INTO `USER_INFO` (`USER_NAME`,`SAP_ID`,`MODEL_NAME`) VALUES (%s,%s,%s)"""
    try:
        cursor.executemany(sql,data) #sql执行
        db.commit() #提交到数据库
    except Exception as e: #获取报错信息
        print(e)

    cursor.close()#先关闭游标
    db.close()#再关闭数据库连接
    print('创建数据库成功')


import sqlite3
conn = sqlite3.connect("production.db")
cursor = conn.cursor()
sql = """select name from sqlite_master where type='table' order by name"""
cursor.execute(sql)
tab_name = cursor.fetchall()
tab_name = [line[0] for line in tab_name]
print(tab_name)
cursor.execute('pragma table_info({})'.format(tab_name[2]))
col_name=cursor.fetchall()
col_name=[x[1] for x in col_name]
print(col_name)
#
# cursor.execute('select '+ col_name[6] +' from ' + (tab_name[2]))
# ca_set = cursor.fetchall()
# print(ca_set)

cursor.execute('select * from '+ tab_name[2])
cdset=cursor.fetchall()
cdset=[list(line) for line in cdset] #将结果集的元组转为列表，才能修改。
for line in cdset:
    print(line)



print('...')
