# This file is placed in the Public Domain.


import unittest


from opq.objects import Object, dumps, loads


class TestDecoder(unittest.TestCase):

    def test_loads(self):
        obj = Object()
        obj.test = "bla"
        oobj = loads(dumps(obj))
        self.assertEqual(oobj.test, "bla")

