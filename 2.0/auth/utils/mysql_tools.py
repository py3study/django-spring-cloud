#!/usr/bin/env python3
# coding: utf-8
"""
远程执行mysql语句
"""
# if __name__ == '__main__':
#     # 添加当前目录到环境变量中
#     import os
#     import sys
#
#     base_dir = os.getcwd()
#     sys.path.append(base_dir)

import pymysql


class ExecutionSql(object):
    def __init__(self, host, user, password, port):
        self.host = host
        self.user = user
        self.password = password
        self.port = port

    def select(self, sql):
        """
        执行sql命令
        :param sql: 命令
        :return: 元祖
        """
        try:
            conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port,
                charset='utf8',
                cursorclass=pymysql.cursors.DictCursor
            )
            cur = conn.cursor()  # 创建游标
            cur.execute(sql)  # 执行sql命令
            res = cur.fetchall()  # 获取执行的返回结果
            cur.close()
            conn.close()  # 关闭mysql 连接
            return res
        except Exception as e:
            print(e)
            return False

    def update(self, sql):
        """
        更新操作，比如insert, delete,update
        :param sql: sql命令
        :return: bool
        """
        try:
            conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port,
            )
            cur = conn.cursor(cursor=pymysql.cursors.DictCursor)  # 创建游标
            rows = cur.execute(sql)  # 执行sql命令，返回影响的行数
            # res = cur.fetchall()  # 获取执行的返回结果
            if not isinstance(rows, int):  # 判断返回结果, 是数字就是正常的
                print('错误，执行sql: %s 失败' % sql)
                return False

            conn.commit()  # 主动提交，否则执行sql不生效
            cur.close()
            conn.close()  # 关闭mysql 连接
            return rows
        except Exception as e:
            print(e)
            print('错误，执行命令: {} 异常'.format(sql))
            return False

    def insert(self, sql):
        """
        插入操作
        :param sql: sql命令
        :return: bool
        """
        return self.update(sql)

    def delete(self, sql):
        """
        删除操作
        :param sql: sql命令
        :return: bool
        """
        return self.update(sql)
