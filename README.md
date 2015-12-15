#AppHub
爬虫抓取豌豆荚的游戏数据, 存储到爬虫数据库. 提供了必要的接口, 用于查询\同步数据, 调用爬虫.

###部署方法

虚拟机需要预先安装libfii-devel

1. 使用essay发版和部署
2. 部署爬虫

	修改crontab, `crontab -e`
	
	添加:
	
	`0 0 * * * sh /home_path/bin/crawl_wandoujia.sh -profile test -env a &>>/log`
	
	说明:
	
	profile:  项目profile
	
	env:  项目部署的虚拟环境
	
	/log:  log文件路径

###接口
####api只读接口
eg: api/apps/?apk_name=com.tuniu.app.ui

**1.url**

api/apps/

**2.method**

get

**3.params**

apk_name 非必须, 查询的应用包名.如果不提供报名,则返回所有应用;如果提供多个apk_name参数,则查询参数指定的所有应用

**4.response body**

	{
	count: 1,
	next: null,
	previous: null,
	results: [
	{
	category: "出行必用",
	tags: [
	"旅游",
	...
	],
	screen_shots: [
	"http://img.wdjimg.com/mms/screenshot/2/d9/8ecd39b51e30acf87f9be611b4c7ed92_320_533.jpeg",
	],
	app_id: "com.tuniu.app.ui",
	top_type: 1,
	url: "http://127.0.0.1:8000/api/apps/10258/",
	data_source: 2,
	name: "途牛旅游",
	logo_origin_url: "http://img.wdjimg.com/mms/icon/v1/5/a3/b3403442d27072aae231f039f0baaa35_256_256.png",
	download_url: "http://apps.wandoujia.com/apps/com.tuniu.app.ui/download",
	score: 0,
	permissions_str: "防止手机休眠;录音;查看网络状态;修改全局系统设置;读取",
	intro: "【产品简介】",
	is_crawled: true,
	last_version: "4.6.0",
	rom: "Android 2.2.x 以上",
	language: null,
	size: "8.14M",
	update_log: null,
	update_date: null,
	developer: "途牛旅游网",
	is_continue: false,
	last_crawl_time: null,
	permissions: [ ]
	}
	]
	}

如果查询不到应用,response_code==200, body.count==0

####爬虫调用接口

eg: spider/crawl/?apk_name=com.tuniu.app.ui, 调用爬虫抓取com.tuniu.app.ui的的数据,并同步到后台.

**1.url**

spider/crawl/

**2.method**

get

**3.param**

apk_name 必须, 可指定多个, 指定要抓取的应用包名.

**4.response**

status_code == 200: 访问成功,body:

	{
	success_apps: [ ],    # 成功抓取到的应用的包名列表
	success: false/true   # 抓取是否全部成功
	}

status_code == 400 : 参数错误
status_code == 5xx:  爬虫程序出了问题
