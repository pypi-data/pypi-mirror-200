#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Contact :   liuyuqi.gov@msn.cn
@Time    :   2022/12/17 00:24:54
@License :   Copyright © 2017-2022 liuyuqi. All Rights Reserved.
@Desc    :   
'''
from gpt_muti_gen.cgpt_wp import CgptWp
import os
def main():
    if os.path.exists('title.txt') and os.path.exists('conf/config.json'):
        cgptWp = CgptWp()
        cgptWp.run()
    else:
        print("template file is created, please edit it and run again")
        if not os.path.exists('title.txt'):
            with open('title.txt', 'w', encoding='utf-8') as f:
                f.write('婴儿吐奶怎么回事\n十一个月宝宝奶量多大')
        if not os.path.exists('conf'):
            os.mkdir('conf')
        if not os.path.exists('conf/config.json'):
            with open('conf/config.json', 'w', encoding='utf-8') as f:
                f.write('''{
    "token": "A4V71G4q5JHL",
    "apiKey": "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"
}''')
