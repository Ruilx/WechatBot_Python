# -*- encoding: utf-8 -*-

###       ###                ###             ###    #######b.                ###                           ###
###   o   ###                ###             ###    ###   Y##b               ###                           ###
###  d#b  ###                ###             ###    ###    ###               ###                           ###
### d###b ### .d##b.  .d####b#####b.  ####b. ###### ###   d##P###d### .d##b. ###### .d##b.  .d####b .d##b. ###
###d#####b###d#P  Y#bd##P"   ### "##b    "##b###    #######P" ###P"  d##""##b###   d##""##bd##P"   d##""##b###
#####P Y################     ###  ###.d#########    ###       ###    ###  ######   ###  ######     ###  ######
####P   Y####Y#b.    Y##b.   ###  ######  ###Y##b.  ###       ###    Y##..##PY##b. Y##..##PY##b.   Y##..##P###
###P     Y### "Y####  "Y####P###  ###"Y###### "Y### ###       ###     "Y##P"  "Y### "Y##P"  "Y####P "Y##P" ###

"""
Wechat Protocol Class

Made by Ruilx
"""

import sys, json

from wechatprotocol.protocol import Protocol
from wechatprotocol.makeup import Makeup
from wechatprotocol.contact import Contact
from wechatprotocol.request import Request
from wechatprotocol.headers import WechatHeaders
from wechatprotocol.urls import WechatUrl
from wechatprotocol.exceptions import WechatProtocolException, ErrorCode
import wechatprotocol.utils
from wechatprotocol.utils import dump
from wechatprotocol.params import Params
from qrcode import QRCode
from threading import Timer as basicTimer

from requests import ConnectionError
import time

__title__ = 'wechatprotocol'
__version__ = '0.1.0'
__build__ = 0x000100
__author__ = 'Ruilx'
__license__ = 'GNU v3'
__copyright__ = 'Copyright 2017 GT-Soft Studio'


