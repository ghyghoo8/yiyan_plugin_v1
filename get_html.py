from parsel import Selector
import requests

#模拟请求
res = requests.get('https://www.runoob.com/')
res.encoding='UTF-8'#设置编码(这里不写可能会乱码)

print(res.text) #输出接收的内容