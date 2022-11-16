import datetime
import pandas as pd
import pm4py
import Discovery
from pm4py.statistics.rework.cases.log import get as cases_rework_get


def rework(el):
    '''
    Analyse how many traces include reworked activities
    :param el: event log
    :return: dict of all activities that were reworked and the corresponding cases
    '''
    from pm4py import get_rework_cases_per_activity
    dic = get_rework_cases_per_activity(el)
    for i in dic:
        print(f"{i} : {dic[i]} ({round(dic[i] * 100 / len(el), 2)}%)")
    return dic


def sojo(el):
    '''
    Print Sojourn Time for activities in the event log, AVG duration of activity
    :param el: event log
    :return: dict of ech activity and the corresponding sojo time
    '''
    from pm4py.statistics.sojourn_time.log import get as soj_time_get
    sojo_time = soj_time_get.apply(el, parameters={soj_time_get.Parameters.TIMESTAMP_KEY: "endtime",
                                                   soj_time_get.Parameters.START_TIMESTAMP_KEY: "created"})
    print(f"Sojo time: {sojo_time}")
    return sojo_time


def add_event_dur(df):
    '''
    Add event duration column to a data frame or event log
    :param el: event log
    :return: data frame that contains the duration for each event
    '''
    if type(df) != pd.DataFrame:
        df = pm4py.convert_to_dataframe(df)
    df["endtime"] = pd.to_datetime(df["endtime"])
    df["created"] = pd.to_datetime(df["created"])
    df['duration'] = df["endtime"] - df["created"]
    return df


def statistics_event_duration(df):
    '''
    Return a string that includes for each phase the avg duration, median and quantiles
    :param el: event log
    :return: readable activity with each activity and the corresponding time measures average time, median, 0.25 and 0.75
    '''
    df = add_event_dur(df)
    phases = Discovery.Model.get_phases(df)
    phases_dist = ""
    for p in phases:
        pl = df[df['phase'] == p]
        avg_time = sum(pl['duration'], datetime.timedelta(0)) / len(pl)
        median_event = pl['duration'].median()
        tfqu = pl['duration'].quantile(0.25)
        sfqu = pl['duration'].quantile(0.75)
        str_event_dur = f" avg time: {avg_time} median: {median_event} 0.25: {tfqu} 0.75: {sfqu}"
        phases_dist += f"{p} : {str_event_dur} \n "
        print(f"{p} / {str_event_dur}")
    return phases_dist


def batch(el):
    '''
    Collect batches from an event log
    :param el: event log to analyse
    :return: Batches list of a given event log
    '''
    from pm4py.algo.discovery.batches import algorithm
    batches = algorithm.apply(el)
    for act in batches:
        print(f"{act[0][0]} / {act[0][1]} ({str(act[1])})")
    return batches


def get_batch_id(batches):
    '''
    Collect all traces ID that are part of a batch list
    :param batches:
    :return: dict with each batch and the corresponding cases it which are involved in the batch
    '''
    id_dict = {}
    for b in batches:
        title = b[0]
        list_title = []
        for t in b[2]['Concurrent batching']:
            for s in t[2]:
                list_title.append(s[2])
        id_dict[title] = list_title
    return id_dict


def batch_time_diff(df, batches):
    '''
    Print the time difference between activities in a batch
    :param df: dataframe
    :param batches: batches list with the corresponding cases' id
    :return:data frame that includes time difference between previous activity / batch
    '''
    ids_batch = get_batch_id(batches=batches)
    for i in ids_batch:
        dfc = df.copy()
        id_list = ids_batch[i]
        dfc = dfc[dfc["case:concept:name"].isin(id_list)]
        dfc = dfc[dfc["concept:name"] == i[0]]
        dfc = dfc[dfc["org:resource"] == i[1]]
        dfc = dfc.sort_values(by="created")
        dfc["time_diff"] = dfc["created"].diff()
    return dfc

