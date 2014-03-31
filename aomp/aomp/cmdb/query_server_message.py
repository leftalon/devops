#!/usr/bin/python
# encoding: utf-8
__authors__ = ['left']
__version__ = 1.0
__date__    = '2013-10-19 11:38:23'
__licence__ = 'GPL licence'

#import modules
from aomp.cmdb.server_search import server_search_dict
from math import ceil
from aomp.cmdb.models import Game_name_all
from django.db.models import Q

#define global valiable
def query_server_message(distinct_server,game_type):
    global all_server,ip_server_dict
    all_server = {}
    ip_server_dict = {}
    server_product = ''
    temp_game_all_name = []
    game_all_name = []
    if game_type != '' and game_type != 'none':
        temp_game_all_name = Game_name_all.objects.filter(game_type=game_type)
        for i in temp_game_all_name:
            game_all_name.append(i.game_name)
    for ip_message in distinct_server:
        server_message = server_search_dict(**ip_message)
        for ip_id in ip_message:
            if ip_id == "server_in_ip":
                if ip_message[ip_id] == '':
                    in_ip = '0.0.0.0'
                else:
                    in_ip = ip_message[ip_id]
            elif ip_id == "server_out_ip":
                if ip_message[ip_id] == '':
                    out_ip = '0.0.0.0'
                else:
                    out_ip = ip_message[ip_id]
            else:
                server_product = ip_message[ip_id]
        #把内外网组成一个元组作为一个key,内外网相同的所有信息作为value,得到合服的情况
        ip_key = (in_ip,out_ip)
        if game_type == '' or game_type == 'none' or server_product in game_all_name:
            if ip_key in all_server:
                all_server[ip_key] += [server_message]
            else:
                all_server[ip_key] = [server_message]
            
        #得到ip字符串和合服的游戏服唯一标示字典
   # for k,v in all_server.items():
   #     server_list = []
   #     for s in v:
   #         for i in range(len(s)):
   #             server_list.append(s[i].server_id)
   #         ip_server_dict[k] = server_list
    return all_server#,ip_server_dict
