'''
Created on 2019年4月30日

yaml一般用来写配置文件。
@author: liuyuqi
'''

import yaml
import os

config_path ="conf/config.yml"

class YamlConf:
    '''
    yaml配置
    '''
    @staticmethod
    def save(data):
        global config_path
        try:
            yaml.dump(data, open(config_path, "w"))
        except Exception as e:
            print(e)

    @staticmethod
    def load():
        global config_path
        config = {}
        try:
            config = yaml.load(open(config_path, "r", encoding="utf-8"), Loader=yaml.SafeLoader)
            if config is None:
                config = {}
        except Exception as e:
            print(e)
        return config

    @staticmethod
    def set(data_dict):
        json_obj = YamlConf.load()
        for key in data_dict:
            json_obj[key] = data_dict[key]
        YamlConf.save(json_obj)
    
    @staticmethod
    def get(key, default_val=""):
        try:
            result = YamlConf.load()[key]
            return result
        except Exception as e:
            return default_val