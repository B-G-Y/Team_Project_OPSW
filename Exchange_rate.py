from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import requests
import urllib.request as req
import urllib

import json


app = Flask(__name__)

#######################
#  환율 제공서비스 함수  #
#######################

@app.route('/exchange_rate', methods=['POST'])
def exchange_rate():
    #   환율 제공 API

    req = request.get_json()

    input_text = req['userRequest']['utterance']  # 사용자가 전송한 실제 메시지

    # HTML 가져오기

    if '미국' in input_text:
        url = 'https://finance.naver.com/marketindex/exchangeDetail.nhn?marketindexCd=FX_USDKRW'
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')

        rate = soup.select_one('table.tbl_calculator > tbody > tr >td').get_text()
        nation = "미국 1USD 기준"

    if '일본' in input_text:
        url = 'https://finance.naver.com/marketindex/exchangeDetail.nhn?marketindexCd=FX_JPYKRW'
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')

        rate = soup.select_one('table.tbl_calculator > tbody > tr >td').get_text()
        nation = "일본 100엔 기준"

    if '중국' in input_text:
        url = 'https://finance.naver.com/marketindex/exchangeDetail.nhn?marketindexCd=FX_CNYKRW'
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')

        rate = soup.select_one('table.tbl_calculator > tbody > tr >td').get_text()
        nation = "중국 1위안 기준"

    # 일반 텍스트형 응답용 메시지
    res = {
        "contents": [
            {
                "type": "text",
                "text": nation + " 환율: " + rate
            }
        ]
    }

    return jsonify(res)

# 메인 함수
if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, debug = True, threaded=True)