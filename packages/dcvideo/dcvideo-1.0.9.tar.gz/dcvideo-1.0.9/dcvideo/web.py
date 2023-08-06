from flask import Flask, request, jsonify, send_from_directory
from flask_cors import cross_origin, CORS
import os
import datetime
import argparse
from .config import read_web,save_config

BASE_URL = ''  # f'http://{get_host_ip()}:8019'

# 获取当前文件所在目录的绝对路径
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


UPLOAD_PATH = ''  # os.path.join(BASE_DIR, 'static')

app = Flask(__name__)
CORS(app)


@app.route('/ping')
@cross_origin(origins='*')
def ping():
    return jsonify({'success': True})


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)


@app.route('/', methods=['GET', 'POST'])
@cross_origin(origins='*')
def upload():
    if request.method == 'GET':
        return '''
            <!doctype html>
            <title>局域网存储</title>
            <h1>短视频工作平台之局域网存储</h1>
        '''

    key = request.form.get('key')
    f = request.files['file']
    if not f and not key:
        return jsonify({'success': False, 'msg': '缺少必要参数'})

    isVideo = f.mimetype.startswith('video/mp4')
    isImage = f.mimetype.startswith('image/')
    if not isVideo and not isImage:
        return jsonify({'success': False, 'msg': '必须上传mp4或图片文件'})

    save_dir = os.path.join(
        UPLOAD_PATH, datetime.date.today().strftime('%Y%m%d'))
    # 如果目录不存在则创建
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # 保存文件
    save_path = os.path.join(save_dir, key)
    f.save(save_path)
    url_path = save_path.replace(BASE_DIR, '')
    # 返回文件路径
    return jsonify({'success': True, 'msg': BASE_URL+url_path})


def run(host: str, port: int, workdir: str):
    global BASE_URL, UPLOAD_PATH
    BASE_URL = f'http://{host}:{port}'
    UPLOAD_PATH = workdir
    app.run(host=host, port=port, threaded=True)


def main():
    
    version, host, port, workdir = read_web()
    if not port or not workdir:
        return
    parser = argparse.ArgumentParser()
    parser.add_argument('-port', type=int, default=0)
    parser.add_argument('-dir', type=str, default='')

    args = parser.parse_args()
    if args.port and args.port!=port:
        port = args.port
        save_config('web','port',port)

    if args.dir and args.dir!=workdir:
        if not os.path.exists(args.dir):
            print(f'{args.dir}目录不存在')
            return
        workdir = args.dir
        save_config('web','workdir',workdir)

    print(f'\n\n《八戒来了之上传服务 - {version}》\nhost：{host}:{port}\n工作目录：{workdir}\n')
    run(host, port, workdir)
