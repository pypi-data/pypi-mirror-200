#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Contact :   liuyuqi.gov@msn.cn
@Time    :   2022/05/24 15:07:14
@License :   Copyright © 2017-2022 liuyuqi. All Rights Reserved.
@Desc    :   yaml util
'''
import os
import json

config_path = "conf/config.json"


class JsonConf:
    '''json配置文件类'''
    @staticmethod
    def save(data):
        global config_path
        with open(config_path, 'w') as json_file:
            json_file.write(json.dumps(data, indent=4))

    @staticmethod
    def load():
        global config_path
        if not os.path.exists(config_path):
            with open(config_path, 'w') as json_file:
                pass
        with open(config_path, encoding="utf-8") as json_file:
            try:
                data = json.load(json_file)
            except Exception as e:
                if(str(e).index("utf-8-sig") > 0):
                    with open(config_path, encoding="utf-8-sig") as json_file:
                        data = json.load(json_file)
                        return data
                else:
                    print(e)
            return data

    @staticmethod
    def set(data_dict):
        json_obj = JsonConf.load()
        for key in data_dict:
            json_obj[key] = data_dict[key]
        JsonConf.save(json_obj)
        print(json.dumps(json_obj, indent=4))

    @staticmethod
    def get(key, default_val=""):
        '''
        配置文件获取key对象的值，如果没有设置就返回默认值
        '''
        try:
            result = JsonConf.load()[key]
            return result
        except Exception as e:
            print(e)
            return default_val

    @staticmethod
    def getFrom(jsonData, key, default_val=""):
        try:
            return jsonData[key]
        except Exception as e:
            return default_val
