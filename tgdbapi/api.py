import urllib.parse
import urllib.request
import xml.etree.ElementTree

import tgdbapi.parser

GAMESDB_BASE_URL = "http://thegamesdb.net/api/"

def get_game_list(name, platform=None, genre=None):
    assert(name is not None)
    GAME_LIST_URL = GAMESDB_BASE_URL + "GetGamesList.php"

    args = {"name": name}
    if platform is not None:
        args["platform"] = platform
    if genre is not None:
        args["genre"] = genre

    xmlgames = read_request(GAME_LIST_URL, args)
    return tgdbapi.parser.parse_game_xml(xmlgames)


def get_game(id):
    assert(id is not None)
    GAME_URL = GAMESDB_BASE_URL + "GetGame.php"

    args = {"id": str(id)}
    xmlgames = read_request(GAME_URL, args)
    games = tgdbapi.parser.parse_game_xml(xmlgames)
    if len(games) > 0:
        return games[0]
    return None


def get_art(id):
    assert(id is not None)
    GAME_ART_URL = GAMESDB_BASE_URL + "GetArt.php"

    args = {"id": str(id)}
    xmlart = read_request(GAME_ART_URL, args)
    images = tgdbapi.parser.parse_images_tag(xmlart)
    return images


def get_platform_list():
    PLATFORM_LIST_URL = GAMESDB_BASE_URL + "GetPlatformsList.php"

    xmlplatforms = read_request(PLATFORM_LIST_URL)
    platformstag = xmlplatforms.findall("Platforms")
    return tgdbapi.parser.parse_platform_xml(platformstag[0])


def get_platform(id):
    assert(id is not None)
    PLATFORM_URL = GAMESDB_BASE_URL + "GetPlatform.php"

    args = {"id": str(id)}
    xmlplatforms = read_request(PLATFORM_URL, args)
    platform = tgdbapi.parser.parse_platform_xml(xmlplatforms)
    if len(platform) > 0:
        return platform[0]
    return None


def get_platform_games(platform_id):
    PLATFORM_URL = GAMESDB_BASE_URL + "GetPlatformGames.php"

    args = {"platform": str(platform_id)}
    xmlgames = read_request(PLATFORM_URL, args)
    return tgdbapi.parser.parse_game_xml(xmlgames)


def platform_games(name):
    PLATFORM_URL = GAMESDB_BASE_URL + "PlatformGames.php"

    args = {"platform": name}
    xmlgames = read_request(PLATFORM_URL, args)
    return tgdbapi.parser.parse_game_xml(xmlgames)


def updates(time):
    UPDATES_URL = GAMESDB_BASE_URL + "Updates.php"

    args = {"time": str(time)}
    xmlgames = read_request(UPDATES_URL, args)
    return tgdbapi.parser.parse_updates_xml(xmlgames)


def get_user_rating(accountid, itemid):
    USER_RATING_URL = GAMESDB_BASE_URL + "User_Rating.php"

    args = {
        "accountid": accountid,
        "itemid": str(itemid)
    }
    xmlgames = read_request(USER_RATING_URL, args)
    return tgdbapi.parser.parse_rating_xml(xmlgames)


def set_user_rating(accountid, itemid, rating):
    USER_RATING_URL = GAMESDB_BASE_URL + "User_Rating.php"

    data = {
        "accountid": accountid,
        "itemid": str(itemid),
        "rating": str(rating)
    }
    xmlrating = read_request(USER_RATING_URL, None, data)
    return tgdbapi.parser.parse_rating_xml(xmlrating)


def get_user_favorites(accountid):
    USER_FAVORITES_URL = GAMESDB_BASE_URL + "User_Favorites.php"

    args = {"accountid": accountid}
    xmlgames = read_request(USER_FAVORITES_URL, args)
    return tgdbapi.parser.parse_favorites_xml(xmlgames)


def add_user_favorite(accountid, gameid):
    USER_FAVORITES_URL = GAMESDB_BASE_URL + "User_Favorites.php"

    data = {
        "accountid": accountid,
        "gameid": gameid,
        "type": "add"
    }
    xmlgames = read_request(USER_FAVORITES_URL, None, data)
    return tgdbapi.parser.parse_favorites_xml(xmlgames)


def remove_user_favorite(accountid, gameid):
    USER_FAVORITES_URL = GAMESDB_BASE_URL + "User_Favorites.php"

    data = {
        "accountid": accountid,
        "gameid": gameid,
        "type": "remove"
    }
    xmlgames = read_request(USER_FAVORITES_URL, None, data)
    return tgdbapi.parser.parse_favorites_xml(xmlgames)


class TGDBError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


def read_request(url, args=None, data=None):
    if args is not None and len(args) > 0:
        url = ''.join([url, '?', urllib.parse.urlencode(
            args, quote_via=urllib.parse.quote)])

    if data is not None and len(data) > 0:
        data = bytes(
            urllib.parse.urlencode(data, quote_via=urllib.parse.quote),
            'utf-8'
        )
    request = urllib.request.Request(url, data)
    request.add_header("Referer", "http://thegamesdb.net/")
    request.add_header("User-agent", "Mozilla/5.0")

    try:
        response = urllib.request.urlopen(request, data)
        xmlstr = response.read()
        xmlresponse = xml.etree.ElementTree.fromstring(xmlstr)
    except urllib.error.HTTPError as err:
        raise TGDBError(err.reason)
    except xml.etree.ElementTree.ParseError as err:
        raise TGDBError("Bad result. Code: {0}, Position: {1}".format(
            err.code, err.position))

    return xmlresponse
