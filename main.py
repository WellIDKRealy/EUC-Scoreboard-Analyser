import cv2
import numpy as np
import pytesseract
import json

import math
import re

import argparse
import tempfile
import sys
import os

# CLI

parser = argparse.ArgumentParser(
    prog='scoreboard-analyser',
    description='analyse EUC scoreboard screenshots',
    epilog='Report any bugs to <https://github.com/WellIDKRealy/EUC-Scoreboard-Analyser>')

parser.add_argument('scoreboard', help='scoreboard screenshots path')
parser.add_argument('-d', '--debug',
                    action='store_true',
                    help='enables debug mode')
parser.add_argument('-s', '--silent',
                    action='store_true',
                    help='suepresses unnecessary output')

args = parser.parse_args()

DEBUG = args.debug
SILENT = args.silent

# END CLI

# Setup environment

CWD = dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(CWD)

OUTPUT_PARENT ='/tmp/scoreboard-analyser-output'
if not os.path.isdir(OUTPUT_PARENT):
    os.mkdir(OUTPUT_PARENT)

OUTPUT = tempfile.TemporaryDirectory(dir=OUTPUT_PARENT).name
os.mkdir(OUTPUT)

def print_log(log):
    if not SILENT:
        print(log, file=sys.stderr)

def print_debug(debug):
    if DEBUG:
        print(debug, file=sys.stderr)

# END Setup environment

if not os.path.exists(args.scoreboard):
    print(f'No such file: {args.scoreboard}', file=sys.stderr)
    exit(2)

print_log('READING IMAGE')
img = cv2.imread(args.scoreboard)

def crop_out(img):
    height, width = img.shape[:-1]

    return img[math.floor(0.11*height):math.floor(0.81*height),
               math.floor(0.13*width):math.floor(0.85*width)]

def filter_background(img):
    v = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)[:,:,2]
    _, thresh = cv2.threshold(v,100,255,cv2.THRESH_BINARY)

    return thresh

print_log('FILTERING')
filtered = filter_background(crop_out(img))

if DEBUG:
    cv2.imwrite(f'{OUTPUT}/filtered.png', filtered)

# DATA EXTRACTION

def teams(img):
    width = img.shape[1]//2
    return (img[:, :width],
            img[:, width:])

def find_template(img, template):
    result = cv2.matchTemplate(template, img, cv2.TM_SQDIFF_NORMED)
    mn,_,mnLoc,_ = cv2.minMaxLoc(result)

    return mnLoc

def extract_image(img, start_x, start_y, end_x, end_y):
    width, height = img.shape
    return img[math.floor(start_y*height):math.floor(end_y*height),
               math.floor(start_x*width):math.floor(end_y*width)]

def ocr(img):
    os.chdir(OUTPUT)
    string = pytesseract.image_to_string(img, lang='eng', config='--psm 7').strip()
    os.chdir(CWD)

    return string

def extract_int(string):
    string = string.replace('O', '0')
    groups = re.match('[^\d]*(\d+)[^\d]*', string).groups()
    return int(groups[0])

def get_int_template(img, template, factor_left=0, factor_right=1, debug_img=None):
    x, y = find_template(img, template)
    rows, cols = template.shape

    if DEBUG:
        cv2.rectangle(debug_img, (x, y), (x + cols, y + rows), 255, 1)
        cv2.rectangle(debug_img, (x - math.floor(cols*factor_left), y), (x + math.floor(cols*factor_right), y + rows), 255, 1)

    img = img[y:(y + rows),
              (x - math.floor(cols*factor_left)):(x + math.floor(cols*factor_right))]

    return extract_int(ocr(img))

# TEMPLATES

print_log('READING TEMPLATES')
player_template = filter_background(cv2.imread('Templates/PlayerName.png'))
kills_template = filter_background(cv2.imread('Templates/Kills.png'))
deaths_template = filter_background(cv2.imread('Templates/Deaths.png'))
ping_template = filter_background(cv2.imread('Templates/Ping.png'))

player_count_template = filter_background(cv2.imread('Templates/PlayerCount.png'))
alive_count_template = filter_background(cv2.imread('Templates/AliveCount.png'))
score_template = filter_background(cv2.imread('Templates/Score.png'))

# END TEMPLATES

def get_faction_name_and_player_count(img, debug_img=None):
    factor_left = 3.5/7
    factor_right = 1
    factor_right_name = 4

    x, y = find_template(img, player_count_template)
    rows, cols = player_count_template.shape

    if DEBUG:
        cv2.rectangle(debug_img, (x, y), (x + cols, y + rows), 255, 1)
        cv2.rectangle(debug_img, (x - math.floor(cols*factor_left), y), (x + math.floor(cols*factor_right), y + rows), 255, 1)
        cv2.rectangle(debug_img, (x - math.floor(cols*factor_left), y - rows*2), (x + math.floor(cols*factor_right_name), y), 255, 1)

    img_player_count = img[y:(y + rows),
                           (x - math.floor(cols*factor_left)):(x + math.floor(cols*factor_right))]

    img_name = img[y - rows*2:y,
                   x - math.floor(cols*factor_left):x + math.floor(cols*factor_right_name)]

    return extract_int(ocr(img_player_count)), ocr(img_name)

# def get_player_count(img, debug_img=None):
#     return get_int_template(img, player_count_template, 3.5/7, debug_img=debug_img)

def get_alive_count(img, debug_img=None):
    return get_int_template(img, alive_count_template, 3.5/5, debug_img=debug_img)

def get_score(img, debug_img=None):
    return get_int_template(img, score_template, 0, 8/6, debug_img=debug_img)

