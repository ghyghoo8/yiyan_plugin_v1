#!/usr/env python3
# -*- coding: UTF-8 -*-

from flask import Flask, request, send_file, make_response
from flask_cors import CORS
import json
import random

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://yiyan.baidu.com"}})

wordbook = []

def make_json_response(data, status_code=200):
    response = make_response(json.dumps(data), status_code)
    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/add_word", methods=['POST'])
async def add_word():
    """
        添加一个单词
    """
    word = request.json.get('word', "")
    wordbook.append(word)
    return make_json_response({"message": "单词添加成功"})


@app.route("/delete_word", methods=['DELETE'])
async def delete_word():
    """
        删除一个单词
    """
    word = request.json.get('word', "")
    if word in wordbook:
        wordbook.remove(word)
    return make_json_response({"message": "单词删除成功"})


@app.route("/get_wordbook")
async def get_wordbook():
    """
        获得单词本
    """
    return make_json_response({"wordbook": wordbook})


@app.route("/generate_sentences", methods=['POST'])
async def generate_sentences():
    """
        生成句子
    """
    number = request.get_json()['word_number']
    number = min(number, len(wordbook))
    random_words = random.sample(wordbook, number)
    prompt = "利用英文单词（words）生成一个英文段落，要求这个段落不超过100个英文单词且必须全英文，" \
             "并包含上述英文单词，同时是一个有逻辑的句子，" \
             "并将英文段落翻译成中文，同时用体育老师的口吻陈述这个段落"
    # API返回字段"prompt"有特殊含义：开发者可以通过调试它来调试输出效果
    return make_json_response({"words": random_words, "prompt": prompt})


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