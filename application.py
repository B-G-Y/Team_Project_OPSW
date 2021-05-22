# flask용 모듈
from flask import Flask, request, jsonify
# crawling용 모듈
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from selenium import webdriver

import requests
import urllib
import json

from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)


class issue():
    session = requests.Session()
    url = "https://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1="  # naver news url
    map_categoryNum = {  # 뉴스 장르별 매핑
        '정치': "100", '경제': "101", '사회': "102"
    }
    map_cateTitleKey = {  # 장르별 페이지 소스 타이틀(url) 클래스 상이값 매핑
        '정치': "cluster_text_headline nclicks(cls_pol.clsart)", '경제': "cluster_text_headline nclicks(cls_eco.clsart)",
        '사회': "cluster_text_headline nclicks(cls_nav.clsart)"
    }
    map_cateImgUrlKey = {  # 장르별 페이지 소스 image 클래스 상이값 매핑
        '정치': "cluster_thumb_link nclicks(cls_pol.clsart)", '경제': "cluster_thumb_link nclicks(cls_eco.clsart)",
        '사회': "cluster_thumb_link nclicks(cls_nav.clsart)"
    }

    def __init__(self, cate='정치'):  # 장르 입력값이 없다면 default category = 정치
        self.cate = cate
        self.url = None
        self.categoryKey = None
        self.result = None

        categoryNum = issue.map_categoryNum[cate]
        self.url = issue.url + categoryNum
        self.categoryTitleKey = issue.map_cateTitleKey[cate]
        self.categoryImgUrlKey = issue.map_cateImgUrlKey[cate]

        self.search()

    def search(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}
        res = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        lis = soup.find_all("a", class_=self.categoryTitleKey)
        img_tag = soup.find_all("a", class_=self.categoryImgUrlKey)
        img_url = []                # img_url 저장 리스트
        for src in img_tag:         # img_url 추가
            src_img = src.find('img')
            img_url.append(src_img.get('src'))

        title1 = lis[0].text            # 기사 제목
        link1 = lis[0].attrs.get('href')    # 기사 url
        img_url1 = img_url[0]               # img url
        title2 = lis[4].text
        link2 = lis[4].attrs.get('href')
        img_url2 = img_url[1]
        title3 = lis[8].text
        link3 = lis[8].attrs.get('href')
        img_url3 = img_url[2]

        self.result =[
                title1, link1, img_url1,
                title2, link2, img_url2,
                title3, link3, img_url3
        ]



    def getIssue(self):
        return self.result


