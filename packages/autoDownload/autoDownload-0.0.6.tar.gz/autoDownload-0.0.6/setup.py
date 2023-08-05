# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name = 'autoDownload',
    version = '0.0.6',
    keywords = ['requests',"download","http","thread"],
    description = 'download files quickly',
    long_description = open("README.rst","r",encoding="utf-8").read(),
    author = 'kuankuan',
    author_email = '2163826131@qq.com',
    url="https://kuankuan2007.gitee.io/docs/multithreaded-download/",
    install_requires = [
        'requests',
        'rich',
    ],
    packages = ['autoDownload'],
    
    license = 'Mulan PSL v2',
    platforms=[
        "windows",
        "linux",
        "macos"
    ] ,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Programming Language :: Python :: 3',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'License :: OSI Approved :: Mulan Permissive Software License v2 (MulanPSL-2.0)'
    ],
    entry_points = {
        'console_scripts': [
            'auto-download = autoDownload.terminal:main',
        ],
    }
)
