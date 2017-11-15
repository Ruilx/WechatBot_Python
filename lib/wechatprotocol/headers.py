# -*- coding: utf-8 -*-

class WechatHeaders:

    @staticmethod
    def login():
        return {
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "zh-CN,zh;q=0.8",
            'cache-control': "max-age=0",
            'host': "login.wx.qq.com",
            'content-type': "application/json; charset=UTF-8",
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"
        }

    @staticmethod
    def common():
        return {
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "zh-CN,zh;q=0.8",
            'cache-control': "max-age=0",
            'host': "wx2.qq.com",
            'referer': "https://wx2.qq.com/",
            'content-type': "application/json; charset=UTF-8",
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"
        }

    @staticmethod
    def message():
        return {
            'accept': "application/json, text/plain, */*",
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "zh-CN,zh;q=0.8",
            'cache-control': "max-age=0",
            'host': "wx2.qq.com",
            'referer': "https://wx2.qq.com/",
            'content-type': "application/json; charset=UTF-8",
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"
        }

    @staticmethod
    def contact():
        return {
            'accept': "application/json, text/plain, */*",
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "zh-CN,zh;q=0.8",
            'cache-control': "max-age=0",
            'host': "wx2.qq.com",
            'referer': "https://wx2.qq.com/",
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"
        }