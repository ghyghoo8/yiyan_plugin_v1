#!/usr/env python3
# -*- coding: UTF-8 -*-

from flask import Flask, request, send_file, make_response
from flask_cors import CORS
import json
import random

import get_html

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://yiyan.baidu.com"}})

wordbook = []

def make_json_response(data, status_code=200):
    response = make_response(json.dumps(data), status_code)
    response.headers["Content-Type"] = "application/json"
    return response

@app.route("/get_code", methods=['POST'])
async def get_code():
    """
        获取电影资源
    """
    word = request.json.get('word', "")
    # 可使用markdown格式加入html标签
    return make_json_response({"message": "下面是对应的电影资源",  "wordKey": word})


@app.route("/search_word", methods=['POST'])
async def search_word():
    """
        搜索电影名称
    """
    word = request.json.get('word', "")
    htmlStr = get_html.getHtmlContent(word)
    soup = get_html.getSoup(htmlStr)

    descList = []
    # 取前6个结果
    for s in soup.find_all('h2')[0:5]:
        spans = s.find_parent().find_all('span')
        desc = spans.pop().get_text().strip()
        title = s.a.get_text().strip()
        item = { "title": title, "desc": desc}
        descList.append(item)
    print('descList===>', descList)

    links = list(set(s.a for s in soup.find_all('h2')))
    # print('links====>',links)
    titles = list(set([link.get_text().strip() for link in links]))
    # print('titles====>',titles)
    # 清除空值
    if '' in titles:
        titles.remove('')
    # print('selector titles===>', titles)
    # print('htmlStr==>', htmlStr)
    prompt = "搜索结果列表List##(descList)##的JSON数据格式包含标题##title##和剧情描述##desc##， 并且只针对当前搜索结果。"\
             "根据当前搜索结果列表，将搜索列表的标题##title##作为选项内容,"\
             "保留该选项内容对应的标题##title##与##(wordKey)##匹配度较高的前三个选项,"\
             "且只保留三个选项并按列表选项的形式排列展示,"\
             "优化列表选项的中文内容并删除非中文内容,"\
             "将每一个选项内容翻译成英文并且展示在后面," \
             "并在第二行summary该选项对应的剧情描述##desc##,"\
             "格式如下：##中文内容##(##英文内容##),"\
             "最后提示用户选择一个列表选项。"\
             "如果没有匹配到列表选项，必须展示三个与##(wordKey)##匹配度很高的电影名称推荐给用户，"\
             "并按列表选项的形式排列展示，序号从4开始累加。"\
             "用户选择举例: ##1##等于第一部，##2##等于第二部，##选项1##等于第一部。"
    return make_json_response({"message": "搜索结果",  "wordKey": word,"descList": descList, prompt: prompt})

@app.route("/logo.png")
async def plugin_logo():
    """
        注册用的：返回插件的logo，要求48 x 48大小的png文件.
        注意：API路由是固定的，事先约定的。
    """
    return send_file('logo-n.png', mimetype='image/png')


@app.route("/.well-known/ai-plugin.json")
async def plugin_manifest():
    """
        注册用的：返回插件的描述文件，描述了插件是什么等信息。
        注意：API路由是固定的，事先约定的。
    """
    host = request.host_url
    with open(".well-known/ai-plugin.json", encoding="utf-8") as f:
        text = f.read().replace("PLUGIN_HOST", host)
        return text, 200, {"Content-Type": "application/json"}


@app.route("/.well-known/openapi.yaml")
async def openapi_spec():
    """
        注册用的：返回插件所依赖的插件服务的API接口描述，参照openapi规范编写。
        注意：API路由是固定的，事先约定的。
    """
    with open(".well-known/openapi.yaml", encoding="utf-8") as f:
        text = f.read()
        return text, 200, {"Content-Type": "text/yaml"}




@app.route('/')
def index():
    return 'welcome to my webpage!'

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8081)