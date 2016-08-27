import os

import argparse

from rate_utils import make_screenshot, create_driver, get_html_source


SCR_NAME = 'img.png'
SOURCE_NAME = 'source.html'


def arguments():
    parser = argparse.ArgumentParser(description ='This script allows' +
    ' you to download web scrinshots')

    parser.add_argument('url', type = str 
                , help = 'Enter the url of page, which should be processed')
    parser.add_argument('path', type = str 
                , help = 'Enter the path to store')

    return parser.parse_args()

if __name__ == '__main__':
    try:
        args = arguments()
        driver = create_driver()
        
        scr_path = path.join(args.path, SCR_NAME)
        source_path = path.join(args.path, SOURCE_NAME)
        make_screenshot(args.url, path=scr_path, driver=driver)
        get_html_source(args.url, path=source_path, driver=driver)
        
        driver.close()
    except KeyboardInterrupt:
        print('\nExiting')
