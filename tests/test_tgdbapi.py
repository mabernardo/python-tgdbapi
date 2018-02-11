import unittest
from urllib.error import HTTPError
from unittest.mock import patch, Mock

import tgdbapi
from tgdbapi import GameImage, ImageType, Platform, Game


class TestTGDBAPI(unittest.TestCase):
    GET_GAME_LIST_XML = ["<Data><Game>"
                         "<id>2190</id><GameTitle>Baldur's Gate</GameTitle>"
                         "<ReleaseDate>11/30/1998</ReleaseDate>"
                         "<Platform>PC</Platform>"
                         "</Game><Game>"
                         "<id>2191</id>"
                         "<GameTitle>Baldur's Gate II: Shadows of Amn</GameTitle>"
                         "<ReleaseDate>09/24/2000</ReleaseDate>"
                         "<Platform>PC</Platform>"
                         "</Game><Game>"
                         "<id>2192</id>"
                         "<GameTitle>Baldur's Gate II: Throne of Bhaal</GameTitle>"
                         "<ReleaseDate>06/22/2001</ReleaseDate>"
                         "<Platform>PC</Platform>"
                         "</Game></Data>".encode()]

    IMAGES_TAG = '<Images><fanart>' \
                 '<original width="1920" height="1080">fanart/original/2-1.jpg' \
                 '</original><thumb>fanart/thumb/2-1.jpg</thumb></fanart>' \
                 '<fanart><original width="1920" height="1080">fanart/original/2-2.jpg' \
                 '</original><thumb>fanart/thumb/2-2.jpg</thumb></fanart>' \
                 '<fanart><original width="1920" height="1080">fanart/original/2-3.jpg' \
                 '</original><thumb>fanart/thumb/2-3.jpg</thumb></fanart>' \
                 '<fanart><original width="1920" height="1080">fanart/original/2-4.jpg' \
                 '</original><thumb>fanart/thumb/2-4.jpg</thumb></fanart>' \
                 '<fanart><original width="1920" height="1080">fanart/original/2-5.jpg' \
                 '</original><thumb>fanart/thumb/2-5.jpg</thumb></fanart>' \
                 '<fanart><original width="1920" height="1080">fanart/original/2-6.jpg' \
                 '</original><thumb>fanart/thumb/2-6.jpg</thumb></fanart>' \
                 '<boxart side="back" width="1525" height="2162" ' \
                 'thumb="boxart/thumb/original/back/2-1.jpg">' \
                 'boxart/original/back/2-1.jpg</boxart>' \
                 '<boxart side="front" width="1525" height="2160" ' \
                 'thumb="boxart/thumb/original/front/2-1.jpg">' \
                 'boxart/original/front/2-1.jpg</boxart>' \
                 '<banner width="760" height="140">graphical/2-g2.jpg</banner>' \
                 '<banner width="760" height="140">graphical/2-g3.jpg</banner>' \
                 '<screenshot><original width="1920" height="1080">screenshots/2-1.jpg' \
                 '</original><thumb>screenshots/thumb/2-1.jpg</thumb></screenshot>' \
                 '<clearlogo width="400" height="100">clearlogo/2.png</clearlogo>' \
                 '</Images>'

    GET_GAME_XML = [bytes('<Data>'
                          '<baseImgUrl>http://thegamesdb.net/banners/</baseImgUrl>'
                          '<Game><id>2</id><GameTitle>Crysis</GameTitle>'
                          '<PlatformId>1</PlatformId><Platform>PC</Platform>'
                          '<ReleaseDate>11/13/2007</ReleaseDate>'
                          '<Overview>From the makers of Far Cry, Crysis offers ...</Overview>'
                          '<ESRB>M - Mature</ESRB><Genres><genre>Shooter</genre></Genres>'
                          '<Players>4+</Players><Co-op>No</Co-op>'
                          '<Youtube>http://www.youtube.com/watch?v=i3vO01xQ-DM</Youtube>'
                          '<Publisher>Electronic Arts</Publisher><Developer>Crytek</Developer>'
                          '<Rating>7.3077</Rating><Similar><SimilarCount>2</SimilarCount>'
                          '<Game><id>15246</id><PlatformId>15</PlatformId></Game>'
                          '<Game><id>15225</id><PlatformId>12</PlatformId></Game></Similar>' +
                          IMAGES_TAG +
                          '</Game></Data>', 'utf-8')]

    NOT_FOUND_XML = [bytes('<Data>'
                           '<baseImgUrl>http://thegamesdb.net/banners/</baseImgUrl>'
                           '</Data>', 'utf-8')]

    GET_ART_XML = [bytes('<Data>'
                         '<baseImgUrl>http://thegamesdb.net/banners/</baseImgUrl>'
                         + IMAGES_TAG + '</Data>', 'utf-8')]

    PLATFORM_LIST_XML = [bytes('<Data>'
                               '<basePlatformUrl>http://thegamesdb.net/platform/</basePlatformUrl>'
                               '<Platforms><Platform><id>4916</id><name>Android</name>'
                               '<alias>android</alias></Platform><Platform><id>22</id>'
                               '<name>Atari 2600</name><alias>atari-2600</alias></Platform>'
                               '<Platform><id>4929</id><name>MSX</name><alias>msx</alias></Platform>'
                               '<Platform><id>4912</id><name>Nintendo 3DS</name>'
                               '<alias>nintendo-3ds</alias></Platform><Platform><id>8</id>'
                               '<name>Nintendo DS</name><alias>nintendo-ds</alias></Platform>'
                               '<Platform><id>9</id><name>Nintendo Wii</name>'
                               '<alias>nintendo-wii</alias></Platform><Platform><id>38</id>'
                               '<name>Nintendo Wii U</name><alias>nintendo-wii-u</alias></Platform>'
                               '<Platform><id>1</id><name>PC</name><alias>pc</alias></Platform>'
                               '</Platforms></Data>', 'utf-8')]

    PLATFORM_XML = [bytes('<Data>'
                          '<baseImgUrl>http://thegamesdb.net/banners/</baseImgUrl>'
                          '<Platform><id>15</id><Platform>Microsoft Xbox 360</Platform>'
                          '<console>http://www.youtube.com/watch?v=15.png</console>'
                          '<controller>http://www.youtube.com/watch?v=15.png</controller>'
                          '<overview>The Xbox 360 is the second video game console...</overview>'
                          '<developer>Microsoft</developer><manufacturer>Microsoft</manufacturer>'
                          '<cpu>3.2 GHz PowerPC Tri-Core Xenon</cpu>'
                          '<memory>512 MB of GDDR3 RAM clocked at 700 MHz</memory>'
                          '<graphics>500 MHz ATI Xenos</graphics>'
                          '<sound>Dolby Digital 5.1 (TOSLINK and HDMI)</sound>'
                          '<display>1920x1080</display><media>Disc</media>'
                          '<maxcontrollers>4</maxcontrollers><Rating>8.6</Rating>'
                          '<Images><fanart><original width="1920" height="1080">'
                          'platform/fanart/15-1.jpg</original><thumb>'
                          'platform/fanart/thumb/15-1.jpg</thumb></fanart><fanart>'
                          '<original width="1920" height="1080">'
                          'platform/fanart/15-2.jpg</original><thumb>'
                          'platform/fanart/thumb/15-2.jpg</thumb></fanart>'
                          '<boxart side="back" width="1524" height="2162">'
                          'platform/boxart/15-1.jpg</boxart><banner width="760" height="140">'
                          'platform/banners/15-1.jpg</banner><consoleart>'
                          'platform/consoleart/15.png</consoleart><controllerart>'
                          'platform/controllerart/15.png</controllerart></Images></Platform>'
                          '</Data>', 'utf-8')]

    PLATFORM_GAMES_XML = [bytes('<Data><Game><id>10</id>'
                                '<GameTitle>Ace Combat 6: Fires of Liberation</GameTitle>'
                                '<thumb>boxart/original/front/10-1.jpg</thumb></Game>'
                                '<Game><id>11</id><GameTitle>Army of Two</GameTitle>'
                                '<thumb>boxart/original/front/11-1.jpg</thumb></Game>'
                                '<Game><id>24</id><GameTitle>Gears of War 2</GameTitle>'
                                '<thumb>boxart/original/front/24-1.jpg</thumb></Game>'
                                '<Game><id>27</id><GameTitle>Golden Axe: Beast Rider</GameTitle>'
                                '<ReleaseDate>10/14/2008</ReleaseDate>'
                                '<thumb>boxart/original/front/27-1.jpg</thumb></Game></Data>', 'utf-8')]

    UPDATES_XML = [bytes('<Items><Time>1477087829</Time>'
                         '<Game>10881</Game><Game>10882</Game><Game>10883</Game>'
                         '<Game>10905</Game><Game>10906</Game><Game>35990</Game>'
                         '<Game>40344</Game></Items>', 'utf-8')]

    NO_UPDATES_XML = [bytes('<Items><Time>1477337654</Time></Items>', 'utf-8')]

    RATING_XML = [bytes('<Data><game>'
                        '<Rating>7.3</Rating></game></Data>', 'utf-8')]

    FAVORITES_XML = [bytes('<Favorites><Game>12707</Game><Game>21206</Game>'
                           '<Game>2190</Game></Favorites>', 'utf-8')]

    BAD_XML = [bytes('<Data><Game></Data>', 'utf-8')]

    fa1 = GameImage(type=ImageType.fanart, width=1920, height=1080,
                    url="http://thegamesdb.net/banners/fanart/original/2-1.jpg",
                    thumb="http://thegamesdb.net/banners/fanart/thumb/2-1.jpg")
    fa2 = GameImage(type=ImageType.fanart, width=1920, height=1080,
                    url="http://thegamesdb.net/banners/fanart/original/2-2.jpg",
                    thumb="http://thegamesdb.net/banners/fanart/thumb/2-2.jpg")
    fa3 = GameImage(type=ImageType.fanart, width=1920, height=1080,
                    url="http://thegamesdb.net/banners/fanart/original/2-3.jpg",
                    thumb="http://thegamesdb.net/banners/fanart/thumb/2-3.jpg")
    fa4 = GameImage(type=ImageType.fanart, width=1920, height=1080,
                    url="http://thegamesdb.net/banners/fanart/original/2-4.jpg",
                    thumb="http://thegamesdb.net/banners/fanart/thumb/2-4.jpg")
    fa5 = GameImage(type=ImageType.fanart, width=1920, height=1080,
                    url="http://thegamesdb.net/banners/fanart/original/2-5.jpg",
                    thumb="http://thegamesdb.net/banners/fanart/thumb/2-5.jpg")
    fa6 = GameImage(type=ImageType.fanart, width=1920, height=1080,
                    url="http://thegamesdb.net/banners/fanart/original/2-6.jpg",
                    thumb="http://thegamesdb.net/banners/fanart/thumb/2-6.jpg")

    ba1 = GameImage(type=ImageType.boxart, side="back",
                    width=1525, height=2162,
                    url="http://thegamesdb.net/banners/boxart/original/back/2-1.jpg",
                    thumb="http://thegamesdb.net/banners/"
                          "boxart/thumb/original/back/2-1.jpg")

    ba2 = GameImage(type=ImageType.boxart, side="front",
                    width=1525, height=2160,
                    url="http://thegamesdb.net/banners/boxart/original/front/2-1.jpg",
                    thumb="http://thegamesdb.net/banners/"
                          "boxart/thumb/original/front/2-1.jpg")

    bn1 = GameImage(type=ImageType.banner, width=760, height=140,
                    url="http://thegamesdb.net/banners/graphical/2-g2.jpg")
    bn2 = GameImage(type=ImageType.banner, width=760, height=140,
                    url="http://thegamesdb.net/banners/graphical/2-g3.jpg")

    ss1 = GameImage(type=ImageType.screenshot, width=1920, height=1080,
                    url="http://thegamesdb.net/banners/screenshots/2-1.jpg",
                    thumb="http://thegamesdb.net/banners/screenshots/thumb/2-1.jpg")

    cl1 = GameImage(type=ImageType.clearlogo, width=400, height=100,
                    url="http://thegamesdb.net/banners/clearlogo/2.png")

    @patch("urllib.request.urlopen")
    def test_get_game_list(self, mocked_request):
        req = Mock()
        req.read.side_effect = self.GET_GAME_LIST_XML
        mocked_request.return_value = req

        gl = tgdbapi.get_game_list("Baldur", platform="PC", genre="RPG")
        self.assertIsNotNone(gl)
        self.assertEqual(len(gl), 3)
        self.assertEqual(gl[0].id, 2190)
        self.assertEqual(gl[0].title, "Baldur's Gate")
        self.assertEqual(gl[0].platform, "PC")
        self.assertEqual(gl[0].release_date, "11/30/1998")

    @patch("urllib.request.urlopen")
    def test_get_game_not_found(self, mocked_request):
        req = Mock()
        req.read.side_effect = self.NOT_FOUND_XML
        mocked_request.return_value = req

        game = tgdbapi.get_game(99999)
        self.assertIsNone(game)

    @patch("urllib.request.urlopen")
    def test_get_game(self, mocked_request):
        req = Mock()
        req.read.side_effect = self.GET_GAME_XML
        mocked_request.return_value = req

        game = tgdbapi.get_game(2)
        self.assertIsNotNone(game)
        self.assertEqual(game.id, 2)
        self.assertEqual(game.title, "Crysis")
        self.assertEqual(game.platform_id, 1)
        self.assertEqual(game.platform, "PC")
        self.assertEqual(game.release_date, "11/13/2007")
        self.assertEqual(game.overview,
                         "From the makers of Far Cry, Crysis offers ...")
        self.assertEqual(game.esrb, "M - Mature")
        self.assertEqual(len(game.genres), 1)
        self.assertEqual(game.genres[0], "Shooter")
        self.assertEqual(game.players, "4+")
        self.assertEqual(game.coop, "No")
        self.assertEqual(game.youtube,
                         "http://www.youtube.com/watch?v=i3vO01xQ-DM")
        self.assertEqual(game.publisher, "Electronic Arts")
        self.assertEqual(game.developer, "Crytek")
        self.assertEqual(game.rating, 7.3077)
        self.assertEqual(len(game.similar), 2)
        self.assertIn(15246, game.similar)
        self.assertIn(15225, game.similar)
        self.assertIsNotNone(game.images)
        self.assertEqual(len(game.images), 12)

        self.assertIn(self.fa1, game.images)
        self.assertIn(self.fa2, game.images)
        self.assertIn(self.fa3, game.images)
        self.assertIn(self.fa4, game.images)
        self.assertIn(self.fa5, game.images)
        self.assertIn(self.fa6, game.images)
        self.assertIn(self.ba1, game.images)
        self.assertIn(self.ba2, game.images)
        self.assertIn(self.bn1, game.images)
        self.assertIn(self.bn2, game.images)
        self.assertIn(self.ss1, game.images)
        self.assertIn(self.cl1, game.images)

    @patch("urllib.request.urlopen")
    def test_get_art(self, mocked_request):
        req = Mock()
        req.read.side_effect = self.GET_ART_XML
        mocked_request.return_value = req

        images = tgdbapi.get_art(2)
        self.assertIn(self.fa1, images)
        self.assertIn(self.fa2, images)
        self.assertIn(self.fa3, images)
        self.assertIn(self.fa4, images)
        self.assertIn(self.fa5, images)
        self.assertIn(self.fa6, images)
        self.assertIn(self.ba1, images)
        self.assertIn(self.ba2, images)
        self.assertIn(self.bn1, images)
        self.assertIn(self.bn2, images)
        self.assertIn(self.ss1, images)
        self.assertIn(self.cl1, images)

    @patch("urllib.request.urlopen")
    def test_get_platform_list(self, mocked_request):
        req = Mock()
        req.read.side_effect = self.PLATFORM_LIST_XML
        mocked_request.return_value = req

        pl = tgdbapi.get_platform_list()
        self.assertIsNotNone(pl)
        self.assertEqual(len(pl), 8)

        p1 = Platform(id=1)
        p2 = Platform(id=4916)
        self.assertIn(p1, pl)
        self.assertIn(p2, pl)

    @patch("urllib.request.urlopen")
    def test_get_platform_not_found(self, mocked_request):
        req = Mock()
        req.read.side_effect = self.NOT_FOUND_XML
        mocked_request.return_value = req

        p = tgdbapi.get_platform(9999)
        self.assertIsNone(p)

    @patch("urllib.request.urlopen")
    def test_get_platform(self, mocked_request):
        req = Mock()
        req.read.side_effect = self.PLATFORM_XML
        mocked_request.return_value = req

        p = tgdbapi.get_platform(15)
        self.assertIsNotNone(p)
        self.assertEqual(p.id, 15)
        self.assertEqual(p.name, "Microsoft Xbox 360")
        self.assertEqual(p.console, "http://www.youtube.com/watch?v=15.png")
        self.assertEqual(p.controller, "http://www.youtube.com/watch?v=15.png")
        self.assertEqual(p.overview,
                         "The Xbox 360 is the second video game console...")
        self.assertEqual(p.developer, "Microsoft")
        self.assertEqual(p.manufacturer, "Microsoft")
        self.assertEqual(p.cpu, "3.2 GHz PowerPC Tri-Core Xenon")
        self.assertEqual(p.memory, "512 MB of GDDR3 RAM clocked at 700 MHz")
        self.assertEqual(p.graphics, "500 MHz ATI Xenos")
        self.assertEqual(p.sound, "Dolby Digital 5.1 (TOSLINK and HDMI)")
        self.assertEqual(p.display, "1920x1080")
        self.assertEqual(p.media, "Disc")
        self.assertEqual(p.maxcontrollers, "4")
        self.assertEqual(p.rating, 8.6)

        fa1 = GameImage(type=ImageType.fanart, width=1920, height=1080,
                        url="http://thegamesdb.net/banners/platform/fanart/15-1.jpg",
                        thumb="http://thegamesdb.net/banners/"
                              "platform/fanart/thumb/15-1.jpg")
        fa2 = GameImage(type=ImageType.fanart, width=1920, height=1080,
                        url="http://thegamesdb.net/banners/platform/fanart/15-2.jpg",
                        thumb="http://thegamesdb.net/banners/"
                              "platform/fanart/thumb/15-2.jpg")

        ba1 = GameImage(type=ImageType.boxart, side="back",
                        width=1524, height=2162,
                        url="http://thegamesdb.net/banners/platform/boxart/15-1.jpg")

        consoleart = GameImage(type=ImageType.consoleart,
                               url="http://thegamesdb.net/banners/platform/consoleart/15.png")

        controllerart = GameImage(type=ImageType.controllerart,
                                  url="http://thegamesdb.net/banners/platform/controllerart/15.png")

        self.assertIn(fa1, p.images)
        self.assertIn(fa2, p.images)
        self.assertIn(ba1, p.images)
        self.assertIn(consoleart, p.images)
        self.assertIn(controllerart, p.images)

    @patch("urllib.request.urlopen")
    def test_get_platform_games(self, mocked_request):
        req = Mock()
        req.read.side_effect = self.GET_GAME_LIST_XML
        mocked_request.return_value = req

        gl = tgdbapi.get_platform_games(1)
        self.assertIsNotNone(gl)
        self.assertEqual(len(gl), 3)
        self.assertEqual(gl[0].id, 2190)
        self.assertEqual(gl[0].title, "Baldur's Gate")
        self.assertEqual(gl[0].platform, "PC")
        self.assertEqual(gl[0].release_date, "11/30/1998")

    @patch("urllib.request.urlopen")
    def test_platform_games(self, mocked_request):
        req = Mock()
        req.read.side_effect = self.PLATFORM_GAMES_XML
        mocked_request.return_value = req

        gl = tgdbapi.platform_games("microsoft xbox 360")
        self.assertIsNotNone(gl)
        self.assertEqual(len(gl), 4)
        self.assertEqual(gl[3].id, 27)
        self.assertEqual(gl[3].title, "Golden Axe: Beast Rider")
        self.assertEqual(gl[3].release_date, "10/14/2008")
        self.assertEqual(gl[3].thumb, "boxart/original/front/27-1.jpg")

    @patch("urllib.request.urlopen")
    def test_updates(self, mocked_request):
        req = Mock()
        req.read.side_effect = self.UPDATES_XML
        mocked_request.return_value = req

        gl = tgdbapi.updates(10000)
        self.assertIsNotNone(gl)
        self.assertEqual(type(gl), dict)
        self.assertEqual(gl["time"], 1477087829)
        self.assertEqual(type(gl["games"]), list)
        self.assertEqual(len(gl["games"]), 7)

        g1 = Game(id=10881)
        self.assertIn(g1, gl["games"])

        req.read.side_effect = self.NO_UPDATES_XML
        mocked_request.return_value = req

        gl = tgdbapi.updates(1)
        self.assertIsNotNone(gl)
        self.assertEqual(type(gl), dict)
        self.assertEqual(gl["time"], 1477337654)
        self.assertEqual(type(gl["games"]), list)
        self.assertEqual(len(gl["games"]), 0)

    @patch("urllib.request.urlopen")
    def test_get_user_rating(self, mocked_request):
        req = Mock()
        req.read.side_effect = self.RATING_XML
        mocked_request.return_value = req

        gr = tgdbapi.get_user_rating("A1B2C3D4E5F6", 2190)
        self.assertIsNotNone(gr)
        self.assertEqual(gr, 7.3)

    @patch("urllib.request.urlopen")
    def test_set_user_rating(self, mocked_request):
        req = Mock()
        req.read.side_effect = self.RATING_XML
        mocked_request.return_value = req

        gr = tgdbapi.set_user_rating("A1B2C3D4E5F6", 2190, 7.5)
        self.assertIsNotNone(gr)
        self.assertEqual(gr, 7.3)

    @patch("urllib.request.urlopen")
    def test_get_user_favorites(self, mocked_request):
        req = Mock()
        req.read.side_effect = self.FAVORITES_XML
        mocked_request.return_value = req

        fg = tgdbapi.get_user_favorites("A1B2C3D4E5F6")
        self.assertIsNotNone(fg)

        g1 = Game(id=2190)
        self.assertIn(g1, fg)

    @patch("urllib.request.urlopen")
    def test_add_user_favorite(self, mocked_request):
        req = Mock()
        req.read.side_effect = self.FAVORITES_XML
        mocked_request.return_value = req

        fg = tgdbapi.add_user_favorite("A1B2C3D4E5F6", 2190)
        self.assertIsNotNone(fg)

        g1 = Game(id=2190)
        self.assertIn(g1, fg)

    @patch("urllib.request.urlopen")
    def test_remove_user_favorite(self, mocked_request):
        req = Mock()
        req.read.side_effect = self.FAVORITES_XML
        mocked_request.return_value = req

        fg = tgdbapi.remove_user_favorite("A1B2C3D4E5F6", 2190)
        self.assertIsNotNone(fg)

        g1 = Game(id=2190)
        self.assertIn(g1, fg)

    @patch("urllib.request.urlopen")
    def test_TGDBError(self, mocked_request):
        req = Mock()
        req.read.side_effect = self.BAD_XML
        mocked_request.return_value = req
        with self.assertRaises(tgdbapi.api.TGDBError) as err:
            tgdbapi.get_game(2)
        e = err.exception
        self.assertEqual(str(e), "Bad result. Code: 7, Position: (1, 14)")

        req.read.side_effect = HTTPError(404, "Not Found", None, None, None)
        mocked_request.return_value = req
        with self.assertRaises(tgdbapi.api.TGDBError):
            tgdbapi.get_game(2)
