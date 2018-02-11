import unittest
from tgdbapi import Game, GameImage, ImageType, Platform


class TestEntity(unittest.TestCase):

    def test_game(self):
        game1 = Game(id=1, title="Baldur's Gate")
        game2 = Game(id=1, title="Baldur's Gate")
        game3 = Game(id=2, title="Divinity: Original Sin")

        self.assertEqual(game1, game2)
        self.assertEqual(game1.__hash__(), game2.__hash__())
        self.assertEqual(str(game1), '<Game(1, "Baldur\'s Gate")>')
        self.assertNotEqual(game1, game3)
        self.assertTrue(game3 > game1)

    def test_game_image(self):
        image1 = GameImage(type=ImageType.boxart, side="front", width=1920,
                           height=1080, url="http://someurl.com", thumb="http://thumb.com")
        image2 = GameImage(type=ImageType.boxart, side="front", width=1920,
                           height=1080, url="http://someurl.com", thumb="http://thumb.com")
        image3 = GameImage(type=ImageType.banner, side="back", width=1920,
                           height=1080, url="http://xsomeurl.com", thumb="http://thumb.com")

        self.assertEqual(image1, image2)
        self.assertEqual(image1.__hash__(), image2.__hash__())
        self.assertEqual(str(image1), "http://someurl.com")
        self.assertEqual(repr(image1),
                         '<GameImage(ImageType.boxart, "http://someurl.com")>')
        self.assertNotEqual(image1, image3)
        self.assertTrue(image3 > image1)

    def test_platform(self):
        plat1 = Platform(id=1, name="PC")
        plat2 = Platform(id=1, name="PC")
        plat3 = Platform(id=2, name="Nintendo 3DS")

        self.assertEqual(plat1, plat2)
        self.assertEqual(plat1.__hash__(), plat2.__hash__())
        self.assertEqual(str(plat1), '<Platform(1, "PC")>')
        self.assertNotEqual(plat1, plat3)
        self.assertTrue(plat1 > plat3)
