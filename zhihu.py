import requests
import time
from bs4 import BeautifulSoup
from PIL import Image

headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
    'Host': 'www.zhihu.com',
    'Referer': 'https://www.zhihu.com/'
}

class zhihu(object):
    '''
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
        'Host': 'www.zhihu.com',
        'Referer': 'https://www.zhihu.com/'
    }
    '''

    def __init__(self, url):
        self.url = url

    def login(self):
        s = requests.session()
        html_xsrf = s.get('https://www.zhihu.com/', headers=headers)
        html_xsrf.raise_for_status()
        print(html_xsrf.status_code)
        html_xsrf.encoding = html_xsrf.apparent_encoding

        soup_xsrf = BeautifulSoup(html_xsrf.text, "html.parser")
        xsrf = soup_xsrf.find('input', attrs={'name': '_xsrf'})
        xsrf_str = xsrf.get('value')

        captcha_url = "https://www.zhihu.com/captcha.gif?r=" + str(int(time.time()*1000)) + '&type=login&lang=en'
        captcha_gif = s.get(captcha_url, headers=headers)
        with open('captcha.gif', 'wb') as f:
            f.write(captcha_gif.content)
        img = Image.open('captcha.gif')
        img.show()
        captcha = input('Please input captcha:')
        time.sleep(3)

        data = {
            'phone_num': '18287108118',
            'password': 'zzz970504',
            'captcha_type': 'en',
            'captcha': captcha,
            '_xsrf': xsrf_str
        }

        signin = s.post('https://www.zhihu.com/login/phone_num', headers=headers, data=data)
        print(signin.json()['msg'])
    '''
        myHomePage = s.get('https://www.zhihu.com/people/resistzyx', headers=headers)
        print(myHomePage.text)
    '''

    def getHtml(self, url):
        pass

    def findUrl(self, html):
        pass


if __name__ == '__main__':
    pachong = zhihu('https://www.zhihu.com/')
    pachong.login()

