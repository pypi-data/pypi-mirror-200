import configparser
import os
import re
from tkinter import filedialog
from .utils import port_is_used,get_host_ip

filepath = os.path.join(os.path.dirname(__file__), 'config.ini')
config = configparser.ConfigParser()
VERSION = '1.0.9'
HOST = 'https://www.shortvideo.work'

def save_config(section,key,value):
    config.read(filepath)
    if not config.has_section(section):
        config.add_section(section)
    config.set(section, key, value)
    config.write(open(filepath, "w"))

def read():
    if not os.path.exists(filepath):
        config.add_section("video")
        config.set("video", "version", VERSION)
        config.set("video", "desc", "请不在擅自修改配置文件，以免引发异常！")
        config.write(open(filepath, "w"))

    config.read(filepath)

    if not config.has_section('server'):
        config.add_section("server")
        config.set("server", "host", HOST)
        config.write(open(filepath, "w"))

    version = config.get('video', 'version', fallback=VERSION)
    host = config.get('server', 'host', fallback=HOST)
    appid = config.get('server', 'appid', fallback='')
    appsecret = config.get('server', 'appsecret', fallback='')

    while not appid:
        value = input('请输入appid：')
        if value:
            appid = value
            config.set('server', 'appid', value)
            config.write(open(filepath, "w"))
            break

    while not appsecret:
        value = input('请输入appsecret：')
        if value:
            appsecret = value
            config.set('server', 'appsecret', value)
            config.write(open(filepath, "w"))
            break


    return version, host, appid, appsecret

def read_workdir(key:str):
    if key not in ['publish','export','web']:
        print('无效的类型')
        return
    
    config.read(filepath)
    if not config.has_section(key):
        config.add_section(key)
    workdir = config.get(key, 'workdir', fallback='')
    text = {
        'publish':'请选择一个存放发布视频时的缓存目录（建议使用一个剩余空间较大的分区）',
        'export':'请选择一个存放导出视频和封面的目录（建议使用一个剩余空间较大的分区）',
        'web':'请选择一个存放上传视频和封面的目录（建议使用一个剩余空间较大的分区）'
    }
    while not workdir:
        if input(f'\n{text[key]}\n请按 y 键并回车继续：').lower() == 'y':
            value = filedialog.askdirectory()
            if value:
                workdir = value
                config.set(key, 'workdir', value)
                config.write(open(filepath, "w"))
                break
        else:
            break
    return workdir

def read_web():
    if not os.path.exists(filepath):
        config.add_section("video")
        config.set("video", "version", VERSION)
        config.set("video", "desc", "请不在擅自修改配置文件，以免引发异常！")
        config.write(open(filepath, "w"))

    config.read(filepath)
    if not config.has_section('web'):
        config.add_section("web")
        config.write(open(filepath, "w"))

    version = config.get('video', 'version', fallback=VERSION)
    port = config.getint('web', 'port', fallback=None)
    host = get_host_ip()
    while not port:
        value = input('请输入端口号：')
        if value and re.fullmatch('\d+',value):
            if port_is_used(host,int(value)):
                print(f'{value}端口已被占用')
                continue

            port = int(value)
            config.set('web', 'port', value)
            config.write(open(filepath, "w"))
            break

    workdir = read_workdir('web')
    return version,host, port, workdir