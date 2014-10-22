# coding: utf-8
#!/usr/bin/env python

from setuptools import setup, find_packages

readme = open('README').read()

setup(
    name='apphub',
    version='${version}',
    description=readme.partition('\n')[0],
    long_description=readme,
    author='lianboshao',
    author_email='lianboshao@sohu-inc.com',
    url='http://git.m.sohuno.com/lianboshao/apphub',
    packages=find_packages('apphub'),
    package_dir={'': 'apphub'},
    include_package_data=True,
    scripts=[
        'apphub/manage.py',
        'crawl_wandoujia.sh'
    ],
    install_requires=[
        "django==1.7",
        "cffi",       # 在scrapy之前安装cffi, 否则在无法访问外网时, scrapy安装失败
        "Scrapy",
        "gunicorn",
        "supervisor",
        "mysql-python",
        "pillow",
        "djangorestframework",
        "gevent"
    ],
)
