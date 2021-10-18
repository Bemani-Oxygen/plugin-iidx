import os
import json

from core import root_exe
from core.data import Data
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from .factory import MANAGED_VERSION

templates = Jinja2Templates(os.path.join(root_exe, "plugins", "iidx", "templates"))

themeTypeList = [
    "frame",
    "turntable",
    "burst",
    "bgm",
    "towel",
    "voice",
    "noteskin",
    "full_combo",
    "beam",
    "judge",
    "pacemaker"
]


def menu_handler(add_menu):
    add_menu("theme", "User Theme")
    add_menu("qpro", "Change QPro")


def static_handler(add_static):
    add_static(os.path.join(root_exe, "plugins", "iidx", "static"))


async def handle_iidx_getversions_post(request: Request, data: Data):
    resData = []

    for version in MANAGED_VERSION:
        resData.append(version)

    res = {'success': 1, 'error_msg': '', 'data': resData}
    return JSONResponse(content=res)


async def handle_iidx_getcards_post(request: Request, data: Data):
    formData = await request.form()

    try:
        version = int(formData['version'])
    except:
        res = {'success': 0, 'error_msg': "Wrong input value."}
        return JSONResponse(content=json.dumps(res))

    cardsList = await data.local.user.get_all_cards()

    resData = []
    for card in cardsList:
        userid = card[1]
        profile = await data.local.user.get_profile('iidx', version, userid)

        resData.append({
            "userid": userid,
            "name": profile['name']
        })

    res = {'success': 1, 'error_msg': '', 'data': resData}
    return JSONResponse(content=res)


async def handle_iidx_theme_get(request: Request, data: Data):
    return templates.TemplateResponse("theme.html", {"request": request})


async def handle_iidx_theme_post(request: Request, data: Data):
    formData = await request.form()

    themeInputMap = {}

    try:
        userid = int(formData['userid'])
        version = int(formData['version'])

        for themeType in themeTypeList:
            themeInputMap[themeType] = int(formData[themeType])
    except:
        res = {'success': 0, 'error_msg': "Wrong input value."}
        return JSONResponse(content=json.dumps(res))

    profile = await data.local.user.get_profile('iidx', version, userid)

    if 'settings' not in profile:
        profile['settings'] = {}

    for themeType in themeTypeList:
        profile['settings'][themeType] = themeInputMap[themeType]

    await data.local.user.put_profile('iidx', version, userid, profile)

    res = {'success': 1, 'error_msg': ''}
    return JSONResponse(content=res)


async def handle_iidx_gettheme_post(request: Request, data: Data):
    formData = await request.form()

    try:
        userid = int(formData['userid'])
        version = int(formData['version'])
    except ValueError:
        res = {'success': 0, 'error_msg': "Wrong request form."}
        return JSONResponse(content=res)

    profile = await data.local.user.get_profile('iidx', version, userid)

    if 'settings' not in profile:
        profile['settings'] = {}

    resData = {}
    for themeType in themeTypeList:
        if themeType in profile['settings']:
            resData[themeType] = profile['settings'][themeType]
        else:
            resData[themeType] = 0

    res = {'success': 1, 'error_msg': '', 'data': resData}
    return JSONResponse(content=res)


async def handle_iidx_qpro_get(request: Request, data: Data):
    return templates.TemplateResponse("qpro.html", {"request": request})


async def handle_iidx_qpro_post(request: Request, data: Data):
    formData = await request.form()

    try:
        userid = int(formData['userid'])
        version = int(formData['version'])
        head = int(formData['head'])
        hair = int(formData['hair'])
        face = int(formData['face'])
        hand = int(formData['hand'])
        body = int(formData['body'])
    except ValueError:
        res = {'success': 0, 'error_msg': "Wrong Form Value."}
        return JSONResponse(content=res)

    profile = await data.local.user.get_profile('iidx', version, userid)

    if 'settings' not in profile:
        profile['settings'] = {}

    if 'qpro' not in profile['settings']:
        profile['settings']['qpro'] = {}

    profile['settings']['qpro']['head'] = head
    profile['settings']['qpro']['hair'] = hair
    profile['settings']['qpro']['face'] = face
    profile['settings']['qpro']['hand'] = hand
    profile['settings']['qpro']['body'] = body

    await data.local.user.put_profile('iidx', version, userid, profile)

    res = {'success': 1, 'error_msg': ''}
    return JSONResponse(content=res)


async def handle_iidx_getqpro_post(request: Request, data: Data):
    formData = await request.form()

    try:
        userid = int(formData['userid'])
        version = int(formData['version'])
    except:
        res = {'success': 0, 'error_msg': "Wrong input value."}
        return JSONResponse(content=json.dumps(res))

    profile = await data.local.user.get_profile('iidx', version, userid)

    try:
        settings = profile['settings']
        resData = {
            "head": settings['qpro']['head'],
            "hair": settings['qpro']['hair'],
            "face": settings['qpro']['face'],
            "hand": settings['qpro']['hand'],
            "body": settings['qpro']['body']
        }
    except:
        resData = {
            "head": 0,
            "hair": 0,
            "face": 0,
            "hand": 0,
            "body": 0,
        }
    res = {'success': 1, 'error_msg': '', 'data': resData}
    return JSONResponse(content=res)
