#!/usr/bin/env python
#coding: utf-8
# 多线程
import sys, os, urllib, urllib2, re, codecs, bs4, threading, time, random, socket

socket.setdefaulttimeout(30)
base_url='http://mm.taobao.com/json/request_top_list.htm?page='
base_dir=os.getcwd()+'\\pics\\'
rc = re.compile(r'src=\"(http\:\/\/img[\w\/!\-\.]*\.jpg)\"')  #正则表达式匹配所有的图片，提前编译

# lock=threading.Lock()

def download(mm_name, mm_url):
    path_name = os.path.join(base_dir, mm_name)
    if not os.path.exists(path_name):
        os.mkdir(path_name)  # 根据mm的姓名新建文件夹
    print path_name;
    mm_page = urllib2.urlopen(mm_url, timeout=60)
    mm_html = mm_page.read()
    mm_html = bs4.BeautifulSoup(mm_html).find('div', {'id': 'J_AixiuShow'})  #mm主页中有两个区域有图片，我们在还需要此区域的
    pics = re.findall(rc, str(mm_html))  #用正则匹配
    print '-------name: ' + mm_name + '   images count: ' + str(len(pics)) + '------'
    print '-------name:' + path_name + '------begin download-------------'
    count = 0  #图片编号
    for pic_url in pics:
        count += 1
        pic_name = os.path.join(path_name, str(count) + '.jpg')
        print '-------pic name:' + pic_name
        #lock.acquire()
        urllib.urlretrieve(pic_url, pic_name)
        #lock.release()
    print '-------name:' + path_name + '------finish download------------'


class DownloadThread(threading.Thread):
    def __init__(self, mm_name, mm_url):
        threading.Thread.__init__(self)
        self.mm_name = mm_name
        self.mm_url = mm_url

    def __unicode__(self):
        return self.mm_name, self.mm_url

    def run(self):
        download(self.mm_name, self.mm_url)


def get_mms(start_page,end_page):
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)  #创建目录
    for i in range(start_page,end_page):
        page_num=str(i)
        print '-------page:' + page_num+'----------------'
        list_url=base_url+page_num;
        list_page=urllib2.urlopen(list_url)
        list_html=list_page.read().decode('GBK')#中文乱码
        bs_html=bs4.BeautifulSoup(list_html)
        list_mm_tag_a = bs_html.find_all('a', {'class': 'lady-name'})  # 获取多有包含mm姓名的所有a标签
        list_mm_url = bs_html.find_all('a', {'class': 'lady-avatar', 'target': '_blank'})  # 获取所有mm的空间图片页的url
        threads = []
        lens = len(list_mm_tag_a)
        for j in range(lens):
            mm_name = list_mm_tag_a[j].get_text()  # 获取mm姓名
            mm_url = list_mm_url[j].get('href')  # 获取mm的url
            # 启动多线程下载各个mm的图片，一个mm启动一个线程，一页大约有10个mm
            t = DownloadThread(mm_name, mm_url)
            threads.append(t)
            time.sleep(random.random())
            t.start()

        for t in threads:
            t.join()



if __name__=='__main__':
    start = time.time()
    get_mms(1, 2)
    end = time.time()
    print end-start






