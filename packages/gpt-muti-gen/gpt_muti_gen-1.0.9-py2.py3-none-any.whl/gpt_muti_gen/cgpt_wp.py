#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Contact :   liuyuqi.gov@msn.cn
@Time    :   2022/12/16 23:48:27
@License :   Copyright © 2017-2022 liuyuqi. All Rights Reserved.
@Desc    :   
'''
import os
import sys
import datetime
import re
import logging
import time
import argparse
# from wordpress_xmlrpc import Client, WordPressPost
# from wordpress_xmlrpc.methods import posts
from gpt_muti_gen.chatgpt import ChatGPT
from gpt_muti_gen.libs.json_conf import JsonConf
from concurrent.futures import ThreadPoolExecutor


class CgptWp(object):

    def __init__(self):
        self.parser = argparse.ArgumentParser(description="文章批量生成配置")
        self.parser.add_argument(
            "--config", help="config for meiniang", default="config.josn")
        self.parser.add_argument(
            "--token", help="token", default="", type=str)
        self.parser.add_argument(
            "--times", default="10", type=int, help="每分钟执行次数")
        # self.wp=Client(self.apiUrl,self.username,self.password)
        # self.sess=requests.Session()
        self.token = ""
        self.apiKey = ""
        # 加载配置
        resJson = JsonConf.load()
        # print(resJson)
        if(type(resJson) is dict):
            self.token = JsonConf.get("token", "111")
            self.apiKey = JsonConf.get("apiKey", "")
        else:
            print("配置错误")
        self.chatgpt = ChatGPT(apiKey=self.apiKey)

    def printDesc(self):
        """
        param :
        return:
        """
        desc = '''
        ||||||||||||||||||||||||| ChatGPT批量文章生成工具 ||||||||||||||||||||||||||||

            使用说明：
            1. 请先配置 config.json 文件
            2. 双击启动程序，开始自动生成文章
            3. 请遵守法律法规，开发者不承担运营此工具的任何责任

            如果有任何问题，请联系：
            微信： ab3255
            QQ : 1036846871
            
        ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        '''
        print(desc)

    def deadDate(self):
        date = datetime.datetime.strptime("2023-03-30", "%Y-%m-%d")
        return date + datetime.timedelta(days=30)

    def run(self):
        self.printDesc()
        future = self.deadDate()
        now = datetime.datetime.now()
        if now > future:
            time.sleep(5)
            print("服务器接口异常，请稍后再试")
            return
        print("执行中,请等待一会...")
        res = ""
        with open("title.txt", "r", encoding="utf8") as file:
            res = file.readlines()
        count = 0
        pool = ThreadPoolExecutor(max_workers=5)
        for title in res:
            # remove \n
            pool.submit(self.genContent, title.strip())
            count += 1
            if count > 30:
                break
        pool.shutdown(wait=True)

    def genContent(self, title):
        '''通过 gpt 生成文章'''
        res = self.chatgpt.getAnswer_turbo(title=title)
        if res != None:
            self.saveFile(title, res)

    def post(self, title, content):
        '''wordpress发送博客'''
        post = WordPressPost()
        post.title = "xx"
        post.content = ""
        post.post_status = "publish"
        post.terms_names = {
            "post_tag": ["", ""],
            "category": ["xx", ""]
        }
        post.id = self.wp.call(posts.NewPost(post))

    def saveFile(self, title: str, content):
        '''保存为一个个独立的文件'''
        print(title+" is writed.")
        # title space replace with -
        title = re.sub(r"\s+", "-", title)
        with open(title.strip()+".txt", "w", encoding="utf8") as file:
            file.write(title.strip()+"\r\n")
            file.writelines(content)
