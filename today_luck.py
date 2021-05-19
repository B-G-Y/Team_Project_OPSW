# flask용 모듈
from flask import Flask, request, jsonify
# crawling용 모듈
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from selenium import webdriver

import requests
import urllib
import json

app = Flask(__name__)


@app.route('/today_luck', methods=['POST'])
def today_luck():
    req = request.get_json()

    input_text = req['userRequest']['utterance']  # 사용자가 전송한 실제 메시지

    url = 'https://unse.daily.co.kr/?p=zodiac'
    res = requests.get(url)

    soup = BeautifulSoup(res.text, 'html.parser')

    # 1. 내가 찾고자 하는 데이터를 포함하는 가장 근접한 부모
    parent = soup.select_one('#card')

    if '쥐띠' in input_text:
        # 2. 부모 밑에 있는 자식 요소
        children = parent.select('ul')  # select: 여러개의 요소 / select_one: 가장 첫번째 요소
        for i in children:
            lis = i.select('li')
            for n, li in enumerate(lis):
                if n == 0:
                    animal = li.select_one('div > b').get_text()  # 태그 중 텍스트 추출
                    if animal == '쥐':
                        total = li.select_one('div > p').get_text()

    if '소띠' in input_text:
        # 2. 부모 밑에 있는 자식 요소
        children = parent.select('ul')  # select: 여러개의 요소 / select_one: 가장 첫번째 요소
        for i in children:
            lis = i.select('li')
            for n, li in enumerate(lis):
                if n == 0:
                    animal = li.select_one('div > b').get_text()  # 태그 중 텍스트 추출
                    if animal == '소':
                        total = li.select_one('div > p').get_text()

    if '호랑이띠' in input_text:
        # 2. 부모 밑에 있는 자식 요소
        children = parent.select('ul')  # select: 여러개의 요소 / select_one: 가장 첫번째 요소
        for i in children:
            lis = i.select('li')
            for n, li in enumerate(lis):
                if n == 0:
                    animal = li.select_one('div > b').get_text()  # 태그 중 텍스트 추출
                    if animal == '호랑이':
                        total = li.select_one('div > p').get_text()

    if '토끼띠' in input_text:
        # 2. 부모 밑에 있는 자식 요소
        children = parent.select('ul')  # select: 여러개의 요소 / select_one: 가장 첫번째 요소
        for i in children:
            lis = i.select('li')
            for n, li in enumerate(lis):
                if n == 0:
                    animal = li.select_one('div > b').get_text()  # 태그 중 텍스트 추출
                    if animal == '토끼':
                        total = li.select_one('div > p').get_text()

    if '용띠' in input_text:
        # 2. 부모 밑에 있는 자식 요소
        children = parent.select('ul')  # select: 여러개의 요소 / select_one: 가장 첫번째 요소
        for i in children:
            lis = i.select('li')
            for n, li in enumerate(lis):
                if n == 0:
                    animal = li.select_one('div > b').get_text()  # 태그 중 텍스트 추출
                    if animal == '용':
                        total = li.select_one('div > p').get_text()

    if '뱀띠' in input_text:
        # 2. 부모 밑에 있는 자식 요소
        children = parent.select('ul')  # select: 여러개의 요소 / select_one: 가장 첫번째 요소
        for i in children:
            lis = i.select('li')
            for n, li in enumerate(lis):
                if n == 0:
                    animal = li.select_one('div > b').get_text()  # 태그 중 텍스트 추출
                    if animal == '뱀':
                        total = li.select_one('div > p').get_text()

    if '말띠' in input_text:
        # 2. 부모 밑에 있는 자식 요소
        children = parent.select('ul')  # select: 여러개의 요소 / select_one: 가장 첫번째 요소
        for i in children:
            lis = i.select('li')
            for n, li in enumerate(lis):
                if n == 0:
                    animal = li.select_one('div > b').get_text()  # 태그 중 텍스트 추출
                    if animal == '말':
                        total = li.select_one('div > p').get_text()

    if '양띠' in input_text:
        # 2. 부모 밑에 있는 자식 요소
        children = parent.select('ul')  # select: 여러개의 요소 / select_one: 가장 첫번째 요소
        for i in children:
            lis = i.select('li')
            for n, li in enumerate(lis):
                if n == 0:
                    animal = li.select_one('div > b').get_text()  # 태그 중 텍스트 추출
                    if animal == '양':
                        total = li.select_one('div > p').get_text()

    if '원숭이띠' in input_text:
        # 2. 부모 밑에 있는 자식 요소
        children = parent.select('ul')  # select: 여러개의 요소 / select_one: 가장 첫번째 요소
        for i in children:
            lis = i.select('li')
            for n, li in enumerate(lis):
                if n == 0:
                    animal = li.select_one('div > b').get_text()  # 태그 중 텍스트 추출
                    if animal == '원숭이':
                        total = li.select_one('div > p').get_text()

    if '닭띠' in input_text:
        # 2. 부모 밑에 있는 자식 요소
        children = parent.select('ul')  # select: 여러개의 요소 / select_one: 가장 첫번째 요소
        for i in children:
            lis = i.select('li')
            for n, li in enumerate(lis):
                if n == 0:
                    animal = li.select_one('div > b').get_text()  # 태그 중 텍스트 추출
                    if animal == '닭':
                        total = li.select_one('div > p').get_text()

    if '개띠' in input_text:
        # 2. 부모 밑에 있는 자식 요소
        children = parent.select('ul')  # select: 여러개의 요소 / select_one: 가장 첫번째 요소
        for i in children:
            lis = i.select('li')
            for n, li in enumerate(lis):
                if n == 0:
                    animal = li.select_one('div > b').get_text()  # 태그 중 텍스트 추출
                    if animal == '개':
                        total = li.select_one('div > p').get_text()

    if '돼지띠' in input_text:
        # 2. 부모 밑에 있는 자식 요소
        children = parent.select('ul')  # select: 여러개의 요소 / select_one: 가장 첫번째 요소
        for i in children:
            lis = i.select('li')
            for n, li in enumerate(lis):
                if n == 0:
                    animal = li.select_one('div > b').get_text()  # 태그 중 텍스트 추출
                    if animal == '돼지':
                        total = li.select_one('div > p').get_text()

    # 일반 텍스트형 응답용 메시지
    res = {
        "contents": [
            {
                "type": "text",
                "text": total
            }
        ]
    }

    return jsonify(res)


# 메인 함수
if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, debug = True, threaded=True)

