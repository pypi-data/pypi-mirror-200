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
from .message import Message
from .result import Result
from .youban import Youban
from .utils import download, md5_value, sign_dict, to_cos

log = logging.getLogger(__name__)


class Publish:
    do_action: str

    def __init__(self, version: str, host: str, workdir: str, appid: str, appsecret: str) -> None:
        self.do_action = ''
        self.version = version
        self.host = host
        self.workdir = workdir
        self.appid = appid
        self.appsecret = appsecret

    async def run(self) -> Result:
        res = await self.query('/publish/read')
        if(not res.success or not res.data):
            return res

        await self.start(res.data)
        return Result(True, wait=0)

    async def start(self, data: dict):
        message = Message(**data)

        message.console_title()

        if message.category.mode not in ['web', 'api']:
            error = f'{message.category.mode}无效的发布类型'
            print(f'\n\t{error}')
            await self.update(message._id, 'completed', 'error', message=error)
            return

        start_seconds = datetime.datetime.now().timestamp()
        # 下载失败则直接中止
        if not await self.download(message):
            return

        if datetime.datetime.now().timestamp()-start_seconds < 2:
            await asyncio.sleep(5)

        if(message.category.mode == 'web'):
            await self.web_publish(message)
        elif message.category.mode == 'api':
            await self.api_publish(message)

    def remove_local_files(self, message: Message):
        for f in message.files:
            if f.local_path and os.path.exists(f.local_path):
                os.remove(f.local_path)

    async def download(self, message: Message):
        savepath = os.path.join(self.workdir, 'cache')
        os.makedirs(savepath, exist_ok=True)

        error = ''
        for file in message.files:
            filepath = os.path.join(savepath, file.name)
            if os.path.exists(filepath) and md5_value(filepath) == file.md5:
                file.local_path = filepath
                message.setFileDown(file, 100)
            else:
                success = await download(filepath, file.src, lambda p, s, t: message.setFileDown(file, p))
                if success:
                    if md5_value(filepath) != file.md5:
                        error = file.label + ' 文件校验码不一致'
                        break
                    else:
                        file.local_path = filepath

                    """ if os.path.getsize(filepath) != file.size:
                        error = file.label + ' 文件尺寸不一致'
                        break """
                else:
                    error = file.label+' 下载失败'
                    break

        if error:
            if(message.retried < message.download_retry):
                message.retried += 1
                print(f'\n\t{error}，5秒后尝试第{message.retried+1}次重试')
                await asyncio.sleep(5)
                return await self.download(message)
            print(f'\n\t{error}')
            await self.update(message._id, 'completed', 'error', message=error)
            return False
        else:
            return True

    async def web_publish(self, message: Message):
        youban = Youban(message.category.platform, message.account)
        # 先登录
        res = await youban.login()
        if not res.success:
            print(f'\n\t{res.msg}')
            await self.update(message._id, 'completed', 'error', message=res.msg)
            return

        error = ''
        # 文件上传到cos
        for file in message.files:
            module = 'upload_cover' if file.accept == 'video/jpeg' else 'upload_video'
            res = await youban.web_get_token(module)

            if not res.success:
                error = res.msg
                break

            res = await to_cos(res.data, file.local_path, file.accept, lambda p, s, t: message.setFileUp(file, p))
            if not res.success:
                error = res.msg or '上传时未知错误'
                break

            if file.id == 0:
                message.video_cos = res.data
            elif file.id == 1:
                message.coverinfo_cos = res.data  # 是横版封面
            elif file.id == 2:
                message.coverinfo2_cos = res.data  # 是竖版封面
            elif file.id == 3:
                message.coverinfo1_cos = res.data  # 好像是分屏封面

        if error:
            print(f'\n\t{error}')
            await self.update(message._id, 'completed', 'error', title=message.value.title, message=error)
        else:
            try:
                Location = message.video_cos.get('Location')
                await self.update(message._id, 'publishing', 'uploaded', location=Location)
            except:
                pass

            payload = message.payload
            if message.category.platform == 'tp':
                payload['substance_cateid'] = '混剪'

            res = await youban.web_submit(message.files[0].local_path, payload)
            if res.success:
                print(f'\n\t\033[32m发布成功\033[0m')
                await self.update(message._id, 'completed', 'publish', title=message.value.title)
                self.remove_local_files(message)
            else:
                print(f'\n\t\033[31m{res.msg}\033[0m')
                await self.update(message._id, 'completed', 'error', message=res.msg)

    async def api_publish(self, message: Message):
        error = ''
        youban = Youban(message.category.platform, message.account)
        # 文件上传到cos
        for file in message.files:
            module = 'upload_cover' if file.accept == 'video/jpeg' else 'upload_video'
            res = await youban.api_get_token(module)

            if not res.success:
                error = res.msg
                break

            res = await to_cos(res.data, file.local_path, file.accept, lambda p, s, t: message.setFileUp(file, p))
            if not res.success:
                error = res.msg or '上传时未知错误'
                break

            if file.id == 0:
                message.video_cos = res.data
            elif file.id == 1:
                message.coverinfo_cos = res.data  # 是横版封面
            elif file.id == 2:
                message.coverinfo2_cos = res.data  # 是竖版封面
            elif file.id == 3:
                message.coverinfo1_cos = res.data  # 好像是分屏封面

        if error:
            print(f'\n\t{error}，暂停5秒后继续下一条')
            await self.update(message._id, 'completed', 'error', message=error)
            await asyncio.sleep(5)
        else:
            try:
                Location = message.video_cos.get('Location')
                await self.update(message._id, 'publishing', 'uploaded', location=Location)
            except:
                pass
            res = await youban.api_submit(message.payload)
            if res.success:
                print(f'\n\t\033[32m发布成功\033[0m')
                await self.update(message._id, 'completed', 'publish', title=message.value.title)
                self.remove_local_files(message)
            else:
                print(f'\n\t{res.msg}')
                await self.update(message._id, 'completed', 'error', message=res.msg)

    async def update(self, _id: str, status: str, childStatus: str, title: str = None, message: str = None, location: str = None):
        kwargs = dict(_id=_id, status=status, childStatus=childStatus)
        if title:
            kwargs['title'] = title
        if message:
            kwargs['message'] = message
        if location:
            kwargs['location'] = location
        await self.query('/publish/update', **kwargs)
        return Result(True, wait=0)

    async def query(self, url: str, **kwargs):
        sign, nonce = sign_dict(kwargs, self.appsecret)

        url = f'{self.host}{url}?appid={self.appid}&nonce={nonce}&sign={sign}&version={self.version}'

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
exit_flag2 = False

