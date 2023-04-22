import sys
from text.disclaimers import disc
from termcolor import colored
import json
import glob
import os.path

def getModel(model_type: int, module_id: int):
    # print('=========================')
    # print(colored('注意：黄色声线需要配置 Azure API', 'yellow'))
    # print('ID\t声线')
    model_info = None
    with open("model/config.json", "r", encoding="utf-8") as f:
        model_info = json.load(f)

    i = 0
    key_list = []
    for key, info in model_info.items():
        if model_type == 0 and info['language'] == 'Chinese':
            key_list.append(key)
            # if 'zh-CN' in key:
            #     print(colored(str(i) + '\t' + info['name_zh'] + '(' + info['describe'] + ')', 'yellow'))
            # else:
            #     print(str(i) + '\t' + info['name_zh'] + '(' + info['describe'] + ')')
            # i = i + 1
        elif model_type == 1 and info['language'] == 'Japanese':
            key_list.append(key)
            # if 'zh-CN' in key:
            #     print(colored(str(i) + '\t' + info['name_zh'] + '(' + info['describe'] + ')', 'yellow'))
            # else:
            #     print(str(i) + '\t' + info['name_zh'] + '(' + info['describe'] + ')')
            # i = i + 1
    print('=========================')
    key = key_list[module_id]
    return model_info[key]['sid'], key