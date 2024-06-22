# -*- coding : utf-8 -*-
# @Time      : 2023/4/11 20:12
# @Author    : 木木
# @FileName  : config.py
# description:全局从这里获取配置文件信息
import yaml
yamlPath = 'config.yaml'
config=yaml.load(open(yamlPath,'r',encoding='utf-8'), Loader=yaml.FullLoader,)
