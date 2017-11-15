# -*- coding: utf-8 -*-

import re as regex
import xml.dom.minidom as minidom
import json
from wechatprotocol.exceptions import WechatProtocolException, ErrorCode
from utils import dump

class Protocol:

    @staticmethod
    def resolve_jslogin(data):
        if not (isinstance(data, (str, unicode))):
            raise WechatProtocolException(ErrorCode.ResolveJsLoginError_dataIsEmpty)
        reg = r'window.QRLogin.code = (\d+); window.QRLogin.(\S+?) = "(\S+?)"'
        pm = regex.search(reg, data)
        if pm:
            code = pm.group(1)
            item = pm.group(2)
            uuid = pm.group(3)
        else:
            raise WechatProtocolException(ErrorCode.ResolveJsLoginError, {'data': data})
        return [code, item, uuid]

    @staticmethod
    def resolve_login(data):
        if not (isinstance(data, (str, unicode))):
            raise WechatProtocolException(ErrorCode.ResolveLoginError_dataIsEmpty)
        param = regex.search(r'window.code=(\d+);', data)
        retCode = param.group(1)
        redirectUri = ""
        if retCode == "201":
            return [retCode, redirectUri]
        elif retCode == "200":
            redirectUri = regex.search(r'\"(?P<redirect_url>.*)\"', data)
            redirectUri = redirectUri.group('redirect_url')
            if redirectUri:
                return [retCode, redirectUri]
            else:
                raise WechatProtocolException(ErrorCode.ResolveLoginError, {'data': data})
        elif retCode == "400":
            # 400 means error.
            return [retCode, redirectUri]
        elif retCode == "408":
            # 408 means the login is out of time, need to retry.
            return [retCode, redirectUri]
        else:
            raise WechatProtocolException(ErrorCode.ResolveLoginError, {'data': data})

    @staticmethod
    def resolve_webwxnewloginpage(data):
        if not (isinstance(data, (str, unicode))):
            raise WechatProtocolException(ErrorCode.ResolveWebnewloginpageError_dataIsEmpty)
        doc = minidom.parseString(data)
        root = doc.documentElement

        skey = ""
        sid = ""
        uin = ""
        pass_ticket = ""
        isgrayscale = ""

        for node in root.childNodes:
            if node.nodeName == "skey":
                skey = node.childNodes[0].data
            elif node.nodeName == "wxsid":
                sid = node.childNodes[0].data
            elif node.nodeName == "wxuin":
                uin = node.childNodes[0].data
            elif node.nodeName == "pass_ticket":
                pass_ticket = node.childNodes[0].data
            elif node.nodeName == "isgrayscale":
                isgrayscale = node.childNodes[0].data
        if all([skey, sid, uin, pass_ticket]):
            return [skey, sid, uin, pass_ticket, isgrayscale]
        else:
            raise WechatProtocolException(ErrorCode.ResolveWebnewloginpageError, {'data': data})

    @staticmethod
    def resolve_webwxinit(data):
        if not (isinstance(data, (str, unicode))):
            raise WechatProtocolException(ErrorCode.ResolveWebwxinitError_dataIsEmpty)
        r = json.loads(data)
        if not r:
            raise WechatProtocolException(ErrorCode.ResolveWebwxinitError, {'data', data})
        else:
            return r

    @staticmethod
    def resolve_webwxstatusnotify(data):
        if not (isinstance(data, (str, unicode))):
            raise WechatProtocolException(ErrorCode.ResolveWebwxstatusnotifyError_dataIsEmpty)
        r = json.loads(data)
        if not r:
            raise WechatProtocolException(ErrorCode.ResolveWebwxstatusnotifyError, {'data': data})
        else:
            return r

    @staticmethod
    def resolve_webwxgetcontact(data):
        if not (isinstance(data, (str, unicode))):
            raise WechatProtocolException(ErrorCode.ResolveWebwxgetcontactError_dataIsEmpty)
        r = json.loads(data)
        if not r:
            raise WechatProtocolException(ErrorCode.ResolveWebwxgetcontactError, {'data': data})
        else:
            return r

    @staticmethod
    def resolve_webwxgetbatchcontact(data):
        if not (isinstance(data, (str, unicode))):
            raise WechatProtocolException(ErrorCode.ResolveWebwxbatchgetcontactError_dataIsEmpty)
        r = json.loads(data)
        if not r:
            raise WechatProtocolException(ErrorCode.ResolveWebwxbatchgetcontactError, {'data': data})
        else:
            return r

    @staticmethod
    def resolve_synccheck(data):
        if not (isinstance(data, (str, unicode))):
            raise WechatProtocolException(ErrorCode.ResolveSynccheckError_dataIsEmpty)
        reg = r'window.synccheck=\{retcode:"(\d+)",selector:"(\d+)"\}'
        pm = regex.search(reg, data)
        if pm == None:
            raise WechatProtocolException(ErrorCode.ResolveSynccheckError, {'data': data})
        retcode = pm.group(1)
        selector = pm.group(2)
        if retcode == None or selector == None:
            raise WechatProtocolException(ErrorCode.ResolveSynccheckError, {'data': data})
        return [retcode, selector]

    @staticmethod
    def resolve_webwxsync(data):
        if not (isinstance(data, (str, unicode))):
            raise WechatProtocolException(ErrorCode.ResolveWebwxsyncError_dataIsEmpty)
        r = json.loads(data)
        if not r:
            raise WechatProtocolException(ErrorCode.ResolveWebwxsyncError, {'data': data})
        else:
            return r

    @staticmethod
    def resolve_webwxpushloginurl(data):
        if not (isinstance(data, (str, unicode))):
            raise WechatProtocolException(ErrorCode.ResolveWebwxpushloginurlError_dataIsEmpty)
        r = json.loads(data)
        if not r:
            raise WechatProtocolException(ErrorCode.ResolveWebwxpushloginurlError, {'data': data})
        else:
            return r


