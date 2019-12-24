# -*- coding: utf-8 -*-
import random
import urllib.request
import re
import time
from pylab import mpl
from lxml import etree
from xlwt import Workbook
import pygal


mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
headers = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
]

def main():
    # 用来存放所有的电脑数据
    allNames = []
    allCommentNums = {}
    allPrices = {}
    allShops = {}
    allGoodCommentNums={}
    allGeneralCommentNums={}
    allPoorCommentNums={}
    #保存数据
    book = Workbook()
    sheet = book.add_sheet('京东电脑数据')
    sheet.write(0,0,"电脑")
    sheet.write(0,1,"店铺")
    sheet.write(0,2,"价格")
    sheet.write(0,3,"评论数")
    sheet.write(0,4,"好评数")
    sheet.write(0,5,"中评数")
    sheet.write(0,6,"差评数")

    # 爬取前15页的所有笔记本电脑
    for i in range(0, 1):
        # 每页地址规律：https://list.jd.com/list.html?cat=670,671,672&page=【页码】
        print('正在爬取第'+str(i+1)+'页的信息...')
        url = 'https://list.jd.com/list.html?cat=670,671,672&page='+str(i+1)
        get_page_data(url, allNames, allCommentNums, allPrices, allShops,allGoodCommentNums,allGeneralCommentNums,allPoorCommentNums)

    # 以上为获取信息，以下为数据的可视化
    names = allNames
    commentNums = []
    GoodCommentNums=[]
    GenerCommentNums=[]
    poorCommentNums=[]
    #评论数
    for name in names:
        if allCommentNums[name] == None:
            commentNums.append(0)
        else:
            commentNums.append(eval(allCommentNums[name]))
    #好评数
    for name in names:
        if allGoodCommentNums[name] == None:
            GoodCommentNums.append(0)
        else:
           GoodCommentNums.append(eval(allGoodCommentNums[name]))
    #中评数
    for name in names:
        if allGeneralCommentNums[name] == None:
            GenerCommentNums.append(0)
        else:
            GenerCommentNums.append(eval(allGeneralCommentNums[name]))
    #差评数
    for name in names:
        if allPoorCommentNums[name] == None:
           poorCommentNums.append(0)
        else:
            poorCommentNums.append(eval(allPoorCommentNums[name]))
    prices = []
    for name in names:
        if allPrices[name] == None:
            prices.append(0)
        else:
            prices.append(eval(allPrices[name]))
    shops = []
    try:
        for name in names:
            if allShops[name] == None:
                shops.append(0)
            else:
                shops.append(allShops[name])
    except:
      print ("请求超时")
    print(len(names)+1)
    for i in range(0, len(names)):
        sheet.write(i+1,0,names[i])
        sheet.write(i+1,1,shops[i])
        sheet.write(i+1,2,prices[i])
        sheet.write(i+1,3,commentNums[i])
        sheet.write(i+1,4,GoodCommentNums[i])
        sheet.write(i+1,5,GenerCommentNums[i])
        sheet.write(i+1,6,poorCommentNums[i])
        book.save("数据.xls")
        print(names[i])
        print(commentNums[i])
        print(prices[i])
        print(shops[i])
        print(GenerCommentNums[i])
        print(GoodCommentNums[i])
        print(poorCommentNums[i])
    # 先需要统计每个店铺的个数
    shopNames = list(set(shops))
    nums = []
    for i in range(0, len(shopNames)):
        nums.append(0)
    for shop in shops:
        for i in range(0, len(shopNames)):
            if shop == shopNames[i]:
                nums[i] += 1

