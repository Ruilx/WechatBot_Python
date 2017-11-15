# -*- coding: utf-8 -*-

import sys
from time import time
from random import random
from hashlib import md5
from wechatprotocol.exceptions import WechatProtocolException, ErrorCode

now = lambda: str(int(time() * 1000))
time_negate = lambda: str(~int(time()))
rand = lambda x: repr(random())[2: x + 2]

def dump(info, level = "DEBUG"):
    if not isinstance(info, str):
        print >> sys.stderr, "[" + level + "]: "
        print >> sys.stderr, info
    else:
        print >> sys.stderr, "[" + level + "]: " + info

def urlPrarmsBuilder(dicts):
    if not isinstance(dicts, dict):
        raise WechatProtocolException(ErrorCode.CallingArgumentError)
    return "&".join((str(key) + "=" + str(dicts[key])) for key in dicts)

def syncKeyStrBuilder(syncdict):
    if not (isinstance(syncdict, list) and syncdict[0].has_key('Key') and syncdict[0].has_key('Val')):
        raise WechatProtocolException(ErrorCode.CallingArgumentError)
    return '|'.join(str(key['Key']) + '_' + str(key['Val']) for key in syncdict)

def easyCert(salt, secretKey, token, r):
    if not (isinstance(salt, str) and isinstance(secretKey, str) and isinstance(token, str) and isinstance(r, long)):
        raise WechatProtocolException(ErrorCode.CallingArgumentError)
    hash = md5()
    hash.update(salt.encode('utf-8') + secretKey.encode('utf-8') + token.encode('utf-8') + str(r))
    return hash.hexdigest().upper()