import numpy as np
import cv2

import argparse
import sys

def parse_args():
    parser = argparse.ArgumentParser("Image to ASCII")
    parser.add_argument("-i", "--input", type=str, help="input image")
    parser.add_argument("-o", "--output", type=str,
                        default=None, help="output text file (default: sys.stdout)")
    parser.add_argument("-n", "--num_cols", type=int, default=128,
                        help="number of character for output's width (default: maximum resolution)")
    args = parser.parse_args()
    return args


def main(opt):
    CHAR_LIST = {30: '{', 36: '9', 22: '|', 34: 'H', 28: '5', 23: '>', 45: 'g', 33: '2', 31: '3', 20: 'T', 32: 'V', 29: '4', 18: '*', 24: ']', 27: '}', 21: '\\', 42: '8',
                 40: '&', 25: '1', 19: ';', 37: 'W', 35: '#', 26: 'Z', 44: '0', 39: '6', 0: ' ', 16: '!', 14: '[', 41: '$', 43: '%', 6: '_', 13: ',', 5: '`', 12: '~', 47: '@', 17: '^'}
    keys = np.sort(list(CHAR_LIST.keys()))
    num_cols = opt.num_cols or np.inf
    image = cv2.imread(opt.input)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height, width = image.shape
    cell_width = width / num_cols
    cell_height = 2 * cell_width or np.inf
    num_rows = int(height / cell_height)
    if num_cols > width or num_rows > height:
        cell_width = 1
        cell_height = 2
        num_cols = int(width / cell_width)
        num_rows = int(height / cell_height)

    with (open(opt.output, "w") if opt.output else sys.stdout) as output_file:
        for i in range(num_rows):
            for j in range(num_cols):
                output_file.write(
                    CHAR_LIST[keys[np.searchsorted(keys, max(keys) * (1-np.mean(image[int(i * cell_height):int(
                        (i + 1) * cell_height), int(j * cell_width):int((j + 1) * cell_width)])/255))]]
                )
            output_file.write("\n")


if __name__ == '__main__':
    opt = parse_args()
    main(opt)
