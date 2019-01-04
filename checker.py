#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/1/4 21:20 

import re
import os
import logging

class Checker:
    def __init__(self):
        LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
        self.log = logging.basicConfig(filename='./log/my.log', level=logging.DEBUG, format=LOG_FORMAT)

    def md_check(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            md = f.readlines()
        line_str = []
        for line in md:
            line_str.append(line.strip())
        line_str = [re.match(r'^[#]+ (.*)', line)[1] for line in line_str if line != '']

        logging.info('='*100)
        logging.info('开始检查项目拓扑关系markdown文件%s' % (file_path.split('/')[-1]))
        # 项目节点检查
        for i in range(len(line_str)):
            line = line_str[i]
            # 英文"："/"/"和空格检查
            if len(re.findall(r'[：\s\\、，,;；]', line))>0:
                logging.error('节点%s存在:或者/或者空格,或者中文输入错误，请排查!' % (line))
        logging.info('markdown文件%s检查完毕' % (file_path.split('/')[-1]))
        logging.info('=' * 100)

if __name__ == '__main__':
    checker = Checker()
    checker.md_check('./input/neo.md')