# 信号处理函数


def signal_handler(signum, frame):
    global exit_flag2
    exit_flag2 = True
    print("\nExiting...")


# 注册信号处理函数
signal.signal(signal.SIGINT, signal_handler)


async def run(version, host, appid, appsecret, workdir):

    print(
        f'\n\n《八戒来了之发布程序 - {version}》\n服务器：{host}\nAppId：{appid}\n工作目录：{workdir}\n')

    client = Publish(version, host, workdir, appid, appsecret)

    while not exit_flag2:
        try:
            res = await client.run()
        except Exception as e:
            # log.error(e,exc_info=True)
            print(f'\n\t{e}')
            await asyncio.sleep(5)
        else:
            if res.msg:
                print(f'\n{res.msg}')
            if not res.success:
                break

            if res.wait > 0:
                next = datetime.datetime.now()+datetime.timedelta(seconds=res.wait)
                print(
                    f'\r暂无任务，{res.wait}秒后({next.strftime("%H:%M:%S")})将再次读取...', end=" ")
                await asyncio.sleep(res.wait)

        if exit_flag2:
            break

    print('已退出程序')
    await client.query('/publish/exit')


def main():
    version, host, appid, appsecret = read()
    if not appid or not appsecret:
        return
    workdir = read_workdir('publish')
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
        save_config('publish','workdir',workdir)

    if sys.version_info.minor >= 10:
        asyncio.run(run(version, host, appid, appsecret, workdir))
    else:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run(version, host, appid, appsecret, workdir))
        loop.close()
