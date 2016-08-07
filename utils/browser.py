import os
import inspect
import logging
from selenium import webdriver 


def site_screenshot(url, save_to, warn_on_overwrite=True): 
    '''
      Creates and saves screenshot of the webpage

      @param  url               <str>   URL of webpage
      @param  save_to           <str>   Path to save screenshot 
      @param  warn_on_overwrite <bool>  If this param is True - in the case of overwrite
                                        file by the path, specified in 'save_to' - will 
                                        be logger warning message
    '''

    assert(isinstance(url,               str ))
    assert(isinstance(save_to,           str ))
    assert(isinstance(warn_on_overwrite, bool))

    if os.path.exists(save_to) and warn_on_overwrite:
        tmpl = '[{file}:{line} {func}] Screenshot will overwrite existed file {path!r}'
        stack_frame = inspect.stack()[0]

        logging.warning(tmpl.format(file=stack_frame.filename,
        	                        line=stack_frame.lineno, 
        	                        func=stack_frame.function,
        	                        path=os.path.abspath(save_to)))


    if not url.startswith('http'): 
        url = 'http://' + url

        tmpl = '[{file}:{line} {func}] URL not starts with \'http\' - it will be added automaticly'
        stack_frame = inspect.stack()[0]

        logging.warning(tmpl.format(file=stack_frame.filename,
                                    line=stack_frame.lineno,
                                    func=stack_frame.function))


    browser = webdriver.Firefox()
    browser.get(url)
    browser.save_screenshot(save_to)
    browser.quit()