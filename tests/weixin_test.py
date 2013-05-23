#-*-coding: utf-8-*-

from nose.tools import *
from weixin.Weixin import Weixin
import hashlib
import time


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
    assert_equal(weixinhandler.CreateTime, "1348831860")
    assert_equal(weixinhandler.FuncFlag, 0)


def test_cdata():
    weixinhandler = Weixin(token="weixin-token")
    cdata_str = weixinhandler._cdata("hello")
    assert_equal(cdata_str, '<![CDATA[hello]]>')


def test_toxml():
    weixinhandler = Weixin(token='weixin-token')
    dic1 = {"name": "cloudaice", "age": 23}
    xml = weixinhandler._toxml(dic1)
    assert_equal(xml, "<name><![CDATA[cloudaice]]></name><age>23</age>")


def test_music():
    weixinhandler = Weixin(token="weixin-token")
    content = dict(Title="天空之城", Description="著名陶笛音乐",
                   MusicUrl="http://cloudaice.com/music",
                   HQMusicUrl="http://cloudaice.com/hqmusic")
    weixinhandler.music(content)
    assert_equal(weixinhandler.content, )
