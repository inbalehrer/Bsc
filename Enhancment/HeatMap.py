from matplotlib import pyplot as plt
import matplotlib as mpl
import numpy as np


def heatmap(data, row_labels, col_labels, xlabel=None, ylabel=None, ax=None, cbar_kw={}, cbarlabel="", **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array
    row_labels
        A list or array of length n with labels
    col_labels
        A list or array of length m with labels
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if not ax:
        ax = plt.gca()
    # create heatmap
    img = ax.imshow(data, aspect='auto', vmin=0, vmax=20, **kwargs)

    # Create colorbar
    colorbar = ax.figure.colorbar(img, ax=ax, **cbar_kw)
    colorbar.ax.set_ylabel(cbarlabel, rotation=90, va="bottom", labelpad=20)

    # Set tickets values
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_yticks(np.arange(data.shape[0]))

    # Set ticks labels
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels)

    ax.set_xlabel(xlabel=xlabel)
    ax.set_ylabel(ylabel=ylabel)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=False, bottom=True, labeltop=False, labelbottom=True)

    # Turn spines off and create white grid.
    for edge, spine in ax.spines.items():
        spine.set_visible(False)

    ax.set_xticks(np.arange(data.shape[1] + 1) - .5, minor=True)
    ax.set_yticks(np.arange(data.shape[0] + 1) - .5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return img, colorbar


def annotate_heatmap(im, data=None, valfmt="{x:.2f}", textcolors=["black", "white"],
                     threshold=None, **textkw):
    """
    A function to annotate a heatmap.

    Parameters
    ----------
    im
        The AxesImage to be labeled.
    data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A list or array of two color specifications.  The first is used for
        values below a threshold, the second for those above.  Optional.
    threshold
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max()) / 2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = mpl.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw, size=8)
            texts.append(text)

    return texts


def heatmap_average_values(df, phase, path):
    # df = pd.read_csv('{}'.format(file_name), index_col=0, parse_dates=True, dayfirst=True)
    df.loc[:, 'weekday'] = df['time:timestamp'].dt.weekday
    df.loc[:, 'hour'] = df['time:timestamp'].dt.hour
    df = df[df["concept:name"] == phase]

    array = np.zeros((7, 24))
    hours = df["hour"].values
    days = df["weekday"].values
    # Accumulate the count of each hour and day of an activity in the data frame
    for i in range(len(df)):
        hour = hours[i]
        day = days[i]
        array[day, hour] += 1

    fig, ax = plt.subplots(figsize=[16 / 2, 8 / 2])

    # Set heat map visualization
    img, colorbar = heatmap(data=array,
                            row_labels=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                            col_labels=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14',
                                        '15',
                                        '16', '17', '18', '19', '20', '21', '22', '23'],
                            ax=ax, cmap="YlGn", cbarlabel=r"Number of appearance", xlabel=r'hour', ylabel='day',
                            cbar_kw={'pad': 0.02, 'fraction': 0.06, 'shrink': 1})

    texts = annotate_heatmap(img, valfmt="{x:.0f}")

    plt.title(f"{phase}")
    fig.tight_layout()
    plt.savefig(path, format='png',
                bbox_inches='tight')
