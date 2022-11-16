import datetime

import pandas as pd
import pm4py

from Discovery import Model, Filters
from Enhancment import Statistics
from Enhancment.Statistics import add_event_dur
from main import to_eventlog


def get_analysis():
    df_a = pd.read_csv("../Data/csv/a.csv", ";")
    df_b = pd.read_csv("../Data/csv/b.csv", ";")
    df_c = pd.read_csv("../Data/csv/c.csv", ";")
    data_frames = {"a": add_event_dur(df_a), "b": add_event_dur(df_b), "c": add_event_dur(df_c)}
    event_logs = {}
    for d in data_frames:
        el = pm4py.format_dataframe(data_frames[d], case_id='ticket', activity_key='phase', timestamp_key='created')
        event_log = pm4py.convert_to_event_log(el)
        event_logs[d] = event_log

    analysis_dic = {}
    for i in event_logs:
        details = print_details(data_frames[i])
        stat_by = get_statistics_by(event_logs[i])
        event_dur = Statistics.statistics_event_duration(event_logs[i])
        skipp_info = skipped_statistics(event_logs[i])
        traces = pm4py.get_variants(event_logs[i])
        trace_dur = avg_traces_duration(event_logs[i])
        x, var_str = get_top_n_var(traces, 5)
        analysis_dic[i] = {"Details Event log:" : details, "Statistics by:": stat_by, "Event duration:" : event_dur,
                           "Skipped issues:": skipp_info, "Traces duration:": trace_dur, "Variants:": var_str}
    return analysis_dic


def avg_traces_duration(el):
    '''
    Return an avg time for traces in event log
    :param title:
    :param el:
    :return:
    '''
    traces_dur = traces_duration(el)
    traces_dur_df = pd.DataFrame.from_dict(traces_dur.items())
    avg = sum(traces_dur_df[1], datetime.timedelta(0)) / len(traces_dur)
    median_t = traces_dur_df[1].median()
    tfqu = traces_dur_df[1].quantile(0.25)
    sfqu = traces_dur_df[1].quantile(0.75)
    str_trace_dur = f"Traces - Avg: {avg}, median: {median_t}, 0.25: {tfqu}, 0.75: {sfqu}"
    return str_trace_dur


def traces_duration(el):
    """
    :param el: event log
    :return: Returns a dictionary contains the duration (in timedelta) of all traces in the event log
    """
    d = dict()
    for t in el:
        start_date = first_event(t)['time:timestamp']
        end_date = last_event(t)['time:timestamp']
        d[t.attributes['concept:name']] = (end_date - start_date)
    return d


def first_event(t):
    first_event = t._list[0]
    return first_event


def last_event(t):
    trace_index = len(t)
    last_event = t._list[trace_index - 1]
    return last_event


def skipped_statistics(el):
    tickets_skipped, skipped_ann_el = Filters.short_activity(el, 10)
    skipped_traces = get_skipped_tickets(el, tickets_skipped)
    tickets_skipped_prio = skipped_per_prio(el, skipped_traces)
    tickets_skipped_issuetype = skipped_per_issuetype(el, skipped_traces)
    tickets_skipped_phase = skipped_per_phase(el, tickets_skipped)
    s = f"{len(tickets_skipped)} tickets skipped a phase. \n " \
        f"Priority: \n {tickets_skipped_prio} \n " \
        f"Issue Type: \n {tickets_skipped_issuetype} \n " \
        f"Phases: \n  {tickets_skipped_phase}"

    return s


def get_skipped_tickets(df, tickets_skipped):
    '''
    Return a list of all traces that include skipped activity
    :param df:
    :param tickets_skipped:
    :return:
    '''
    tickets = tickets_skipped.keys()
    tickets_info = []
    # Collect all traces where a phase is skipped
    for t in df:
        if t.attributes['concept:name'] in tickets: tickets_info.append(t)
    return tickets_info


def skipped_per_prio(el, tickets_skipped):
    '''
    Return to each priority how many issues skipped an activity
    :param df:
    :param tickets_skipped:
    :return: dict: key - priority value - number of times that got skipped
    '''
    skipped_per_prio = {}
    skipped_prec = {}
    prios = Model.priorities(pm4py.convert_to_dataframe(el))
    for i in prios:
        skipped_per_prio[i] = 0
        for t in tickets_skipped:
            if t._list[0]._dict['priority'] == i: skipped_per_prio[i] += 1
        skipped_prec[i] = f"{skipped_per_prio[i]} ({round((skipped_per_prio[i] * 100) / len(tickets_skipped), 2)}%)"
    return skipped_prec


