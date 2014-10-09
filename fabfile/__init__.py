#coding:utf-8

import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

from fabric.state import env

from essay.tasks import build
from essay.tasks import deploy
#from essay.tasks import nginx
#from essay.tasks import supervisor

env.GIT_SERVER = 'git.m.sohuno.com'  # ssh地址只需要填：github.com
env.PROJECT = 'apphub'
env.BUILD_PATH = '/home/solar/build/'
env.PROJECT_OWNER = 'lianboshao'
env.DEFAULT_BRANCH = 'master'
env.PYPI_INDEX = 'http://10.13.85.57:12180/simple'


######
# deploy settings:
env.PROCESS_COUNT = 2  #部署时启动的进程数目
env.roledefs = {
    'build': ['solar@10.10.81.160'],  # 打包服务器配置
    'test': ['solar@10.10.93.39'],
}

env.VIRTUALENV_PREFIX = '/home/solar/apphub'
env.SUPERVISOR_CONF_TEMPLATE = os.path.join(PROJECT_ROOT, 'conf', 'supervisord.conf')

# 根据工程确定项目编号
PROJECT_NUM = 102
env.VENV_PORT_PREFIX_MAP = {
    'a': '%d0' % PROJECT_NUM,
    'b': '%d1' % PROJECT_NUM,
    'c': '%d2' % PROJECT_NUM,
    'd': '%d3' % PROJECT_NUM,
    'e': '%d4' % PROJECT_NUM,
    'f': '%d5' % PROJECT_NUM,
    'g': '%d6' % PROJECT_NUM,
    'h': '%d7' % PROJECT_NUM,
    'i': '%d8' % PROJECT_NUM,
}

# env.NGINX_BIN = '/opt/apps/nginx/sbin/nginx'
# env.NGINX_CONF = '/opt/apps/nginx/conf/nginx.conf'
# env.NGINX_SWITCH_CONF = '/opt/apps/nginx/conf/nginx.conf'
# A环境配置:"upstream_pvrs_A"
# B环境配置:"upstream_pvrs_B"
