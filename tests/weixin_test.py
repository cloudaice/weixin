#-*-coding: utf-8-*-

from nose.tools import *
from weixin.Weixin import Weixin
import hashlib
import time
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def test_weixin_token():
    weixinhandler = Weixin("weixin-token")
    assert_equal(weixinhandler.token, "weixin-token")


def test_verify_requset():
    token = "weixin-token"
    weixinhandler = Weixin(token)
    timestamp = str(int(time.time()))
    nonce = "hello"
    echostr = "good"
    args = [token, timestamp, nonce]
    args.sort()
    signature = hashlib.sha1(''.join(args)).hexdigest()
    is_verify, new_echo = weixinhandler.verify_request(
        signature=signature, timestamp=timestamp, nonce=nonce, echostr=echostr)
    assert_equal(is_verify, True)
    assert_equal(new_echo, echostr)
    is_verify, new_echo = weixinhandler.verify_request(
        signature=signature, timestamp="1223434334", nonce=nonce, echostr=echostr)
    assert_equal(is_verify, False)
    assert_equal(new_echo, echostr)


def test_handle_request():
    weixinhandler = Weixin(token="weixin")
    body = """
        <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>1348831860</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[this is a test]]></Content>
        <MsgId>1234567890123456</MsgId>
        </xml>
    """
    params = weixinhandler.handle_request(body)
    assert_equal(params["ToUserName"], "toUser")
    assert_equal(params["FromUserName"], "fromUser")
    assert_equal(params["CreateTime"], 1348831860)
    assert_equal(params["MsgType"], "text")
    assert_equal(params["Content"], "this is a test")
    assert_equal(params["MsgId"], 1234567890123456)
    assert_equal(weixinhandler.MsgType, "text")
    assert_equal(weixinhandler.ToUserName, "toUser")
    assert_equal(weixinhandler.FromUserName, "fromUser")
    assert_equal(weixinhandler.CreateTime, 1348831860)
    assert_equal(weixinhandler.FuncFlag, 0)


def test_cdata():
    weixinhandler = Weixin(token="weixin-token")
    cdata_str = weixinhandler._cdata("hello")
    assert_equal(cdata_str, '<![CDATA[hello]]>')


def test_toxml():
    weixinhandler = Weixin(token='weixin-token')
    dic1 = {"name": "cloudaice", "age": 23}
    xml = weixinhandler._toxml(dic1)
    root = ET.fromstring("<xml>" + xml + "</xml>")
    params = dict()
    for elem in root:
        params[elem.tag] = elem.text
    if "age" in params:
        params["age"] = int(params["age"])
    assert_equal(params, dic1)


def test_music():
    weixinhandler = Weixin(token="weixin-token")
    content = dict(Title=u"天空之城", Description=u"著名陶笛音乐",
                   MusicUrl=u"http://cloudaice.com/music",
                   HQMusicUrl=u"http://cloudaice.com/hqmusic")
    weixinhandler.music(content)
    root = ET.fromstring(weixinhandler.content.encode("utf-8"))
    params = dict()
    for elem in root:
        params[elem.tag] = elem.text
    assert_equal(content, params)


def test_text():
    weixinhandler = Weixin(token="weixin-token")
    content = u"你好，我在测试微信开放API的Python包"
    weixinhandler.text(content)
    assert_equal(weixinhandler.content, u"<Content><![CDATA[你好，我在测试微信开放API的Python包]]></Content>")


def test_news():
    weixinhandler = Weixin(token="weixin-token")
    content = [
        dict(
            Title=u"Python Web 开发之道",
            Description=u"Tornado 是一个好框架",
            PicUrl="http://cloudaice.com/tornado",
            Url="http://cloudaice.com/tornado"
        ),
        dict(
            Title=u"Python 开发微信应用",
            Description=u"使用Python开发微信应用",
            PicUrl="http://cloudaice.com/python",
            Url="http://cloudaice.com/weixin"
        )]
    weixinhandler.news(content)

    weixincontent = u"<xml>" + weixinhandler.content + u"</xml>"
    root = ET.fromstring(weixincontent.encode("utf-8"))

    def foo(root):
        dic = {}
        for elem in root:
            if elem.text is None:
                if elem.tag in dic:
                    if isinstance(dic[elem.tag], list):
                        dic[elem.tag].append(foo(elem))
                    else:
                        dic[elem.tag] = [dic[elem.tag]]
                        dic[elem.tag].append(foo(elem))
                else:
                    dic[elem.tag] = foo(elem)
            else:
                if elem.tag in dic:
                    if isinstance(dic[elem.tag], list):
                        dic[elem.tag].append(elem.text)
                    else:
                        dic[elem.tag] = [dic[elem.tag]]
                        dic[elem.tag].append(elem.text)
                else:
                    dic[elem.tag] = elem.text
        return dic

    params = foo(root)
    if "ArticleCount" in params:
        params['ArticleCount'] = int(params['ArticleCount'])
    content = {"ArticleCount": 2, "Articles": {"item": content}}
    assert_equal(params, content)
