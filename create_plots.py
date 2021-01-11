import argparse
import os.path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors

from generate_data import get_results

FONT_SIZE = 24
PINK = '#f505d5'
ORANGE = '#eb7413'
LIGHT_BLUE = '#05bdf5'


def create_plot(min_x: int = None, max_x: int = None, min_y: int = None, max_y: int = None,
                data_csv: str = 'data/default_data.csv', img_file: str = None,
                plot_2i3i4i: bool = False, plot_upper_lower_curves: bool = False, figsize: (int, int) = (16, 16),
                dpi: int = 100):
    if min_x < 1:
        raise ValueError('min_x must be >= 1')
    if min_y < 0:
        raise ValueError('min_y must be >= 0')
    if min_x >= max_x:
        raise ValueError('min_x must be < max_x')
    if min_y >= max_y:
        raise ValueError('min_y must be ><max_y')

    data = np.genfromtxt(data_csv, delimiter=',')
    data = data[::-1]
    if None not in [min_x, max_x, min_y, max_y]:
        data = data[min_y:max_y + 1, min_x - 1:max_x]

    cmap = colors.ListedColormap(['black', 'white'])
    fig, ax = plt.subplots(figsize=figsize)

    ax.xaxis.set_tick_params(labelsize=24)
    ax.yaxis.set_tick_params(labelsize=24)
    ax.imshow(data, cmap=cmap, origin='lower')

    ax.set_xlim([-.5, max_x - min_x + .5])
    ax.set_ylim([-.5, max_y - min_y + .5])

    if plot_2i3i4i:
        x = np.linspace(min_x, max_x)
        ax.plot(x, get_2i_curve(x), color='green', linewidth=6)
        ax.plot(x, get_3i_curve(x), color='red', linewidth=6)
        ax.plot(x, get_4i_curve(x), color='blue', linewidth=6)

    if plot_upper_lower_curves:
        for curve, color in [(get_upper_curves, PINK), (get_lower_curves, LIGHT_BLUE)]:
            i = 0
            while i < 100:
                x = np.linspace(min_x, max_x)
                if max(curve(x, i)) < min_y:
                    i += 1
                else:
                    break
            while True:
                values_min_x = min([x for x in range(min_x, max_x) if curve(x, i) < get_2i_curve(x)])
                curve_domain = np.linspace(values_min_x, max_x)
                curve_range = curve(curve_domain, i)
                if min(curve_range > max_y):
                    break
                ax.plot(curve_domain - min_x, curve_range - min_y, color=color, linewidth=4)
                i += 1

    original_xticks = ax.get_xticks()
    new_xticks = []
    for tick in original_xticks:
        if min_x == 1:
            if min_x <= tick <= max_x:
                new_xticks.append(tick)
            elif tick == 0:
                new_xticks.append(1)
            continue
        if min_x <= tick + min_x <= max_x:
            new_xticks.append(tick + min_x)
    new_x_tick_locations = [0 if x == 1 else x - min_x for x in new_xticks]
    ax.set_xticks(new_x_tick_locations)
    ax.set_xticklabels(np.array(new_xticks).astype(int))
    original_yticks = ax.get_yticks()
    ax.set_yticklabels(np.array([y + min_y for y in original_yticks]).astype(int))
    ax.set_xlabel('Previous Pick', fontsize=FONT_SIZE)
    ax.set_ylabel('Number of Stones Left', fontsize=FONT_SIZE)
    ax.set_aspect('auto')
    ax.tick_params(pad=10)
    [i.set_linewidth(3) for i in ax.spines.values()]
    [i.set_edgecolor('gray') for i in ax.spines.values()]

    format = img_file.split('.')[-1]

    if img_file:
        plt.savefig(img_file, bbox_inches='tight', format=format, dpi=dpi)
    else:
        plt.show()


