import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors

FONT_SIZE = 24
PINK = '#f505d5'
ORANGE = '#eb7413'
LIGHT_BLUE = '#05bdf5'


def create_plot(min_x: int = None, max_x: int = None, min_y: int = None, max_y: int = None, file_name: str = None,
                plot_2i3i4i: bool = False, plot_upper_lower_curves: bool = False, figsize: (int, int) = (16, 16)):
    if min_x < 1:
        raise IndexError('min_x must be >= 1')
    if min_y < 0:
        raise IndexError('min_y must be >= 0')
    if min_x >= max_x:
        raise IndexError('min_x must be < max_x')
    if min_y >= max_y:
        raise IndexError('min_y must be ><max_y')

    data_csv = 'test_data.csv'
    data = np.genfromtxt(data_csv, delimiter=',')
    data = data[::-1]
    if None not in [min_x, max_x, min_y, max_y]:
        data = data[min_y:max_y + 1, min_x - 1:max_x]

    cmap = colors.ListedColormap(['black', 'white'])
    fig, ax = plt.subplots(figsize=figsize)

    ax.xaxis.set_tick_params(labelsize=24)
    ax.yaxis.set_tick_params(labelsize=24)
    ax.imshow(data, cmap=cmap, origin='lower')

    ax.set_xlim([1, max_x - min_x])
    ax.set_ylim([0, max_y - min_y])

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

    if file_name:
        plt.savefig(file_name, bbox_inches='tight', dpi=1000)
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
    return x ** 2 - (5 / 2) * x + 1 / 2


def get_3i_curve(x):
    return (2 / 3) * x ** 2 - (5 / 3) * x - 1


def get_4i_curve(x):
    return (1 / 2) * x ** 2 + (1 / 4) * x - (3 / 2)


def main():
    create_plot(50, 100, 3500, 4000, 'imgs/50-100_3500-4000_upper_lower_curves_V1.png', plot_upper_lower_curves=True)


# TODOS:
#   - imgs/1-100_0-4000_V1.png


main()
