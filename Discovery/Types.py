import pm4py
from Discovery import Model, Filters, Visual


def get_el_type(el):
    '''
    Return a dict with each issue type and the corresponding event log that include only traces of this type.
    :param el:
    :return:
    '''
    types = Model.tasks(el)
    df_types = {}
    for i in types:
        df_types[i] = Filters.filter_attribute(el, "issuetype", [str(i)], True)
    return df_types


def mining_types(el, path):
    el_types = get_el_type(pm4py.convert_to_dataframe(el))
    for t in el_types:
        Visual.discovery_inductive(el_types[t], f"{path}{t}_")
        Visual.discovery_alpha(el_types[t], f"{path}{t}_")