def get_lower_curves(x, i):
    b = (2 * i - 1) / 3
    c = i / 3
    return -(2 / 3) * x ** 2 + b * x + c


def get_upper_curves(x, i):
    b = i * (2 / 3)
    c = -(4 + i) / 3
    return -(2 / 3) * x ** 2 + b * x + c


def get_fig_dims(width, height):
    ratio = width / height * 20
    if ratio > 1:
        return 16 * ratio, 16
    return 16, 16 / ratio


def get_2i_curve(x):
    return x ** 2 - (3 / 2) * x - 1


def get_3i_curve(x):
    return (2 / 3) * x ** 2 + (2 / 3) * x - 2


def get_4i_curve(x):
    return (1 / 2) * x ** 2 + (3 / 4) * x - (3 / 4)


def figsize(s):
    try:
        x, y = map(int, s.split(','))
        return x, y
    except:
        raise argparse.ArgumentTypeError("figsize must be x,y")


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="python %(prog)s [--x_min] [--x_max] [--y_min] [--y_max] [--img_file] [--data_file] [--figsize] [--show-i-curves] [--dpi]",
        description="Create results from nim game."
    )
    parser.add_argument('-xl', '--x_min', help='minimum x value displayed on output', default=1, type=int)
    parser.add_argument('-xh', '--x_max', help='maximum x value displayed on output', default=100, type=int)
    parser.add_argument('-yl', '--y_min', help='minimum y value displayed on output', default=0, type=int)
    parser.add_argument('-yh', '--y_max', help='maximum y value displayed on output', default=2000, type=int)
    parser.add_argument('--img-file', help='filename of output img', dest='img_file', type=str)
    parser.add_argument('--data-file', help='filename of data to read instead of generating new data', dest='data_file',
                        type=str)
    parser.add_argument('--figsize', help='tuple of width, height in inches', type=figsize, default=(16, 16))
    parser.add_argument('-i', '--show-i-curves', dest='show_i_curves', help='if true, output will display i curves',
                        action='store_true')
    parser.add_argument('-u', '--show-upper-lower-curves',
                        help='if true, output will display the upper and lower curves',
                        dest='show_upper_lower_curves', action='store_true')
    parser.add_argument('-d', '--dpi',
                        help='dots per inch (dpi) for output figure',
                        default=100, type=int)
    return parser


def validate_input(x_min: int, x_max: int, y_min: int, y_max: int):
    if x_min < 1: raise ValueError('x_min must be >= 1')
    if x_min >= x_max: raise ValueError('x_min must be less than x_max')
    if y_min < 0: raise ValueError('y_min must be >= 0')
    if y_min >= y_max: raise ValueError('y_min must be <= y_max')


if __name__ == "__main__":
    parser = init_argparse()
    args = parser.parse_args()
    x_min = args.x_min
    x_max = args.x_max
    y_min = args.y_min
    y_max = args.y_max

    validate_input(x_min, x_max, y_min, y_max)

    if not os.path.isdir('data'):
        print('Creating data directory.')
        os.makedirs('data')
    if not os.path.isdir('imgs'):
        print('Creating imgs directory')
        os.makedirs('imgs')

    data_file = args.data_file if args.data_file else f'data/{y_min}-{y_max}_{x_min}-{x_max}.csv'
    if not os.path.isfile(data_file):
        print('Generating data')
        get_results(y_max, x_max, data_file)
        print(f'Data wrote to: {data_file}')
    else:
        print(f'Using data from file: {data_file}')

    img_file = args.img_file if args.img_file else f'imgs/{y_min}-{y_max}_{x_min}-{x_max}.png'
    print(f'Generating plot...')
    create_plot(x_min, x_max, y_min, y_max, img_file=img_file, figsize=args.figsize, data_csv=data_file,
                plot_2i3i4i=args.show_i_curves, plot_upper_lower_curves=args.show_upper_lower_curves, dpi=args.dpi)
    print(f'Plot available at {img_file}')
