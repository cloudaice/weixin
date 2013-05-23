#-*-coding: utf-8-*-

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import hashlib


Api_Request = {
    "text": ["ToUserName", "FromUserName", "CreateTime", "Content", "MsgId"],
    "image": ["ToUserName", "FromUserName", "CreateTime", "PicUrl", "MsgId"],
    "location": ["ToUserName", "FromUserName", "CreateTime", "Location_X",
                 "Location_Y", "Scale", "Label", "MsgId"],
    "link": ["ToUserName", "FromUserName", "CreateTime", "Title", "Description",
             "Url", "MsgId"],
    "event": ["ToUserName", "FromUserName", "CreateTime", "Event", "EventKey"]
}


class Weixin(object):
    def __init__(self, token=None):
        self.token = token
        self.MsgType = None
        self.FromUserName = None
        self.ToUserName = None
        self.CreateTime = None
        self.FuncFlag = None
        self.content = ''

    def verify_request(self, signature=None, timestamp=None, nonce=None, echostr=None):
        if signature and timestamp and nonce and echostr:
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
        try:
            MsgType = root.find("MsgType").text
        except AttributeError, e:
            raise e
        
        Param_dict = dict()
        for KeyName in Api_Request[MsgType]:
            try:
                Param_dict[KeyName] = root.find(KeyName).text
            except AttributeError, e:
                raise e
        self.MsgType = MsgType
        self.ToUserName = Param_dict["ToUserName"]
        self.FromUserName = Param_dict["FromUserName"]
        self.CreateTime = Param_dict['CreateTime']
        self.FuncFlag = Param_dict['FuncFlag']
        return MsgType, Param_dict

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
        return xml_body

    def _cdata(self, s):
        return "<![CDATA[%s]]>" % s

    def _toxml(self, content):
        seq = []
        if isinstance(content, dict):
            for key, value in content.itmes():
                if isinstance(value, (unicode, str)):
                    seq.append("<%s>%s</%s>" % (key, value, key))
                elif isinstance(value, (list, dict)):
                    seq.append("<%s>%s</%s>" % (key, self._toxml(value), key))
                else:
                    raise "%s is not support" % type(content)
        elif isinstance(content, list):
            for item in content:
                if isinstance(item, dict):
                    seq.append("<%s>%s</%s>" % (self.tag, self._toxml(item), self.tag))
                else:
                    raise "%s is not support" % type(content)
        else:
            raise "%s is not support" % type(content)

        return ''.join(seq)

    def misic(self, content):
        for key in ["Title", "Description", "MusicUrl", "HQMusicUrl"]:
            if key not in content:
                raise "%s can't be None" % key
        self.content = self._toxml(dict(Music=content))
    
    def news(self, content):
        articles = len(content)
        self.tag = "item"
        self.content = "<ArticleCount>%s</ArticleCount>" % articles
        self.content += self._toxml(dict(Articles=content))

    def text(self, content):
        self.content = self._toxml(dict(Content=content))
