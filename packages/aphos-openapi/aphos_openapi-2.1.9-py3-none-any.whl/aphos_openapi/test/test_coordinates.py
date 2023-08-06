import unittest
from aphos_openapi.models import coordinates

class TestCoordinates(unittest.TestCase):
    def test(self):
        self.assertEqual(coordinates.parse_coordinates("20 54 05.689 +37 01 17.38", 'h'), ("20:54:05.689", "37:01:17.38"))