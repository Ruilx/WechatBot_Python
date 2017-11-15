# -*- coding: utf-8 -*-

from enum import Enum

class ErrorCode(Enum):
    UnknownError = -1
    NoError = 0
    CallingArgumentError = 1
    NetworkError = 2

    LoginRetcodeFailed = 10
    LoginQrlogincodeFailed = 11
    InitFailed = 12
    StatusNotifyFailed = 13
    GetContactFailed = 14
    SyncHostCheckFailed = 15
    GetBatchContactFailed = 16
    SyncFailed = 17
    SyncMessageFailed = 18

    ResolveJsLoginError = 1000
    ResolveJsLoginError_dataIsEmpty = 1001

    ResolveLoginError = 1010
    ResolveLoginError_dataIsEmpty = 1011

    ResolveWebnewloginpageError = 1020
    ResolveWebnewloginpageError_dataIsEmpty = 1021

    ResolveWebwxinitError = 1030
    ResolveWebwxinitError_dataIsEmpty = 1031

    ResolveWebwxstatusnotifyError = 1040
    ResolveWebwxstatusnotifyError_dataIsEmpty = 1041

    ResolveWebwxgetcontactError = 1050
    ResolveWebwxgetcontactError_dataIsEmpty = 1051

    ResolveWebwxbatchgetcontactError = 1060
    ResolveWebwxbatchgetcontactError_dataIsEmpty = 1061

    ResolveSynccheckError = 1070
    ResolveSynccheckError_dataIsEmpty = 1071

    ResolveWebwxsyncError = 1080
    ResolveWebwxsyncError_dataIsEmpty = 1081

    ResolveWebwxpushloginurlError = 1090
    ResolveWebwxpushloginurlError_dataIsEmpty = 1091

    ForceToExit = 2000

class Translations:
    translations = {
        ErrorCode.UnknownError: "Unknown error.",
        ErrorCode.NoError: "No error.",
        ErrorCode.CallingArgumentError: "Calling argument error.",
        ErrorCode.NetworkError: "Network error.",

        ErrorCode.ResolveJsLoginError: "Resolve Jslogin Error: {data}",
        ErrorCode.ResolveJsLoginError_dataIsEmpty: "Resolve JsLogin Error, data is empty or not string.",

        ErrorCode.ResolveLoginError: "Resolve Login Error: {data}",
        ErrorCode.ResolveLoginError_dataIsEmpty: "Resolve Login Error, data is empty or not string.",

        ErrorCode.ResolveWebnewloginpageError: "Resolve webnewloginpage Error: {data}",
        ErrorCode.ResolveWebnewloginpageError_dataIsEmpty: "Resolve webnewloginpage Error, data is empty or not string.",

        ErrorCode.ResolveWebwxinitError: "Resolve webwxinit Error: {data}",
        ErrorCode.ResolveWebwxinitError_dataIsEmpty: "Resolve webwxinit Error: data is empty.",

        ErrorCode.ResolveWebwxstatusnotifyError: "Resolve webwxstatusnotify Error: {data}",
        ErrorCode.ResolveWebwxstatusnotifyError_dataIsEmpty: "Resolve webwxstatusnotify Error: data is empty.",

        ErrorCode.ResolveWebwxgetcontactError: "Resolve webwxgetcontact Error: {data}",
        ErrorCode.ResolveWebwxgetcontactError_dataIsEmpty: "Resolve webwxgetcontact Error: data is empty.",

        ErrorCode.ResolveWebwxbatchgetcontactError: "Resolve webexbatchgetcontactError: {data}",
        ErrorCode.ResolveWebwxbatchgetcontactError_dataIsEmpty: "Resolve webexbatchgetcontact Error: data is empty.",

        ErrorCode.ResolveSynccheckError: "Resolve synccheck Error: {data}",
        ErrorCode.ResolveSynccheckError_dataIsEmpty: "Resolve synccheck Error: data is empty.",

        ErrorCode.ResolveWebwxpushloginurlError: "Resolve webwxpushloginurl Error: {data}",
        ErrorCode.ResolveWebwxpushloginurlError_dataIsEmpty: "Resolve webwxpushloginurl Error: data is empty",

        ErrorCode.LoginRetcodeFailed: "Login retcode unknown: {data}",
        ErrorCode.LoginQrlogincodeFailed: "Login Qr login code: {data} != 200",
        ErrorCode.InitFailed: "Init Failed. Json: {data}",
        ErrorCode.StatusNotifyFailed: "Status Notify Failed. Json: {data}",
        ErrorCode.GetContactFailed: "Get Contact Failed: {data}",
        ErrorCode.SyncHostCheckFailed: "Get SyncHostCheck Failed.",
        ErrorCode.GetBatchContactFailed: "Get Batch contact failed: {data}",
        ErrorCode.SyncFailed: "Sync failed: {data}",
        ErrorCode.SyncMessageFailed: "Sync message failed: {data}",

        ErrorCode.ForceToExit: "Force to exit.",

    }

    def getTranslations(self, code):
        return self.translations[code]


class WechatProtocolException(Exception):
    def __init__(self, errCode, params = None, errMsg = None):
        self.err_code = errCode
        self.err_msg = errMsg
        self.params = params
        self.errorTrans = Translations()

    def setParams(self, params):
        if not isinstance(params, dict):
            raise WechatProtocolException(ErrorCode.CallingArgumentError)
        self.params = params

    def __str__(self):
        return repr(self.err_msg if self.err_msg else self.errorTrans.getTranslations(self.err_code).format(**self.params))

