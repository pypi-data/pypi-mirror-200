# -*- coding: utf-8 -*-
# @Time    : 2023/1/31 16:42:40
# @Author  : Pane Li
# @File    : tools.py
"""
tools

"""
import logging
import os.path
import re
import subprocess
import time
import datetime
import pytz
import requests
from inhandtest.file import file_hash


def loop_inspector(flag='status', timeout=90, interval=5, assertion=True):
    """装饰器，期望接收函数返回的值为True，如果为False时进行轮询，直至超时失败，如果正确就退出

    :param flag:  功能名称，用以输出日志，如果不填  默认为’状态’二字
    :param timeout:  循环检测超时时间
    :param interval:  循环检测时间间隔
    :param assertion: 默认期望断言，如果为False时 返回值
    :return:  assertion为False时，返回函数的值
    """

    def timeout_(func):
        def inspector(*args, **kwargs):
            for i in range(0, timeout + 1, interval):
                result = func(*args, **kwargs)
                if not result:
                    logging.info(f'{flag} assert failure, wait for {interval}s inspection')
                    time.sleep(interval)
                    continue
                else:
                    logging.info(f'{flag} assert normal')
                    return result
            else:
                if assertion:
                    raise AssertionError(f'{flag} assert timeout failure')

        return inspector

    return timeout_


def dict_merge(*dicts):
    """合并多个字典

    :param dicts:
    :return:
    """
    result = {}
    for dict_ in dicts:
        if dict_ is not None:
            result.update(dict_)
    return result


def dict_flatten(in_dict, separator=":", dict_out=None, parent_key=None):
    """ 平铺字典

    :param in_dict: 输入的字典
    :param separator: 连接符号
    :param dict_out:
    :param parent_key:
    :return: dict
    """
    if dict_out is None:
        dict_out = {}

    for k, v in in_dict.items():
        k = f"{parent_key}{separator}{k}" if parent_key else k
        if isinstance(v, dict):
            dict_flatten(in_dict=v, dict_out=dict_out, parent_key=k)
            continue

        dict_out[k] = v

    return dict_out


def timezone_change(time_str, src_timezone, dst_timezone=None, time_format=None):
    """
    将任一时区的时间转换成指定时区的时间
    如果没有指定目的时区，则默认转换成当地时区  时区参考https://www.beijing-time.org/shiqu/

    :param time_str:
    :param src_timezone: 要转换的源时区，如"Asia/Shanghai" 即东八区， 'Europe/London' 零时区  'Canada/Eastern' 西五区 UTC-5
    :param dst_timezone: 要转换的目的时区，如"Asia/Shanghai", 如果没有指定目的时区，则默认转换成当地时区
    :param time_format: 默认格式"%Y-%m-%d %H:%M:%S"
    :return: str, 字符串时间格式
    """
    if not time_format:
        time_format = "%Y-%m-%d %H:%M:%S"

    # 将字符串时间格式转换成datetime形式
    old_dt = datetime.datetime.strptime(time_str, time_format)

    # 将源时区的datetime形式转换成GMT时区(UTC+0)的datetime形式
    dt = pytz.timezone(src_timezone).localize(old_dt)
    utc_dt = pytz.utc.normalize(dt.astimezone(pytz.utc))

    # 将GMT时区的datetime形式转换成指定的目的时区的datetime形式
    if dst_timezone:
        _timezone = pytz.timezone(dst_timezone)
        new_dt = _timezone.normalize(utc_dt.astimezone(_timezone))
    else:
        # 未指定目的时间，默认转换成当地时区
        new_dt = utc_dt.astimezone()
    # 转换成字符串时间格式
    return new_dt.strftime(time_format)


def check_windows_process(process: str or int or list, kill=False) -> bool or list:
    """ 检测进程是否运行
    :param process: str|int|list, 进程名称或进程pid(不一定是应用程序名称！), eg:'3CDaemon'|'mosquitto'|49040 如果有多个时使用list传入
    :param kill: True|False 当为True时，将检测到的进程杀死
    :return: boolean
    """

    def _search(process_):
        if process_:
            if isinstance(process_, str) or isinstance(process_, int):
                command = f'tasklist |findstr {process_}'
            else:
                raise Exception("not support process type")
            logging.info(command)
            p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='gbk')
            task_result = p.communicate()[0].strip()
            logging.info(f'find {process_} process is: {task_result}')
            try:
                task_result = re.sub('\s+', ' ', task_result).split(' ')
                if len(task_result) == 6:
                    server_name = task_result[0]
                else:
                    server_name = False
            except Exception:
                server_name = False
            return server_name
        else:
            return False

    if not kill:
        if isinstance(process, list):
            return [_search(name_) for name_ in process]
        else:
            return _search(process)
    else:
        process = process if isinstance(process, list) else [process]
        for name_ in process:
            if isinstance(name_, str):
                pid = _search(name_)
                if pid:
                    logging.info(f'taskkill /F /IM {pid}')
                    p = subprocess.Popen(f'taskkill /F /IM {pid}', shell=True, stdout=subprocess.PIPE,
                                         stderr=subprocess.STDOUT, encoding='gbk')
                    logging.info(p.communicate()[0])
                    time.sleep(3)  # 删除服务应等待几秒，服务完全退出
                else:
                    logging.info(f'not found task {name_}')
            elif isinstance(name_, int):
                logging.info(f'taskkill /pid {name_} /F')
                p = subprocess.Popen(f'taskkill /pid {name_} /F', shell=True, stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT, encoding='gbk')
                logging.info(p.communicate()[0])
                time.sleep(3)  # 删除服务应等待几秒，服务完全退出
            else:
                raise Exception("not support process type")


