# -*- coding: utf-8 -*-

from wechatprotocol.exceptions import WechatProtocolException, ErrorCode

class Contact:

    def __init__(self):
        self.selfUser = None
        self.contacts = dict()

    @staticmethod
    def isGroup(userName):
        if not isinstance(userName, (str, unicode)):
            raise WechatProtocolException(ErrorCode.CallingArgumentError)
        if userName[0:2] == '@@':
            return True
        else:
            return False

    def addContact(self, contact):
        if not isinstance(contact, dict):
            raise WechatProtocolException(ErrorCode.CallingArgumentError)
        if not contact.has_key("UserName"):
            raise WechatProtocolException(ErrorCode.CallingArgumentError)
        self.contacts[contact['UserName']] = contact

    def setSelfUser(self, selfUser):
        if not isinstance(selfUser, dict):
            raise WechatProtocolException(ErrorCode.CallingArgumentError)
        self.selfUser = selfUser
        self.addContact(selfUser)

    def getContact(self, userName):
        if not isinstance(userName, (str, unicode)):
            raise WechatProtocolException(ErrorCode.CallingArgumentError)
        if self.contacts.has_key(userName):
            return self.contacts[userName]
        else:
            return None

    def getContacts(self):
        return self.contacts