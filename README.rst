weixin
------

weixin － simple weixin public acount python sdk.


Install
-------

    pip install weixin

    or 

    pip install https://github.com/cloudaice/weixin/archive/master.zip

Usage
-----

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