def download_svn_package(svn: dict, file_path, check_package=True):
    """

    :param svn: dict {'url': $url, 'username': $username, 'password': $password} 固件全路径
    :param file_path: 本地存放固件文件夹路径
    :param check_package: True|False 支持下载完文件后校验文件正确性
    :return:
    """
    from requests.auth import HTTPBasicAuth
    from requests.adapters import HTTPAdapter

    if svn.get("url") and svn.get('username') and svn.get('password') and file_path:
        url_path = svn.get("url")
        firmware_name = url_path.split('/')[-1]
        local_firmware_path = os.path.join(file_path, firmware_name)
        svn_hash_file_path = url_path.replace(firmware_name, 'sha256.txt')
        auth = HTTPBasicAuth(svn.get('username'), svn.get('password'))
        if not os.path.isfile(local_firmware_path):
            logging.info(f"download {local_firmware_path} from svn and wait for a moment!")
            s = requests.Session()
            s.mount('http://', HTTPAdapter(max_retries=3))  # 本身请求失败会重试3次
            for i in range(3):  # 文件下载错误再继续下载
                r = s.get(url_path, auth=auth)
                if r.status_code == 401:
                    raise Exception("svn username or password error")
                elif r.status_code == 200:
                    with open(local_firmware_path, 'wb') as fi_:  # 覆盖写入
                        fi_.write(r.content)
                    r_hash_file = s.get(svn_hash_file_path, auth=auth)
                    if check_package:
                        for co_ in r_hash_file.content.split(b'\n'):
                            if co_.decode('utf-8').endswith(firmware_name):
                                hash_sha256_value = co_.decode('utf-8').split(' ')[0].upper()
                                break
                        else:
                            raise Exception(f'{svn_hash_file_path} not contain {firmware_name} hash_sha256 value')
                        if file_hash(local_firmware_path, 'sha256') == hash_sha256_value:
                            logging.info(f'{local_firmware_path} download success')
                            break
                        else:
                            logging.warning(f'download package failed, try {i + 1} time')
                    else:
                        break
                else:
                    raise Exception("svn server down error")
            else:
                raise Exception('download package failed')


def get_time_stamp(time_='', delta=0, delta_type='h', time_format='%Y-%m-%dT%H:%M:%SZ') -> str:
    """获取时间戳

    :param time_: 默认获取当前时间
    :param delta: 要增加或者减少的时间
    :param delta_type: 单位 d:天 h:小时 m:分钟 s:秒
    :param time_format: 显示格式 ,为空时返回对应时间的时间戳
    :return:
    """
    delta_type = delta_type.lower()
    if delta_type == 'h':
        delta_time = datetime.timedelta(hours=delta)
    elif delta_type == 'm':
        delta_time = datetime.timedelta(minutes=delta)
    elif delta_type == 's':
        delta_time = datetime.timedelta(seconds=delta)
    elif delta_type == 'd':
        delta_time = datetime.timedelta(days=delta)
    else:
        delta_time = 0
    if not time_:
        time_stamp = datetime.datetime.utcnow() + delta_time
    else:
        time_stamp = datetime.datetime.strptime(time_, time_format) + delta_time
    res = time_stamp.strftime(time_format) if time_format else time_stamp.timestamp()
    return res


def dict_in(expect_dict: dict, contain: dict):
    """验证字典包含关系

    :param expect_dict: dict {key: value}
    :param contain: dict,  支持${value} 表达式判断
    :return: True or False
    """
    if expect_dict and contain:
        contain_flatten = dict_flatten(contain)  # 平铺字典
        expect_dict_flatten = dict_flatten(expect_dict)  # 平铺字典
        for contain_item, contain_value in contain_flatten.items():
            value = expect_dict_flatten.get(contain_item)
            if isinstance(contain_value, str) and '${value}' in contain_value:
                expect_value = contain_value.replace('${value}', str(value))
                if not eval(expect_value):
                    raise AssertionError(f'expect_item {contain_item} value is {expect_value} is False')
            else:
                assert value == contain_value, f'expect_item {contain_item} value is {contain_value} is False'

        else:
            logging.info(f'{contain} in {expect_dict} assert ok')


def replace_str(old: str or list or dict, replace_value: dict):
    """深度替换字符串，避免替换重复出问题

    :param old:
    :param replace_value:
    :return:
    """
    new_old = old

    def replace_(replace_str_: str):
        for k_, i_ in zip(replace_value.keys(), range(0, len(replace_value.keys()))):
            replace_str_ = replace_str_.replace(k_, '${' + str(i_) + '}')
        for v_, i_ in zip(replace_value.values(), range(0, len(replace_value.keys()))):
            replace_str_ = replace_str_.replace('${' + str(i_) + '}', v_)
        return replace_str_

    if old and replace_value:
        if isinstance(old, str):
            new_old = replace_(old)
        elif isinstance(old, list):
            new_old = [replace_(str(old_)) for old_ in old]
        elif isinstance(old, dict):
            new_old = {}
            for k, v in old.items():
                new_old.update({replace_(str(k)): v})
        else:
            raise Exception('Not support this type')
    return new_old


if __name__ == '__main__':
    import sys

    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO,
                        stream=sys.stdout)
    # print(timezone_change('2022-02-18 13:39:32', 'Canada/Eastern', 'Asia/Shanghai'))
    print(check_windows_process('mosquitto.exe', kill=True))
    # print(get_time_stamp('2022-02-18T13:39:32Z', -2))