@app.route('/news', methods=['POST'])
def news():
    req = request.get_json()

    input_text = req['userRequest']['utterance']  # 사용자가 전송한 실제 메시지

    if '정치' in input_text:  # 정치 항목 선택시
        issueList = issue('정치').getIssue()    # title, url 받을 리스트
        res = {
            "contents": [
                {
                    "type": "card.list",
                    "cards": [
                        {
                            "listItems": [
                                {
                                    "type": "title",
                                    "title": "정치 헤드라인 뉴스 TOP3",
                                    "linkUrl": {
                                        "type": "OS",  # PC나 모바일별 별도 url설정 가능하나 web용으로 동일 적용
                                        "webUrl": "https://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=100"  # 정보 링크 url
                                    }

                                },
                                {
                                    "type": "item",
                                    "imageUrl": issueList[2],
                                    "title": issueList[0],
                                    "linkUrl": {
                                        "type": "OS",  # PC나 모바일별 별도 url설정 가능하나 web용으로 동일 적용
                                        "webUrl": issueList[1]  # 정보 링크 url
                                    }
                                },
                                {
                                    "type": "item",
                                    "imageUrl": issueList[5],
                                    "title": issueList[3],
                                    "linkUrl": {
                                        "type": "OS",
                                        "webUrl": issueList[4]
                                    }
                                },
                                {
                                    "type": "item",
                                    "imageUrl": issueList[8],
                                    "title": issueList[6],
                                    "linkUrl": {
                                        "type": "OS",
                                        "webUrl": issueList[7]
                                    }
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    elif '경제' in input_text:    # 경제 항목 선택시
        issueList = issue('경제').getIssue()  # title, url 받을 리스트
        res = {
            "contents": [
                {
                    "type": "card.list",
                    "cards": [
                        {
                            "listItems": [
                                {
                                    "type": "title",
                                    "title": "경제 헤드라인 뉴스 TOP3",
                                    "linkUrl": {
                                        "type": "OS",  # PC나 모바일별 별도 url설정 가능하나 web용으로 동일 적용
                                        "webUrl": "https://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=101"  # 정보 링크 url
                                    }
                                },
                                {
                                    "type": "item",
                                    "imageUrl": issueList[2],
                                    "title": issueList[0],
                                    "linkUrl": {
                                        "type": "OS",  # PC나 모바일별 별도 url설정 가능하나 web용으로 동일 적용
                                        "webUrl": issueList[1]  # 정보 링크 url
                                    }
                                },
                                {
                                    "type": "item",
                                    "imageUrl": issueList[5],
                                    "title": issueList[3],
                                    "linkUrl": {
                                        "type": "OS",
                                        "webUrl": issueList[4]
                                    }
                                },
                                {
                                    "type": "item",
                                    "imageUrl": issueList[8],
                                    "title": issueList[6],
                                    "linkUrl": {
                                        "type": "OS",
                                        "webUrl": issueList[7]
                                    }
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    elif '사회' in input_text:  # 사회 항목 선택시
        issueList = issue('사회').getIssue()  # title, url 받을 리스트
        res = {
            "contents": [
                {
                    "type": "card.list",
                    "cards": [
                        {
                            "listItems": [
                                {
                                    "type": "title",
                                    "title": "사회 헤드라인 뉴스 TOP3",
                                    "linkUrl": {
                                        "type": "OS",  # PC나 모바일별 별도 url설정 가능하나 web용으로 동일 적용
                                        "webUrl": "https://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=102"  # 정보 링크 url
                                    }
                                },
                                {
                                    "type": "item",
                                    "imageUrl": issueList[2],
                                    "title": issueList[0],
                                    "linkUrl": {
                                        "type": "OS",  # PC나 모바일별 별도 url설정 가능하나 web용으로 동일 적용
                                        "webUrl": issueList[1]  # 정보 링크 url
                                    }
                                },
                                {
                                    "type": "item",
                                    "imageUrl": issueList[5],
                                    "title": issueList[3],
                                    "linkUrl": {
                                        "type": "OS",
                                        "webUrl": issueList[4]
                                    }
                                },
                                {
                                    "type": "item",
                                    "imageUrl": issueList[8],
                                    "title": issueList[6],
                                    "linkUrl": {
                                        "type": "OS",
                                        "webUrl": issueList[7]
                                    }
                                }
                            ]
                        }
                    ]
                }
            ]
        }

    # 전송
    return jsonify(res)

class covid():
    session = requests.Session()  # covid-19 naver.com search result
    tend_url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=covid-19"
    news_url = "https://search.naver.com/search.naver?where=news&sm=tab_jum&query=%EC%BD%94%EB%A1%9C%EB%82%98"

    def __init__(self):  # 장르 입력값이 없다면 default category = 정치
        self.cate = None
        self.tend_url = covid.tend_url
        self.tend_result = None
        self.news_url = covid.news_url
        self.news_result = None

        self.search()

    def search(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}
        tend_res = requests.get(self.tend_url, headers=headers)
        tend_soup = BeautifulSoup(tend_res.text, 'html.parser')
        tend_cum_lis = tend_soup.find_all("p", class_="info_num", limit=5)  # 누적 확진자, 격리해제, 사망자, 검사진행
        tend_add_lis = tend_soup.find_all("em", class_="info_variation", limit=5)  # 추가 (누적 확진자, 격리해제, 사망자, 검사진행)

        news_res = requests.get(self.news_url, headers=headers)
        news_soup = BeautifulSoup(news_res.text, 'html.parser')
        news_lis = news_soup.find_all("a", class_="news_tit")
        img_tag = news_soup.find_all("a", class_="dsc_thumb")
        img_url = []  # img_url 저장 리스트
        for src in img_tag:  # img_url 추가
            src_img = src.find('img')
            img_url.append(src_img.get('src'))

        cumulative = tend_cum_lis[0].text  # 누적 확진자
        add_cum = tend_add_lis[0].text  # (오늘자)추가 확진자
        release = tend_cum_lis[1].text  # 누적 격리해제
        add_rel = tend_add_lis[1].text  # 추가 격리해제
        died = tend_cum_lis[2].text  # 누적 사망자
        add_died = tend_add_lis[2].text  # 추가 사망자
        examination = tend_cum_lis[3].text  # 누적 검사진행
        add_exm = tend_add_lis[3].text  # 추가 검사진행

        news_title1 = news_lis[0].text
        news_link1 = news_lis[0].attrs.get('href')
        news_img1 = img_url[0]
        news_title2 = news_lis[1].text
        news_link2 = news_lis[1].attrs.get('href')
        news_img2 = img_url[1]
        news_title3 = news_lis[2].text
        news_link3 = news_lis[2].attrs.get('href')
        news_img3 = img_url[2]

        self.tend_result = [
            cumulative, add_cum,
            release, add_rel,
            died, add_died,
            examination, add_exm
        ]
        self.news_result = [
            news_title1, news_link1, news_img1,
            news_title2, news_link2, news_img2,
            news_title3, news_link3, news_img3
        ]

    def getCovid_tend(self):
        return self.tend_result

    def getCovid_news(self):
        return self.news_result


@app.route('/covid_19', methods=['POST'])
def covid_19():
    req = request.get_json()

    input_text = req['userRequest']['utterance']  # 사용자가 전송한 실제 메시지 (text 출력)

    if '발생동향' in input_text:  # '발생동향' 항목 선택 시 (확진자, 격리해제수 등의 정보 text 출력)
        tendList = covid().getCovid_tend()   # 발생 동향 List = (누적 확진자, 추가 확진자, 격리해제, 추가 격리해제, 사망자, 추가 사망자, 검사 진행, 추가 검사)
        tendText = ("누적 확진자 : " + tendList[0] + " (+" + tendList[1] + ")\n"      # tendList를 정보 문자열과 함께 저장
                    + "격리해제 : " + tendList[2] + " (+" + tendList[3] + ")\n"
                    + "사망자 : " + tendList[4] + " (+" + tendList[5] + ")\n"
                    + "검사진행 : " + tendList[6] + " (+" + tendList[7] + ")")
        res = {
            "contents": [
                {
                    "type": "text",
                    "text": tendText
                }
            ]
        }
    elif '의심증상 발생 시' in input_text:  # '의심증상 발생 시' 항목 선택 시 (text 출력)
        res = {  # 행동수칙 text 출력
            "contents": [
                {
                    "type": "text",
                    "text": "1. 외출을 자제하고 보건소 또는 콜센터(1339)로 먼저 상담\n2. 콜센터 안내에 따라 반드시 마스크를 착용한 후 선별진료소가 있는 의료기관을 방문\n3. 방문 시 의료진에게 해외여행력을 알림"

                }
            ]
        }
    elif '관련 보도자료' in input_text:  # '관련 보도자료' 항목 선택시 (관련기사 3개 card.list 출력)
        newsList = covid().getCovid_news()  # title, url, img 받을 리스트
        res = {
            "contents": [
                {
                    "type": "card.list",
                    "cards": [
                        {
                            "listItems": [
                                {
                                    "type": "title",
                                    "title": "COVID-19 NEWS TOP 3",
                                    "linkUrl": {
                                        "type": "OS",  # PC나 모바일별 별도 url설정 가능하나 web용으로 동일 적용
                                        "webUrl": "http://ncov.mohw.go.kr/tcmBoardList.do?brdId=&brdGubun=&dataGubun=&ncvContSeq=&contSeq=&board_id=140&gubun="
                                        # 정보 링크 url
                                    }
                                },
                                {
                                    "type": "item",
                                    "imageUrl": newsList[2],
                                    "title": newsList[0],
                                    "linkUrl": {
                                        "type": "OS",
                                        "webUrl": newsList[1]
                                    }
                                },
                                {
                                    "type": "item",
                                    "imageUrl": newsList[5],
                                    "title": newsList[3],
                                    "linkUrl": {
                                        "type": "OS",
                                        "webUrl": newsList[4]
                                    }
                                },
                                {
                                    "type": "item",
                                    "imageUrl": newsList[8],
                                    "title": newsList[6],
                                    "linkUrl": {
                                        "type": "OS",
                                        "webUrl": newsList[7]
                                    }
                                }
                            ]
                        }
                    ]
                }
            ]
        }

    # 전송
    return jsonify(res)

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
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