def skipped_per_phase(el, tickets_skipped):
    '''
    Return to each phase how many issues skipped an activity

    :param df:
    :param tickets_skipped:
    :return:dict: key - phase value - number of times that got skipped
    '''
    skipped_per_phase = {}
    skipped_prec = {}
    phases = Model.get_phases(pm4py.convert_to_dataframe(el))
    for i in phases:
        skipped_per_phase[i] = 0
        for t in tickets_skipped.values():
            if t == i: skipped_per_phase[i] += 1
        skipped_prec[i] = f"{skipped_per_phase[i]} ({round((skipped_per_phase[i] * 100) / len(tickets_skipped), 2)}%)"

    return skipped_prec


def skipped_per_issuetype(el, tickets_skipped):
    '''
    Return to each issue type how many issues skipped an activity
    :param df:
    :param tickets_skipped:
    :return:  dict: key - issue type value - number of times that got skipped
    '''
    skipped_per_type = {}
    skipped_prec = {}
    issuetype = Model.tasks(pm4py.convert_to_dataframe(el))
    for i in issuetype:
        skipped_per_type[i] = 0
        for t in tickets_skipped:
            if t._list[0]._dict['issuetype'] == i: skipped_per_type[i] += 1
        skipped_prec[i] = f"{skipped_per_type[i]} ({round((skipped_per_type[i] * 100) / len(tickets_skipped), 2)}%)"
    return skipped_prec


def print_details(el):
    """
    Information log of following properties: Event and Cases Numbers, File columns and data.
    :param el: The event log
    :return:
    """
    num_events = len(el)
    num_cases = len(el.ticket.unique())
    avg_time = sum(el['duration'], datetime.timedelta(0)) / len(el)
    median_event = el['duration'].median()
    tfqu = el['duration'].quantile(0.25)
    sfqu = el['duration'].quantile(0.75)
    str_details = f" Events: {num_events} Cases: {num_cases}, \n avg duration: {avg_time} median: {median_event} 0.25: {tfqu} 0.75: {sfqu} \n"
    return str_details


def get_statistics_by(el):
    '''
    Return appearance statistics of each priority and issue type in an event log
    :param el:
    :return:
    '''
    prio_per_el = get_prio_el(el)
    issuetype_per_el = get_issuetype_el(el)
    prio_str_el, issuetype_str_el = "", ""
    for p in prio_per_el:
        precp = round((prio_per_el[p] * 100) / len(el), 2)
        prio_str_el += f"{p}: {prio_per_el[p]} ({precp}%) "
    for i in issuetype_per_el:
        preci = round((issuetype_per_el[i] * 100) / len(el), 2)
        issuetype_str_el += f"{i}: {issuetype_per_el[i]} ({preci}%) "
    s = f"{prio_str_el} \n {issuetype_str_el}"
    return s


def get_prio_el(el):
    '''
    Return the distribution of each priority in the event log
    :param el:
    :return:
    '''
    prios_el = Model.priorities(pm4py.convert_to_dataframe(el))
    el_by_prio = {}
    for p in prios_el:
        el_by_prio[p] = 0
        for t in el._list:
            if t._list[0]._dict['priority'] == p: el_by_prio[p] += 1
    return el_by_prio


def get_issuetype_el(el):
    '''
    Return the distribution of each issue type in the event log
    :param el:
    :return:
    '''
    issuetype_el = Model.tasks(pm4py.convert_to_dataframe(el))
    el_by_issuetype = {}
    for i in issuetype_el:
        el_by_issuetype[i] = 0
        for t in el._list:
            if t._list[0]._dict['issuetype'] == i: el_by_issuetype[i] += 1
    return el_by_issuetype


def get_top_n_var(dictvar, n):
    sorted_l = sorted(dictvar.items(), key=lambda x: len(x[1]), reverse=True)
    x = sorted_l[:n]
    str_x = ""
    for i in x:
        str_x += f"{i[0]} : {len(i[1])} "
    return x, str_x
