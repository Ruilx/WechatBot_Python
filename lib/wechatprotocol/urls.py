# -*- coding: utf-8 -*-

import urllib as urllib

class WechatUrl:

    @staticmethod
    def jsLogin(_, appid = 'wx782c26e4c19acffb', fun='new', lang='zh_CN'):
        return "https://login.wx.qq.com/jslogin?appid={appid}&fun={fun}&lang={lang}&_={_}".format(
            appid = appid,
            fun = fun,
            lang = lang,
            _ = _
        )

    @staticmethod
    def l(uuid):
        return "https://login.weixin.qq.com/l/{uuid}".format(
            uuid = uuid
        )

    @staticmethod
    def qrcode(uuid):
        return "https://login.weixin.qq.com/qrcode/{uuid}".format(
            uuid = uuid
        )

    @staticmethod
    def login(tip, uuid, _, loginicon = 'false'):
        return "https://login.wx.qq.com/cgi-bin/mmwebwx-bin/login?tip={tip}&uuid={uuid}&_={_}&loginicon={loginicon}".format(
            tip = tip,
            uuid = uuid,
            _ = _,
            loginicon = loginicon
        )

    @staticmethod
    def synccheck(base_host, r, skey, sid, uin, deviceid, synckey, _):
        return "https://{base_host}/cgi-bin/mmwebwx-bin/synccheck?r={r}&skey={skey}&sid={sid}&uin={uin}&deviceid={deviceid}&synckey={synckey}&_={_}".format(
            base_host = base_host,
            r = r,
            skey = skey,
            sid = sid,
            uin = uin,
            deviceid = deviceid,
            synckey = synckey,
            _ = _
        )

    @staticmethod
    def webwxsync(base_uri, sid, skey, pass_ticket, lang = 'zh_CN'):
        return "{base_uri}/webwxsync?sid={sid}&skey={skey}&lang={lang}&pass_ticket={pass_ticket}".format(
            base_uri = base_uri,
            sid = sid,
            skey = skey,
            lang = lang,
            pass_ticket = pass_ticket
        )

    @staticmethod
    def webwxinit(base_uri, r, pass_ticket, lang = 'zh_CN'):
        return "{base_uri}/webwxinit?r={r}&lang={lang}&pass_ticket={pass_ticket}".format(
            base_uri = base_uri,
            r = r,
            lang = lang,
            pass_ticket = pass_ticket
        )

    @staticmethod
    def webwxstatusnotify(base_uri, pass_ticket):
        return "{base_uri}/webwxstatusnotify?pass_ticket={pass_ticket}".format(
            base_uri = base_uri,
            pass_ticket = pass_ticket
        )

    @staticmethod
    def webwxsendmsg(base_uri):
        return "{base_uri}/webwxsendmsg".format(
            base_uri = base_uri
        )

    @staticmethod
    def webwxlogout(base_uri, redirect, skey, type = 0):
        return "{base_uri}/webwxlogout?redirect={redirect}&type={type}&skey={skey}".format(
            base_uri = base_uri,
            redirect = redirect,
            type = type,
            skey = skey
        )

    @staticmethod
    def webwxgetcontact(base_uri, r, seq, skey, pass_ticket):
        return "{base_uri}/webwxgetcontact?r={r}&seq={seq}&skey={skey}&pass_ticket={pass_ticket}".format(
            base_uri = base_uri,
            r = r,
            seq = seq,
            skey = skey,
            pass_ticket = pass_ticket
        )

    @staticmethod
    def webwxbatchgetcontact(base_uri, r, pass_ticket, type = 'ex', lang = 'zh_CN'):
        return "{base_uri}/webwxbatchgetcontact?type={type}&r={r}&lang={lang}&pass_ticket={pass_ticket}".format(
            base_uri = base_uri,
            type = type,
            r = r,
            lang = lang,
            pass_ticket = pass_ticket
        )

    @staticmethod
    def webwxpushloginurl(base_uri, uin):
        return "{base_uri}/webwxpushloginurl?uin={uin}".format(
            base_uri = base_uri,
            uin = urllib.urlencode({'': uin})[1:]
        )
