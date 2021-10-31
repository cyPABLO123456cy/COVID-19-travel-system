# coding:utf-8
import csv
from bs4 import BeautifulSoup
import urllib.parse
import requests
from lxml import etree
import re
import pandas as pd
import dataframe
import numpy
import execjs

if __name__ == "__main__":
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'
    }
    url = 'https://c.m.163.com/ug/api/wuhan/app/data/list-total?'
    res = requests.get(url=url, headers=headers)
    import json

    data_json = json.loads(res.text)
    data = data_json['data']
    data_china_today_confirm = data['chinaTotal']['today']['confirm']
    if not (data_china_today_confirm is None):
        if data_china_today_confirm > 0:
            data_china_today_confirm = '+' + str(data_china_today_confirm)
    if data_china_today_confirm is None:
        data_china_today_confirm = '较昨日待公布'
    data_china_total_confirm = data['chinaTotal']['total']['confirm']
    data_china_today_heal = data['chinaTotal']['today']['heal']
    data_china_total_heal = data['chinaTotal']['total']['heal']
    if not (data_china_today_heal is None):
        if data_china_today_heal > 0:
            data_china_today_heal = '+' + str(data_china_today_heal)
    if data_china_today_heal is None:
        data_china_today_confirm = '较昨日待公布'
    data_china_today_dead = data['chinaTotal']['today']['dead']
    data_china_total_dead = data['chinaTotal']['total']['dead']
    if data_china_total_dead > 0:
        data_china_today_dead = '+' + str(data_china_today_dead)
    data_china_today_storeconfirm = data['chinaTotal']['today']['storeConfirm']
    data_china_total_storeconfirm = data_china_total_confirm - data_china_total_dead - data_china_total_heal
    if not (data_china_today_storeconfirm is None):
        if data_china_today_storeconfirm > 0:
            data_china_today_storeconfirm = '+' + str(data_china_today_storeconfirm)
    data_china_today_incrNoSymptom = data['chinaTotal']['extData']['incrNoSymptom']
    data_china_total_noSymptom = data['chinaTotal']['extData']['noSymptom']
    if data_china_today_incrNoSymptom > 0:
        data_china_today_incrNoSymptom = '+' + str(data_china_today_incrNoSymptom)
    data_china_today_input = data['chinaTotal']['today']['input']
    data_china_total_input = data['chinaTotal']['total']['input']
    if data_china_today_input > 0:
        data_china_today_input = '+' + str(data_china_today_input)
    data_province = data['areaTree'][2]['children']
    free_data = pd.DataFrame(data_province)[['id', 'lastUpdateTime', 'name']]
    today_data = pd.DataFrame([province['today'] for province in data_province])
    total_data = pd.DataFrame([province['total'] for province in data_province])
    today_data.columns = ("today_" + i for i in today_data.columns)
    total_data.columns = ("total_" + i for i in total_data.columns)
    China_data = pd.concat([free_data, today_data, total_data], axis=1)
    file_name = '今天中国各省.csv'
    China_data.to_csv(file_name, index=None, encoding='utf_8_sig')
    print("中国各省疫情数据保存成功！！！")
    china_data = pd.read_csv('今天中国各省.csv')
    name_dic = {
        'date': '日期',
        'name': '名称',
        'id': '编号',
        'lastUpdateTime': '更新时间',
        'today_confirm': '当日新增确诊',
        'today_suspect': '当日新增疑似',
        'today_heal': '当日新增治愈',
        'today_dead': '当日新增死亡',
        'today_severe': '当日新增重症',
        'today_storeConfirm': '当日现存确诊',
        'total_confirm': '累计确诊',
        'total_suspect': '累计疑似',
        'total_heal': '累计治愈',
        'total_dead': '累计死亡',
        'total_severe': '累计重症',
        'total_input': '累计输入',
        'today_input': '当日新增输入',
    }
    china_data.rename(columns=name_dic, inplace=True)
    array = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
             29, 30, 31, 32, 33]
    china_data.to_csv('今天中国各省中文版.csv', index=None, encoding='utf_8_sig')
    print("地图加载完成！！！")
    print("柱状图加载完成！！！")
    zhexian_url = 'https://c.m.163.com/ug/api/wuhan/app/data/list-by-area-code?areaCode=66&t=1611976818326'
    zhexian_res = requests.get(url=zhexian_url, headers=headers)
    zhexian_data_json = json.loads(zhexian_res.text)
    zhexian_data = zhexian_data_json['data']
    zhexian_data_list = zhexian_data['list']
    zhexian_free_data = pd.DataFrame(zhexian_data_list)[['date']]
    zhexian_total_data = pd.DataFrame([list['total'] for list in zhexian_data_list])
    zhexian_total_data.columns = ("total_" + i for i in zhexian_total_data.columns)
    zhexian_today_data = pd.DataFrame([list['today'] for list in zhexian_data_list])
    zhexian_today_data.columns = ("today_" + i for i in zhexian_today_data.columns)
    zhexian_data = pd.concat([zhexian_free_data, zhexian_total_data, zhexian_today_data], axis=1)
    for i in range(0,34):
        province_nowconfirm = data_province[i]['total']['confirm'] - data_province[i]['total']['dead'] - data_province[i]['total']['heal']
        data_city_name = data_province[i]['name']
        data_city = data_province[i]['children']
        free_data_city = pd.DataFrame(data_city)[['id', 'lastUpdateTime', 'name']]
        today_data = pd.DataFrame([city['today'] for city in data_city])
        total_data = pd.DataFrame([city['total'] for city in data_city])
        today_data.columns = ("today_" + i for i in today_data.columns)
        total_data.columns = ("total_" + i for i in total_data.columns)
        liaoning_data = pd.concat([free_data_city, today_data, total_data], axis=1)
        file_name = data_city_name + '.csv'
        liaoning_data.to_csv(file_name, index=None, encoding='utf_8_sig')
        print(data_city_name + "疫情数据保存成功！！！")
        liaoning_data = pd.read_csv(file_name)
        total = 0
        liaoning_data.rename(columns=name_dic, inplace=True)
        with open(file_name, 'r', encoding='UTF-8') as f:
            csv_reader = csv.reader(f)
    world_url = 'https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=FAutoGlobalStatis,FAutoGlobalDailyList,FAutoCountryConfirmAdd'
    world_res = requests.get(url=world_url, headers=headers)
    world_res.text  # 提取内容和文字
    world_data_json = json.loads(world_res.text)
    world_data = world_data_json['data']
    world_confirm = world_data['FAutoGlobalStatis']['confirm']
    world_confirmAdd = world_data['FAutoGlobalStatis']['confirmAdd']
    world_dead = world_data['FAutoGlobalStatis']['dead']
    world_deadAdd = world_data['FAutoGlobalStatis']['deadAdd']
    world_heal = world_data['FAutoGlobalStatis']['heal']
    world_healAdd = world_data['FAutoGlobalStatis']['healAdd']
    world_nowConfirm = world_data['FAutoGlobalStatis']['nowConfirm']
    world_nowConfirmAdd = world_data['FAutoGlobalStatis']['nowConfirmAdd']
    if world_nowConfirmAdd > 0 or world_nowConfirmAdd == 0:
        x = '+' + str(world_nowConfirmAdd)
    else:
        x = world_nowConfirmAdd
    if world_confirmAdd > 0 or world_confirmAdd == 0:
        x = '+' + str(world_confirmAdd)
    else:
        x = world_confirmAdd
    if world_healAdd > 0 or world_healAdd == 0:
        x = '+' + str(world_healAdd)
    else:
        x = world_healAdd
    if world_deadAdd > 0 or world_deadAdd == 0:
        x = '+' + str(world_deadAdd)
    else:
        x = world_deadAdd
    foreign_url = 'https://c.m.163.com/ug/api/wuhan/app/data/list-total?t=324433143493'
    foreign_res = requests.get(url=foreign_url, headers=headers)
    foreign_data_json = json.loads(foreign_res.text)
    foreign_data = foreign_data_json['data']['areaTree']
    print("各国疫情数据保存成功！！！")
    page_three_url = 'http://so.news.cn/getNews?keyword=%E7%96%AB%E6%83%85&curPage=1&sortField=0&searchFields=1&lang=cn'
    dynamic_res = requests.get(url=page_three_url, headers=headers)
    dynamic_data_json = json.loads(dynamic_res.text)
    dynamic_data = dynamic_data_json['content']['results']
    for i in range(10):
        dynamic_time = dynamic_data[i]['pubtime']
        dynamic_source = dynamic_data[i]['sitename']
        dynamic_content = dynamic_data[i]['des']
        if str(dynamic_content) == 'None':
            dynamic_content = str(' ')
        dynamic_title = dynamic_data[i]['title']
        dynamic_url = dynamic_data[i]['url']
    print("新闻加载完成！！！")
    page_three_url = 'https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list?sub_srv_id=antip&srv_id=pc&offset=0&limit=20&strategy=1&ext={%22pool%22:[%22high%22,%22top%22],%22is_filter%22:10,%22check_type%22:true}'
    guanfang_res = requests.get(url=page_three_url, headers=headers)
    guanfang_data_json = json.loads(guanfang_res.text)
    guanfang_data = guanfang_data_json['data']['list']
    guanfang_len = len(guanfang_data)
    for i in range(guanfang_len):
        guanfang_time = guanfang_data[i]['publish_time']
        guanfang_source = guanfang_data[i]['media_name']
        guanfang_img = guanfang_data[i]['img']
        guanfang_title = guanfang_data[i]['title']
        guanfang_url = guanfang_data[i]['url']
    print("新闻加载完成！！！")
    print("write_finished!")
