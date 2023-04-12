import hashlib

from utils import logger, encryption, file, err, api

def create_blank_acc(data):
    registerTs = api.getTs()
    account = 'someacc'
    passwd = 'kaltsit'
    passwd_hash = hashlib.md5(passwd.encode()).hexdigest()
    token = encryption.get_rand_str(32)

    logger.info("Read Initial User Data From Files")

    # Construct initial user data

    initial_chars = file.readFile('./serverData/userDataInit/troop_chars.json')
    initial_squads = file.readFile('./serverData/userDataInit/troop_squads.json')
    initial_charGroup = file.readFile('./serverData/userDataInit/troop_charGroup.json')
    initial_status = file.readFile('./serverData/userDataInit/status.json')
    initial_dexNav = file.readFile('./serverData/userDataInit/dexNav.json')
    initial_shop = file.readFile('./serverData/userDataInit/shop.json')
    initial_building = file.readFile('./serverData/userDataInit/building.json')
    initial_medal = file.readFile('./serverData/userDataInit/medal.json')
    initial_mission = file.readFile('./serverData/userDataInit/mission.json')
    initial_social = file.readFile('./serverData/userDataInit/social.json')
    initial_gacha = file.readFile('./serverData/userDataInit/gacha.json')

    """
    Stage & Retro List Generation Moved to sync
    """
    for index in initial_chars:
        initial_chars[index]['gainTime'] = registerTs

    # New User
    uid = api.getNewUid()
    initial_status['uid'] = uid
    userData = {
        "account": account,
        "uid": uid,
        "password": passwd_hash,
        "token": token,
        "token_24": data['token'],

        # Beginning of original user data
        "status": initial_status,
        "dungeon": {
            "stages": {},
            "cowLevel": {}
        },
        "troop": {
            "curCharInstId": len(initial_chars) + 1,
            "curSquadCount": 4,
            "squads": initial_squads,
            "chars": initial_chars,
            "charGroup": initial_charGroup,
            "charMission": {},
            "addon": {}
        },
        "dexNav": initial_dexNav,
        "building": initial_building,
        "medal": initial_medal,
        "mission": initial_mission,
        "gacha": initial_gacha,
        "skin": {
            "characterSkins": {},
            "skinTs": {}
        },
        "shop": initial_shop,
        "inventory": {},
        "social": initial_social,
        "storyreview": {
            "groups": {},
            "tags": {
                "knownStoryAcceleration": 0
            }
        },
        "retro": {
            "coin": 999,
            "supplement": 1,
            "block": {},
            "lst": -1,
            "nst": -1,
            "trial": {}
        },
        "background": {
            "selected": "bg_rhodes_day",
            "bgs": {}
        },

        # End of original user data
        "battleReplay": {},
        "gachaStatus": {
            "guaranteed": 50,  # 保底数量(修改为0时无保底)
            "total": 0,  # 总抽取数量
            "save": 0  # 保底统计
        },
        "jobQueue": {}
    }

    userData['status']['lastOnlineTs'] = registerTs
    userData['status']['lastRefreshTs'] = registerTs
    userData['status']['registerTs'] = registerTs

    api.addUser(userData)
    return userData