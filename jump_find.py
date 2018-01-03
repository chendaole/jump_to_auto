import cv2
from PIL import Image
from numpy import nper

path_chess = './res/chess.jpg'


def find_chess(stage_path):
    im_chess = cv2.imread(path_chess, 0)
    im_stage = cv2.imread(stage_path, 0)

    res = cv2.matchTemplate(im_stage, im_chess, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if max_val > 0.8:
        im_chess_ = Image.open(path_chess)
        width, height = im_chess_.size
        return (max_loc[0] + width / 2, max_loc[1] + height / 2)
    return (-1, -1)


def find_target(stage_path, chess_rect):
    im = cv2.imread(stage_path)
    im = cv2.GaussianBlur(im,(5,5),0)
    im_canny = cv2.Canny(im, 1, 10)
    chess_x, chess_y = chess_rect
    im_chess = Image.open(path_chess)
    w, h = im_chess.size

    for k in range(chess_y - h / 2, chess_y + h / 2):
        for b in range(chess_x - w / 2, chess_x + w / 2):
            im_canny[k][b] = 0


    cv2.imwrite('./last.png', im_canny)


chess_rect = find_chess('./res/stage.png')

find_target('./res/stage.png', chess_rect)