def get_page_data(url, allNames, allCommentNums, allPrices, allShops,allGoodCommentNums, allGeneralCommentNums,allPoorCommentNums):
    # 爬取该页内所有电脑的id、电脑名称和该电脑的具体网址
    response = urllib.request.Request(url)
    response.add_header('User-Agent', random.choice(headers))
    data = urllib.request.urlopen(response, timeout=1000).read().decode('utf-8', 'ignore')
    data = etree.HTML(data)
    ids = data.xpath('//a[@class="p-o-btn contrast J_contrast contrast-hide"]/@data-sku')
    names = data.xpath('//div[@class="p-name"]/a/em/text()')
    hrefs = data.xpath('//div[@class="p-name"]/a/@href')
    # 去掉重复的网址
  #  print(len(hrefs))
    hrefs = list(set(hrefs))
  #  print(len(hrefs))
    # 将每个电脑的网址构造完全,加上'https:'
    for i in range(0, len(hrefs)):
        hrefs[i] = 'https:'+hrefs[i]

    # 根据id构造存放每台电脑评论数的js包的地址
    # 其网址格式为：https://club.jd.com/comment/productCommentSummaries.action?my=pinglun&referenceIds=100000323510,100002368328&callback=jQuery5043746
    str = ''
    for id in ids:
        str = str + id + ','
    commentJS_url = 'https://club.jd.com/comment/productCommentSummaries.action?my=pinglun&referenceIds='+str[:-1]+'&callback=jQuery5043746'
    # 爬取该js包，获取每台电脑的评论数
    response2 = urllib.request.Request(commentJS_url)
    response2.add_header('User-Agent', random.choice(headers))
    data = urllib.request.urlopen(response2, timeout=1).read().decode('utf-8', 'ignore')
    pat = '{(.*?)}'
    commentStr = re.compile(pat).findall(data)  # commentStr用来存放每个商品的关于评论数方面的所有信息
    GoodStr=re.compile(pat).findall(data)#关于好评数的信息
    poorStr=re.compile(pat).findall(data)   #关于差评数
    GenerStr=re.compile(pat).findall(data)  # 关于中评数
    comments = {}
    goodComments={}
    generalComments={}
    poorComments={}


    # 评论数
    for id in ids:
        for str in commentStr:
            if id in str:
                pat2 = '"CommentCount":(.*?),'
                comments[id] = re.compile(pat2).findall(str)[0]
    #好评数
    for id in ids:
        for str in GoodStr:
            if id in str:
                pat4 = '"GoodCount":(.*?),'
                goodComments[id] = re.compile(pat4).findall(str)[0]

        # 中评数
        for id in ids:
            for str in GenerStr:
                if id in str:
                    pat5 = '"GeneralCount":(.*?),'
                    generalComments[id] = re.compile(pat5).findall(str)[0]

    #差评数
    for id in ids:
        for str in poorStr:
            if id in str:
                pat5 = '"PoorCount":(.*?),'
                poorComments[id] = re.compile(pat5).findall(str)[0]
    print("ids为：", len(ids),ids)
    print("name为:", len(names), names)
    print("评论数为：", len(comments), comments)
    print("好评数为：",len(goodComments),goodComments)
    print("中评数为：",len(generalComments),generalComments)
    print("差评数为：", len(poorComments), poorComments)

    # 根据id构造存放每台电脑价格的js包的地址
    # 其网址格式为：https://p.3.cn/prices/mgets?callback=jQuery1702366&type=1&skuIds=J_7512626%2CJ_44354035037%2CJ_100003302532
    str = ''
    for i in range(0, len(ids)):
        if i == 0:
            str = str + 'J_' + ids[i] + '%'
        else:
            str = str + '2CJ_' + ids[i] + '%'
    priceJS_url = 'https://p.3.cn/prices/mgets?callback=jQuery1702366&type=1&skuIds=' + str[:-1]
    # 爬取该js包，获取每台电脑的价格
    response3 = urllib.request.Request(priceJS_url)
    response3.add_header('User-Agent', random.choice(headers))
    data = urllib.request.urlopen(response3, timeout=1).read().decode('utf-8', 'ignore')
    priceStr = re.compile(pat).findall(data)  # priceStr用来存放每个商品关于价格方面的信息
    prices = {}
    for id in ids:
        for str in priceStr:
            if id in str:
                pat3 = '"p":"(.*?)"'
                prices[id] = re.compile(pat3).findall(str)[0]
    #print("价格为：", prices)

    # 爬取每个商品的店铺,需要进入到对应的每个电脑的页面去爬取店铺信息
    shops = {}
    for id in ids:
        for href in hrefs:
            if id in href:
                try:
                    response4 = urllib.request.Request(href)
                    response4.add_header('User-Agent', random.choice(headers))
                    data = urllib.request.urlopen(response4, timeout=1).read().decode('gbk', 'ignore')
                    shop = etree.HTML(data).xpath('//*[@id="crumb-wrap"]/div/div[2]/div[2]/div[1]/div/a/@title')
                    print(shop)
                    if shop == []:
                        shops[id] = None
                    else:
                        shops[id] = shop[0]
                    time.sleep(2)
                except Exception as e:
                    shops[id]=None
                    print(e)
    # 先去掉电脑名两边的空格和换行符
    [name.strip() for name in names]
    # 将数据分别添加到item中
    for name in names:
        allNames.append(name)
    # 名字对应评论数的字典形式
    for i in range(0, len(ids)):
        if comments[ids[i]] == '':
            allCommentNums[names[i]] = None
        else:
            allCommentNums[names[i]] = comments[ids[i]]
    # goodComments = {}
    # generalComments = {}
    # poorComments = {}
   #名字与对应的好评数的字典形式
    for i in range(0, len(ids)):
        if goodComments[ids[i]] == '':
            allGoodCommentNums[names[i]] = None
        else:
            allGoodCommentNums[names[i]] = goodComments[ids[i]]
   #名字与中评数的字典形式
    for i in range(0, len(ids)):
        if generalComments[ids[i]] == '':
            allGeneralCommentNums[names[i]] = None
        else:
            allGeneralCommentNums[names[i]] = generalComments[ids[i]]
   #名字与差评数的字典形式
    for i in range(0, len(ids)):
        if poorComments[ids[i]] == '':
            allPoorCommentNums[names[i]] = None
        else:
            allPoorCommentNums[names[i]] = poorComments[ids[i]]
    # 名字与价格对应起来
    for i in range(0, len(ids)):
        if prices[ids[i]] == '':
            allPrices[names[i]] = None
        else:
            allPrices[names[i]] = prices[ids[i]]
    # 名字与店铺对应起来
    try:
        for i in range(0, len(ids)):
            allShops[names[i]] = shops[ids[i]]
    except:
       print ("请求超时")

if __name__ == '__main__':
	main()
