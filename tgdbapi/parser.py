from tgdbapi.entity import Game, GameImage, ImageType, Platform


def parse_game_xml(gamesxml):
    game_list = []
    for el in gamesxml.findall("Game"):
        game = Game()
        game.id = safe_read_int(el, "id")
        game.title = safe_read_el(el, "GameTitle")
        game.release_date = safe_read_el(el, "ReleaseDate")
        game.platform_id = safe_read_int(el, "PlatformId")
        game.platform = safe_read_el(el, "Platform")
        game.overview = safe_read_el(el, "Overview")
        game.esrb = safe_read_el(el, "ESRB")
        game.genres = parse_genres_tag(el)
        game.players = safe_read_el(el, "Players")
        game.coop = safe_read_el(el, "Co-op")
        game.youtube = safe_read_el(el, "Youtube")
        game.publisher = safe_read_el(el, "Publisher")
        game.developer = safe_read_el(el, "Developer")
        game.rating = safe_read_float(el, "Rating")
        game.similar = parse_similar_tag(el)
        game.images = parse_images_tag(gamesxml)
        game.thumb = safe_read_el(el, "thumb")

        game_list.append(game)
    return game_list


def parse_genres_tag(tag):
    genres_list = None
    for genres in tag.iter("Genres"):
        genres_list = list()
        for genre in genres:
            genres_list.append(genre.text)
    return genres_list


def parse_similar_tag(tag):
    similar = tag.find("Similar")
    similiar_list = None
    if similar is not None:
        similiar_list = list()
        for sim in similar.findall("Game"):
            similiar_list.append(int(sim.find("id").text))
    return similiar_list


def parse_images_tag(tag):
    image_list = None
    base_url = safe_read_el(tag, "baseImgUrl")
    for images in tag.iter("Images"):
        image_list = list()
        for image in images:
            img = GameImage(type=ImageType[image.tag])
            if img.type in [ImageType.fanart, ImageType.screenshot]:
                attrs = image.find("original")
                img.url = make_url(base_url, attrs.text)
                img.thumb = make_url(base_url, safe_read_el(image, "thumb"))
                img.width = int(attrs.get("width", 0))
                img.height = int(attrs.get("height", 0))
            elif img.type is ImageType.boxart:
                img.url = make_url(base_url, image.text)
                img.thumb = make_url(base_url, image.get("thumb"))
                img.width = int(image.get("width"))
                img.height = int(image.get("height"))
                img.side = image.attrib.get("side")
            elif img.type in [ImageType.clearlogo, ImageType.banner]:
                img.url = make_url(base_url, image.text)
                img.width = int(image.attrib.get("width", 0))
                img.height = int(image.attrib.get("height", 0))
            elif img.type in [ImageType.consoleart, ImageType.controllerart]:
                img.url = make_url(base_url, image.text)
            image_list.append(img)
    return image_list


def make_url(base_url, endpoint):
    return "".join([base_url, endpoint]) if endpoint else None


def parse_platform_xml(platformxml):
    platform_list = []
    for el in platformxml.findall("Platform"):
        p = Platform()
        p.id = safe_read_int(el, "id")
        p.name = safe_read_el(el, "name")
        if p.name is None:
            # The GetPlatformList returns the name in tag <name>
            # but the GetPlatform returns it in the <Platform> tag.
            p.name = safe_read_el(el, "Platform")
        p.console = safe_read_el(el, "console")
        p.controller = safe_read_el(el, "controller")
        p.overview = safe_read_el(el, "overview")
        p.developer = safe_read_el(el, "developer")
        p.manufacturer = safe_read_el(el, "manufacturer")
        p.cpu = safe_read_el(el, "cpu")
        p.memory = safe_read_el(el, "memory")
        p.graphics = safe_read_el(el, "graphics")
        p.sound = safe_read_el(el, "sound")
        p.display = safe_read_el(el, "display")
        p.media = safe_read_el(el, "media")
        p.maxcontrollers = safe_read_el(el, "maxcontrollers")
        p.rating = safe_read_float(el, "Rating")
        p.similar = parse_similar_tag(el)
        p.images = parse_images_tag(platformxml)

        platform_list.append(p)
    return platform_list


def parse_updates_xml(updatesxml):
    game_list = []
    t = safe_read_int(updatesxml, "Time")
    for el in updatesxml.findall("Game"):
        g = Game(id=int(el.text))
        game_list.append(g)
    return dict(time=t, games=game_list)


def parse_favorites_xml(favoritesxml):
    game_list = []
    for el in favoritesxml.findall("Game"):
        g = Game(id=int(el.text))
        game_list.append(g)
    return game_list


def parse_rating_xml(ratingxml):
    return safe_read_float(ratingxml, "game/Rating")


def safe_read_int(el, match):
    tag = el.find(match)
    if tag is None:
        return None
    return int(tag.text)


def safe_read_float(el, match):
    tag = el.find(match)
    if tag is None:
        return None
    return float(tag.text)


def safe_read_el(el, match):
    tag = el.find(match)
    if tag is None:
        return None
    return tag.text