def get_bounding_lines(img, debug_img=None):
    results = []
    height, width = img.shape

    lines = cv2.HoughLinesP(img, 3, np.pi / 180, 50, None, math.floor(width*0.5), 0)
    for line in lines:
        start_x, start_y, end_x, end_y = line[0]
        if(abs(start_y - end_y) < 2):
            results.append(line[0])
            if DEBUG:
                cv2.line(debug_img,
                         (start_x, start_y),
                         (end_x, end_y),
                         255,
                         3)

    assert(len(lines) == 2)

    if results[0][1] < results[1][1]:
        return (results[0], results[1])
    return (results[1], results[0])


def get_player_data(img, team_player_count, player_count, debug_img=None):
    player_x, player_y = find_template(img, player_template)
    player_rows, player_cols = player_template.shape

    kills_x, kills_y = find_template(img, kills_template)
    kills_rows, kills_cols = kills_template.shape

    deaths_x, deaths_y = find_template(img, deaths_template)
    deaths_rows, deaths_cols = deaths_template.shape

    ping_x, ping_y = find_template(img, ping_template)
    ping_rows, ping_cols = ping_template.shape

    # Extrapolate location of Alive
    alive_rows = kills_rows
    alive_cols = kills_cols//5*10

    alive_x = (player_x + player_cols - alive_cols//2 + kills_x)//2
    alive_y = (player_y + kills_y)//2

    if DEBUG:
        cv2.rectangle(debug_img,
                      (player_x, player_y),
                      (player_x+player_cols, player_y+player_rows),
                      255,
                      2)

        cv2.rectangle(debug_img,
                      (kills_x, kills_y),
                      (kills_x+kills_cols, kills_y+kills_rows),
                      255,
                      2)

        cv2.rectangle(debug_img,
                      (deaths_x, deaths_y),
                      (deaths_x+deaths_cols, deaths_y+deaths_rows),
                      255,
                      2)

        cv2.rectangle(debug_img,
                      (ping_x, ping_y),
                      (ping_x+ping_cols, ping_y+ping_rows),
                      255,
                      2)

        cv2.rectangle(debug_img,
                      (alive_x, alive_y),
                      (alive_x+alive_cols, alive_y+alive_rows),
                      255,
                      2)

    bound_up, bound_down = get_bounding_lines(img, debug_img=debug_img)

    start_x, start_y, end_x = bound_up[:3]
    end_y = bound_down[1]

    # print(start_x, start_y, player_count)

    size_y = (end_y - start_y)//player_count

    results = []
    for i in range(team_player_count):
        y = start_y + size_y*i

        out = {}

        print_log(f'PROCESSING {i + 1}/{team_player_count}')

        out['name'] = ocr(img[y:y + size_y, player_x:player_x + player_cols])
        out['alive'] = ocr(img[y:y + size_y, alive_x:alive_x + alive_cols])
        out['kills'] = ocr(img[y:y + size_y, kills_x:kills_x + kills_cols])
        out['deaths'] = ocr(img[y:y + size_y, deaths_x:deaths_x + deaths_cols])
        out['ping'] = ocr(img[y:y + size_y, ping_x - ping_cols//4:ping_x + ping_cols])

        if DEBUG:
            cv2.rectangle(debug_img, (player_x, y), (player_x + player_cols, y + size_y), 255, 2)
            cv2.rectangle(debug_img, (alive_x, y), (alive_x + alive_cols, y + size_y), 255, 2)
            cv2.rectangle(debug_img, (kills_x, y), (kills_x + kills_cols, y + size_y), 255, 2)
            cv2.rectangle(debug_img, (deaths_x, y), (deaths_x + deaths_cols, y + size_y), 255, 2)
            cv2.rectangle(debug_img, (ping_x - ping_cols//4, y), (ping_x + ping_cols, y + size_y), 255, 2)

        results.append(out)
    return results

team_one, team_two = teams(filtered)
team_one_debug = np.copy(team_one) if DEBUG else None
team_two_debug = np.copy(team_two) if DEBUG else None

try:
    print_log('SCRAPING PLAYER COUNTS')
    team_one_player_count, team_one_name = get_faction_name_and_player_count(team_one, debug_img=team_one_debug)
    team_two_player_count, team_two_name = get_faction_name_and_player_count(team_two, debug_img=team_two_debug)

    # team_one_player_count = get_player_count(team_one, debug_img=team_one_debug)
    # team_two_player_count = get_player_count(team_two, debug_img=team_two_debug)

    print_log('SCRAPING ALIVE COUNTS')
    team_one_alive_count = get_alive_count(team_one, debug_img=team_one_debug)
    team_two_alive_count = get_alive_count(team_two, debug_img=team_two_debug)

    print_log('SCRAPING SCORES COUNTS')
    team_one_score = get_score(team_one, debug_img=team_one_debug)
    team_two_score = get_score(team_two, debug_img=team_two_debug)

    player_count = max(team_one_player_count, team_two_player_count)

    print_log(f'PLAYER_COUNT: {team_one_player_count + team_two_player_count}')

    print_log('SCRAPING TEAM 1 PLAYER DATA')
    team_one_player_data = get_player_data(team_one, team_one_player_count, player_count, debug_img=team_one_debug)

    print_log('SCRAPING TEAM 2 PLAYER DATA')
    team_two_player_data = get_player_data(team_two, team_two_player_count, player_count, debug_img=team_two_debug)
finally:
    if DEBUG:
        cv2.imwrite(f'{OUTPUT}/team_one.png', team_one_debug)
        cv2.imwrite(f'{OUTPUT}/team_two.png', team_two_debug)
        print_debug(f'DEBUG OUTPUT: {OUTPUT}')

print(json.dumps({
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
    }}))
