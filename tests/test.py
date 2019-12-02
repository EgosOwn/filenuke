import unittest
import sys
import os
import uuid
import shutil
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
        filenuke.nuke._nuke(f)
        self.assertFalse(os.path.exists(f))
    
    def test_overwrite_single(self):
        f = get_file()
        with open(f, "w") as test_f:
            test_f.write('hello world')
        nuke._overwrite_file(f, 1)
        with open(f, "rb") as test_f:
            self.assertNotEqual(test_f.read(), b'hello world')

    def test_nuke_single(self):
        f = get_file()
        with open(f, "w") as test_f:
            test_f.write('hello world')
        nuke._nuke(f)
        self.assertFalse(os.path.exists(f))

    def test_nuke(self):
        try:
            os.mkdir('test')
        except FileExistsError: pass
        with open('test/test.txt', 'w') as f:
            f.write('test')
        try:
            os.mkdir('test/test2/')
        except FileExistsError: pass
        try:
            os.mkdir('test/test2/test3/')
        except FileExistsError: pass
        with open('test/test2/test-f.txt', 'w') as f:
            f.write('test')
        nuke._nuke('test')
        self.assertFalse(os.path.exists('test/'))
    
    def test_rename(self):
        f = os.path.basename(get_file())
        with open(f, "w") as test_f:
            test_f.write('hello world')
        with open(f, "r") as test_f:
            self.assertEqual(test_f.read(), 'hello world')   
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
        f = os.path.basename(get_file())
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

try:
    os.mkdir('testdata')
except FileExistsError:
    pass
os.chdir('testdata')
unittest.main()
os.chdir('..')
shutil.rmtree('testdata')
