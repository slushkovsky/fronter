import os
import sys
import unittest

TESTS_ROOT = os.path.dirname(os.path.realpath(__file__))
RESOURCES_DIR = os.path.join(TESTS_ROOT, 'resources')

sys.path.append(os.path.join(TESTS_ROOT, '..'))

class TestCase(unittest.TestCase): 

    def __init__(self, name, *args, **kw): 
        super().__init__(*args, **kw)
        self.name = name

    def resource_path(self, resource_name): 
        assert isinstance(resource_name, str)

        path = os.path.join(RESOURCES_DIR, self.name, resource_name)

        if not os.path.exists(path):
            tmpl = 'Couldn\'t find resource {name!r} required for test {test!r}' 
            raise FileNotFoundError(tmpl.format(test=self.name, name=resource_name))

        return path



from .test_utils_browser import TestBrowserUtils


def run(): 
    suite = unittest.TestSuite()
    suite.addTest(TestBrowserUtils())

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

    