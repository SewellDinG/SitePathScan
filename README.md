# 简介

**SitePathScan** 是一个扫描路径的脚本工具，基于 Python 语言，总体结构较简单，参照王松师傅之前所写的 [webdirscan](https://github.com/Strikersb/webdirscan) 实现了多线程，不过速度上仍然与御剑这类扫描工具差距甚远。

由于 Windows 下拥有众多优秀目录扫描工具，且速度很快；而对于 Mac/Linux 环境， Python 脚本最合适不过。

# 安装

基于 Python 2.x

获取源代码：

```shell
git clone https://github.com/L4oZu1/SitePathScan.git
```

或者直接按URL下载：

```shell
https://github.com/L4oZu1/SitePathScan/archive/master.zip
```

由于使用的是urllib库，直接安装`requests`模块即可：

```shell
pip install requests
```

# 步骤

查看帮助文档：`python SitePathScan.py -h`

```shell
python SitePathScan.py -h
     ____  _ _       ____       _   _     ____
    / ___|(_) |_ ___|  _ \ __ _| |_| |__ / ___|  ___ __ _ _ ___
    \___ \| | __/ _ \ |_) / _` | __| '_ /\___ \ / __/ _` | '_  /
     ___) | | ||  __/  __/ (_| | |_| | | |___) | (_| (_| | | | |
    |____/|_|\__\___|_|   \__,_|\__|_| |_|____/ \___\__,_|_| |_|
    
usage: SitePathScan.py [-h] [-d SCANDICT] [-o SCANOUTPUT] [-t THREADNUM]
                       website

This script uses the urllib library's head() method to determine the status
word and error status。

positional arguments:
  website               The website that needs to be scanned

optional arguments:
  -h, --help            show this help message and exit
  -d SCANDICT, --dict SCANDICT
                        Dictionary for scanning
  -o SCANOUTPUT, --output SCANOUTPUT
                        Results saved files
  -t THREADNUM, --thread THREADNUM
                        Number of threads running the program
```

基本扫描格式：

```shell
python SitePathScan.py https://www.bodkin.ren
python SitePathScan.py https://www.bodkin.ren -d dict/dict.txt -t 20 -o dir.txt
```

默认目录字典文件为 `dict/default.txt`，里面只放了10条目录用于测试我的博客，识别率准确：

```shell
[ 200 ] https://www.bodkin.ren/tools/root.tar
[ 200 ] https://www.bodkin.ren/wp-content/themes/mylife-wp/screenshot.png
[ Forbidden ] https://www.bodkin.ren/wp-content/themes/mylife-wp/1.txt
[ 200 ] https://www.bodkin.ren/web.config
[ 200 ] https://www.bodkin.ren/wp-login.php
[ Forbidden ] https://www.bodkin.ren/wp-content/themes/mylife-wp
[ 200 ] https://www.bodkin.ren/
```

包含200（压缩文件），403，500页面，由于脚本简单，可自定义修改。

# Note

- 默认扫描结果保存路径为当前目录；
- 默认线程数为50，当字典较小时，线程数不宜过大；当字典较大时，可以将线程数调大，但会出现线程竞争而出现报错，脚本报错不会停止运行；
- 没个字典说个求？   ☺，Github一搜一堆，猪猪侠师傅的字典一搜一堆，想要精简的自己搜集吧；
- 本脚本适合学习，实际情况还是需要开个虚拟机用御剑...

# ToDo

- 考虑协程，对比多线程