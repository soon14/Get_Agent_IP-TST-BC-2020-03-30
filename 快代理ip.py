'''
爬取内容每页的ip以及端口
starturl：               “https://www.kuaidaili.com/free/inha/1/”
导入依赖：               bs4,requests
'''
import requests,concurrent.futures,time
import lxml
from bs4 import BeautifulSoup
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36"
}

#验证ip是否可以使用
def testing_ip(ip):
    try:
        # print("ip:{}".format(ip))
        proxies = {
            'http': 'http://{}'.format(ip),
            'https': 'https://{}'.format(ip)
        }
        url = "https://www.baidu.com/"
        req = requests.get(url, proxies=proxies, timeout=10)
        print("该ip：{}可以使用".format(ip))
        download_txt(ip)
    except Exception as a:
        print("该ip{}无法使用".format(ip))
        print(a)

#验证通过写入文件
def download_txt(ip):
    with open("ip.txt", "a+") as f:
        f.write(ip + "\n")

#获取并解析获得每页ip
def get_iphtml(url):
    print(url)
    req = requests.get(url, headers=headers)
    print(req.status_code)
    soup = BeautifulSoup(req.text,"lxml")
    ip_list = soup.select(".table.table-bordered.table-striped tbody tr")
    ips = ["{1}:{2}".format(i[3].text, i[0].text, i[1].text) for i in [a.select("td") for a in ip_list]]
    print(ips)
    with concurrent.futures.ProcessPoolExecutor(max_workers=10) as threads:
        fun1 = [threads.submit(testing_ip, ip1) for ip1 in ips]

if __name__ == '__main__':
    urls = ["https://www.kuaidaili.com/free/inha/{}/".format(i) for i in range(1, 22)]
    # url = "https://www.kuaidaili.com/free/inha/2/"
    # with concurrent.futures.ProcessPoolExecutor(max_workers=5) as proces:
    #     fun2 = [proces.submit(get_iphtml, u) for u in urls]
    for u in urls:
        get_iphtml(u)
        time.sleep(3)
    with open("ip.txt", "r") as f:
        w = f.readlines()
    print("共可用ip为{}条".format(len(w)))
