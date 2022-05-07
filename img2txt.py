"""
@author: Viet Nguyen <nhviet1009@gmail.com>
"""
import argparse

import cv2
import numpy as np


def get_args():
    parser = argparse.ArgumentParser("Image to ASCII")
    parser.add_argument("-i","--input", type=str, help="input image")
    parser.add_argument("-o","--output", type=str, default="output.txt", help="output text file")
    parser.add_argument("-n","--num_cols", type=int, default=128, help="number of character for output's width")
    args = parser.parse_args()
    return args


def main(opt):
    CHAR_LIST = {30: '{', 36: '9', 22: '|', 34: 'H', 28: '5', 23: '>', 45: 'g', 33: '2', 31: '3', 20: 'T', 32: 'V', 29: '4', 18: '*', 24: ']', 27: '}', 21: '\\', 42: '8', 40: '&', 25: '1', 19: ';', 37: 'W', 35: '#', 26: 'Z', 44: '0', 39: '6', 0: ' ', 16: '!', 14: '[', 41: '$', 43: '%', 6: '_', 13: ',', 5: '`', 12: '~', 47: '@', 17: '^'}
    keys = np.sort(list(CHAR_LIST.keys()))
    num_cols = opt.num_cols
    image = cv2.imread(opt.input)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height, width = image.shape
    cell_width = width / opt.num_cols
    cell_height = 2 * cell_width
    num_rows = int(height / cell_height)
    if num_cols > width or num_rows > height:
        print("Too many columns or rows. Use default setting")
        cell_width = 6
        cell_height = 12
        num_cols = int(width / cell_width)
        num_rows = int(height / cell_height)

    output_file = open(opt.output, 'w')
    for i in range(num_rows):
        for j in range(num_cols):
            output_file.write(
                CHAR_LIST[keys[np.searchsorted(keys, max(keys) * (1-np.mean(image[int(i * cell_height):int(
                    (i + 1) * cell_height), int(j * cell_width):int((j + 1) * cell_width)])/255))]]
            )
        output_file.write("\n")
    output_file.close()


if __name__ == '__main__':
    opt = get_args()
    main(opt)
