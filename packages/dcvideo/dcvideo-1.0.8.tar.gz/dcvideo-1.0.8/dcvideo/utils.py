import datetime
import hashlib
import hmac
import random
import socket
from contextlib import closing
from typing import Callable

import requests
from qcloud_cos import CosConfig, CosS3Client
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

from .result import Result


def ymd():
    return datetime.datetime.now().strftime('%Y%m%d')


def sign_dict(data, secret):
    """
    对dict数据进行签名
    :param data: 需要签名的数据
    :param secret: 密钥
    :return: 签名后的字符串
    """
    # 对key键进行降序排列
    sorted_data = sorted(data.items(), key=lambda x: x[0], reverse=True)
    # 将排列后的dict转换成字符串
    data_str = '&'.join([f'{k}={v}' for k, v in sorted_data])
    # 随机生成一个字符串作为盐值
    nonce = str(random.random())
    # 拼接数据和盐值
    message = nonce + data_str
    # 使用HMAC对数据进行签名
    sign = hmac.new(secret.encode(), message.encode(),
                    hashlib.sha256).hexdigest()
    # 返回签名后的字符串和盐值
    return sign, nonce


async def download(savepath: str, src: str, callback: Callable[[int, int, int], None]):
    try:
        with closing(requests.get(src, stream=True)) as response:
            chunk_size = 1024  # 单次请求最大值
            total = int(response.headers['content-length'])  # 内容体总大小
            size = 0
            with open(savepath, "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    size = size + len(data)
                    progress = (size / total) * 100
                    callback(progress, size, total)
    except:
        return False
    else:
        return True
    

async def to_cos(cos: dict, filepath: str, accept: str, callback):
    def cb(monitor):
        progress = (monitor.bytes_read / monitor.len) * 100
        callback(progress, monitor.bytes_read, monitor.len)

    bucket = cos.get('bucket')
    key = cos.get('filekey')
    region = cos.get('region')
    StartTime = cos.get('startTime')
    expiredTime = cos.get('expiredTime')
    credentials = cos.get('credentials') or []
    secret_id = credentials.get('tmpSecretId')
    secret_key = credentials.get('tmpSecretKey')
    token = credentials.get('sessionToken')
    url = f'https://{bucket}.cos.ap-shanghai.myqcloud.com{key}'

    config = CosConfig(Region=region, SecretId=secret_id,
                       SecretKey=secret_key, Token=token)
    client = CosS3Client(config)

    def cb(monitor):
        progress = (monitor.bytes_read / monitor.len) * 100
        callback(progress, monitor.bytes_read, monitor.len)

    fields = {
        'key': key,
        'Content-Type': accept,
        'file': (key, open(filepath, 'rb'), accept)
    }
    e = MultipartEncoder(fields)
    m = MultipartEncoderMonitor(e, cb)
    headers = {
        'Host': f'{bucket}.cos.ap-shanghai.myqcloud.com',
        'Content-Type': m.content_type,
        'x-cos-security-token': token
    }
    headers['Authorization'] = client.get_auth(
        "POST", bucket, key, Expired=expiredTime-StartTime)

    try:
        r = requests.post(url, data=m, headers=headers)

        if(r.status_code == 200 or r.status_code == 204):
            return Result(
                success=True,
                data={
                    'ETag': r.headers.get('ETag').replace('"', ''),
                    'Location': r.headers.get('Location'),
                    'x-cos-request-id': r.headers.get('x-cos-request-id')
                }
            )
        else:
            return Result(msg=r.text)
    except Exception as ex:
        return Result(msg=str(ex), data=ex)

#计算文件md5
def md5_value(filename):
    m = hashlib.md5()
    with open(filename, 'rb') as f:
        while True:
            data = f.read(8192)
            if not data:
                break
            m.update(data)
    return m.hexdigest()

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        address = ("8.8.8.8", 80)
        s.connect(address)
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
        
    return ip

def port_is_used(ip,port):
    """
    判断端口是否可用
    """
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((ip, port))
        return True
    except Exception as e:
        return False
    finally:
        if s:
            s.close()
            