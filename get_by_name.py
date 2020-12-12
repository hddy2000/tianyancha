import requests
import urllib
from bs4 import BeautifulSoup
import os
import shutil
headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "www.tianyancha.com",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
    }
url = 'https://www.tianyancha.com/search?key='
company_name="中公教育科技股份有限公司"
page_url=url+company_name
proxy_id=None
# 请求url的html内容
def get_html(url, count):
    if count > 5:
        print("重试超过5次：建议停机检查：", url)
        return ""
        # exit(1)
    # time.sleep(1)
    print("爬取此网页：", url, "次数：", count, " 代理IP：", proxy_id)
    # 代理 IP ,具体刷新获取代理IP需要自己实现下面的refresh_proxy_ip() 函数
    # proxy = {
    #     'http': 'http://' + proxy_id,
    #     'https': 'https://' + proxy_id
    # }
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "www.tianyancha.com",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        # response = requests.get(url, headers=headers, proxies=proxy, timeout=5)
    except BaseException:
        print("异常发生")
        # 这里没有对异常情况作具体处理，只是直接换代理IP 重新请求 就完事昂
        refresh_proxy_ip()
        return get_html(url, count + 1)

    if response.status_code is not 200:
        print("不正常")
        refresh_proxy_ip()
        return get_html(url, count + 1)
    else:
        return response.text
# 根据搜索页获得公司
def get_page_company(page_url):
    html = get_html(page_url, 0)
    soup = BeautifulSoup(html, 'html.parser')
    # print(html)

    # 页内公司href 链表
    company_href_list = []
    company_list_div = soup.find('div', class_="result-list sv-search-container")
    no_company_div = soup.find('div', class_="no-result-container deep-search-detail")
    # 此条件下确实没有分页信息或者公司
    if no_company_div is not None:
        return True
    # 如果没有上面的条件，说明被反爬挡住了
    if company_list_div is None:
        print("此页查找不到分页 scope：", page_url, "注意这个必须要查到哦哦哦哦哦哦哦！！！！！！！！！！！")
        refresh_proxy_ip_free()
        return get_page_company(page_url)
    a_list = company_list_div.find_all('a')

    if a_list is not None:
        for item in a_list:
            if 'https://www.tianyancha.com/company/' in str(item.get("href")):
                if len(str(item.get("href"))) > 36:
                    return str(item.get("href"))

def get_company_info(page_url):
    global headers
    url=get_page_company(page_url)
    res=get_html(url,0)
    # with open(company_name+".html", encoding="UTF-8", mode='w') as f:
    #     f.write(res)
    return res
def get_detail_lawsuits(html):
    soup = BeautifulSoup(html, 'html.parser')
    lawsuit=soup.find("div",id="_container_lawsuit")
    announcement=soup.find("div",id="_container_announcementcourt")
    judical_case_count=soup.find("div",id="nav-main-judicialCaseCount")
    judical_case=soup.find("div",id="_container_judicialCase")

    # print(lawsuit)
    # print(announcement)
    # print(judical_case)
    return lawsuit,announcement

if __name__=="__main__":
    dir="./"+company_name+"/"
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.mkdir(dir)
    # a=get_html(page_url,1)
    # b=get_page_company(page_url)
    res=get_company_info(page_url=page_url)
    # print(res)
    with open(dir+"main.html", encoding="UTF-8", mode='w') as f:
        f.write(res)
    lawsuit,announcement=get_detail_lawsuits(res)
    with open(dir+"lawsuit.html", encoding="UTF-8", mode='w') as f:
        f.write(str(lawsuit))
    with open(dir+"announcement.html", encoding="UTF-8", mode='w') as f:
        f.write(str(announcement))
