#!/usr/bin/python
# encoding: utf-8
__authors__	= ['left']
__version__	= 1.0
__date__	= '2013-11-29 09:29:36'
__licence__	= 'GPL licence'

#import models
from django.core.paginator import Paginator

def pagination(page_list,page_num):
    #分页页码展示
    page_len = len(page_list)
    last_page_value = page_len
    if page_num == "all":
        if page_len <= 10:
            page_start_end = page_list
        else:
            page_start_end = page_list[:10]
    else:
        if page_len <= 10:
            page_start_end = page_list
        else:
            if page_num <= 5:
                page_start_end = page_list[:10]
            elif page_len - page_num <= 5:
                start_page = page_len - 10
                end_page = page_len
                page_start_end = page_list[start_page:end_page]
            else:
                start_page = page_num - 5
                end_page = page_num + 5
                page_start_end = page_list[start_page:end_page]
    
    # 1表示True,0表示False
    if page_len:
        if page_len == 1:
            page_next = 0
            page_up = 0
            first_page = 0
            last_page = 0
        else:
            if page_num == 1:
                page_up = 0
                page_next = 1
                first_page = 1
                last_page = 1
            elif page_num == "all":
                page_up = 0
                page_next = 0
                first_page = 1
                last_page = 1
            elif page_num == page_len:
                page_up = 1
                page_next = 0
                first_page = 1
                last_page = 1
            else:
                page_up = 1
                page_next = 1
                first_page = 1
                last_page = 1
    else:
        page_next = 0
        page_up = 0
        first_page = 0
        last_page = 0
    return page_start_end,page_up,page_next,first_page,last_page,last_page_value

def pagination_django(page_data,page_value,page_num):
    #分页器
    p = Paginator(page_data,page_value)
    last_page_value = p.num_pages
    page_list = [x+1 for x in range(p.num_pages)]
    page_len = len(page_list)
    if page_num == "all":
        if page_len <= 10:
            page_start_end = page_list
        else:
            page_start_end = page_list[:10]
        page_all_data = page_data
    else:
        if page_len <= 10:
            page_start_end = page_list
        else:
            if page_num <= 5:
                page_start_end = page_list[:10]
            elif page_len - page_num <= 5:
                start_page = page_len - 10
                end_page = page_len
                page_start_end = page_list[start_page:end_page]
            else:
                start_page = page_num - 5
                end_page = page_num + 5
                page_start_end = page_list[start_page:end_page]
        page = p.page(page_num)
        page_all_data = page.object_list
    if page_len:
        if page_len == 1:
            page_next = 0
            page_up = 0
            first_page = 0
            last_page = 0
        else:
            if page_num == 1:
                page_up = 0
                page_next = 1
                first_page = 1
                last_page = 1
            elif page_num == "all":
                page_up = 0
                page_next = 0
                first_page = 1
                last_page = 1
            elif page_num == page_len:
                page_up = 1
                page_next = 0
                first_page = 1
                last_page = 1
            else:
                page_up = 1
                page_next = 1
                first_page = 1
                last_page = 1
    else:
        page_next = 0
        page_up = 0
        first_page = 0
        last_page = 0
    return page_start_end,page_up,page_next,first_page,last_page,page_all_data,last_page_value
