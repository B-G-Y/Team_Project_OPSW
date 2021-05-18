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

######################################################################
#뉴스 시작
######################################################################
class issue():
    session = requests.Session()
    url = "https://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1="       # naver news url
    map_categoryNum = {                                                       # 뉴스 장르별 매핑
        '정치': "100", '경제': "101", '사회': "102", '생활/문화': "103", '생활': "103", '문화': "103", '세계': "104",
        'IT/과학': "105", 'IT': "105", '과학': "105"
    }
    map_categoryKey = {                                                       # 장르별 페이지 소스 클래스 상이값 매핑
        '정치': "cluster_text_headline nclicks(cls_pol.clsart)", '경제': "cluster_text_headline nclicks(cls_eco.clsart)",
        '사회': "cluster_text_headline nclicks(cls_nav.clsart)", '생활/문화': "cluster_text_headline nclicks(cls_lif.clsart)",
        '생활': "cluster_text_headline nclicks(cls_lif.clsart)", '문화': "cluster_text_headline nclicks(cls_lif.clsart)",
        '세계': "cluster_text_headline nclicks(cls_wor.clsart)", 'IT/과학': "cluster_text_headline nclicks(cls_sci.clsart)",
        'IT': "cluster_text_headline nclicks(cls_sci.clsart)", '과학': "cluster_text_headline nclicks(cls_sci.clsart)"
    }

    def __init__(self, cate='정치'):           # 장르 입력값이 없다면 default category = 정치
        self.cate = cate
        self.url = None
        self.categoryKey = None
        self.result = None

        categoryNum = issue.map_categoryNum[cate]
        if not categoryNum:                 # 매핑 실패 시
            print("잘못된 장르 선택")
            return
        self.url = issue.url + categoryNum
        self.categoryKey = issue.map_categoryKey[cate]

        self.search()

    def search(self):
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}
        res = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        lis = soup.find_all("a", class_=self.categoryKey, limit=13)

        title1 = lis[0].text
        link1 = lis[0].attrs.get('href')
        title2 = lis[4].text
        link2 = lis[4].attrs.get('href')
        title3 = lis[8].text
        link3 = lis[8].attrs.get('href')

        self.result = (
            title1 + " (" + link1 + ")\n" +
            title2 + " (" + link2 + ")\n" +
            title3 + " (" + link3 + ")"
        )

    def getIssue(self):
        return self.result

######################################################################  
#뉴스 끝

#코로나 시작 
######################################################################





@app.route('/news', methods=['POST'])  # 뉴스 정보 블럭에 스킬로 연결된 경로
def news():
    req = request.get_json()
    
    input_text = req['userRequest']['utterance'] # 사용자가 전송한 실제 메시지
    
    if '경제' in input_text: # 전송 메시지에 "경제"이 있을 경우는 경제 뉴스 정보를 응답
        res = {
        "contents": [
            {
                "type": "text",
                "text": issue('경제').getIssue()
            }
        ]
    }
    elif '과학'in input_text: # 전송 메시지에 "과학"이 있을 경우는 과학 뉴스 정보를 응답
        res = {
        "contents": [
            {
                "type": "text",
                "text": issue('과학').getIssue()
            }
        ]
    }
    elif '생활' in input_text: # 전송 메시지에 "생활"이 있을 경우는 생활 뉴스 정보를 응답
        res = {
        "contents": [
            {
                "type": "text",
                "text": issue('생활').getIssue()
            }
        ]
    }
    
    # 전송
    return jsonify(res)



# 메인 함수
if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, debug = True, threaded=True)
