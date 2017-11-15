# -*- coding: utf-8 -*-

from wechatprotocol.utils import now, time_negate, rand, syncKeyStrBuilder
from wechatprotocol.exceptions import WechatProtocolException, ErrorCode
from wechatprotocol.makeup import Makeup

import pickle
import os

class Params:

    def __init__(self):
        self.uuid = None
        self.skey = None
        self.sid = None
        self.uin = None
        self.pass_ticket = None
        self.device_id = None

        self.base_uri = None
        self.base_host = None

        self.sync_host = None
        self.sync_key = None
        self.sync_key_str = None

        self.directory = os.path.abspath(os.getcwd())
        self.paramsFile = "{dir}/params.pkl".format(dir = self.directory)

    def saveParams(self):
        with open(self.paramsFile, 'w') as fp:
            params = {
                'uuid': self.uuid,
                'skey': self.skey,
                'sid': self.sid,
                'uin': self.uin,
                'pass_ticket': self.pass_ticket,
                'device_id': self.device_id,
                'base_uri': self.base_uri,
                'base_host': self.base_host,
                'sync_host': self.sync_host,
                'sync_key': self.sync_key,
                'sync_key_str': self.sync_key_str
            }
            pickle.dump(params, fp)

    def loadParams(self):
        if not os.path.exists(self.paramsFile):
            return
        with open(self.paramsFile, 'r') as fp:
            # params = {
            #     'uuid': None,
            #     'skey': None,
            #     'sid': None,
            #     'uin': None,
            #     'pass_ticket': None,
            #     'device_id': None,
            #     'base_uri': None,
            #     'base_host': None,
            #     'sync_host': None,
            #     'sync_key': None,
            #     'sync_key_str': None,
            # }
            params = pickle.load(fp)
            self.uuid = params['uuid']
            self.skey = params['skey']
            self.sid = params['sid']
            self.uin = params['uin']
            self.pass_ticket = params['pass_ticket']
            self.device_id = params['device_id']
            self.base_uri = params['base_uri']
            self.base_host = params['base_host']
            self.sync_host = params['sync_host']
            self.sync_key = params['sync_key']
            self.sync_key_str = params['sync_key_str']


    def setUuid(self, uuid):
        if not isinstance(uuid, (str, unicode)):
            raise WechatProtocolException(ErrorCode.CallingArgumentError)
        self.uuid = uuid

    def getUuid(self):
        return self.uuid

    def setSkey(self, skey):
        if not isinstance(skey, (str, unicode)):
            raise WechatProtocolException(ErrorCode.CallingArgumentError)
        self.skey = skey

    def getSkey(self):
        return self.skey

    def setSid(self, sid):
        if not isinstance(sid, (str, unicode)):
            raise WechatProtocolException(ErrorCode.CallingArgumentError)
        self.sid = sid

    def getSid(self):
        return self.sid

    def setUin(self, uin):
        if not isinstance(uin, (str, int, long, unicode)):
            raise WechatProtocolException(ErrorCode.CallingArgumentError)
        self.uin = str(uin)

    def getUin(self):
        return self.uin

    def resetUin(self):
        self.uin = None

    def setPassTicket(self, pass_ticket):
        if not isinstance(pass_ticket, (str, unicode)):
            raise WechatProtocolException(ErrorCode.CallingArgumentError)
        self.pass_ticket = pass_ticket

    def getPassTicket(self):
        return self.pass_ticket

    def setDeviceId(self, device_id):
        if not (isinstance(device_id, (str, unicode)) and device_id[:1] == 'e'):
            raise WechatProtocolException(ErrorCode.CallingArgumentError)
        self.device_id = device_id

    def getDeviceId(self):
        return self.device_id

    def setBaseUri(self, base_uri):
        if not isinstance(base_uri, (str, unicode)):
            raise WechatProtocolException(ErrorCode.CallingArgumentError)
        self.base_uri = base_uri
        temp_host = self.base_uri[8:]
        self.setBaseHost(temp_host[:temp_host.find("/")])

    def getBaseUri(self):
        return self.base_uri

    def setBaseHost(self, base_host):
        if not isinstance(base_host, (str, unicode)):
            raise WechatProtocolException(ErrorCode.CallingArgumentError)
        self.base_host = base_host

    def getBaseHost(self):
        return self.base_host

    def setSyncHost(self, sync_host):
        if not isinstance(sync_host, (str, unicode)):
            raise WechatProtocolException(ErrorCode.CallingArgumentError)
        self.sync_host = sync_host

    def getSyncHost(self):
        return self.sync_host

    def setSyncKey(self, sync_key):
        if not isinstance(sync_key, list):
            raise WechatProtocolException(ErrorCode.CallingArgumentError)
        self.sync_key = sync_key
        self.setSyncKeyStr(syncKeyStrBuilder(self.sync_key))

    def getSyncKey(self):
        return self.sync_key

    def setSyncKeyStr(self, sync_key_str):
        if not isinstance(sync_key_str, str):
            raise WechatProtocolException(ErrorCode.CallingArgumentError)
        self.sync_key_str = sync_key_str

    def getSyncKeyStr(self):
        return self.sync_key_str

    def getBaseRequest(self):
        return Makeup.makeBaseRequest(uin = self.uin, sid = self.sid, skey = self.skey, deviceId = self.device_id)

    def getSyncKeys(self):
        #return Makeup.makeSyncKey(syncKeys = self.sync_key)
        return self.sync_key