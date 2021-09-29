##Downlaod Chinese novel by python spider.

###环境介绍
python 3.6解释器

pytharm 编辑器

requests >>> pip install requests

BeautifulSoup

pandas

tqdm


###爬虫基本思路流程：
####一。数据来源分析
    1. 确定需求
        爬取笔趣阁小说内容（一本）
        进行搜索功能（当输入一本小说名字或者作责选择下载相应的小说内容）
    2. 数据来源分析
####二.代码实现过程
    1. 发送请求 对小说章节列表页发送请求
    2. 获取数据 获取网页源代码（响应体的文本数据response.txt）
    3. 解析数据 提取小说章节名字 /url地址
    4. 发送请求 对小说章节url地址发送请求
    5. 获取数据 获取网页源代码（响应体的文本数据response.txt）
    6. 解析数据 提取小说的内容 、 小说章节名
    7. 保持数据
    8. 实现一个搜索功能