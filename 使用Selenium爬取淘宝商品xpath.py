#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  3 13:25:14 2018

@author: oyc
"""

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import time


def get_productlist(browser,txtname,current_page):
    print('正在爬取'+'第'+current_page+'页内容')
    productlist=browser.find_elements_by_xpath("//div[@id='mainsrp-itemlist']//div[@class='items']//div[@class='item J_MouserOnverReq  ']")
    #print(producelist)
    pricelist=[]
    locationlist=[]
    namelist=[]
    imagelist=[]
    shoplist=[]
    for product in productlist:
        price=product.find_element_by_xpath(".//div[@class='ctx-box J_MouseEneterLeave J_IconMoreNew']//div[@class='price g_price g_price-highlight']//strong").text
        name=product.find_element_by_xpath(".//div[@class='ctx-box J_MouseEneterLeave J_IconMoreNew']//div[@class='row row-2 title']//a").text
        shop=product.find_element_by_xpath(".//div[@class='ctx-box J_MouseEneterLeave J_IconMoreNew']//div[@class='row row-3 g-clearfix']//div[@class='shop']//a").text
        location=product.find_element_by_xpath(".//div[@class='ctx-box J_MouseEneterLeave J_IconMoreNew']//div[@class='row row-3 g-clearfix']//div[@class='location']").text
        image=product.find_element_by_xpath(".//div[@class='pic-box J_MouseEneterLeave J_PicBox']//div[@class='pic-box-inner']//div[@class='pic']//a//img").get_attribute('src')
        pricelist.append(price)
        locationlist.append(location)
        namelist.append(name)
        imagelist.append(image)
        shoplist.append(shop)
        print(price+' '+image)

    #写入文件中
    documentname=txtname+'.txt'
    for i in range(0,len(pricelist)):
        with open(documentname,'w+',encoding='utf-8') as f:
            f.write(str(namelist[i])+'\t'+str(shoplist[i])+'\t'+str(locationlist[i])+'\t'+str(pricelist[i])+'\t'+str(imagelist[i])+'\n')
    
def scrollTo(browser):
    #每次应该用 selenium去控制游标向下滑一点   让多一点的产品加载出来
    for i in range(0,5):
        js = 'window.scrollTo( 800 ,' + str((i + 1) * 1280) + ')'
        browser.execute_script(js)
        time.sleep(2)
    
    
def next_page(browser):
    #跳转下一页
    browser.find_element_by_xpath("//div[@id='mainsrp-pager']//div[@class='m-page g-clearfix']//div[@class='wraper']//div[@class='inner clearfix']//ul[@class='items']//li[@class='item next']//a").click()
    time.sleep(5)
    
#获取当前页码
def get_currentpage(browser):
    page_current=browser.find_element_by_xpath("//div[@id='mainsrp-pager']//div[@class='m-page g-clearfix']//div[@class='wraper']//div[@class='inner clearfix']//ul[@class='items']//li[@class='item active']").text
    
    return page_current


#获取句柄
def hanle(browser):
    all_handles = browser.window_handles #获取所有窗口句柄
    #now_handle = browser.current_window_handle #获取当前窗口句柄
    #print(now_handle)
    for handle in all_handles:
        #print(handle)    #输出待选择的窗口句柄
        browser.switch_to_window(handle)
        next_page(browser)#跳转下一页
        #browser.close() #关闭当前窗口
    

#browser.close()
if __name__=='__main__':
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
           'Accept-Charset': 'utf-8',
           'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
           'Connection': 'keep-alive'
           }

    cap = DesiredCapabilities.PHANTOMJS.copy()  #使用copy()防止修改原代码定义dict

    for key, value in headers.items():
        cap['phantomjs.page.customHeaders.{}'.format(key)] = value
    
    url='https://www.taobao.com/'
    #browser = webdriver.PhantomJS(desired_capabilities=cap) #selenium设置phantomjs请求头
    options = webdriver.ChromeOptions()# 进入浏览器设置
    options.add_argument('lang=zh_CN.UTF-8')# 设置中文
    #selenium设置chrome请求头
    options.add_argument('user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36"')# 更换头部
    options.add_argument('Accept="text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"')
    options.add_argument('Connection="keep-alive"')
    options.add_argument('Accept-Charset="utf-8"')
    options.add_argument('Accept-Language="zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3"')
    browser=webdriver.Chrome(chrome_options=options)
    browser.set_window_size(1920,1080)
    browser.get(url)
    #browser.implicitly_wait(3)
    time.sleep(3)
    
    #跳转到https://s.taobao.com/search?q=apple
    try:
        searchKey=browser.find_element_by_xpath("//form[@id='J_TSearchForm']//input[@id='q']")
        searchKey.send_keys('apple')

        searchButton=browser.find_element_by_xpath("//form[@id='J_TSearchForm']/div[@class='search-button']")
        searchButton.click()
    except Exception as e:
        print(e)
    
    
    '''
    get_productlist(browser,'taobao1',get_currentpage(browser))
    hanle(browser)#获取句柄
    next_page(browser)
    get_productlist(browser,'taobao2',get_currentpage(browser))
    hanle(browser)#获取句柄
    next_page(browser)
    get_productlist(browser,'taobao3',get_currentpage(browser))
    page_next=browser.find_element_by_xpath("//div[@id='mainsrp-pager']//div[@class='m-page g-clearfix']//div[@class='wraper']//div[@class='inner clearfix']//ul[@class='items']//li[@class='item active']").text
    print("当前页码为："+page_next)
    
    '''
    #,'taobao4','taobao5','taobao6','taobao7','taobao8','taobao9','taobao10'
    txtnamelist=['taobao1','taobao2','taobao3']
    start_page=0
    end_page=3
    for i in range(start_page,end_page):
        #scrollTo(browser)
        get_productlist(browser,txtnamelist[i],get_currentpage(browser))
        hanle(browser)#获取句柄
            
            
    page_next=browser.find_element_by_xpath("//div[@id='mainsrp-pager']//div[@class='m-page g-clearfix']//div[@class='wraper']//div[@class='inner clearfix']//ul[@class='items']//li[@class='item active']").text
    print("当前页码为："+page_next)  
    




