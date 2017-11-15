# -*- coding: utf-8 -*-

import sys, os
import requests
import pickle
from utils import dump
from HTMLParser import HTMLParser
from wechatprotocol.exceptions import WechatProtocolException, ErrorCode
from wechatprotocol.headers import WechatHeaders

class Request:

    def __init__(self):
        self.directory = os.path.abspath(os.getcwd())
        self.cookiePklfileName = "{dir}/cookie.pkl".format(dir = self.directory)

        self.session = requests.Session()
        self.htmlParser = HTMLParser()
        self.headers = WechatHeaders.common()
        self.timeout = 30

    def loadCookies(self):
        if not os.path.exists(self.cookiePklfileName):
            return
        with open(self.cookiePklfileName, 'r') as fp:
            requests.utils.add_dict_to_cookiejar(self.session.cookies, pickle.load(fp))

    def saveCookies(self):
        with open(self.cookiePklfileName, 'w') as fp:
            pickle.dump(self.session.cookies, fp, protocol = 2)

    def setHeaders(self, headers):
        if not isinstance(headers, dict):
            raise WechatProtocolException(ErrorCode.CallingArgumentError)
        self.headers = headers

    def setTimeOut(self, timeout):
        if not isinstance(timeout, int):
            raise WechatProtocolException(ErrorCode.CallingArgumentError)
        self.timeout = timeout


    def doNetworkGet(self, url):
        if not isinstance(url, (str, unicode)):
            raise WechatProtocolException(ErrorCode.CallingArgumentError)
        dump("Request GET URL:" + url, "INFOR")
        r = self.session.get(url, headers = self.headers, timeout = self.timeout)
        r.encoding = 'utf-8'
        return r

    def doNetworkPost(self, url, postData):
        if not (isinstance(url, (str, unicode)) and isinstance(postData, (str, unicode, dict))):
            raise WechatProtocolException(ErrorCode.CallingArgumentError)
        dump("Request POST URL:" + url, "INFOR")
        dump(postData, "INFOR")
        # if isinstance(postData, dict):
        #     return self.session.post(url, headers = self.headers, timeout = self.timeout, params = postData)
        # elif isinstance(postData, str):
        #     return self.session.post(url, headers = self.headers, timeout = self.timeout, data = postData)
        r = self.session.post(url, headers = self.headers, timeout = self.timeout, data = postData)
        r.encoding = 'utf-8'
        return r

