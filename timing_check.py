# -*- coding: utf-8 -*-
# desc:实现网站内容定时监测 time：2023-08-19
import requests
import re
from bs4 import BeautifulSoup
import ssl
from requests.packages.urllib3.exceptions import InsecureRequestWarning

#创建列表/记录爬虫的最新捕获
pathlist=[]
#实现文件下载并保存
def Fileload(url,filename):
	headers={'User-Agent': 'Mozilla/5.0'}
	response = requests.get(url,headers=headers)
	with open(filename,'wb') as f:
		f.write(response.content)
#捕获网页中的下载内容
def getContent(url):
	headers={'User-Agent': 'Mozilla/5.0'}
	response = requests.get(url,headers=headers)
	response.encoding='utf-8-sig'
	soup = BeautifulSoup(response.text, 'html.parser')
	fileText = soup.find_all('div',{'id':'content'})
	fileName = r'>(.*?).pdf</a>'
	filePath = r'https://(.*?)">'
	matchesName = re.findall(fileName,str(fileText))
	matchesPath = re.findall(filePath,str(fileText))
	for match in matchesName:
		match = match.strip()  # 去除字符串两端的空格、换行符等
		i=0
		Fileload("https://"+matchesPath[i], match+".pdf")
		print(match+".pdf"+"文件下载完成")
		i=i+1

def timing_check(url):
	headers={'User-Agent': 'Mozilla/5.0'}
	proxies = {'http': 'http://127.0.0.1:8888', 'https': 'http://127.0.0.1:8888'}
	response = requests.get(url,proxies=proxies,verify="cacert.pem")
	response.encoding='utf-8-sig'
	fileText = BeautifulSoup(response.text, 'html.parser')
	fileText = soup.find_all('div',{'class':'content'})
	pattern = r'<li>(.*?)</li>'
	matches = re.findall(pattern,str(fileText))[0]
	soup2 = BeautifulSoup(matches, 'html.parser')
	if soup2.a['href'] in pathlist:
		print("列表已到最新，无所重新获取……")
	else:
		pathlist.append(soup2.a['href'])
		print("文件下载中")
		getContent(soup2.a['href'])

if __name__ == '__main__':
	timing_check("https://kjt.sc.gov.cn/kjt/zfcg/newszwxxgkchild.shtml")
	
