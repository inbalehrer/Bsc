import pm4py
from matplotlib import pyplot as plt
import matplotlib
import numpy as np
import seaborn as sns


def dist_event(el, path):
    '''
    Distribution of all of the events over days of the week and hours.
    :param el:
    :return:
    '''
    # hours, days_month, months, years
    pm4py.save_vis_events_distribution_graph(el,file_path=f"{path}_days.png", distr_type="days_week")
    pm4py.save_vis_events_distribution_graph(el,file_path=f"{path}_hours.png", distr_type="hours")
    pm4py.save_vis_events_distribution_graph(el,file_path=f"{path}_months.png", distr_type="months")


def dist_activity(df, path):
    '''
    Create plot of the distribution of all events over the days of the week
    :param df:
    :return:
    '''
    df["days"] = df["time:timestamp"].dt.dayofweek
    df["hours"] = df["time:timestamp"].dt.hour
    sns.displot(data=df, x="days", hue="concept:name", multiple="dodge", shrink=1.5)
    plt.xticks(ticks=[0, 1, 2, 3, 4, 5, 6], labels=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
    plt.savefig(f"{path}_dist_activities.png")
    #plt.show()


def time_for_activity(df, outlier, path, i):
    '''
    Plot the distribution of activity duration
    :param df:
    :param outlier:
    :return:
    '''
    df['timedelta'] = df['endtime'] - df['created']
    df['timedelta_days'] = df['timedelta'] / np.timedelta64(24, 'h')
    filtered_outliers = df[df['timedelta_days'] < outlier]
    matplotlib.use('MacOSX')
    boxplot = filtered_outliers.boxplot(column=['timedelta_days'], by=['phase'], rot=45, fontsize=10)
    boxplot.set_ylabel('Time in days')
    boxplot.set_xlabel('Activity')
    #boxplot.set_title(f"Activities duration - Project {i}")
    boxplot.set()
    plt.savefig(f"{path}boxplot_time.png")
    #plt.show()



