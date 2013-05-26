#-*-coding: utf-8-*-

import hashlib
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


class WeixinException(Exception):
    pass


class Weixin(object):
    def __init__(self, token=None):
        self.token = token
        self.MsgType = None
        self.FromUserName = None
        self.ToUserName = None
        self.CreateTime = None
        self.FuncFlag = None
        self.content = ''

    def verify_request(self, signature=None, timestamp=None,
                       nonce=None, echostr=None):
        if signature and timestamp and nonce and echostr:
            if not isinstance(timestamp, (str, unicode)):
                timestamp = str(timestamp)
            if self.token is None:
                raise WeixinException("token can not be None")
            args = [timestamp, self.token, nonce]
            args.sort()
            new_signature = hashlib.sha1(''.join(args)).hexdigest()
            if new_signature == signature:
                is_valid = True
            else:
                is_valid = False
            return is_valid, echostr

    def handle_request(self, body):
        root = ET.fromstring(body)
        Param_dict = dict()
        for elem in root:
            Param_dict[elem.tag] = elem.text
        if "CreateTime" in Param_dict:
            Param_dict["CreateTime"] = int(Param_dict["CreateTime"])
        if "MsgId" in Param_dict:
            Param_dict["MsgId"] = long(Param_dict["MsgId"])
        self.MsgType = Param_dict["MsgType"]
        self.ToUserName = Param_dict["ToUserName"]
        self.FromUserName = Param_dict["FromUserName"]
        self.CreateTime = Param_dict['CreateTime']
        self.FuncFlag = 0
        return Param_dict

    def handle_response(self, **kwargs):
        resp = {
            "ToUserName": kwargs.get("FromUserName", self.FromUserName),
            "FromUserName": kwargs.get("ToUserName", self.ToUserName),
            "CreateTime": kwargs.get("CreateTime", self.CreateTime),
            "MsgType": kwargs.get("MsgType", self.MsgType),
            "FuncFlag": kwargs.get("FuncFlag", self.FuncFlag)
        }
        resp = self._toxml(resp)
        xml_body = "<xml>" + resp + self.content + "</xml>"
        if isinstance(xml_body, unicode):
            xml_body.encode("utf-8")
        return xml_body

    def _cdata(self, s):
        return "<![CDATA[%s]]>" % s

    def _toxml(self, content):
        seq = []
        if isinstance(content, dict):
            for key, value in content.items():
                if isinstance(value, (unicode, str)):
                    seq.append("<%s>%s</%s>" % (key, self._cdata(value), key))
                elif isinstance(value, (list, dict)):
                    seq.append("<%s>%s</%s>" % (key, self._toxml(value), key))
                elif isinstance(value, int):
                    seq.append("<%s>%d</%s>" % (key, value, key))
                else:
                    raise WeixinException("type %s is not support in dict" %
                                          type(content))
        elif isinstance(content, list):
            for item in content:
                if isinstance(item, dict):
                    seq.append("<%s>%s</%s>" % (self.tag, self._toxml(item), self.tag))
                else:
                    raise WeixinException("%s is not support in list" %
                                          type(content))
        else:
            raise WeixinException("%s is not support in content" %
                                  type(content))

        return ''.join(seq)

    def music(self, content):
        for key in ["Title", "Description", "MusicUrl", "HQMusicUrl"]:
            if key not in content:
                raise WeixinException("%s can't be None" % key)
        self.content = self._toxml(dict(Music=content))
    
    def news(self, content):
        articles = len(content)
        self.tag = "item"
        self.content = "<ArticleCount>%d</ArticleCount>" % articles
        self.content += self._toxml(dict(Articles=content))

    def text(self, content):
        self.content = self._toxml(dict(Content=content))
