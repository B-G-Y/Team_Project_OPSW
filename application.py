# flask�� ���
from flask import Flask, request, jsonify
# crawling�� ���
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from selenium import webdriver

import requests
import urllib
import json

app = Flask(__name__)

######################################################################
#���� ����
######################################################################
class issue():
    session = requests.Session()
    url = "https://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1="       # naver news url
    map_categoryNum = {                                                       # ���� �帣�� ����
        '��ġ': "100", '����': "101", '��ȸ': "102", '��Ȱ/��ȭ': "103", '��Ȱ': "103", '��ȭ': "103", '����': "104",
        'IT/����': "105", 'IT': "105", '����': "105"
    }
    map_categoryKey = {                                                       # �帣�� ������ �ҽ� Ŭ���� ���̰� ����
        '��ġ': "cluster_text_headline nclicks(cls_pol.clsart)", '����': "cluster_text_headline nclicks(cls_eco.clsart)",
        '��ȸ': "cluster_text_headline nclicks(cls_nav.clsart)", '��Ȱ/��ȭ': "cluster_text_headline nclicks(cls_lif.clsart)",
        '��Ȱ': "cluster_text_headline nclicks(cls_lif.clsart)", '��ȭ': "cluster_text_headline nclicks(cls_lif.clsart)",
        '����': "cluster_text_headline nclicks(cls_wor.clsart)", 'IT/����': "cluster_text_headline nclicks(cls_sci.clsart)",
        'IT': "cluster_text_headline nclicks(cls_sci.clsart)", '����': "cluster_text_headline nclicks(cls_sci.clsart)"
    }

    def __init__(self, cate='��ġ'):           # �帣 �Է°��� ���ٸ� default category = ��ġ
        self.cate = cate
        self.url = None
        self.categoryKey = None
        self.result = None

        categoryNum = issue.map_categoryNum[cate]
        if not categoryNum:                 # ���� ���� ��
            print("�߸��� �帣 ����")
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
#���� ��

#�ڷγ� ���� 
######################################################################





@app.route('/news', methods=['POST'])  # ���� ���� ���� ��ų�� ����� ���
def news():
    req = request.get_json()
    
    input_text = req['userRequest']['utterance'] # ����ڰ� ������ ���� �޽���
    
    if '����' in input_text: # ���� �޽����� "����"�� ���� ���� ���� ���� ������ ����
        res = {
        "contents": [
            {
                "type": "text",
                "text": issue('����').getIssue()
            }
        ]
    }
    elif '����'in input_text: # ���� �޽����� "����"�� ���� ���� ���� ���� ������ ����
        res = {
        "contents": [
            {
                "type": "text",
                "text": issue('����').getIssue()
            }
        ]
    }
    elif '��Ȱ' in input_text: # ���� �޽����� "��Ȱ"�� ���� ���� ��Ȱ ���� ������ ����
        res = {
        "contents": [
            {
                "type": "text",
                "text": issue('��Ȱ').getIssue()
            }
        ]
    }
    
    # ����
    return jsonify(res)



# ���� �Լ�
if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, debug = True, threaded=True)
