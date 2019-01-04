#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/1/4 21:18 

import sys
import os
import re
from py2neo import Graph, Node
import pandas as pd

class Md2Neo4j:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.graph = Graph(host=self.host, user=self.user, password=self.password)


    def markdown_transform(self, file_path, pjt_id):
        with open(file_path, 'r') as f:
            md = f.readlines()
        line_str = []
        for line in md:
            line_str.append(line.strip())
        line_str = [line for line in line_str if line != '']

        m = 1
        for i in range(1, len(line_str)):
            title = len(re.match(r'^[#]+', line_str[i])[0])
            if title > m:
                node_a, _ = self.str2node(line_str[i-1], pjt_id)
                node_b, relation = self.str2node(line_str[i], pjt_id)
                self.graph.run("merge (a%s) merge (b%s) merge (a)-[:%s]->(b)" % (node_a, node_b, relation))
                m = title
            else:
                j = 0
                while len(re.match(r'^[#]+', line_str[i-j])[0]) >= title:
                    j += 1
                node_a, _ = self.str2node(line_str[i - j], pjt_id)
                node_b, relation = self.str2node(line_str[i], pjt_id)
                self.graph.run("merge (a%s) merge (b%s) merge (a)-[:%s]->(b)" % (node_a, node_b, relation))

    def str2node(self, node_info, pjt_id):
        line = re.match(r'#* (.*)', node_info)[1]
        lines = line.split('/')
        for i in range(len(lines)):
            try:
                result = re.match(r'(.*):(.*)', lines[i])
                if i == 0:
                    str_re = ':' + result[2] + ' {'
                else:
                    str_re += "%s:'%s', " % (result[1], result[2])
            except:
                relation = re.match(r'\{(.*)\}', lines[i])[1]
            else:
                relation = 'TRANSFER'
        str_re += "PROJECT_ID: '%s'" % (pjt_id)
        return str_re, relation



if __name__ == '__main__':
    md2neo = Md2Neo4j(host='localhost', user='neo4j', password='neo4j')
    md2neo.md_check('./input/neo.md')