import unittest
import sys
import os
import uuid
sys.path.append(".")
import filenuke
from filenuke import nuke

def get_file():
    return str(uuid.uuid4()) + '.tmp'

class TestErase(unittest.TestCase):

    def test_single_delete(self):
        f = get_file()
        with open(f, "w") as test_f:
            test_f.write('hello world')
        filenuke.nuke.nuke(f)
        self.assertFalse(os.path.exists(f))
    
    def test_overwrite_single(self):
        f = get_file()
        with open(f, "w") as test_f:
            test_f.write('hello world')
        nuke._overwrite_file(f, 1)
    
    def test_rename(self):
        f = get_file()
        with open(f, "w") as test_f:
            test_f.write('hello world')
        
        new_name = nuke._rename_inode(f)
        self.assertFalse(os.path.exists(f))
        self.assertTrue(os.path.exists(new_name))

        for char in os.path.basename(new_name):
            if char != '0':
                break
        else:
            raise ValueError('New inode name is all zeros in default mode')

        self.assertEqual(len(os.path.basename(new_name)), len(f))
        self.assertGreater(len(os.path.basename(new_name)), 0)
        with open(new_name, "r") as test_f:
            self.assertEqual(test_f.read(), 'hello world')

    def test_rename_zeros(self):
        f = get_file()
        with open(f, "w") as test_f:
            test_f.write('hello world')
        
        new_name = nuke._rename_inode(f, zeros=True)

        for char in os.path.basename(new_name):
            if char != '0':
                raise ValueError('New inode name has non zero in zeros mode')

        self.assertFalse(os.path.exists(f))
        self.assertTrue(os.path.exists(new_name))

        self.assertEqual(len(os.path.basename(new_name)), len(f))
        self.assertGreater(len(os.path.basename(new_name)), 0)
        with open(new_name, "r") as test_f:
            self.assertEqual(test_f.read(), 'hello world')

unittest.main()