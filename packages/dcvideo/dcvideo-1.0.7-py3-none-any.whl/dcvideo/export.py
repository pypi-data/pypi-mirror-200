import argparse
import asyncio
import datetime
import json
import logging
import os
import signal
import sys

import requests

from .config import read, read_workdir, save_config
from .message import ExportMessage
from .result import Result
from .utils import download, md5_value, sign_dict, ymd

log = logging.getLogger(__name__)

class Export:
    def __init__(self, version: str, host: str, workdir: str, appid: str, appsecret: str) -> None:
        self.do_action = ''
        self.version = version
        self.host = host
        self.workdir = workdir
        self.appid = appid
        self.appsecret = appsecret

    async def run(self) -> Result:
        res = await self.query('/publish/export?action=get')
        
        if(not res.success or not res.data):
            return res

        for data in res.data:
            try:
                await self.download(ExportMessage(**data))
            except Exception as e:
                print(str(e))

        return Result(True, wait=5)
        
    async def download(self, message: ExportMessage):
        message.console_title()

        savepath = os.path.join(self.workdir, ymd(), message.category)
        os.makedirs(savepath, exist_ok=True)

        def remove_file(path):
            if os.path.exists(path):
                os.remove(path)

        error = ''
        for file in message.files:
            filepath = os.path.join(savepath, file.name)
            if os.path.exists(filepath) and md5_value(filepath) != file.md5:
                file.local_path = filepath
                message.setFileDown(file, 100)
            else:
                success = await download(filepath, file.src, lambda p, s, t: message.setFileDown(file, p))
                if success:
                    if md5_value(filepath) != file.md5:
                        error = file.label + ' 文件尺寸不一致'
                        remove_file(filepath)
                        break
                    else:
                        file.local_path = filepath
                else:
                    error = file.label+' 下载失败'
                    remove_file(filepath)
                    break

        if error:
            if(message.retried < message.download_retry):
                message.retried += 1
                print(f'\n\t{error}，5秒后尝试第{message.retried+1}次重试')
                await asyncio.sleep(5)
                return await self.download(message)
            print(f'\n\t{error}')
            await self.query('/publish/export?action=update',_id=message._id, status='error', error=error)
            return False
        else:
            print(f'\n\t\033[32m导出完成\033[0m')
            await self.query('/publish/export?action=update',_id=message._id, status='success')
            return True

    async def query(self, url: str, **kwargs):
        sign, nonce = sign_dict(kwargs, self.appsecret)

        url = f'{self.host}{url}&appid={self.appid}&nonce={nonce}&sign={sign}&version={self.version}'

        headers = {'Content-Type': 'application/json'}

        response = requests.post(url, data=json.dumps(
            kwargs), headers=headers) if kwargs else requests.get(url, headers=headers)

        if(response.status_code == 200):
            value = response.json()

            res = Result(
                success=value.get('success'),
                msg=value.get('msg'),
                data=value.get('data'),
                wait=value.get('wait')
            )
            return res
        else:
            return Result(True, msg=f'{response.text},{response.status_code}', wait=5)
        

# 定义标志位
exit_flag1 = False

# 信号处理函数
def signal_handler(signum, frame):
    global exit_flag1
    exit_flag1 = True
    print("\nExiting...")


# 注册信号处理函数
signal.signal(signal.SIGINT, signal_handler)

async def run(version, host, appid, appsecret,workdir):

    print(f'\n\n《八戒来了之导出程序 - {version}》\n服务器：{host}\nAppId：{appid}\n工作目录：{workdir}\n')
    
    client = Export(version, host, workdir, appid, appsecret)
    
    while not exit_flag1:
        try:
            res = await client.run()
        except Exception as e:
            log.error(e,exc_info=True)
            print(f'\n\t{e}')
            await asyncio.sleep(5)
        else:
            if res.msg:
                print(f'\n{res.msg}')
            if not res.success:
                break
            if res.wait>0:
                next = datetime.datetime.now()+datetime.timedelta(seconds=res.wait)
                print(f'\r暂无任务，{res.wait}秒后({next.strftime("%H:%M:%S")})将再次读取...',end=" ")
                await asyncio.sleep(res.wait)
                
        if exit_flag1:
            break

    print('已退出程序')
    

def main():
    version, host, appid, appsecret = read()
    if not appid or not appsecret:
        return
    workdir = read_workdir('export')
    if not workdir:
        return
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-dir', type=str, default='')
    parser.add_argument('-appid', type=str, default='')
    parser.add_argument('-appsecret', type=str, default='')
    parser.add_argument('-host', type=str, default='')
    args = parser.parse_args()

    if args.host and args.host!=host:
        host = args.host
        save_config('server','host',host)

    if args.appid and args.appid!=appid:
        appid = args.appid
        save_config('server','appid',appid)

    if args.appsecret and args.appsecret!=appsecret:
        appsecret = args.appsecret
        save_config('server','appsecret',appsecret)
    
    if args.dir and args.dir!=workdir:
        if not os.path.exists(args.dir):
            print(f'{args.dir}目录不存在')
            return
        workdir = args.dir
        save_config('export','workdir',workdir)

    if sys.version_info.minor >= 10:
        asyncio.run(run(version, host, appid, appsecret,workdir))
    else:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run(version, host, appid, appsecret,workdir))
        loop.close()