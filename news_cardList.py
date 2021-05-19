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


# 메인 함수
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)