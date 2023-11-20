from parsel import Selector
import requests
from string import Template

urlTemp =Template('https://xunlei8.cc/s/${s1}.html')
# 设置请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}

def getHtmlContent(word):
  searchUrl = urlTemp.safe_substitute(s1 = word)
  print('searchUrl===>', searchUrl)
  response = requests.get(searchUrl, headers=headers)
  page_text = response.text
  return page_text

def getParseSelector(htmlContent):
  selector = Selector(text=htmlContent)
  return selector