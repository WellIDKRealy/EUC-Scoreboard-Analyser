import cv2
import numpy as np
import easyocr
import json

import math
import re

import sys

class IMG_DATA:
    def __init__(self, filtered, debug, ocr):
        self.filtered = filtered
        self.debug = debug
        self.ocr = ocr

class IO_DATA:
    def __init__(self, log, debug, debug_output, worker_no):
        self.log = log
        self.debug = debug
        self.debug_output = debug_output

        self.worker_no = worker_no

    def print_log(self, msg):
        if self.log:
            print(f'[{self.worker_no}] {msg}', file=sys.stderr)

    def print_debug(self, msg):
        if self.debug:
            print(f'[{self.worker_no}] {msg}', file=sys.stderr)

def crop_out(img):
    height, width = img.shape[:-1]

    return img[math.floor(0.11*height):math.floor(0.81*height),
               math.floor(0.13*width):math.floor(0.85*width)]

def filter_background(img):
    grayscale = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)[:,:,2]
    _, thresh = cv2.threshold(grayscale, 100, 255, cv2.THRESH_BINARY)

    return thresh

def filter_background_ocr(img):
    grayscale = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)[:,:,2]
    # thresh = cv2.adaptiveThreshold(grayscale, 0, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

    # print(thresh.shape)

    return grayscale

# DATA EXTRACTION

def get_team_one(img):
    width = img.shape[1]//2
    return img[:, :width]

def get_team_two(img):
    width = img.shape[1]//2
    return img[:, width:]

def find_template(img, template):
    result = cv2.matchTemplate(template, img, cv2.TM_SQDIFF_NORMED)
    mn,_,mnLoc,_ = cv2.minMaxLoc(result)

    return mnLoc

def ocr(img, reader, io, sep=' ', whitelist=None):
    # os.chdir(io.debug_OUTPUT)
    # string = pytesseract.image_to_string(img, lang='eng', config='--psm 7').strip()
    # os.chdir(CWD)

    height, width = img.shape[0:2]

    factor = 512/width if 512/width > 1 else 1

    img = cv2.resize(img, None, fx=factor, fy=factor, interpolation=cv2.INTER_CUBIC)

    # kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    # img = cv2.dilate(img, kernel)
    # img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)[:,:,2]
    # cv2.imwrite('/tmp/test.png', img)

    string = reader.readtext(img, paragraph=True, detail=0, text_threshold=0.5, allowlist=whitelist)

    assert(string != [])
    return string[0]

def extract_int(string):
    string = string.replace('O', '0').replace('S', '5')
    groups = re.match('[^\d]*(\d+)[^\d]*', string).groups()
    return int(groups[0])

def get_int_template(dimg, template, reader, io, factor_left=0, factor_right=1):
    x, y = find_template(dimg.filtered, template)
    rows, cols = template.shape

    if io.debug:
        cv2.rectangle(dimg.debug, (x, y), (x + cols, y + rows), 255, 1)
        cv2.rectangle(dimg.debug, (x - math.floor(cols*factor_left), y), (x + math.floor(cols*factor_right), y + rows), 255, 2)

    img = dimg.ocr[y:(y + rows),
                   (x - math.floor(cols*factor_left)):(x + math.floor(cols*factor_right))]

    return int(ocr(img, reader, io, sep='', whitelist='0123456789'))

def get_faction_name_and_player_count(dimg, player_count_template, reader, io):
    factor_left = 3.5/7
    factor_right = 1
    factor_right_name = 4

    x, y = find_template(dimg.filtered, player_count_template)
    rows, cols = player_count_template.shape

    if io.debug:
        cv2.rectangle(dimg.debug, (x, y), (x + cols, y + rows), 255, 1)
        cv2.rectangle(dimg.debug, (x - math.floor(cols*factor_left), y), (x + math.floor(cols*factor_right), y + rows), 255, 2)
        cv2.rectangle(dimg.debug, (x - math.floor(cols*factor_left), y - rows*2), (x + math.floor(cols*factor_right_name), y), 255, 1)

    img_player_count = dimg.ocr[y:(y + rows),
                                (x - math.floor(cols*factor_left)):(x + math.floor(cols*factor_right))]

    img_name = dimg.ocr[y - rows*2:y,
                        x - math.floor(cols*factor_left):x + math.floor(cols*factor_right_name)]

    return (extract_int(ocr(img_player_count, reader, io)),
            ocr(img_name, reader, io))

