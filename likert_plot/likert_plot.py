from typing import List, Optional, Tuple, Dict, Any

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib import patches
from mpl_format.axes.axis_utils import new_axes
from pandas import DataFrame


def plot_likert_scales(data: DataFrame, align_category: str, color: List[str],
                       align_type: Optional[str] = 'center',
                       bar_kws: Optional[Dict[str, Any]] = None,
                       legend_kws: Optional[Dict[str, Any]] = None,
                       legend_edge_color: Optional[str] = 'white',
                       line_at_zero: Optional[bool] = True,
                       legend_loc: Optional[str] = 'upper center',
                       legend_bbox_to_anchor: Optional[Tuple[float, float]] = (
                       .5, -0.05)):
    """

    :param data: DataFrame with counts of Likert choices as columns and
    question names as rows. DataFrame columns need to be sorted with most
    negative choice as the first column and most positive choice as the
    last column.
    :param align_category: Likert scale/choice name to be aligned at 0.
    :param color: list of color names for each likert scale. Needs to be
    sorted with the color for the most negative choice as the first item and
    color for the most positive choice as the last item.
    :param align_type: 'center' of 'left'. Default is center meaning
    mid_cat align at 0. If align_type is left, mid_cat align to the left.
    :param bar_height: bar height. default is 0.8
    :param line_width:
    :param bar_edge_color:
    :param legend_edge_color:
    :param line_at_zero: Optional vertical dashline at x = 0
    :param legend_loc: location of legend. Default is upper center
    :param legend_bbox_to_anchor: location (x,y) coordinates of legend box
    :return:
    """
    neg_x = []
    pos_x = []
    y_position = []
    y = len(data) + 0.5 - 0.5 * bar_height
    ax = new_axes()

    for name, row in data.iterrows():
        mid_index = data.columns.get_loc(align_category)
        if align_type == 'center':
            mid_point = -row[align_category] / 2
        elif align_type == 'left':
            mid_point = 0
        else:
            raise ValueError('align type can only be center or left')
        rect = patches.Rectangle((mid_point, y), row[align_category],
                                 bar_height,
                                 edgecolor=bar_edge_color,
                                 facecolor=color[mid_index])
        ax.add_patch(rect)
        for ind, column_name in enumerate(data.columns):
            if ind < mid_index:
                x = -sum(row[x] for i, x in enumerate(data.columns) if
                         ind <= i < mid_index) + mid_point
                neg_x.append(x)
                rect = patches.Rectangle((x, y), row[column_name], bar_height,
                                         edgecolor=bar_edge_color,
                                         facecolor=color[ind])
                ax.add_patch(rect)
            elif ind > mid_index:
                x = sum(row[x] for i, x in enumerate(data.columns) if
                        mid_index <= i < ind) + mid_point
                pos_x.append(x + row[column_name])
                rect = patches.Rectangle((x, y), row[column_name], bar_height,
                                         linewidth=line_width,
                                         edgecolor=bar_edge_color,
                                         facecolor=color[ind])
                ax.add_patch(rect)
        y_position.append(y + 0.5 * bar_height)
        y = y - 1

    plt.xlim(min(neg_x) * 1.1, max(pos_x) * 1.1)
    plt.ylim(0.02, (max(y_position) + 0.5 * bar_height) * 1.05)
    if line_at_zero:
        z = plt.axvline(0, linestyle='--', color='black', alpha=.5)
        z.set_zorder(-1)
    ax.set_yticks(y_position)
    ax.set_yticklabels(data.index)
    ax.set_xlabel('Count')

    handles, labels = ax.get_legend_handles_labels()
    for ind, column_name in enumerate(data.columns):
        patch = mpatches.Patch(color=color[ind], label=column_name)
        handles.append(patch)
    plt.legend(handles=handles, loc=legend_loc,
               bbox_to_anchor=legend_bbox_to_anchor, ncol=data.shape[1],
               edgecolor=legend_edge_color)
    return ax