class Wechat:
    def __init__(self, pipe):
        self.params = Params()
        self.request = Request()
        self.contact = Contact()
        self.pipe = pipe
        self.params.setDeviceId('e' + utils.rand(15))
        self.myUserName = ""
        self.timer = basicTimer(1, self.timerEvent)

        self.failedTimes = 0
        self.failedTimes_TimerEvent = 0
        self.syncCount = 0L

        self.forceToExit = False

    def timerEvent(self):
        self.failedTimes_TimerEvent = 0
        if self.sync() == False:
            if self.forceToExit:
                dump("sync failed, fatal error exit.", "FATAL")
                self.request.saveCookies()
                raise WechatProtocolException(ErrorCode.ForceToExit)
            else:
                if self.failedTimes_TimerEvent < 10:
                    dump("sync failed, but still has retry chance.", "ERROR")
                else:
                    dump("sync failed, no more retry chance.", "FATAL")
                    self.request.saveCookies()
                    self.forceToExit = True
                    raise WechatProtocolException(ErrorCode.ForceToExit)
        else:
            dump("Get sync. Normal state returned.", "INFOR")
        self.params.saveParams()
        self.syncCount += 1
        return True

    def getQrCode(self):
        dump("====================getQrCode====================")
        self.request.setHeaders(WechatHeaders.common())
        response = self.request.doNetworkGet(WechatUrl.jsLogin(utils.now()))
        dump(response.text)
        code, item, uuid = Protocol.resolve_jslogin(response.text)
        print code, item, uuid
        if code != "200" and code != 200:
            raise WechatProtocolException(ErrorCode.LoginQrlogincodeFailed, {'data': code})
        self.params.setUuid(uuid)

        qrContent = WechatUrl.l(uuid)

        qr = QRCode()
        qr.add_data(qrContent)
        qr.error_correction = 1
        qr.print_c()
        dump("********************getQrCode********************")

    def init(self):
        dump("====================init====================")
        url = WechatUrl.webwxinit(self.params.getBaseUri(), utils.now(), self.params.getPassTicket())
        params = {
            "BaseRequest": self.params.getBaseRequest()
        }
        requestJson = json.dumps(params)
        self.request.setHeaders(WechatHeaders.login())
        response = self.request.doNetworkPost(url, requestJson)
        res = Protocol.resolve_webwxinit(response.text)
        if res['BaseResponse']['Ret'] != 0:
            raise WechatProtocolException(ErrorCode.InitFailed, {'data': response.text})
        self.params.setSyncKey(res['SyncKey']['List'])

        for mem in res['ContactList']:
            self.contact.addContact(mem)

        self.contact.addContact(res['User'])
        self.myUserName = res['User']['UserName']
        return True


    def login(self, usingSnapshot):
        dump("====================login====================")
        if usingSnapshot:
            self.params.loadParams()
        else:
            if not all((self.params.getUin(), self.params.getBaseUri())):
                self.getQrCode()
            else:
                self.request.loadCookies()
                self.request.setHeaders(WechatHeaders.common())
                response = self.request.doNetworkGet(WechatUrl.webwxpushloginurl(self.params.getBaseUri(), self.params.getUin()))

                res = Protocol.resolve_webwxpushloginurl(response.text)
                if res['ret'] != 0:
                    self.params.resetUin()
                    return False
                if not all((res['uuid'], )):
                    self.params.resetUin()
                    return False
                self.params.setUuid(res['uuid'])

        if not self.params.getUuid():
            return False

        redirectUrl = ''
        tip = 1

        while not all((redirectUrl, )):
            url = WechatUrl.login(tip, self.params.getUuid(), utils.now())
            self.request.setHeaders(WechatHeaders.login())
            response = self.request.doNetworkGet(url)
            retCode, redirectUri = Protocol.resolve_login(response.text)
            if retCode == 0 or retCode == "0":
                raise WechatProtocolException(ErrorCode.LoginRetcodeFailed, {'data': retCode})
            elif retCode == 201 or retCode == "201":
                tip = 0
            elif retCode == 200 or retCode == "200":
                redirectUrl = redirectUri + '&fun=new'
                self.params.setBaseUri(redirectUri[:redirectUri.rfind('/')])
                temp_host = self.params.getBaseUri()[8:]
                self.params.setBaseHost(temp_host[:temp_host.find('/')])
            elif retCode == 400 or retCode == "400":
                dump("Snapshot expired.", "INFOR")
                return False
            elif retCode == 408 or retCode == "408":
                tip = 1
                continue

        if not redirectUrl:
            dump("RedirectUrl is empty, using QRCode to login.", "INFOR")
            return False

        self.request.setHeaders(WechatHeaders.common())
        response = self.request.doNetworkGet(redirectUrl)
        skey, sid, uin, pass_ticket, isgrayscale = Protocol.resolve_webwxnewloginpage(response.text)
        self.params.setSkey(skey)
        self.params.setSid(sid)
        self.params.setUin(uin)
        self.params.setPassTicket(pass_ticket)

        self.init()
        self.params.saveParams()
        dump("********************login********************")
        return True

    def doLogin(self):
        failedTimes = 0
        if not self.login(True):
            while not self.login(False):
                dump("Login Failed times: " + str(failedTimes), "WARNI")
                if failedTimes >= 20:
                    dump("Failed to login Wechat Platform. max: 20, failed: " + (str(failedTimes)))
                    return False
                else:
                    failedTimes += 1
        return True

    def statusNotify(self):
        dump("====================statusNotify====================")
        url = WechatUrl.webwxstatusnotify(self.params.getBaseUri(), self.params.getPassTicket())
        request = {
            "BaseRequest": self.params.getBaseRequest(),
            "ClientMsgId": utils.now(),
            "Code": 3,
            "FromUserName": self.contact.getContact(self.myUserName)['UserName'],
            "ToUserName": self.contact.getContact(self.myUserName)['UserName']
        }
        requestJson = json.dumps(request)
        self.request.setHeaders(WechatHeaders.message())
        response = self.request.doNetworkPost(url, requestJson)
        res = Protocol.resolve_webwxstatusnotify(response.text)
        if res['BaseResponse']['Ret'] != 0:
            raise WechatProtocolException(ErrorCode.StatusNotifyFailed, {'data': response.text})
        dump("Get Message Id:" + (res['MsgID']), "INFOR")
        dump("********************statusNotify********************")
        return True

    def getContact(self):
        dump("====================GetContact====================")
        url = WechatUrl.webwxgetcontact(self.params.getBaseUri(), utils.now(), "0", self.params.getSkey(), self.params.getPassTicket())
        self.request.setHeaders(WechatHeaders.message())
        response = self.request.doNetworkGet(url)
        res = Protocol.resolve_webwxgetcontact(response.text)
        if not res['BaseResponse']['Ret'] == 0:
            raise WechatProtocolException(ErrorCode.GetContactFailed, {'data', response.text})
        for mem in res["MemberList"]:
            self.contact.addContact(mem)
        dump("********************GetContact********************")
        return True

    def getBatchContact(self, usernames):
        dump("====================GetBatchContact====================")
        if not isinstance(usernames, list):
            raise WechatProtocolException(ErrorCode.CallingArgumentError)
        url = WechatUrl.webwxbatchgetcontact(self.params.getBaseUri(), utils.now(), self.params.getPassTicket())
        usernameList = []
        for username in usernames:
            if username[:2] != "@@":
                continue
            usernameList.append({'UserName': username, 'ChatRoomId': ""})
        params = {
            "BaseRequest": self.params.getBaseRequest(),
            "Count": len(usernames),
            "List": usernameList
        }
        requestJson = json.dumps(params)
        self.request.setHeaders(WechatHeaders.common())
        response = self.request.doNetworkPost(url, requestJson)
        res = Protocol.resolve_webwxgetbatchcontact(response.text)
        if res['BaseResponse']['Ret'] != 0:
            raise WechatProtocolException(ErrorCode.GetBatchContactFailed, {'data', response.text})
        for mem in res['ContactList']:
            self.contact.addContact(mem)
        return True

    def syncCheck(self):
        dump("====================syncCheck====================")
        self.request.setHeaders(WechatHeaders.common())
        self.request.setTimeOut(50)
        failedTimes = 0
        while failedTimes < 10:
            url = WechatUrl.synccheck(
                base_host = self.params.getSyncHost(),
                r = utils.time_negate(),
                skey = self.params.getSkey(),
                sid = self.params.getSid(),
                uin = self.params.getUin(),
                deviceid = self.params.getDeviceId(),
                synckey = self.params.getSyncKeyStr(),
                _ = utils.now()
            )
            try:
                response = self.request.doNetworkGet(url)
                retcode, selector = Protocol.resolve_synccheck(response.text)
                dump("==> sync reply: retcode:{retcode}, selector:{selector}".format(retcode=retcode, selector=selector), "INFOR")
                return [retcode, selector]
            except ConnectionError as error:
                dump("X=> Connection error while syncCheck operating.", "ERROR")
                failedTimes += 1
        dump("X=> Connection error while syncCheck operating for 10 times. Aborted.", "ERROR")
        dump("********************syncCheck********************")
        return ["-1", "-1"]

    def sync(self):
        dump("====================sync====================")
        dump("SyncCount:{count}".format(count = self.syncCount), "INFOR")
        """
        return:  true: 表示此次循环放弃, 择时执行新的循环片段.
        return: false: 表示此循环失败, 不用再进行循环, 已失败.
        """
        retcode, selector = self.syncCheck()
        if retcode == -1 or retcode == "-1":
            return False
            raise WechatProtocolException(ErrorCode.SyncFailed, {'data': "retCode: {retcode}, selector: {selector}".format(retcode = retcode, selector = selector)})
        if retcode == 0 or retcode == "0":
            if selector == 0 or selector == "0":
                # Normal Request
                return True
            elif selector == 2 or selector == "2":
                # New Message
                time.sleep(1)
                self.handleMsg()
                return True
            elif selector == 7 or selector == "7":
                # Enter/Exit the chat area
                #TODO: Reserved.
                return True
        elif retcode == 1100 or retcode == "1100":
            # Failed & exitted
            #TODO: exit or relogin
            loginFailedTimes = 0
            dump("Wechat reported that this account has been logouted. tried to relogin. Failed times: {f}".format(f = loginFailedTimes), "ERROR")
            if loginFailedTimes < 10 and self.doLogin():
                loginFailedTimes = 0
                return True
            else:
                return False
        elif retcode == 1101 or retcode == "1101":
            # 1101 means the request is out of time.
            # give the message to the next sync check.
            dump("Wechat reported that the request is out of date.", "WARNI")
            return True
        elif retcode == 1102 or retcode == "1102":
            # maybe cookie set wrong?
            #TODO: exit...? temp... not exit.
            dump("Wechat reported that this terminal had a bad request cookie?", "ERROR")
            return False
        else:
            dump("an unsupport retcode: {f}".format(f = retcode), "ERROR")

        dump("********************sync********************")
        return False

    def syncHostCheck(self):
        dump("====================syncHostCheck====================")
        # Test webpush(2).wx2.qq.com for sync host
        for host in ["webpush.", "webpush2."]:
            self.params.setSyncHost(host + (self.params.getBaseHost()))
            dump("sync host: {host}".format(host = self.params.getSyncHost()), "INFOR")
            retcode, selector = self.syncCheck()
            if retcode == 0 or retcode == "0":
                return True
            if retcode == 1101 or retcode == "1101":
                # Failed & exitted
                # TODO: exit or relogin
                loginFailedTimes = 0
                dump("Wechat reported that this account has been logouted. tried to relogin. Failed times: {f}".format(
                    f=loginFailedTimes), "ERROR")
                if loginFailedTimes < 10 and self.doLogin():
                    loginFailedTimes = 0
                    continue
                else:
                    return False

        dump("********************syncHostCheck********************")
        raise WechatProtocolException(ErrorCode.SyncHostCheckFailed, {'data': "retCode: {retcode}, selector: {selector}".format(retcode = retcode, selector = selector)})

    def syncMessage(self):
        dump("====================syncMessage====================")
        url = WechatUrl.webwxsync(self.params.getBaseUri(), self.params.getSid(), self.params.getSkey(), self.params.getPassTicket())
        request = {
            "BaseRequest": self.params.getBaseRequest(),
            "SyncKey": {
                "Count": len(self.params.getSyncKeys()),
                "List": self.params.getSyncKeys()
            }
        }
        requestJson = json.dumps(request)
        self.request.setHeaders(WechatHeaders.message())
        response = self.request.doNetworkPost(url, requestJson)
        res = json.loads(response.text)
        if res["BaseResponse"]["Ret"] != 0:
            raise WechatProtocolException(ErrorCode.SyncMessageFailed, {'data': response.text})
        else:
            self.params.setSyncKey(res['SyncKey']['List'])
            return res

    def start(self):
        dump("====================start====================")
        # Do Login
        if not self.doLogin():
            return

        # Status Notify
        if not self.statusNotify():
            dump("Error while doing status notify operation.", "ERROR")

        # Get Contact
        failedTimes = 0
        while not self.getContact():
            if failedTimes >= 10:
                raise WechatProtocolException(ErrorCode.GetContactFailed, {'data', 'Times:' + (str(10))})
            else:
                failedTimes += 1

        # Find sync host
        if not self.syncHostCheck():
            dump("Error while checking sync host.", 'ERROR')
            raise WechatProtocolException(ErrorCode.SyncHostCheckFailed)

        # Findout batch contact
        contacts = self.contact.getContacts()
        batch = []
        for c in contacts:
            if c[:2] != "@@":
                continue
            batch.append(c)

        # do request contact
        if len(batch) > 0:
            if not self.getBatchContact(batch):
                dump("Error while checking batch contact.", "ERROR")
                raise WechatProtocolException(ErrorCode.GetBatchContactFailed, {'data', True})
        else:
            dump("Batch contact not found.", "INFOR")

        while self.timerEvent():
            if self.pipe.poll():
                pipeMsg = self.pipe.recv()
                self.pipeMsg(pipeMsg)
            time.sleep(1.5)

        dump("*********************start*********************")

    def handleMsg(self):
        dump("====================handleMsg====================")
        data = self.syncMessage()
        # if data['BaseResponse']['Ret'] != 0 or data['BaseResponse']['Ret'] != "0":
        #     return
        for msg in data['AddMsgList']:
            message = {
                'fromUserName': msg['FromUserName'],
                'toUserName': msg['ToUserName'],
                'content': msg['Content'].encode('utf-8'),
                'messageId': msg['MsgId']
            }
            self.messageProcessing(message)
        dump("********************handleMsg********************")

    def messageProcessing(self, message):
        if not message['content']:
            return
        content = message['content']
        fromUserNameFromGroup = ''
        if message['content'][:1] == '@':
            fromUserNameFromGroup = message['content'][:message['content'].find(':<br/>')]
            content = message['content'][message['content'].find('<br/>'):][len('<br/>'):]
        dump("Passing Message:")
        dump("==> FromUserName: {}".format(message['fromUserName']))
        dump("==> ToUserName: {}".format(message['toUserName']))
        dump("==> MsgID: {}".format(message['messageId']))
        dump("==> Content: {}".format(('[' + fromUserNameFromGroup + ']' + content) if fromUserNameFromGroup else content))

        content_unicode = content.decode("utf-8")
        if content_unicode[:1] == u"中":
            content = "喵"

        self.sendMsg(message['toUserName'], message['fromUserName'], content,
                     utils.now())
        pass

    def sendMsg(self, fromUserName, toUsername, content, msgId):
        dump("====================sendMsg=====================")
        url = WechatUrl.webwxsendmsg(self.params.getBaseUri())
        _msgId = utils.now() + '0' + utils.rand(3)
        params = {
            'BaseRequest': self.params.getBaseRequest(),
            'Msg': {
                'Type': 1,
                'Content': content.decode('utf-8'),
                'FromUserName': fromUserName,
                'ToUserName': toUsername,
                'LocalID': msgId if msgId else _msgId,
                'ClientMsgID': msgId if msgId else _msgId
            },
            'Scene': 0
        }
        requestJson = json.dumps(params, ensure_ascii=False).encode('utf-8')
        maxFailedTimes = 5
        self.request.setHeaders(WechatHeaders.common())
        for i in range(maxFailedTimes):
            res = self.request.doNetworkPost(url, requestJson)
            if res.status_code != 200:
                continue
            else:
                return True
        raise WechatProtocolException(ErrorCode.NetworkError)

    def pipeMsg(self, message):
        if not isinstance(message, dict):
            raise WechatProtocolException(ErrorCode.CallingArgumentError)
        if message['Type'] == "Reply":
            self.sendMsg(message)