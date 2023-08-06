
import requests
from gpt_muti_gen import api
import json
import uuid

class ChatGPT(object):

    def __init__(self,  apiKey: str):
        self.apiKey = apiKey

    def getAnswer_turbo(self, title: str):
        '''通过接口返回'''
        param = {
            "apiKey": self.apiKey,
            "sessionId":  str(uuid.uuid1()),
            "content": title
        }
        headers = {
            "Content-Type": "application/json"
        }
        res = None
        try:
            resp = json.loads(requests.post(
                api.getAnswer_turbo, data=json.dumps(param, ensure_ascii=False).encode("utf-8"), headers=headers).text)
            print(resp)
            if resp["code"] == 200:
                res = resp["data"]
        except Exception as e:
            print(e)
        return res

    def getAnswer(self, title: str) -> str:
        '''通过接口返回'''

        param = {
            "token": self.apiKey,
            "word": title
        }
        res = None
        try:
            resp = json.loads(requests.get(api.getAnswer, params=param).text)
            if resp["code"] == 0:
                res = resp["result"]
        except Exception as e:
            pass
        return res

    def answer(self, title: str):
        ''' 根据title 调用 gpt 回答问题 '''
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.apiKey
        }
        response = requests.post(
            'https://api.openai.com/v1/completions', headers=headers, json=title)
        return response.json()['choices'][0]['text'].strip()


if __name__ == "__main__":
    pass
