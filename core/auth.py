#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: Auth & Login

from bottle import *
import json
import hashlib

from utils import logger, api, err, encryption
from utils.make_acc import create_blank_acc


# userLogin(auth) -> getToken -> accountLogin


@route('/user/login', method='POST')
def user_login():
    logger.info("Hit /user/login", request.environ.get('HTTP_X_FORWARDED_FOR'))
    try:
        print(request.body.read())
        data = eval(request.body.read())
    except BaseException:
        return json.loads(err.badRequestFormat)

    user = api.user_rol.find_one({'account': data['account']})

    if user is None:
        return json.loads('{"result":1}')

    passwd = data['password'] + 'kaltsit'
    ori = hashlib.md5(passwd.encode()).hexdigest()
    if ori == user['password']:
        # success
        token = encryption.get_rand_str(32)
        api.update(user, {'token': token})
        logger.info("userLogin Succeed," + user['account'], request.environ.get('HTTP_X_FORWARDED_FOR'))
    else:
        logger.info("Wrong Password," + user['account'], request.environ.get('HTTP_X_FORWARDED_FOR'))
        return json.loads('{"result":1}')

    resp = """
{
    "isAuthenticate": true,
    "isLatestUserAgreement": true,
    "isMinor": false,
    "needAuthenticate": false,
    "result": 0,
    "token": "",
    "uid": ""
}
    """
    medium = json.loads(resp)
    medium['token'] = token
    medium['uid'] = user['uid']
#    medium['issuedAt'] = api.getTs()
    return medium

@route('/user/info/v1/need_cloud_auth', method='POST')
def user_login():
    logger.info("Hit /user/info/v1/need_cloud_auth", request.environ.get('HTTP_X_FORWARDED_FOR'))
    
    resp = """
{
    "msg": "OK",
    "status": 0
}
    """
    medium = json.loads(resp)
    return medium


@route('/u8/user/v1/getToken', method='POST')
def get_token():
    logger.info("Hit /u8/user/v1/getToken", request.environ.get('HTTP_X_FORWARDED_FOR'))

    try:
        data = eval(request.body.read())
        token = eval(data['extension'])['access_token']
    except BaseException:
        return json.loads(err.badRequestFormat)

    user = api.getUserByToken(token)

    if user is None:
        return json.loads('{"result":2}')

    resp = """
{
    "channelUid": "0",
    "error": "",
    "extension": "{\\"isMinor\\":false,\\"isAuthenticate\\":true}",
    "isGuest": 0,
    "result": 0,
    "token": "",
    "uid": ""
}
    """
    medium = json.loads(resp)
    medium['channelUid'] = medium['uid'] = user['uid']
    token_24 = encryption.get_rand_str(24)
    api.update(user, {'token_24': token_24})
    medium['token'] = token_24
    return medium


@route('/account/login', method='POST')
def account_login():
    logger.info("Hit /account/login", request.environ.get('HTTP_X_FORWARDED_FOR'))

    try:
        data = eval(request.body.read())
        token24 = data['token']
        uid = data['uid']
    except BaseException:
        return json.loads(err.badRequestFormat)
    
    print('token24: ', token24)

    user = api.getUserByToken24(token24)

    if user is None:
        user = create_blank_acc(data)
        # return json.loads('{"result":3}')

    resp = """
{
    "result": 0,
    "secret": "",
    "serviceLicenseVersion": 0,
    "uid": ""
}
    """
    medium = json.loads(resp)
    medium['uid'] = uid
    secret = encryption.get_rand_str(32)
    medium['secret'] = secret
    api.update(user, {'secret': secret})
    return medium


@route('/user/auth', method='POST')  # 'Remember me'
def user_auth():
    logger.info('Hit /user/auth', request.environ.get('HTTP_X_FORWARDED_FOR'))

    try:
        data = eval(request.body.read())
        token = data['token']
    except BaseException:
        return json.loads(err.badRequestFormat)

    user = api.getUserByToken(token)

    if user is None:
        return json.loads('{"result":3}')

    resp = """
{
    "isAuthenticate": true,
    "isGuest": false,
    "isLatestUserAgreement": true,
    "isMinor": false,
    "needAuthenticate": false,
    "uid": ""
}
    """
    medium = json.loads(resp)
    medium['uid'] = user['uid']
    return medium


@route('/u8/user/verifyAccount', method='POST')
def verifyAccount():
    logger.info("Hit /u8/user/verifyAccount", request.environ.get('HTTP_X_FORWARDED_FOR'))

    resp = """
{
    "result": 0
}
    """
    return json.loads(resp)

@route('/user/oauth2/v1/grant', method='POST')
def verifyAccount():
    logger.info("Hit /user/oauth2/v1/grant", request.environ.get('HTTP_X_FORWARDED_FOR'))

    resp = """
{
    "data": {
        "code": "0"
    },
    "msg": "OK",
    "status": 0
}
    """
    return json.loads(resp)