from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)


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
        tend_cum_lis = tend_soup.find_all("p", class_="info_num")         # 누적 확진자, 격리해제, 사망자, 검사진행
        tend_add_lis = tend_soup.find_all("em", class_="info_variation")  # 추가 (누적 확진자, 격리해제, 사망자, 검사진행)

        news_res = requests.get(self.news_url, headers=headers)
        news_soup = BeautifulSoup(news_res.text, 'html.parser')
        news_lis = news_soup.find_all("a", class_="news_tit")
        img_tag = news_soup.find_all("a", class_="dsc_thumb")
        img_url = []         # img_url 저장 리스트
        for src in img_tag:  # img_url 추가
            src_img = src.find('img')
            img_url.append(src_img.get('src'))

        cumulative = tend_cum_lis[0].text      # 누적 확진자
        add_cum = tend_add_lis[0].text         # (오늘자)추가 확진자
        release = tend_cum_lis[1].text         # 누적 격리해제
        add_rel = tend_add_lis[1].text         # 추가 격리해제
        died = tend_cum_lis[2].text            # 누적 사망자
        add_died = tend_add_lis[2].text        # 추가 사망자
        examination = tend_cum_lis[3].text     # 누적 검사진행
        add_exm = tend_add_lis[3].text         # 추가 검사진행

        news_title1 = news_lis[0].text
        news_link1 = news_lis[0].attrs.get('href')
        news_img1 = img_url[0]
        news_title2 = news_lis[1].text
        news_link2 = news_lis[1].attrs.get('href')
        news_img2 = img_url[1]
        news_title3 = news_lis[2].text
        news_link3 = news_lis[2].attrs.get('href')
        news_img3 = img_url[2]

        self.tend_result = (
                "누적 확진자 : " + cumulative + "(+" + add_cum + ")\n"
                + "격리해제 : " + release + "(+" + add_rel + ")\n"
                + "사망자 : " + died + "(+" + add_died + ")\n"
                + "검사진행 : " + examination + "(+" + add_exm + ")"
        )
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

    if '발생동향' in input_text:         # '발생동향' 항목 선택 시 (확진자, 격리해제수 등의 정보 text 출력)
        res = {
            "contents": [
                {
                    "type": "text",
                    "text": covid().getCovid_tend()
                }
            ]
        }
    elif '의심증상 발생 시' in input_text:    # '의심증상 발생 시' 항목 선택 시 (text 출력)
        res = {                            # 행동수칙 text 출력
            "contents": [
                {
                    "type": "text",
                    "text": "1. 외출을 자제하고 보건소 또는 콜센터(1339)로 먼저 상담\n2. 콜센터 안내에 따라 반드시 마스크를 착용한 후 선별진료소가 있는 의료기관을 방문\n3. 방문 시 의료진에게 해외여행력을 알림"

                }
            ]
        }
    elif '관련 보도자료' in input_text:           # '관련 보도자료' 항목 선택시 (관련기사 3개 card.list 출력)
        newsList = covid().getCovid_news()      # title, url, img 받을 리스트
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
                                        "webUrl": "http://ncov.mohw.go.kr/tcmBoardList.do?brdId=&brdGubun=&dataGubun=&ncvContSeq=&contSeq=&board_id=140&gubun="  # 정보 링크 url
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


# 메인 함수
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)