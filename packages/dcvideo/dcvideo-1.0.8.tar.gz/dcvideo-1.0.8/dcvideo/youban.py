import json
from typing import List

import requests
from fake_useragent import UserAgent
from requests.cookies import RequestsCookieJar

from .message import Account
from .object import Object
from .result import Result

# https://gist.github.com/kazqvaizer/4cebebe5db654a414132809f9f88067b


def multipartify(data, parent_key=None, formatter: callable = None) -> dict:
    if formatter is None:
        def formatter(v): return (None, v)  # Multipart representation of value

    if type(data) is not dict:
        return {parent_key: formatter(data)}

    converted = []

    for key, value in data.items():
        current_key = key if parent_key is None else f"{parent_key}[{key}]"
        if type(value) is dict:
            converted.extend(multipartify(
                value, current_key, formatter).items())
        elif type(value) is list:
            for ind, list_value in enumerate(value):
                iter_key = f"{current_key}[{ind}]"
                converted.extend(multipartify(
                    list_value, iter_key, formatter).items())
        else:
            converted.append((current_key, formatter(value)))

    return dict(converted)


class VideoPayload(Object):
    def __init__(self, title: str, category: str, source: int, tag: List[str],
                 video_cos: dict,
                 coverinfo_cos: dict,
                 coverinfo2_cos: dict = None,
                 coverinfo1_cos: dict = None,
                 inspiration_cateid: str = None,
                 substance_cateid: str = None,
                 desc: str = None,
                 activity: int = None, **kwargs) -> None:
        super().__init__()
        self.title = title
        self.category = category
        self.source = source
        self.tag = tag
        self.video_cos = video_cos
        self.coverinfo_cos = coverinfo_cos
        self.coverinfo2_cos = coverinfo2_cos
        self.coverinfo1_cos = coverinfo1_cos
        self.inspiration_cateid = inspiration_cateid or ''
        self.substance_cateid = substance_cateid or ''
        self.desc = desc or ''
        self.activity = activity or ''

    def __format_cos(self, data: dict, is_video: bool = False):
        result = {'statusCode': 200}
        for key, value in data.items():
            if key == 'Location':
                Location: str = value.replace(
                    'http://', '').replace('https://', '')
                result['Location'] = Location
                if is_video:
                    arr = Location.split('.')
                    result['Bucket'] = arr[0]
                    result['Key'] = '/'.join(Location.split('/')[1:])
            elif key == 'ETag':
                result['ETag'] = f'"{value}"'
            elif key == 'x-cos-request-id':
                result['RequestId'] = value
            elif key == 'UploadId':
                result['UploadId'] = value

        """ if is_video:
            result['headers'] = {
                'content-type': 'application/xml', 'x-cos-request-id': result['RequestId']}
        else:
            result['headers'] = {
                'content-length': '0', 'etag': result['ETag'], 'x-cos-request-id': result['RequestId']} """
        return result

    def get_data(self, mode: str,platform:str):
        payload = {
            'title': self.title,
            'cover': 0,
            'category': self.category,
            'source': self.source,
            'tag': self.tag,
            'inspiration_cateid': self.inspiration_cateid,
            'activity': self.activity,
            'desc': self.desc,
            'video_cos': self.__format_cos(self.video_cos),
            'coverinfo_cos': self.__format_cos(self.coverinfo_cos, False)
        }
        if(platform=='tp'):
            payload['substance_cateid']=self.substance_cateid
            
        if self.coverinfo2_cos:
            payload['coverinfo2_cos'] = self.__format_cos(
                self.coverinfo2_cos, False)
        if self.coverinfo1_cos:
            payload['coverinfo1_cos'] = self.__format_cos(
                self.coverinfo1_cos, False)

        return payload


