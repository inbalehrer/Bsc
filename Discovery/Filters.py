import pm4py


def filter_waiting_phases(el):
    filtered_el = pm4py.filter_event_attribute_values(el, "concept:name",
                                                      ['RFW', 'AcP', 'Plan'], level="event",
                                                      retain=False)
    return filtered_el


def filter_attribute(el, attribute, value, retainit):  # values : {'val1', 'val2'}
    filtered = pm4py.filter_event_attribute_values(el, str(attribute), value, retain=retainit)
    return filtered


def waiting_for_input(el):
    '''
    Filter event log from illegal attribute - WFI
    :param el:
    :return: Filtered event log
    '''
    filtered_log = pm4py.filter_event_attribute_values(el, str("phase"), "WFI", retain=False)
    return filtered_log


def start_end_activities(el, start_acc, end_acc):
    '''
    Filter data frame on both start and end activities
    :param df:
    :param start_acc:
    :param end_acc:
    :return: Filtered data frame
    '''
    filtered_start = pm4py.filter_start_activities(el, start_acc)
    filtered_log = pm4py.filter_end_activities(filtered_start, end_acc)
    return filtered_log


def short_activity(df, min):
    '''
    Return a dict with all ticket numbers as key and the phase they skipped as value, a deep copy include all phases skipped with notation
    :param df:
    :param min:
    :return:
    '''
    df = pm4py.convert_to_dataframe(df)
    df_copy = df.copy(deep=True)
    df_copy = pm4py.convert_to_event_log(df_copy)
    sec = min * 60
    tickets_skipped = {}
    for t in df_copy._list:  # trace
        for e in t._list:
            secondse = (e._dict['endtime'] - e._dict['created']).total_seconds()
            if (secondse > 0) and (secondse < sec):
                prev = e._dict['phase']
                e._dict['concept:name'] = f"Skipped {prev}"
                tickets_skipped[e._dict['ticket']] = e._dict['phase']
    return tickets_skipped, df_copy


def el_skipped(df):
    '''
    Filter Skipped activities (shorter than 10 min) from the event log - on event base.
    '''
    el_filtered_skipped = pm4py.filter_event_attribute_values(df, "concept:name",
                                                              ['Skipped WIog', 'Skipped RFW',
                                                               'Skipped AcIog', 'Skipped AcP',
                                                               'Skipped Plan', 'Skipped RF',
                                                               'Skipped AcD', 'Skipped Closed',
                                                               'Skipped TA', 'Skipped AcIog',
                                                               'Skipped AcP', 'Skipped UxNC',
                                                               'Skipped BL'], level="event",
                                                              retain=False)
    return el_filtered_skipped


def long_traces_between(el, min_days, max_days):
    """
    Filter event log on time frame between min days and max days duration of a trace
    """
    min_days_in_sec = min_days * 86400
    max_days_in_sec = max_days * 86400
    filtered_log = pm4py.filter_case_performance(el, min_days_in_sec, max_days_in_sec)
    return filtered_log


def filter_len(el):
    filter_len = pm4py.filter_case_size(el, 4, 20)
    return filter_len
