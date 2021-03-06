from typing import Optional, Dict, Any, Union, List

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.axes import Axes
from matplotlib.colors import to_rgb
from mpl_format.axes import AxesFormatter
from mpl_format.axes.axis_utils import new_axes
from pandas import DataFrame
from seaborn import color_palette


def plot_likert_scales_temp(data: DataFrame, align_category: str,
                            color_palette_name: Optional[str] = "RdBu",
                            order: Optional[List[str]]= None,
                            color: Optional[Union[Dict[str,str], List[str]]]
                            = None,
                            align_type: Optional[str] = 'center',
                            bar_kws: Optional[Dict[str, Any]] = None,
                            legend_kws: Optional[Dict[str, Any]] = None,
                            line_at_zero: Optional[bool] = True,
                            show_perc: Optional[bool] = True,
                            min_label_perc: Optional[float] = 3.0,
                            bar_pc_to_show: Optional[float] = 0.03,
                            title: Optional[str] = None,
                            qname_mapping: Optional[Dict[str, str]] = None,
                            ax: Optional[Axes]=None):
    """

    :param data: DataFrame with counts of Likert choices as columns and
    question names as rows. DataFrame columns need to be sorted with most
    negative choice as the first column and most positive choice as the
    last column.
    :param align_category: Likert scale/choice name to be aligned at 0.
    :param order: Order of the data columns
    :param color: Dict or List to specify the color of the plot
    :param color_palette_name: name of seaborn color palette to plot likert
    bars
    :param align_type: 'center' of 'left'. Default is center meaning
    mid_cat align at 0. If align_type is left, mid_cat align to the left.
    :param bar_kws: optional keyword arguments for patches.Rectangle
    :param legend_kws: optional keyword arguments for ax.legend
    :param line_at_zero: optional vertical dash line at x = 0
    :param show_perc: option to show percentage of count for each likert choice
    :param min_label_perc: only show percentage text if it is greater or
    equal to the minimum percentage set here. For example, to set it to 1.5%,
    input as 1.5. Default is 3
    :param bar_pc_to_show: only show percentage of text if length of each
    bar is greater than maximum bar length * bar_pc_to_show
    :param title: option to set title for the plot
    :param qname_mapping: option to map the name of the question on
    the y axis. input as {'q1 old name':'q1 new name','q2 old name':'q2 new
    name'}
    :return:
    """

    if order is not None:
        data = data[order]

    fc = None
    if color is None:
        fc = color_palette(color_palette_name, n_colors=data.shape[1])

    if bar_kws is None:
        bar_kws = {'height': 0.8}
    elif 'height' not in bar_kws:
        bar_kws['height'] = 0.8

    if legend_kws is None:
        legend_kws = {'edgecolor': 'white', 'loc': 'upper center',
                      'bbox_to_anchor': (.5, -0.05)}
    elif 'edgecolor' not in legend_kws:
        legend_kws['edgecolor'] = 'white'
    elif 'loc' not in legend_kws:
        legend_kws['loc'] = 'upper center'
    elif 'bbox_to_anchor' not in legend_kws:
        legend_kws['bbox_to_anchor'] = (.5, -0.05)

    neg_x = []
    pos_x = []
    y_position = []
    y = len(data) * bar_kws['height'] + 0.5 - 0.5 * bar_kws['height'] + len(
        data)*0.2
    ax = ax or new_axes()

    for name, row in data.iterrows():
        align_index = data.columns.get_loc(align_category)
        if align_type == 'center':
            mid_point = -row[align_category] / 2
        elif align_type == 'left':
            mid_point = 0
        else:
            raise ValueError('align type can only be center or left')

        if color is not None:
            if type(color) == dict:
                fc_mid = color[align_category]
                r,b,g = to_rgb(fc_mid)
            elif type(color) == list:
                fc_mid = color[align_index]
                r, b, g = to_rgb(fc_mid)
            else:
                raise TypeError('color can only be dict or list')
        else:
            fc_mid = fc[align_index]
            r, b, g = fc_mid

        rect = patches.Rectangle((mid_point, y), row[align_category],
                                 facecolor= fc_mid,
                                 **bar_kws)
        ax.add_patch(rect)
        y_center = y + 0.5 * bar_kws['height']
        text_color = 'white' if r * g * b < 0.25 else 'black'
        bar_perc = 100 * row[align_category]/row.sum()
        if show_perc and bar_perc >= min_label_perc and row[
            align_category] > (data.max().max() * bar_pc_to_show):
            ax.text(mid_point+row[align_category]/2, y_center,
                '{:.0f}%'.format(bar_perc),
                ha='center', va='center', color =text_color)
        print()
        for ind, column_name in enumerate(data.columns):
            if ind == align_index:
                if ind == 0:
                    neg_x.append(mid_point-0.5)
                    continue
                elif ind == len(data.columns)-1:
                    x = sum(row[x] for i, x in enumerate(data.columns) if
                            i == ind) + mid_point
                    pos_x.append(x + row[column_name])
                    continue
                else:
                    continue
            elif ind < align_index:
                x = -sum(row[x] for i, x in enumerate(data.columns) if
                         ind <= i < align_index) + mid_point
                neg_x.append(x)
            else:
                x = sum(row[x] for i, x in enumerate(data.columns) if
                        align_index <= i < ind) + mid_point
                pos_x.append(x + row[column_name])

            if color is not None:
                fc_i = color[column_name] if type(color) == dict else color[
                    ind]
                r, b, g = to_rgb(fc_mid)
            else:
                fc_i = fc[ind]
                r, b, g = fc_i
            rect = patches.Rectangle((x, y), row[column_name],
                                     facecolor=fc_i, **bar_kws)
            ax.add_patch(rect)
            text_color = 'white' if r * g * b < 0.25 else 'black'
            bar_perc = 100 * row[column_name] / row.sum()
            print(column_name, row[column_name],row[
            column_name] > (data.max().max() * 0.01),bar_perc >= min_label_perc)

            if show_perc and bar_perc >= min_label_perc and row[
            column_name] > (data.max().max() * bar_pc_to_show):
                ax.text(x + row[column_name] / 2, y_center,
                        '{:.0f}%'.format(bar_perc),
                        ha='center', va='center', color=text_color)

        y_position.append(y_center)
        y = y - bar_kws['height']-0.2


    plt.xlim(min(neg_x) * 1.1, max(pos_x) * 1.1)
    plt.ylim(0.02, (max(y_position) + 0.5 * bar_kws['height']) * 1.05)
    if line_at_zero:
        z = plt.axvline(0, linestyle='--', color='black', alpha=.5)
        z.set_zorder(-1)
    ax.set_yticks(y_position)
    ax.set_yticklabels(data.index)
    axf = AxesFormatter(ax)
    axf.map_y_tick_labels(qname_mapping).set_x_label_text('Count')
    axf.set_title_text(title)

    handles, labels = ax.get_legend_handles_labels()
    for ind, column_name in enumerate(data.columns):
        if color is not None:
            hc = color[column_name] if type(color) == dict else color[
                ind]
        else:
            hc = fc[ind]
        patch = mpatches.Patch(color=hc, label=column_name)
        handles.append(patch)
    ax.legend(handles=handles, ncol=data.shape[1], **legend_kws)
    return ax
