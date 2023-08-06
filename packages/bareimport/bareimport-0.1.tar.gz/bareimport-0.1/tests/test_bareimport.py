#!/usr/bin/env python3


import tempfile
from bareimport import import_script_as_module
import shutil
from pathlib import Path

import unittest


class TestBareImport(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        modulefile = Path(self.tmpdir).joinpath('bareimporttest')
        with open(modulefile, 'w') as fp:
            fp.write('def func():\n    return("success")\n')

        self.bareimporttest = import_script_as_module("bareimporttest", [str(modulefile)])

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_import(self):
        self.assertEqual(self.bareimporttest.func(), 'success')
