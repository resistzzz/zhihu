import requests
import time
from bs4 import BeautifulSoup
from PIL import Image
import sys
import os

class zhihuSpider(object):
    def __init__(self):
        self.headers = {
            'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
            'Host': 'www.zhihu.com',
            'Referer': 'https://www.zhihu.com/'
        }
        self.homePageUrl = 'https://www.zhihu.com/'
        self.captcha_url = self.homePageUrl + 'captcha.gif?r=' + str(int(time.time() * 1000)) + '&type=login&lang=en'
        self.session = requests.session()

    def login(self):
        try:
            xsrf_str = self._getxsrf()

            captcha = self._getCaptcha()

            data = {
                'phone_num': '18287108118',
                'password': 'zzz970504',
                'captcha_type': 'en',
                'captcha': captcha,
                '_xsrf': xsrf_str
            }

            signin = self.session.post('https://www.zhihu.com/login/phone_num', headers=self.headers, data=data)
            print(signin.json()['msg'])
        except:
            print('login failed!:(')
            sys.exit(-1)


    def _getxsrf(self):
        try:
            html_xsrf = self.session.get(self.homePageUrl, headers=self.headers)
            html_xsrf.raise_for_status()
            html_xsrf.encoding = html_xsrf.apparent_encoding
            soup_xsrf = BeautifulSoup(html_xsrf.text, "html.parser")
            xsrf = soup_xsrf.find('input', attrs={'name': '_xsrf'})
            xsrf_str = xsrf.get('value')
            return  xsrf_str
        except:
            print('get xsrf failed!:(')
            return ""

    def _getCaptcha(self):
        try:
            captcha_gif = self.session.get(self.captcha_url, headers=self.headers)
            captcha_gif.raise_for_status()
            with open('captcha.gif', 'wb') as f:
                f.write(captcha_gif.content)
            '''Auto recognize captcha
            # status = os.system('tesseract captcha.gif result')
            # with open('result.txt', 'r') as f:
            #     captcha = f.read()
            # captcha = captcha[0:4]
            # print(captcha)
            '''
            img = Image.open('captcha.gif')
            img.show()
            captcha = input('Please input captcha:')
            time.sleep(3)

            return captcha
        except:
            print('get captcha failed!:(')
            return ""




if __name__ == '__main__':
    spider = zhihuSpider()
    spider.login()