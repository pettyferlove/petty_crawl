from crawl.common.http.Setting import IP, UA
import requests, random
from urllib import parse
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s Process%(process)d:%(thread)d %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='../../logs/http_utils.log',
                    filemode='a')


class Http:

    def __init__(self, url, headers=None, cookies=None, proxy=None, time_out=5, time_out_retry=5):
        """
        构造函数
        :param url: 请求URL
        :param headers: 请求头
        :param cookies: 请求Cookies
        :param proxy: Http代理
        :param time_out: 超时时间（默认5秒）
        :param time_out_retry: 请求超时重试次数
        """
        self.url = url
        self.headers = headers
        self.cookies = cookies
        self.proxy = proxy
        self.timeOut = time_out
        self.timeOutRetry = time_out_retry
        pass

    def get(self, params):
        """
        Get请求
        :param params: 请求参数
        :return: 响应结果
        """
        if not self.url:
            logging.error('GetError url not exit')
            return 'None'
        logging.info('Get %s' % self.url)
        try:
            params = parse.urlencode(params)
            if not self.headers: self.headers = {'User-Agent': UA[random.randint(0, len(UA) - 1)]}
            if not self.proxy: self.proxy = {'http': "http://" + IP[random.randint(0, len(IP) - 1)]}
            response = requests.get(self.url, params, headers=self.headers, cookies=self.cookies, proxies=self.proxy,
                                    timeout=self.timeOut)
            if response.status_code == 200 or response.status_code == 302:
                html_context = response.text
            else:
                html_context = 'None'
            logging.info('Get %s %s' % (str(response.status_code), self.url))
        except Exception as e:
            logging.error('GetExcept %s' % str(e))
            if self.timeOutRetry > 0:
                response = requests.get(self.url, params, headers=self.headers, cookies=self.cookies,
                                        proxies=self.proxy, timeout=self.timeOut)
                self.timeOutRetry = self.timeOutRetry - 1
                html_context = response.text
            else:
                logging.error('GetTimeOut %s' % self.url)
                html_context = 'None'
        return html_context

    def post(self, params):
        """
        Post请求
        :param params: JSON参数
        :return: 响应结果
        """
        if not self.url or not params:
            logging.error('PostError url or para not exit')
            return None
        logging.info('Post %s' % self.url)
        try:
            if not self.headers: self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3'}
            if not self.proxy: self.proxy = {'http': "http://" + IP[random.randint(0, len(IP) - 1)]}
            response = requests.post(self.url, data=params, headers=self.headers, cookies=self.cookies,
                                     proxies=self.proxy, timeout=self.timeOut)
            if response.status_code == 200 or response.status_code == 302:
                html_context = response.text
            else:
                html_context = None
            logging.info('Post %s %s' % (str(response.status_code), self.url))
        except Exception as e:
            logging.error('PostExcept %s' % str(e))
            if self.timeOutRetry > 0:
                response = requests.post(self.url, params, headers=self.headers, cookies=self.cookies,
                                         proxies=self.proxy, timeout=self.timeOut)
                self.timeOutRetry = self.timeOutRetry - 1
                html_context = response.text
            else:
                logging.error('PostTimeOut %s' % self.url)
                html_context = 'None'
        return html_context
