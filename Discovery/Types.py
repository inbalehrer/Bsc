import pm4py
from Discovery import Model, Filters, Visual


def get_el_type(el):
    '''
    Return a dict with each issue type and the corresponding event log that include only traces of this type.
    :param el: event log
    :return: dict with issuetype as a key and a filtered event log as a value
    '''
    types = Model.tasks(el)
    df_types = {}
    for i in types:
        df_types[i] = Filters.filter_attribute(el, "issuetype", [str(i)], True)
    return df_types


def mining_types(el, path):
    '''
    For each event log which is filtered on issue type - discovery inductive and alpha miner
    :param el: event log
    :param path: path to save figures
    :return: - Saves figures in a corresponding path
    '''
    el_types = get_el_type(pm4py.convert_to_dataframe(el))
    for t in el_types:
        Visual.discovery_inductive(el_types[t], f"{path}{t}_")
        Visual.discovery_alpha(el_types[t], f"{path}{t}_")
