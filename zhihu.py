import requests
import time
from bs4 import BeautifulSoup
from PIL import Image
import os

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
        #print(html_xsrf.status_code)
        html_xsrf.encoding = html_xsrf.apparent_encoding

        soup_xsrf = BeautifulSoup(html_xsrf.text, "html.parser")
        xsrf = soup_xsrf.find('input', attrs={'name': '_xsrf'})
        xsrf_str = xsrf.get('value')

        captcha_url = "https://www.zhihu.com/captcha.gif?r=" + str(int(time.time()*1000)) + '&type=login&lang=en'
        captcha_gif = s.get(captcha_url, headers=headers)
        with open('captcha.gif', 'wb') as f:
            f.write(captcha_gif.content)
        # status = os.system('tesseract captcha.gif result')
        # with open('result.txt', 'r') as f:
        #     captcha = f.read()
        # captcha = captcha[0:4]
        # print(captcha)
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

        r = s.get('https://www.zhihu.com/api/v4/search_v3?t=general&q=%E8%B6%B3%E7%90%83&correction=1&search_hash_id=1304261d7600201178c6bed4d899d973&offset=21&limit=10', headers=headers)
        print(r.json())

        # myHomePage = s.get('https://www.zhihu.com/people/resistzyx', headers=headers)
        # print(myHomePage.text)


    def getHtml(self, url):
        try:
            html = requests.get(url, headers=headers, timeout=40)
            html.raise_for_status()
            html.encoding = html.apparent_encoding
            return html.text
        except:
            print('Sorry for zhihu spider failed! :(')
            return ""

    def getQuestionUrl(self, html):
        # html_print = html
        # print(html_print)
        soup = BeautifulSoup(html, 'html.parser')
        QueUrl = soup.find_all('a', attrs={'target': '_blank'})
        # len(QueUrl)
        # print(QueUrl)
        return QueUrl

    def addList(self, QueUrl, href_List):
        for i in range(len(QueUrl)):
            href_List = href_List.append(QueUrl[i])
        return href_List


def main():
    spider = zhihu('https://www.zhihu.com/')
    spider.login()
    topic = '足球'
    start_url = 'https://www.zhihu.com/search?type=content&q=' + topic
    href_List = []
    depth = 5
    offset = []
    for i in range(depth):
        if i == 0:
            offset.insert(0, 0)
        elif i == 1:
            offset.insert(1, 8)
        else:
            offset.insert(i, offset[i-1]+13)
    print(offset)
    # for i in range(depth):
    #     try:
    #         next_url = start_url + '&offset=' + str(offset[i]) + '&limit=10'
    #         html = zhihu.getHtml(next_url)
    #         QueUrl = zhihu.getQuestionUrl(html)
    #         href_List = zhihu.addList(QueUrl, href_List)
    #     except:
    #         continue
    # print(href_List)

    # html = spider.getHtml(start_url)
    # spider.getQuestionUrl(html)

if __name__ == '__main__':
    main()

