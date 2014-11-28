#!/usr/bin/env python
#coding: utf-8

import sys,os,urllib,urllib2,re,codecs,bs4

base_url='http://mm.taobao.com/json/request_top_list.htm?page='
base_dir=os.getcwd()+'\\pics\\'

def get_mms(start_page,end_page):
    rc=re.compile(r'src=\"(http\:\/\/img[\w\/!\-\.]*\.jpg)\"')#正则表达式匹配所有的图片，提前编译
    for i in range(start_page,end_page):
        page_num=str(i)
        print '-------page:' + page_num+'----------------'
        list_url=base_url+page_num;
        list_page=urllib2.urlopen(list_url)
        list_html=list_page.read().decode('GBK')#中文乱码
        bs_html=bs4.BeautifulSoup(list_html)
        list_mm_tag_a= bs_html.find_all('a',{'class':'lady-name'})
        list_mm_url=bs_html.find_all('a',{'class':'lady-avatar','target':'_blank'})
        if not os.path.exists(base_dir):
            os.mkdir(base_dir)#创建目录
        for j in range(len(list_mm_tag_a)):
            name=list_mm_tag_a[j].get_text()
            path_name=os.path.join(base_dir,name)
            if not os.path.exists(path_name):
                os.mkdir(path_name) # 根据mm的姓名新建文件夹
            mm_url=list_mm_url[j].get('href')
            mm_page=urllib2.urlopen(mm_url)
            mm_html=mm_page.read()
            mm_html=bs4.BeautifulSoup(mm_html).find('div',{'id':'J_AixiuShow'})#mm主页中有两个区域有图片，我们在还需要此区域的
            pics=re.findall(rc,str(mm_html))#用正则匹配
            print '-------name:'+name+'------begin download-------------'
            count=0#图片编号
            for pic_url in pics:
                count+=1
                pic_name=os.path.join(path_name,str(count)+'.jpg')
                print '-------pic name:'+pic_name
                urllib.urlretrieve(pic_url,pic_name)
            print '-------name:'+name+'------finish download------------'


if __name__=='__main__':
    get_mms(2,3)





