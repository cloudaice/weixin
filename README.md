微信公众平台Python包
====================


介绍
----
微信公众平台的Python SDK，为使用Python开发微信公众平台的开发者提供扩展包，目前只支持消息接口。



安装方法
--------

    pip install weixin
    pip install https://github.com/cloudaice/weixin/archive/master.zip



使用方法
--------


    from weixin import  Weixin

    # process GET
    weixinhandler = Weixin(token="your-weixin-token")
    is_valid, echostr = weixinhandler.verify_request(signature='', timestamp='', nonce='', echostr='')
    if is_valid:
        response(echostr)

    # process POST
    weixinhandler = Weixin(token="your-weixin-token")
    params = weixinhandler.handle_request(request.body)
    print params['MsgType']
    print params['ToUserName']
    print params['FromUserName']
    ....
    
    content = "your content"
    weixinhandler.text(content)
    #weixinhandler.music(content)
    #weixinhandler.news(content)
    xml_body = weixinhandler.handle_response(ToUserName='', MsgType='', kwargs)
    response(xml_body)
