import os
import sys
import random
import argparse
import requests


from jinja2 import Environment, FileSystemLoader
    
DEFAULT_ITERS = 10
DEFAULT_OUT_DIR = 'dataset'
DEFAULT_TEXTURES_DIR = 'textures'
TEMPLATE_NAME = 'template.html'
TEMPLATES_DIR = 'templates'
WORDS_RUS = os.path.join(TEMPLATES_DIR, 'Russian.txt')
WORDS_ENG = os.path.join(TEMPLATES_DIR, 'English.txt')
PAGE_RESOLUTION = (1500, 3000)
MAX_SHIFT = PAGE_RESOLUTION[0] // 3    #max left shift of a text
MAX_BRIGHTNESS = 400
MIN_BRIGHTNESS = 50

FONTS_LIST = ['Arial', 'Verdana', 'Times', 'Times New Roman', \
              'Georgia', 'Trebuchet MS', 'Sans', 'Comic Sans MS',
              'Courier New', 'Webdings', 'Garamond', 'Helvetica']
DEFAULT_WORDS_LIST = ['SAMPLE', 'TEXT']

#To make it work: download all branch
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(CURRENT_DIR, '..'))
from rate_utils import make_screenshot, Driver

rand_size = lambda: random.randint(14,64)
rand_col = lambda: random.randint(0, 255)

def random_color(max_br=MAX_BRIGHTNESS, min_br=MIN_BRIGHTNESS):
    assert max_br > min_br
    assert min_br < 255 * 3
    while True:
        r = rand_col()
        g = rand_col()
        b = rand_col()
        if r + g + b <= max_br and r + g + b >= min_br:
            return 'rgb(%d,%d,%d)'%(r,g,b)

def read_words(path):
    assert os.path.exists(path)
    with open(path, 'r') as f:
        words = f.read().split()
    return words

env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
def generate_page(env=env, template_name=TEMPLATE_NAME,
                                    words=DEFAULT_WORDS_LIST,
                                    resolution=PAGE_RESOLUTION,
                                    textures_path=DEFAULT_TEXTURES_DIR):
    screen_w, screen_h = resolution
    textures_path = os.path.abspath(textures_path)

    #text
    lines = []
    cur_h = 0
    while cur_h < screen_h:
        line = {}
        
        #repeat line
        if len(lines) > 0 and random.random() > 0.7:
            line = lines[len(lines) - 1].copy()
            shift_x = line['shift_x']
            cur_h -= line['size']
            line['shift_y'] = cur_h
        else:
            line['font'] = FONTS_LIST[random.randint(0, 
                                                len(FONTS_LIST) - 1)]
            line['size'] = rand_size()
            shift_x = random.randint(0, MAX_SHIFT)
            line['shift_x'] = shift_x
            line['shift_y'] = cur_h
            line['color'] = random_color()
        
        characters = int(((screen_w - shift_x) // line['size']))
        line_len = 0
        text = ""
        while line_len < characters:    
            word_n = random.randint(0, len(words) - 1)
            line_len += len(words[word_n]) + 1
            if line_len >= characters:
                break
            text += words[word_n] + ' '

        line['text'] = text
        lines.append(line)
        cur_h += line['size'] * 3

    #texture
    dir_files = os.listdir(textures_path)
    jpg = [x for x in dir_files if( x.endswith('.jpg')or\
                                                    x.endswith('.png'))]
    if(len(jpg) > 0):
        img_name = jpg[random.randint(0, len(jpg) - 1)]
        img_path = os.path.join('..', textures_path, img_name) 
    else:
        img_path = None   #Nothing wrong, if we specify bad path in html 
    template = env.get_template(template_name)
    html = template.render(bckgrnd=img_path,
                           lines=lines,
                           rand_col=rand_col,
                           rand_size=rand_size)
    return html
    
    
def save_page(page, name='sample_name.html', out_dir=DEFAULT_OUT_DIR):
    out_abs = os.path.abspath(out_dir)
    if not os.path.exists(out_abs):
        os.makedirs(out_abs)
    
    out_html = os.path.join(out_abs, name)
    with open(out_html, 'w') as fh:
        fh.write(page)

def existed_file_type(value):
    if not os.path.exists(value): 
        raise argparse.ArgumentError()
    return value

def arguments():
    parser = argparse.ArgumentParser(description ='This script allows \
                     you to get dataset of random generated web pages')

    parser.add_argument('--iters', type=int, default=DEFAULT_ITERS, 
                                    help='Enter number of \
                                    pages, which you want to get')
    parser.add_argument('--out_dir', type=str, default=DEFAULT_OUT_DIR,
                                    help = 'Enter path to directory,\
                                    where you want to save data')
    parser.add_argument('--textures', type=existed_file_type, 
                                    default=DEFAULT_TEXTURES_DIR,
                                    help = 'Enter path to directory,\
                                    where textures are. They should \
                                    ends with <.jpg> or <.png>')
    parser.add_argument('--res_x', type=int, 
                                    default=PAGE_RESOLUTION[0],
                                    help='Resolution of page. Be \
                                    carefull: it may looks wrong if \
                                    resolution is too large')
    parser.add_argument('--res_y', type=int, 
                                    default=PAGE_RESOLUTION[1],
                                    help='Resolution of page.')
    parser.add_argument('--scrn', action='store_true', 
                        help = 'If you want to store screenshots too')
    parser.add_argument('--rus', action='store_true', 
                        help = 'If you want to use russian words')
    parser.add_argument('--mix', action='store_true', 
                        help = 'If you want to use russian and \
                                                        english words')

    return parser.parse_args()

if __name__ == '__main__':
    args = arguments()
    
    need_scrn = args.scrn
    if need_scrn:
        driver = Driver()
    try:
        if args.mix:
            words = read_words(WORDS_RUS) + read_words(WORDS_ENG)
        else:
            if args.rus:
                words = read_words(WORDS_RUS)
            else:
                words = read_words(WORDS_ENG)
        for i in range(args.iters): 
            page = generate_page(words=words,
                                    textures_path=args.textures,
                                    resolution=(args.res_x, args.res_y))
            #save
            hname = '%s.html'%(i+1)
            iname = '%s.png'%(i+1)
            save_page(page, name=hname, out_dir=args.out_dir)
            if need_scrn:
                abspath = os.path.abspath(args.out_dir)
                page_path = 'file://' + os.path.join(abspath, hname)
                img_path = os.path.join(abspath, iname)
                make_screenshot(page_path, path=img_path, driver=driver,
                                                        sleep_time=0)
    finally:
        if need_scrn:
            driver.close()