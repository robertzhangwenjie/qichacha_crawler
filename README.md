# Crawler

![Build Status](https://travis-ci.org/robertzhangwenjie/qichacha_crawler.svg?branch=master) \
Crawler 是一个专门用来爬取企查查企业信息的爬虫工具，你只需要提供一个拥有企业名称的excel

# 目录结构

- data 存放抓取后保存数据的excel
- page 存放企查查的相关页面的PageObject
- source 存放需要抓取的企业信息excel
- src 存放爬取相关的文件
- utils 存放工具文件
- settings.py 工程的全局配置文件
- run.py 工程的路口

- 使用ScrapyerWithRequests引擎爬取

1. 准备好企业信息的excel,放在source目录下,默认从第二行读取
2. 先手动登录，获取到登录后的cookies，然后替换run.py中的cookies
3. 运行run.py，程序会在data目录自动生成一个与源excel相同名称的excel，并将爬取的信息存入
