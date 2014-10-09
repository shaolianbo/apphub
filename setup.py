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
    packages=find_packages(exclude=['*.pyc']),
    include_package_data=True,
    package_data={
    },
    install_requires=[
        "django==1.7",
        "Scrapy",
        "gunicorn",
        "supervisor",
        "mysql-python",
        "pillow",
        "djangorestframework",
    ],
    entry_points={
        'console_scripts': [
            'apphub = manage:main',
        ]
    },
)
