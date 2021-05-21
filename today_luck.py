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

    # 2. 부모 밑에 있는 자식 요소
    children = parent.select('ul')  # select: 여러개의 요소 / select_one: 가장 첫번째 요소
    for i in children:
        lis = i.select('li')
        for n, li in enumerate(lis):
            if n == 0:
                animal = li.select_one('div > b').get_text()  # 태그 중 텍스트 추출
                if animal == '쥐' and '쥐띠' in input_text:
                    total = li.select_one('div > p').get_text()
                elif animal == '소' and '소띠' in input_text:
                    total = li.select_one('div > p').get_text()
                elif animal == '호랑이' and '호랑이띠' in input_text:
                    total = li.select_one('div > p').get_text()
                elif animal == '토끼' and '토끼띠' in input_text:
                    total = li.select_one('div > p').get_text()
                elif animal == '용' and '용띠' in input_text:
                    total = li.select_one('div > p').get_text()
                elif animal == '뱀' and '뱀띠' in input_text:
                    total = li.select_one('div > p').get_text()
                elif animal == '말' and '말띠' in input_text:
                    total = li.select_one('div > p').get_text()
                elif animal == '양' and '양띠' in input_text:
                    total = li.select_one('div > p').get_text()
                elif animal == '원숭이' and '원숭이띠' in input_text:
                    total = li.select_one('div > p').get_text()
                elif animal == '닭' and '닭띠' in input_text:
                    total = li.select_one('div > p').get_text()
                elif animal == '개' and '개띠' in input_text:
                    total = li.select_one('div > p').get_text()
                elif animal == '돼지' and '돼지띠' in input_text:
                    total = li.select_one('div > p').get_text()

    # 일반 텍스트형 응답용 메시지
    res = {
        "contents": [
            {
                "type": "text",
                "text": "오늘의 운세 \n" + total
            }
        ]
    }

    return jsonify(res)


# 메인 함수
if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, debug = True, threaded=True)

