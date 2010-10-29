#!/usr/bin/env python
import unittest

from .. import packing

class TestPacking(unittest.TestCase):
    def test_rotate(self):
        test1 = [[[True,True],[True,False]],[[True,False],[False,False]]]
        result = packing.get_rotation_chain(test1, 2, 2, 2)
        print result
    
if __name__ == '__main__':
    unittest.main()
