import requests
import parsel
from bs4 import BeautifulSoup
from itertools import islice
import pandas as pd
from tqdm import tqdm

headers ={
 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'
}

def get_response(html_url):
    '''发送请求'''
    response = requests.get(url=html_url, headers=headers)
    response.encoding = response.apparent_encoding
    return response

def save(name, title, content):
    """保存小说"""
    with open(name + '.txt', mode='a', encoding='utf-8') as f:
        f.write(title)
        f.write('\n\n')
        f.write(content)
        f.write('\n\n')

def get_novel_content(html_url):
    """获取小说所以章节的url地址"""
    response = get_response(html_url)
    # 把获取到的html字符串数据 转成 selector对象
    soup = BeautifulSoup(response.content, 'html5lib')
    name = soup.select('#linkleft a')[1].get_text()
    # select 方法返回的结果都是列表形式，可以遍历形式输出，然后用 get_text () 方法来获取它的内容
    for href in tqdm(soup.select('#all_chapter a')):
        # 每个章节的链接
        # http://www.biquger.net/html/3/3360/986103.html
        href = "http://www.biquger.net"+href['href']
        # 获取每章小说的内容
        response = get_response(href)
        soup = BeautifulSoup(response.content, 'html5lib')
        # print(soup.prettify())
        title = soup.select('#nr_title h1')[0].get_text()
        content = soup.select('#nr1')[0].get_text()
        # print(title)
        # print(content)
        save(name, title, content)

if __name__ == '__main__':
    # url = 'http://www.biquger.net/html/3/3360/index.html'
    while True:
        print("输入q即可退出")
        word = input('请输入你要下载的小说名字: ')
        if word == 'q' or word == 'Q':
            break
        search_url = 'http://www.biquger.net/modules/article/search.php'
        data = {
            'searchtype': 'articlename',
            'searchkey': word.encode('GBK')
        }
        searchResult = requests.post(url=search_url, data=data, headers=headers)
        searchResult.encoding = searchResult.apparent_encoding
        # print(searchResult.text)
        soup = BeautifulSoup(searchResult.content, 'html5lib')
        trs = soup.select("#content tr")
        list = []
        if len(trs) > 1:
            # 遍历时排除第一行
            for tr in islice(trs, 1, None):
                # print(tr)
                novel_name = tr.select("td")[0].get_text()
                novel_author = tr.select("td")[2].get_text()
                novel_href = tr.select("td a")[1].get('href')
                novel_info = {
                    '书名': novel_name,
                    '作者': novel_author,
                    '链接': novel_href
                }
                list.append(novel_info)
            print(f'一共搜索到{len(list)}本书')
            print(pd.DataFrame(list))
            num = input('请输入你要下载的小说序号： ')
            try:
                if 0 <= int(num) < (len(trs)-1): # 长度要减去标题多余的一行
                    # 序号对应的就是列表里面的索引位置
                    href = list[int(num)]['链接']
                    print(href)
                    get_novel_content(href)
                    print(f"{list[int(num)]['书名']}已经下载完成了！")
                else:
                    print("输入的序号不存在！")
            except ValueError:
                print("输入的序号不正确，请输入数字序号!")
        else:
            print("抱歉，搜索没有结果...")