# def get_player_count(img):
#     return get_int_template(img, player_count_template, 3.5/7, debug_img=debug_img)

def get_alive_count(dimg, alive_count_template, reader, io):
    return get_int_template(dimg, alive_count_template, reader, io, 3.5/5, 0)

def get_score(dimg, score_template, reader, io):
    return get_int_template(dimg, score_template, reader, io, -1, 8/6)

def get_bounding_lines(dimg, pixel_height, io):
    results = []
    height, width = dimg.filtered.shape

    lines = cv2.HoughLinesP(dimg.filtered, pixel_height, np.pi / 180, 50, None, math.floor(width*0.5), 0)
    for line in lines:
        start_x, start_y, end_x, end_y = line[0]
        if(abs(start_y - end_y) < 2):
            results.append(line[0])
            if io.debug:
                cv2.line(dimg.debug,
                         (start_x, start_y),
                         (end_x, end_y),
                         255,
                         3)

    assert(len(lines) == 2)

    if results[0][1] < results[1][1]:
        return (results[0], results[1])
    return (results[1], results[0])


def get_player_data(dimg, team_player_count, player_count, templates, reader, io):
    player_x, player_y = find_template(dimg.filtered, templates['player'])
    player_rows, player_cols = templates['player'].shape

    kills_x, kills_y = find_template(dimg.filtered, templates['kills'])
    kills_rows, kills_cols = templates['kills'].shape

    deaths_x, deaths_y = find_template(dimg.filtered, templates['deaths'])
    deaths_rows, deaths_cols = templates['deaths'].shape

    ping_x, ping_y = find_template(dimg.filtered, templates['ping'])
    ping_rows, ping_cols = templates['ping'].shape

    # Extrapolate location of Alive
    alive_rows = kills_rows
    alive_cols = kills_cols//5*10

    alive_x = (player_x + player_cols - alive_cols//2 + kills_x)//2
    alive_y = (player_y + kills_y)//2

    if io.debug:
        cv2.rectangle(dimg.debug,
                      (player_x, player_y),
                      (player_x+player_cols, player_y+player_rows),
                      255,
                      1)

        cv2.rectangle(dimg.debug,
                      (kills_x, kills_y),
                      (kills_x+kills_cols, kills_y+kills_rows),
                      255,
                      1)

        cv2.rectangle(dimg.debug,
                      (deaths_x, deaths_y),
                      (deaths_x+deaths_cols, deaths_y+deaths_rows),
                      255,
                      1)

        cv2.rectangle(dimg.debug,
                      (ping_x, ping_y),
                      (ping_x+ping_cols, ping_y+ping_rows),
                      255,
                      1)

        cv2.rectangle(dimg.debug,
                      (alive_x, alive_y),
                      (alive_x+alive_cols, alive_y+alive_rows),
                      255,
                      1)

    bound_up, bound_down = get_bounding_lines(dimg, 3, io)


    start_x, start_y, end_x = bound_up[:3]
    end_y = bound_down[1]

    # Adjust for line height
    start_y = start_y + 3
    end_y = end_y - 3

    # print(start_x, start_y, player_count)

    size_y = (end_y - start_y)/player_count
    isize_y = round(size_y)

    results = []
    for i in range(team_player_count):
        y = start_y + round(size_y*i)

        out = {}

        io.print_log(f'PROCESSING {i + 1}/{team_player_count}')

        NUMS = '0123456789'

        out['name'] = ocr(dimg.ocr[y:y + isize_y, player_x:player_x + player_cols], reader, io)
        out['alive'] = ocr(dimg.ocr[y:y + isize_y, alive_x:alive_x + alive_cols], reader, io)
        out['kills'] = ocr(dimg.ocr[y:y + isize_y, kills_x:kills_x + kills_cols], reader, io, whitelist=NUMS)
        out['deaths'] = ocr(dimg.ocr[y:y + isize_y, deaths_x:deaths_x + deaths_cols], reader, io, whitelist=NUMS)
        out['ping'] = ocr(dimg.ocr[y:y + isize_y, ping_x - ping_cols//4:ping_x + ping_cols], reader, io, whitelist=NUMS)

        if io.debug:
            cv2.rectangle(dimg.debug, (player_x, y), (player_x + player_cols, y + isize_y), 255, 2)
            cv2.rectangle(dimg.debug, (alive_x, y), (alive_x + alive_cols, y + isize_y), 255, 2)
            cv2.rectangle(dimg.debug, (kills_x, y), (kills_x + kills_cols, y + isize_y), 255, 2)
            cv2.rectangle(dimg.debug, (deaths_x, y), (deaths_x + deaths_cols, y + isize_y), 255, 2)
            cv2.rectangle(dimg.debug, (ping_x - ping_cols//4, y), (ping_x + ping_cols, y + isize_y), 255, 2)

        results.append(out)
    return results

# MAIN

def process_image(path, io):
    io.print_log('READING IMAGE')
    img = cv2.imread(path)

    # TEMPLATES

    height, width = img.shape[:-1]

    io.print_log('READING TEMPLATES FOR RESOLUTION')
    templates = {}
    templates['player'] = filter_background(cv2.imread(f'Templates/{width}x{height}/PlayerName.png'))
    templates['kills'] = filter_background(cv2.imread(f'Templates/{width}x{height}/Kills.png'))
    templates['deaths'] = filter_background(cv2.imread(f'Templates/{width}x{height}/Deaths.png'))
    templates['ping'] = filter_background(cv2.imread(f'Templates/{width}x{height}/Ping.png'))

    player_count_template = filter_background(cv2.imread(f'Templates/{width}x{height}/PlayerCount.png'))
    alive_count_template = filter_background(cv2.imread(f'Templates/{width}x{height}/AliveCount.png'))
    score_template = filter_background(cv2.imread(f'Templates/{width}x{height}/Score.png'))

    # END TEMPLATES

    io.print_log('FILTERING')

    cropped = crop_out(img)
    filtered = filter_background(cropped)
    ocr_img = filter_background_ocr(cropped)

    if io.debug:
        cv2.imwrite(f'{io.debug_output}/filtered.png', filtered)

    team_one = get_team_one(filtered)
    team_one = IMG_DATA(team_one, np.copy(team_one) if io.debug else None, get_team_one(ocr_img))

    team_two = get_team_two(filtered)
    team_two = IMG_DATA(team_two, np.copy(team_two) if io.debug else None, get_team_two(ocr_img))

    try:
        io.print_log('INITIALIZING OCR')
        reader = easyocr.Reader(['en'])

        io.print_log('SCRAPING PLAYER COUNTS')
        team_one_player_count, team_one_name = get_faction_name_and_player_count(team_one, player_count_template, reader, io)
        team_two_player_count, team_two_name = get_faction_name_and_player_count(team_two, player_count_template, reader, io)

        # team_one_player_count = get_player_count(team_one)
        # team_two_player_count = get_player_count(team_two)

        io.print_log('SCRAPING ALIVE COUNTS')
        team_one_alive_count = get_alive_count(team_one, alive_count_template, reader, io)
        team_two_alive_count = get_alive_count(team_two, alive_count_template, reader, io)

        io.print_log('SCRAPING SCORES COUNTS')
        team_one_score = get_score(team_one, score_template, reader, io)
        team_two_score = get_score(team_two, score_template, reader, io)

        player_count = max(team_one_player_count, team_two_player_count)

        io.print_log(f'PLAYER_COUNT: {team_one_player_count + team_two_player_count}')

        io.print_log('SCRAPING TEAM 1 PLAYER DATA')
        team_one_player_data = get_player_data(team_one, team_one_player_count, player_count, templates, reader, io)

        io.print_log('SCRAPING TEAM 2 PLAYER DATA')
        team_two_player_data = get_player_data(team_two, team_two_player_count, player_count, templates, reader, io)
    finally:
        if io.debug:
            cv2.imwrite(f'{io.debug_output}/team_one.png', team_one.debug)
            cv2.imwrite(f'{io.debug_output}/team_two.png', team_two.debug)
            io.print_debug(f'DEBUG OUTPUT: {io.output}')

    return {
        "path": path,
        'team1' : {
            'score': team_one_score,
            'name': team_one_name,
            'alive': team_one_alive_count,
            'players_no': team_one_player_count,
            'players': team_one_player_data
        },
        'team2' : {
            'score': team_two_score,
            'name': team_two_name,
            'alive': team_two_alive_count,
            'players_no': team_two_player_count,
            'players': team_two_player_data
        }}
