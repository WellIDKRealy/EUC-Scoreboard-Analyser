import cv2
import numpy as np
import pytesseract
import sys
import os
if len(sys.argv) < 2:
    print(f'usage: {sys.argv[0]} screenshoot')
    exit(1)

if not os.path.isdir('Output'):
    os.mkdir('Output')

img = cv2.imread('SCREEN3.png')
copy = np.copy(img)

# Filter out background

def filter_backround(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    lower = np.array([0, 0, 100])
    upper = np.array([255, 255, 255])
    mask = cv2.inRange(img, lower, upper)

    return cv2.bitwise_and(img, img, mask=mask)

img = filter_backround(img)

cv2.imwrite('Output/copy.png', img)

# Crop only the important part

start = cv2.imread('Templates/start.png')
end  = cv2.imread('Templates/end.png')

def find_template(img, template):
    result = cv2.matchTemplate(template, img, cv2.TM_SQDIFF_NORMED)
    mn,_,mnLoc,_ = cv2.minMaxLoc(result)

    return mnLoc

start_rows,start_cols = start.shape[:2]
start_x, start_y = find_template(img, start)

# DEBUG

cv2.rectangle(copy,
              (start_x,start_y),
              (start_x+start_cols,start_y+start_rows),
              (0,0,255),
              2)

# END DEBUG

end_rows,end_cols = end.shape[:2]
end_x, end_y = find_template(img, end)

# DEBUG

cv2.rectangle(copy,
              (end_x,end_y),
              (end_x+end_cols,end_y+end_rows),
              (0,255,0),
              2)

# END DEBUG

# DEBUG

cv2.rectangle(copy,
              (start_x, start_y),
              (end_x+end_cols, end_y),
              (255, 0, 0),
              2)

# END DEBUG

# Split into team half's

team_one = img[start_y:end_y, start_x:end_x+end_cols//2]
team_two = img[start_y:end_y, start_x+end_cols//2:end_x+end_cols]

templates = [('PlayerName',
              cv2.imread('Templates/PlayerName.png'),
              '--psm 7'),
             ('Kills',
              cv2.imread('Templates/Kills.png'),
              '--psm 7 --user-patterns num.patterns'),
             ('Deaths',
              cv2.imread('Templates/Deaths.png'),
              '--psm 7 --user-patterns num.patterns'),
             ('Ping',
              cv2.imread('Templates/Ping.png'),
              '--psm 7 --user-patterns num.patterns')]

def half_get_data(half):
    # grayscale
    grayscale = cv2.cvtColor(half, cv2.COLOR_BGR2GRAY)
    _, grayscale = cv2.threshold(grayscale, 30, 255, cv2.THRESH_BINARY)

    borders = []

    last = False
    last_index = 0
    for index in range(grayscale.shape[0]):
        avg = sum(grayscale[index]) > 20*255

        if avg != last and index - last_index > 5:
            borders.append(index)
            last = avg
            last_index = index

    height, width = grayscale.shape

    ranges = []
    for start_y, end_y in zip(borders[0::2], borders[1::2]):
        ranges.append((start_y - 5, end_y + 5))
    ranges = ranges[2:]

    template_borders = []
    for _, template, _ in templates:
        rows, cols = template.shape[:2]
        x, y = find_template(half, template)

        cv2.rectangle(half, (x, y), (x + cols, y + rows), (255, 0, 0), 2)
        template_borders.append(x)
    template_borders.append(x + cols)

    # Fix ping
    template_borders[-2] = template_borders[-2] - 15

    template_ranges = []
    for start_x, end_x in zip(template_borders, template_borders[1:]):
        template_ranges.append((start_x, end_x))

    cv2.imwrite('Output/team_two_gray.png', grayscale)
    for start_y, end_y in ranges:
        for ((start_x, end_x), (name, _, config)) in zip(template_ranges, templates):
            img = grayscale[start_y:end_y, start_x:end_x];
            print(name, pytesseract.image_to_string(img, lang='eng', config=config).strip(), sep=':')
            #cv2.imwrite('Output/' + name + '2.png', img)
            cv2.rectangle(half, (start_x, start_y), (end_x, end_y), (255, 0, 0), 2)

print('Team One:')
half_get_data(team_one)
#print('Team Two:')
#half_get_data(team_two)

cv2.imwrite('Output/team_one.png', team_one)
cv2.imwrite('Output/team_two.png', team_two)
cv2.imwrite('Output/copy.png', copy)
