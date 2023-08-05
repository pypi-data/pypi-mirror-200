from datetime import datetime, timedelta

import tornado.options
from bson import ObjectId
from lesscode.utils.encryption_algorithm import AES


def condition_by_like(find_condition, column, value):
    if value:
        find_condition[column] = {"$regex": f".*{value}.*"}


def condition_by_in(find_condition, column, param_list, is_object=False, _include=True, is_need_decrypt_oralce=False):
    if param_list:
        param_list = [i for i in param_list if i not in [None, "", "all"]]
        if len(param_list) > 0:
            if is_object:
                param_list = [ObjectId(id) for id in param_list]
            if is_need_decrypt_oralce:
                try:
                    param_list = [int(AES.decrypt(tornado.options.options.aes_key, id)) for id in param_list]
                except:
                    pass
            if _include is True:
                find_condition[column] = {"$in": param_list}
            else:
                find_condition[column] = {"$ne": {"$in": param_list}}


def condition_by_between(column, data_list, and_condition_list, is_contain_end=True, is_contain_start=True):
    if data_list:
        if data_list[0]:
            if is_contain_start:
                and_condition_list.append({column: {"$gte": data_list[0]}})
            else:
                and_condition_list.append({column: {"$gt": data_list[0]}})
        if len(data_list) == 2 and data_list[1]:
            if is_contain_end:
                and_condition_list.append({column: {"$lte": data_list[1]}})
            else:
                and_condition_list.append({column: {"$lt": data_list[1]}})


def condition_by_eq(find_condition, column, param, _include=True):
    if param is not None and param != "":
        if _include is True:
            find_condition[column] = param
        else:
            find_condition[column] = {"$ne": param}


def mongodb_sql_paging(page_size, page_num):
    limit = int(page_size)
    skip = (int(page_num) - 1) * int(page_size)

    return limit, skip
