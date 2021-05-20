from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from datetime import datetime
import requests
import urllib.request as req
import urllib


import json


app = Flask(__name__)

@app.route('/music', methods=['POST'])
def music():
    req = request.get_json()

    input_text = req['userRequest']['utterance']  # 사용자가 전송한 실제 메시지

    # HTML 가져오기
    if '24H' in input_text:
        RANK = 5  ## 멜론 차트 순위 1 ~ 5위까지

        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
        req = requests.get('https://www.melon.com/chart/index.htm', headers=header)  ## 실시간 차트를 크롤링 할 것임

        html = req.text
        parse = BeautifulSoup(html, 'html.parser')

        titles = parse.find_all("div", {"class": "ellipsis rank01"})
        singers = parse.find_all("div", {"class": "ellipsis rank02"})
        img_urls = parse.select('tbody > tr')
        songInfo_urls = parse.select('tbody > tr')

        title = []
        singer = []

        img_url = []
        imgSrcRank = []

        songInfo = []
        songInfo_Go = []

        ChartRankInfo = []

        for t in titles:
            title.append(t.find('a').text)

        for s in singers:
            singer.append(s.find('span', {"class": "checkEllipsis"}).text)

        for im in img_urls:
            img = im.select_one('td > div.wrap > a > img')
            imgSrc = img.attrs["src"]
            imgSrcRank.append(imgSrc)

        for si in songInfo_urls:
            songi = si.select_one('td > div.wrap.t_right > input')
            songin = songi.attrs["value"]
            songInfo_Go.append(songin)

        for i in range(RANK):
            ChartRankInfo.append(title[i] + "\n" + singer[i])

        res = {
            "contents": [
                {
                    "type": "card.list",
                    "cards": [
                        {
                            "listItems": [
                                {
                                    "type": "title",
                                    "title": "24H 인기차트",
                                    "linkUrl": {
                                        "type": "OS",  # PC나 모바일별 별도 url설정 가능하나 web용으로 동일 적용
                                        "webUrl": "https://www.melon.com/chart/index.htm"  # 정보 링크 url
                                    }
                                },
                                {
                                    "type": "item",
                                    "imageUrl": imgSrcRank[0],
                                    "title": "1등 " + ChartRankInfo[0],  # i=0부터 1등 정보 매겨짐
                                    "linkUrl": {
                                        "type": "OS",  # PC나 모바일별 별도 url설정 가능하나 web용으로 동일 적용
                                        "webUrl": "https://www.melon.com/song/detail.htm?songId=" + songInfo_Go[0]
                                        # 정보 링크 url
                                    }
                                },
                                {
                                    "type": "item",
                                    "imageUrl": imgSrcRank[1],
                                    "title": "2등 " + ChartRankInfo[1],  # i=0부터 1등 정보 매겨짐
                                    "linkUrl": {
                                        "type": "OS",  # PC나 모바일별 별도 url설정 가능하나 web용으로 동일 적용
                                        "webUrl": "https://www.melon.com/song/detail.htm?songId=" + songInfo_Go[1]
                                        # 정보 링크 url
                                    }
                                },
                                {
                                    "type": "item",
                                    "imageUrl": imgSrcRank[2],
                                    "title": "3등 " + ChartRankInfo[2],  # i=0부터 1등 정보 매겨짐
                                    "linkUrl": {
                                        "type": "OS",  # PC나 모바일별 별도 url설정 가능하나 web용으로 동일 적용
                                        "webUrl": "https://www.melon.com/song/detail.htm?songId=" + songInfo_Go[2]
                                        # 정보 링크 url
                                    }
                                },
                                {
                                    "type": "item",
                                    "imageUrl": imgSrcRank[3],
                                    "title": "4등 " + ChartRankInfo[3],  # i=0부터 1등 정보 매겨짐
                                    "linkUrl": {
                                        "type": "OS",  # PC나 모바일별 별도 url설정 가능하나 web용으로 동일 적용
                                        "webUrl": "https://www.melon.com/song/detail.htm?songId=" + songInfo_Go[3]
                                        # 정보 링크 url
                                    }
                                },
                                {
                                    "type": "item",
                                    "imageUrl": imgSrcRank[4],
                                    "title": "5등 " + ChartRankInfo[4],  # i=0부터 1등 정보 매겨짐
                                    "linkUrl": {
                                        "type": "OS",  # PC나 모바일별 별도 url설정 가능하나 web용으로 동일 적용
                                        "webUrl": "https://www.melon.com/song/detail.htm?songId=" + songInfo_Go[4]
                                        # 정보 링크 url
                                    }
                                }
                            ]
                        }
                    ]
                }
            ]
        }

    if '일간' in input_text:
        RANK = 5  ## 멜론 차트 순위 1 ~ 5위까지

        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
        req = requests.get('https://www.melon.com/chart/day/index.htm', headers=header)  ## 일간 차트를 크롤링 할 것임

        html = req.text
        parse = BeautifulSoup(html, 'html.parser')

        titles = parse.find_all("div", {"class": "ellipsis rank01"})
        singers = parse.find_all("div", {"class": "ellipsis rank02"})
        img_urls = parse.select('tr#lst50')
        songInfo_urls = parse.select('tr#lst50')

        title = []
        singer = []

        img_url = []
        imgSrcRank = []

        songInfo = []
        songInfo_Go = []

        ChartRankInfo = []

        for t in titles:
            title.append(t.find('a').text)

        for s in singers:
            singer.append(s.find('span', {"class": "checkEllipsis"}).text)

        for im in img_urls:
            img = im.select_one('div.wrap > a > img')
            imgSrc = img.attrs["src"]
            imgSrcRank.append(imgSrc)

        for si in songInfo_urls:
            songi = si.select_one('div.wrap.t_right > input')
            songin = songi.attrs["value"]
            songInfo_Go.append(songin)

        for i in range(RANK):
            ChartRankInfo.append(title[i] + "\n" + singer[i])

        res = {
            "contents": [
                {
                    "type": "card.list",
                    "cards": [
                        {
                            "listItems": [
                                {
                                    "type": "title",
                                    "title": "일간 인기차트",
                                    "linkUrl": {
                                        "type": "OS",  # PC나 모바일별 별도 url설정 가능하나 web용으로 동일 적용
                                        "webUrl": "https://www.melon.com/chart/day/index.htm"  # 정보 링크 url
                                    }
                                },
                                {
                                    "type": "item",
                                    "imageUrl": imgSrcRank[0],
                                    "title": "1등 " + ChartRankInfo[0],  # i=0부터 1등 정보 매겨짐
                                    "linkUrl": {
                                        "type": "OS",  # PC나 모바일별 별도 url설정 가능하나 web용으로 동일 적용
                                        "webUrl": "https://www.melon.com/song/detail.htm?songId=" + songInfo_Go[0]
                                        # 정보 링크 url
                                    }
                                },
                                {
                                    "type": "item",
                                    "imageUrl": imgSrcRank[1],
                                    "title": "2등 " + ChartRankInfo[1],  # i=0부터 1등 정보 매겨짐
                                    "linkUrl": {
                                        "type": "OS",  # PC나 모바일별 별도 url설정 가능하나 web용으로 동일 적용
                                        "webUrl": "https://www.melon.com/song/detail.htm?songId=" + songInfo_Go[1]
                                        # 정보 링크 url
                                    }
                                },
                                {
                                    "type": "item",
                                    "imageUrl": imgSrcRank[2],
                                    "title": "3등 " + ChartRankInfo[2],  # i=0부터 1등 정보 매겨짐
                                    "linkUrl": {
                                        "type": "OS",  # PC나 모바일별 별도 url설정 가능하나 web용으로 동일 적용
                                        "webUrl": "https://www.melon.com/song/detail.htm?songId=" + songInfo_Go[2]
                                        # 정보 링크 url
                                    }
                                },
                                {
                                    "type": "item",
                                    "imageUrl": imgSrcRank[3],
                                    "title": "4등 " + ChartRankInfo[3],  # i=0부터 1등 정보 매겨짐
                                    "linkUrl": {
                                        "type": "OS",  # PC나 모바일별 별도 url설정 가능하나 web용으로 동일 적용
                                        "webUrl": "https://www.melon.com/song/detail.htm?songId=" + songInfo_Go[3]
                                        # 정보 링크 url
                                    }
                                },
                                {
                                    "type": "item",
                                    "imageUrl": imgSrcRank[4],
                                    "title": "5등 " + ChartRankInfo[4],  # i=0부터 1등 정보 매겨짐
                                    "linkUrl": {
                                        "type": "OS",  # PC나 모바일별 별도 url설정 가능하나 web용으로 동일 적용
                                        "webUrl": "https://www.melon.com/song/detail.htm?songId=" + songInfo_Go[4]
                                        # 정보 링크 url
                                    }
                                }
                            ]
                        }
                    ]
                }
            ]
        }

    if '주간' in input_text:
        RANK = 5  ## 멜론 차트 순위 1 ~ 5위까지

        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
        req = requests.get('https://www.melon.com/chart/week/index.htm', headers=header)  ## 주간 차트를 크롤링 할 것임

        html = req.text
        parse = BeautifulSoup(html, 'html.parser')

        titles = parse.find_all("div", {"class": "ellipsis rank01"})
        singers = parse.find_all("div", {"class": "ellipsis rank02"})
        img_urls = parse.select('tr#lst50')
        songInfo_urls = parse.select('tr#lst50')

        title = []
        singer = []

        img_url = []
        imgSrcRank = []

        songInfo = []
        songInfo_Go = []

        ChartRankInfo = []

        for t in titles:
            title.append(t.find('a').text)

        for s in singers:
            singer.append(s.find('span', {"class": "checkEllipsis"}).text)

        for im in img_urls:
            img = im.select_one('div.wrap > a > img')
            imgSrc = img.attrs["src"]
            imgSrcRank.append(imgSrc)

        for si in songInfo_urls:
            songi = si.select_one('div.wrap.t_right > input')
            songin = songi.attrs["value"]
            songInfo_Go.append(songin)

        for i in range(RANK):
            ChartRankInfo.append(title[i] + "\n" + singer[i])

        res = {
            "contents": [
                {
                    "type": "card.list",
                    "cards": [
                        {
                            "listItems": [
                                {
                                    "type": "title",
                                    "title": "주간 인기차트",
                                    "linkUrl": {
                                        "type": "OS",  # PC나 모바일별 별도 url설정 가능하나 web용으로 동일 적용
                                        "webUrl": "https://www.melon.com/chart/week/index.htm"  # 정보 링크 url
                                    }
                                },
                                {
                                    "type": "item",
                                    "imageUrl": imgSrcRank[0],
                                    "title": "1등 " + ChartRankInfo[0],  # i=0부터 1등 정보 매겨짐
                                    "linkUrl": {
                                        "type": "OS",  # PC나 모바일별 별도 url설정 가능하나 web용으로 동일 적용
                                        "webUrl": "https://www.melon.com/song/detail.htm?songId=" + songInfo_Go[0]
                                        # 정보 링크 url
                                    }
                                },
                                {
                                    "type": "item",
                                    "imageUrl": imgSrcRank[1],
                                    "title": "2등 " + ChartRankInfo[1],  # i=0부터 1등 정보 매겨짐
                                    "linkUrl": {
                                        "type": "OS",  # PC나 모바일별 별도 url설정 가능하나 web용으로 동일 적용
                                        "webUrl": "https://www.melon.com/song/detail.htm?songId=" + songInfo_Go[1]
                                        # 정보 링크 url
                                    }
                                },
                                {
                                    "type": "item",
                                    "imageUrl": imgSrcRank[2],
                                    "title": "3등 " + ChartRankInfo[2],  # i=0부터 1등 정보 매겨짐
                                    "linkUrl": {
                                        "type": "OS",  # PC나 모바일별 별도 url설정 가능하나 web용으로 동일 적용
                                        "webUrl": "https://www.melon.com/song/detail.htm?songId=" + songInfo_Go[2]
                                        # 정보 링크 url
                                    }
                                },
                                {
                                    "type": "item",
                                    "imageUrl": imgSrcRank[3],
                                    "title": "4등 " + ChartRankInfo[3],  # i=0부터 1등 정보 매겨짐
                                    "linkUrl": {
                                        "type": "OS",  # PC나 모바일별 별도 url설정 가능하나 web용으로 동일 적용
                                        "webUrl": "https://www.melon.com/song/detail.htm?songId=" + songInfo_Go[3]
                                        # 정보 링크 url
                                    }
                                },
                                {
                                    "type": "item",
                                    "imageUrl": imgSrcRank[4],
                                    "title": "5등 " + ChartRankInfo[4],  # i=0부터 1등 정보 매겨짐
                                    "linkUrl": {
                                        "type": "OS",  # PC나 모바일별 별도 url설정 가능하나 web용으로 동일 적용
                                        "webUrl": "https://www.melon.com/song/detail.htm?songId=" + songInfo_Go[4]
                                        # 정보 링크 url
                                    }
                                }
                            ]
                        }
                    ]
                }
            ]
        }

    return jsonify(res)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)