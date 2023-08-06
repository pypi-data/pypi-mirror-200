import math
from .object import Object
from typing import Any, List, Union


class VideoValue(Object):
    def __init__(self, title: str, category: str, tag: List[str], source: int, activity: Union[int, None], **kwargs) -> None:
        self.title = title
        self.category = category
        self.tag = tag
        self.source = source
        self.activity = activity


class Category(Object):
    def __init__(self, alias: str, name: str, platform: str, mode: str, creator: str, **kwargs) -> None:
        self.alias = alias
        self.name = name
        self.platform = platform
        self.mode = mode
        self.creator = creator


class File(Object):
    local_path: str
    down_value: str
    up_value: str

    def __init__(self, id: int, label: str, md5: str, src: str, size: int, accept: str, name: str, **kwargs) -> None:
        self.id = id
        self.label = label
        self.md5 = md5
        self.src = src
        self.size = size
        self.accept = accept
        self.name = name
        self.local_path = ''
        self.down_value = '0'
        self.up_value = '0'

    @property
    def sizeStr(self):
        value = 0
        unit = ''
        if self.size < 1024:
            value = self.size
            unit = 'B'
        elif self.size < 1024*1024:
            value = self.size/1024
            unit = 'KB'
        elif self.size < 1024*1024*1024:
            value = self.size/1024/1024
            unit = 'MB'
        else:
            value = self.size/1024/1024/1024
            unit = 'GB'
        return f'{math.ceil(value*10)/10}{unit}'


class Account(Object):
    def __init__(self, _id: str, name: str, weight: str, mobile: str, password: str, app_id: str, app_token: str, **kwargs) -> None:
        self._id = _id
        self.name = name
        self.weight = weight
        self.mobile = mobile
        self.password = password
        self.app_id = app_id
        self.app_token = app_token


Creator = {'mix': '混剪', 'split': '拆条', 'explain': '解说', 'inventory': '盘点'}


class Message(Object):
    _id: str
    value: VideoValue
    category: Category
    files: List[File]
    account: Account
    video_cos: Any
    coverinfo_cos: Any
    coverinfo2_cos: Any
    coverinfo1_cos: Any
    download_retry: int
    retried: int

    def __init__(self, _id: str, value: dict, account: dict, category: dict, files: List[dict]) -> None:
        self._id = _id
        self.value = VideoValue(**value)
        self.category = Category(**category)
        self.files = [File(**file) for file in files]
        self.account = Account(**account)
        self.download_retry = 1
        self.retried = 0
        self.video_cos = None
        self.coverinfo_cos = None
        self.coverinfo1_cos = None
        self.coverinfo2_cos = None

    def setFileDown(self, file: File, value):
        file.down_value = f'{value:.1f}%'
        self.console_progress()

    def setFileUp(self, file: File, value):
        file.up_value = f'{value:.1f}%'
        self.console_progress()

    def console_title(self):
        caption = f'\n【{self.account.name}】【{self.category.mode}发布】{self.value.title}'
        if(self.value.activity):
            caption += '【活动】'

        output = ''
        for file in self.files:
            label = file.label+'('+file.sizeStr+')'
            output += f'{label:<30}'

        print(f'{caption}\n\t{output}')

    def console_progress(self):
        output2 = ''
        for file in self.files:
            output2 += f'↓{file.down_value:<15}'
            output2 += f'↑{file.up_value:<17}'
        
        print(f'\r\t{output2}', end=" ")

    @property
    def payload(self):
        return {
            'title': self.value.title,
            'cover': 0,
            'category': self.value.category,
            'source': self.value.source,
            'tag': self.value.tag,
            'inspiration_cateid': '',
            'substance_cateid': Creator.get(self.category.creator),
            'activity': self.value.activity,
            'desc': '',
            'video_cos': self.video_cos,
            'coverinfo_cos': self.coverinfo_cos,
            'coverinfo2_cos': self.coverinfo2_cos,
            'coverinfo1_cos': self.coverinfo1_cos
        }


class ExportMessage(Object):
    _id: str
    category: str
    title: str
    files: List[File]
    download_retry: int
    retried: int

    def __init__(self, _id: str, category: str, title: str, files: List[dict]) -> None:
        self._id = _id
        self.category = category
        self.files = [File(**file) for file in files]
        self.title = title
        self.download_retry = 1
        self.retried = 0

    def setFileDown(self, file: File, value):
        file.down_value = f'{value:.1f}%'
        self.console_progress()

    def setFileUp(self, file: File, value):
        file.up_value = f'{value:.1f}%'
        self.console_progress()

    def console_title(self):
        caption = f'\n【导出】{self.title}'

        output = ''
        for file in self.files:
            label = file.label+'('+file.sizeStr+')'
            output += f'{label:<30}'

        print(f'{caption}\n\t{output}')

    def console_progress(self):
        output2 = ''
        for file in self.files:
            output2 += f'↓{file.down_value:<15}'

        print(f'\r\t{output2}', end=" ")
