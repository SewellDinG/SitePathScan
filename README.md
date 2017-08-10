# 简介

**SitePathScan** 是一个扫描路径的脚本工具，基于 Python 语言，总体结构较简单，Tag v1.0参照王松师傅之前所写的 [webdirscan](https://github.com/Strikersb/webdirscan) 实现了多线程；Tag v2.0受b0uya师傅帮助，了解了Python3下的asyncio协程高并发，配合aiohttp比之前快了三倍有余，不考虑服务器压力影响下，可以与御剑这类扫描工具抗衡。

由于 Windows 下拥有众多优秀目录扫描工具，且速度很快；而对于 Mac/Linux 环境， Python 脚本最合适不过。

# 安装

基于 Python 3.5 及以上版本

获取源代码：

```shell
git clone https://github.com/L4oZu1/SitePathScan.git
```

或者直接按URL下载：

```shell
https://github.com/L4oZu1/SitePathScan/archive/master.zip
```

仅需要安装`aiohttp`模块：

```shell
pip3 install aiohttp
```

# 步骤

查看帮助文档：`python3 SitePathScan.py -h`

```shell
python3 SitePathScan.py -h
     ____  _ _       ____       _   _     ____
    / ___|(_) |_ ___|  _ \ __ _| |_| |__ / ___|  ___ __ _ _ ___
    \___ \| | __/ _ \ |_) / _` | __| '_ /\___ \ / __/ _` | '_  /
     ___) | | ||  __/  __/ (_| | |_| | | |___) | (_| (_| | | | |
    |____/|_|\__\___|_|   \__,_|\__|_| |_|____/ \___\__,_|_| |_|
    
usage: SitePathScan.py [-h] [-d SCANDICT] [-o SCANOUTPUT] [-t COROUTINENUM]
                       website

This script uses the aiohttp library's head() method to determine the status
word.

positional arguments:
  website               The website that needs to be scanned

optional arguments:
  -h, --help            show this help message and exit
  -d SCANDICT, --dict SCANDICT
                        Dictionary for scanning
  -o SCANOUTPUT, --output SCANOUTPUT
                        Results saved files
  -t COROUTINENUM, --thread COROUTINENUM
                        Number of coroutine running the program
```

基本扫描格式：

```shell
python3 SitePathScan.py https://www.bodkin.ren
python3 SitePathScan.py https://www.bodkin.ren -d dict/dict.txt -t 200 -o dir.txt
```

默认目录字典文件为 `dict/default.txt`，里面只放了10条目录用于测试我的博客，识别率准确：

```shell
* SitePathScan ready to start.
* Current target: https://www.bodkin.ren
* Total Dictionary: 10
[ 301 ] https://www.bodkin.ren/wp-content/themes/mylife-wp
[ 200 ] https://www.bodkin.ren/wp-content/themes/mylife-wp/screenshot.png
[ 301 ] https://www.bodkin.ren/index.php
[ 403 ] https://www.bodkin.ren/wp-content/themes/mylife-wp/1.txt
[ 200 ] https://www.bodkin.ren/tools/root.tar
[ 200 ] https://www.bodkin.ren/web.config
[ 200 ] https://www.bodkin.ren/wp-login.php
* End of scan.
```

包含200（压缩文件），301，403页面，由于脚本简单，可自定义修改。

# Note

- 默认扫描结果保存路径为当前目录；
- 默认协程数为50，当字典较小时，协程数不宜过大；当字典较大时，可以将协程数调大，200-1000都行，看硬件配置；
- 没个字典说个求？   ☺，Github一搜一堆，猪猪侠师傅的字典一搜一堆，想要精简的自己搜集吧；
- 本脚本适合学习，（v1.0实际情况还是需要开个虚拟机用御剑）现在不需要了...

# ToDo

- 放弃自带queue，考虑 asyncio 中的队列方法

| Timeline  |       Method       | Tag  |
| :-------: | :----------------: | :--: |
| 2017.8.9  | threading+requests | v1.0 |
| 2017.8.10 |  asyncio+aiohttp   | v2.0 |

 