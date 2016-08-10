import os
from PIL import Image
from logbook import Logger
from typing import Iterator
from selenium import webdriver
from collections import Iterable, namedtuple

from utils.files import unexisted_file
from utils.geom import Rect

logger = Logger('utils::browser')

TagElem = namedtuple('TagImage', ['name', 'img'])
Browser = webdriver.Firefox


def site_screenshot(url:     str              = None, 
                    browser: webdriver.Remote = None) -> Image: 
    '''
      Takes a screenshot of the webpage

      @url     - URL of the webpage (if None - will be used browser curent page)
      @browser - Browser webdriver (if None - will be opened a new one)
    
      !Bouth of @url and @browser can't be None 
    '''

    assert isinstance(url,     str)              or url     is None
    assert isinstance(browser, webdriver.Remote) or browser is None

    if url is None and browser is None: 
        raise Exception('Both of url and browser is None - nothing to be captured')

    browser_opened = browser is None

    if browser is None:
        browser = Browser()
    
    if url is not None:
        browser.get(with_http(url)) # TODO: HTTP errors warnings
    
    tmp_file = unexisted_file(os.getcwd(), '.png')
    browser.save_screenshot(tmp_file)
    img = Image.open(tmp_file)
    
    os.remove(tmp_file)

    if browser_opened: 
        browser.quit()

    return img


def site_tags_images(url:      str, 
                     h_offset: float = 0.0, 
                     w_offset: float = 0.0) -> Iterator[TagElem]: 
    '''
      Gets an images of the all site visible tags

      @url      - URL of the webpage 
      @h_offset - Tag image horizontal margin (relative to tag height)
      @w_offset - Tag image vertical margin   (relative to tag width) 
    '''

    assert isinstance(url,      str)
    assert isinstance(h_offset, float)
    assert isinstance(w_offset, float)

    browser = Browser()
    browser.get(with_http(url)) # TODO: Check HTTP errors
    browser_size = browser.get_window_size()

    screen = site_screenshot(browser=browser)

    elements = browser.find_elements_by_css_selector('*')

    for elem in elements:
        if elem.size['width'] == 0 or elem.size['height'] == 0: 
            logger.debug('Skipped tag {tag!r} (area = 0)'.format(tag=elem.tag_name))
            continue

        r = Rect.from_selenium_element(elem)

        if r.x > browser_size['width'] or r.y > browser_size['height']:
            continue

        margin_h = r.width  * w_offset
        margin_v = r.height * h_offset

        r.x      = max(r.x - margin_h / 2.0, 0)
        r.y      = max(r.y - margin_v / 2.0, 0)
        r.width  = min(r.width  + margin_h, browser_size['width']  - r.x)
        r.height = min(r.height + margin_v, browser_size['height'] - r.y)

        if r.area() == 0.0: 
          continue 

        yield TagElem(name=elem.tag_name, img=screen.crop(r))

    browser.close()


def with_http(url:       str, 
              with_warn: bool = True) -> str:
    ''' 
      Checks that url startswith http (adds if missed)

      @url       - URL
      @with_warn - Enables warning log message if 'http' is missed
    '''

    assert isinstance(url,       str )
    assert isinstance(with_warn, bool)

    if not url.startswith('http'): 
        if with_warn: 
            logger.warning('URL not starts with \'http\' - it will be added automaticly')

        url = 'http://' + url
    
    return url