class Youban(Object):
    platform: str
    account: Account
    userAgent: str
    cookies: RequestsCookieJar
    xsrfToken: str

    def __init__(self, platform: str, account: Account) -> None:
        self.platform = platform
        self.account = account
        self.BASE_URL = f"https://{self.platform}.xiaozhuyouban.com"
        self.userAgent = UserAgent().random
        self.cookies = None
        self.xsrfToken = ''

    async def api_get_token(self, module: str):
        """
            module = upload_video | upload_cover
        """
        url = f'https://{self.platform}.xiaozhuyouban.com/video/publish/uploadtoken?app_id={self.account.app_id}&app_token={self.account.app_token}&module={module}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 0 and data.get('data') and data['data'].get('cos'):
                return Result(True, data=data['data'].get('cos'))
            else:
                return Result(msg=data.get('message') or '获取上传token失败')
        else:
            return Result(msg='获取上传token失败')

    async def api_submit(self,payload: dict):
        data = VideoPayload(**payload).get_data('api',self.platform)
        data['app_id'] = self.account.app_id
        data['app_token'] = self.account.app_token
        
        headers = {'Content-Type': 'application/json'}
        url = f'https://{self.platform}.xiaozhuyouban.com/video/publish'

        response = requests.post(url, data=json.dumps(data), headers=headers)

        if(response.status_code == 200):
            value = response.json()
            code = value.get('code')
            message = value.get('message') or 'api发布失败'
            return Result(code == 0, message, dict(code=code, message=message))
        else:
            message = f'发布请求异常({response.status_code})'
            return Result(False, message, dict(code=-1, message=message))

    async def login(self):
        r = requests.get(self.BASE_URL)
        self.xsrfToken = r.cookies.get("XSRF-TOKEN")

        headers = {
            'authority': f'{self.platform}.xiaozhuyouban.com',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': self.BASE_URL,
            'referer': f'{self.BASE_URL}/',
            'user-agent': self.userAgent,
            'x-requested-with': 'XMLHttpRequest'
        }

        url = f"https://{self.platform}.xiaozhuyouban.com/signin"
        r = requests.post(
            url,
            data={"xsrfToken": self.xsrfToken,
                  "mobile": self.account.mobile, "password": self.account.password, "agree": "on"},
            cookies=r.cookies,
            headers=headers
        )
        if r.status_code == 200:
            data = r.json() or {'code': -1}
            code = data.get('code')
            message = data.get('message') or '登录未知错误'
            if code == 0:
                r.cookies.set('__root_domain_v', '.xiaozhuyouban.com')
                self.cookies = r.cookies
                return Result(True)
            else:
                action = 0
                if '爬虫' in message:
                    action = 401  # 全部停止
                return Result(msg=message)
        else:
            return Result(msg=f'登录失败：{r.status_code}')

    async def web_get_token(self, module: str):
        url = f'https://{self.platform}.xiaozhuyouban.com/storage/token'

        headers = {
            'authority': f'{self.platform}.xiaozhuyouban.com',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': self.BASE_URL,
            'referer': f'{self.BASE_URL}/content/publish',
            'user-agent': self.userAgent,
            'x-requested-with': 'XMLHttpRequest',
            'x-csrf-token': self.xsrfToken
        }

        r = requests.post(
            url,
            data={'module': module},
            cookies=self.cookies,
            headers=headers
        )

        if r.status_code == 200:
            data = r.json()
            if data.get('code') == 0 and data.get('data') and data['data'].get('cos'):
                return Result(True, data=data['data'].get('cos'))
            else:
                return Result(msg=data.get('message') or '获取上传token失败')
        else:
            return Result(msg=f'获取上传token失败')

    async def web_submit(self, filepath: str, payload: dict):
        data = VideoPayload(**payload).get_data('web',self.platform)
        
        headers = {
            'authority': f'{self.platform}.xiaozhuyouban.com',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
            'origin': self.BASE_URL,
            'referer': f'https://{self.platform}.xiaozhuyouban.com/content/publish',
            'user-agent': self.userAgent,
            'x-requested-with': 'XMLHttpRequest',
            'x-csrf-token': self.xsrfToken,
        }

        data = multipartify(data)
        data["coverfile"] = ('cover.jpg', open(filepath, 'rb'), 'image/jpeg')

        response = requests.post(
            f'https://{self.platform}.xiaozhuyouban.com/content/publish',
            files=data, headers=headers, cookies=self.cookies
        )

        if(response.status_code == 200):
            value = response.json()
            code = value.get('code')
            message = value.get('message') or 'web发布失败'
            return Result(code == 0, message, dict(code=code, message=message))
        else:
            message = f'发布请求异常({response.status_code})'
            return Result(False, message, dict(code=-1, message=message))
