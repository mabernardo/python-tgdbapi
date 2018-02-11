from enum import Enum


class Game(object):

    def __init__(self, id=None, title=None, platform_id=None, platform=None,
                 release_date=None, overview=None, esrb=None, genres=None,
                 players=None, coop=None, youtube=None, publisher=None,
                 developer=None, rating=None, similar=None, images=None):
        self.id = id
        self.title = title
        self.platform_id = platform_id,
        self.platform = platform,
        self.release_date = release_date,
        self.overview = overview,
        self.esrb = esrb,
        self.genres = genres,
        self.players = players,
        self.coop = coop,
        self.youtube = youtube,
        self.publisher = publisher,
        self.developer = developer,
        self.rating = rating,
        self.similar = similar,
        self.images = images

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __lt__(self, other):
        return self.title < other.title

    def __repr__(self):
        return '<{cls}({id}, "{title}")>'.format(
            cls=self.__class__.__name__, id=self.id, title=self.title)


class ImageType(Enum):
    fanart = 1
    boxart = 2
    banner = 3
    screenshot = 4
    clearlogo = 5
    consoleart = 6
    controllerart = 7


class GameImage(object):

    def __init__(self, type=None, side=None, width=None, height=None, url=None,
                 thumb=None):
        self.type = type
        self.side = side
        self.width = width
        self.height = height
        self.url = url
        self.thumb = thumb

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(str(self.__dict__))

    def __lt__(self, other):
        return self.type.value < other.type.value and self.url < other.url

    def __str__(self):
        return self.url

    def __repr__(self):
        return '<{cls}({type}, "{url}")>'.format(
            cls=self.__class__.__name__, type=self.type, url=self.url)


class Platform(object):

    def __init__(self, id=None, name=None, alias=None, controller=None,
                 overview=None, developer=None, manufacturer=None, cpu=None,
                 memory=None, graphics=None, sound=None, display=None, media=None,
                 maxcontrollers=None, rating=None, images=None, thumb=None):
        self.id = id
        self.name = name
        self.alias = alias
        self.controller = controller
        self.overview = overview
        self.developer = developer
        self.manufacturer = manufacturer
        self.cpu = cpu
        self.memory = memory
        self.graphics = graphics
        self.sound = sound
        self.display = display
        self.media = media
        self.maxcontrollers = maxcontrollers
        self.rating = rating
        self.images = images
        self.thumb = thumb

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __lt__(self, other):
        return self.name < other.name

    def __repr__(self):
        return '<{cls}({id}, "{name}")>'.format(
            cls=self.__class__.__name__, id=self.id, name=self.name)
