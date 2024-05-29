from datetime import datetime, timedelta
import os

from django.conf import settings

filter_map = {
    "today": lambda time_list: is_today(time_list),
    "week": lambda time_list: is_in_week(time_list),
    "month": lambda time_list: is_in_month(time_list),
    "year": lambda time_list: is_in_year(time_list)
}


def is_today(time_list):
    if len(time_list) != 3:
        return True
    now = datetime.now().date()
    date = datetime(*[int(time) for time in time_list]).date()
    return date == now


def is_in_month(time_list):
    if len(time_list) != 2:
        return True
    now = datetime.now()
    # 判断年份和月份是否相同
    return int(time_list[0]) == now.year and int(time_list[1]) == now.month


def is_in_week(time_list):
    if len(time_list) != 3:
        return True
    now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    weekday = now.weekday()
    monday = now - timedelta(days=weekday)
    sunday = monday + timedelta(days=6)
    date = datetime(*[int(time) for time in time_list])
    return monday <= date <= sunday


def is_in_year(time_list):
    if len(time_list) != 1:
        return True
    now = datetime.now()
    return int(time_list[0]) in (now.year, now.year-1)


def generate_file_tree(path, tree):
    """生成目录树状结构的递归函数。
    :param path: 要遍历的目录路径。
    :param tree: 存放文件目录结构的字典。
    """
    # 获取目录下的所有文件和目录名
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        # 如果是目录，则递归调用此函数
        if os.path.isdir(item_path):
            tree[item] = {}
            generate_file_tree(item_path, tree[item])
        else:
            file_detail = os.stat(item_path)
            tree[item] = {
                "file_size": file_detail.st_size,
                "create_time": file_detail.st_ctime,
            }


def generate_file_list(path, file_list, time_list):
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        # 如果是目录，则递归调用此函数
        if os.path.isdir(item_path):
            _time_list = [*time_list, item]
            generate_file_list(item_path, file_list, _time_list)
        else:
            file_detail = os.stat(item_path)
            file_list.append({
                "file_name": item,
                "file_path": os.path.relpath(item_path, os.path.join(settings.MEDIA_ROOT)),
                "file_size": file_detail.st_size,
                "created_time": "-".join(time_list)
            })


def generate_filtered_file_list(path, file_list, time_list, _filter=None):
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        # 如果是目录，则递归调用此函数
        if os.path.isdir(item_path):
            _time_list = [*time_list, item]
            if _filter and not filter_map[_filter](_time_list):
                continue
            generate_filtered_file_list(item_path, file_list, _time_list, _filter)
        else:
            file_detail = os.stat(item_path)
            file_list.append({
                "file_name": item,
                "file_path": os.path.relpath(item_path, os.path.join(settings.MEDIA_ROOT)),
                "file_size": file_detail.st_size,
                "created_time": "-".join(time_list)
            })

# def get_week_range():
#     now = datetime.now()
#     weekday = now.weekday()
#     monday = now - timedelta(days=weekday)
#     sunday = monday + timedelta(days=6)
#     return monday, sunday
#
#
# def get_month_range():
#     now = datetime.now()
#     first_day = datetime(now.year, now.month, 1)
#     # 计算下个月的年份和月份，自动处理12月的情况
#     next_month_year = now.year + (now.month // 12)  # 如果是12月，年份加1
#     next_month = (now.month % 12) + 1  # 月份在1月到12月之间循环
#     last_day = datetime(next_month_year, next_month, 1) - timedelta(days=1)
#     return first_day, last_day
