from setuptools import setup,find_packages
from dcvideo.config import VERSION

requires = [
    "requests==2.28.1",
    "requests_toolbelt==0.9.1",
    "cos_python_sdk_v5==1.9.21",
    "fake_useragent==1.1.1",
    "flask==2.2.3",
    "flask-cors==3.0.10",
]


setup(
    name='dcvideo', 
    version=VERSION,
    description='', 
    long_description='', 
    author='netfere', 
    author_email='netfere@gmail.com',
    url='https://www.shortvideo.work',
    packages=['dcvideo'],    # 项目需要的包
    python_requires=">=3.7",  # Python版本依赖
    install_requires=requires,  # 第三方库依赖
    entry_points={
        'console_scripts':[
            'video-pub = dcvideo.publish:main',
            'video-exp = dcvideo.export:main',
            'video-web = dcvideo.web:main'
        ]
    },
)