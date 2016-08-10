import os
import sys
import unittest
from PIL import Image

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

PROJECT_ROOT  = os.path.join(SCRIPT_DIR, '..', '..')
RESOURCES_DIR = os.path.join(SCRIPT_DIR, 'resources')

sys.path.append(PROJECT_ROOT)
import utils.browser as _ub


class TestBrowserUtils(unittest.TestCase): 

	def testWithHttp(self):
		variant = {
			'google.com':         'http://google.com', 
			'http://google.com':  'http://google.com', 
			'https://google.com': 'https://google.com',
			'http://http.com':    'http://http.com'
		}

		for in_str, out in variant.items():
			try:  
				self.assertEqual(_ub.with_http(in_str), out)
			except AssertionError as e: 
				raise AssertionError('[Input: {!r}] '.format(in_str) + str(e))


	def testSiteScreenshot(self):
		''' 
		  Due to some reason (BUG in the PIL or in site_screenshot): 
		  
		  img1 = Image.open(path)
		  img2 = _ub.site_screenshot(url)
		  img1 == img2 # True

		  img2 = _ub.site_screenshot(url)
		  img1 == img2 # False

		  img1 = Image.open(path)
		  img2 = _ub.site_screenshot(url)
		  img1 == img2 # True
		'''

		TEST_SITE = 'http://www.itl.nist.gov/iad/humanid/feret/feret_master.html'
		TRUE_SCREEN_PATH = os.path.join(RESOURCES_DIR, 'itl_nist_gov.png')

		screen = _ub.site_screenshot(url=TEST_SITE)
		self.assertEqual(screen, Image.open(TRUE_SCREEN_PATH)) 

		screen = _ub.site_screenshot(TEST_SITE)
		self.assertEqual(screen, Image.open(TRUE_SCREEN_PATH)) # Image.open again is required (see docstrings) 

		browser = _ub.Browser()
		browser.get(TEST_SITE)
		screen = _ub.site_screenshot(browser=browser) 
		self.assertEqual(screen, Image.open(TRUE_SCREEN_PATH)) # Image.open again is required (see docstrings)
		self.assertEqual(browser.current_url, TEST_SITE)
		browser.close()

		browser = _ub.Browser()
		screen = _ub.site_screenshot(browser=browser, url=TEST_SITE) 
		self.assertEqual(screen, Image.open(TRUE_SCREEN_PATH)) # Image.open again is required (see docstrings)
		self.assertEqual(browser.current_url, TEST_SITE)
		browser.close()


	def testTagsExtractor(self): 
		TEST_SITE = 'http://www.itl.nist.gov/iad/humanid/feret/feret_master.html'
		
		images = _ub.site_tags_images(url=TEST_SITE)
		return


if __name__ == '__main__': 
	unittest.main()