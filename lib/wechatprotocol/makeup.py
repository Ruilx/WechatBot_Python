# -*- coding: utf-8 -*-

import json
from wechatprotocol.exceptions import WechatProtocolException, ErrorCode

class Makeup:

    @staticmethod
    def makeBaseRequest(uin, sid, skey, deviceId):
        return {
            'DeviceId': deviceId,
            'Sid': sid,
            'Skey': skey,
            'Uin': uin
        }

    @staticmethod
    def makeSyncKey(syncKeys):
        return {
            'Count': len(syncKeys),
            'List':[].append({'Key': syncKey['key'], 'Val': syncKey['val']} for syncKey in syncKeys)
        }

    @staticmethod
    def makeMsg(type, content, fromUserName, toUserName, localId, clientMsgId):
        return {
            'Type': type,
            'Content': content,
            'FromUserName': fromUserName,
            'ToUserName': toUserName,
            'LocalID': localId,
            'ClientMsgId': clientMsgId
        }

    @staticmethod
    def makeBatchList(list):
        return [].append({'UserName': listPattarn['userName'], 'ChatRoomId': listPattarn['chatRoomId']} for listPattarn in list)

    @staticmethod
    def makeInitPost(baseRequest):
        request = {
            'BaseRequest': baseRequest
        }
        return json.dumps(request)

    @staticmethod
    def makeStatusNotifyPost(baseRequest, clientMsgId, code, fromUserName, toUserName):
        if not isinstance(baseRequest, dict):
            raise WechatProtocolException(ErrorCode.CallingArgumentError)
        request = {
            'BaseRequest': baseRequest,
            'ClientMsgId': clientMsgId,
            'Code': code,
            'FromUserName': fromUserName,
            'ToUserName': toUserName
        }
        return json.dumps(request)

    @staticmethod
    def makeSyncMessagePost(baseRequest, syncKey, rr):
        if not (isinstance(baseRequest, dict) and isinstance(syncKey, dict)):
            raise WechatProtocolException(ErrorCode.CallingArgumentError)
        request = {
            'BaseRequest': baseRequest,
            'SyncKey': syncKey,
            'rr': rr
        }
        return json.dumps(request)

    @staticmethod
    def makeSendMessagePost(baseRequest, msg, scene):
        if not (isinstance(baseRequest, dict) and isinstance(msg, dict)):
            raise WechatProtocolException(ErrorCode.CallingArgumentError)
        request = {
            'BaseRequest': baseRequest,
            'Msg': msg,
            'Scene': scene
        }
        return json.dumps(request)

    @staticmethod
    def makeGetBatchPost(baseRequest, list):
        if not (isinstance(baseRequest, dict) and isinstance(list, dict)):
            raise WechatProtocolException(ErrorCode.CallingArgumentError)
        request = {
            'BaseRequest': baseRequest,
            'Count': len(list),
            'List': list
        }
        return json.dumps(request)
