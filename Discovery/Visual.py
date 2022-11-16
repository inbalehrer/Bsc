import pm4py


def discovery_inductive(el, path):
    '''
    generate and save BPMN model, petri net and direct follows graph following the inductive miner
    :param el: event log
    :param path: path to save figures
    :return: petri net marking
    '''
    bpmn_model = pm4py.discover_bpmn_inductive(el)
    pm4py.save_vis_bpmn(bpmn_model, f"{path}bpmn_inductive.png")

    net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(el)
    pm4py.save_vis_petri_net(net, initial_marking, final_marking, f"{path}petri_inductive.png")

    dfg, st_acc, end_acc, = pm4py.discover_dfg(el)
    pm4py.save_vis_dfg(dfg, st_acc, end_acc, f"{path}dgf.png", el)

    return net, initial_marking, final_marking


def discovery_alpha(el, path):
    '''
    generate and save petri net and direct follows graph following the alpha miner
    :param el: event log
    :param path: path to save figures
    :return: petri net marking
    '''
    net, initial_marking, final_marking = pm4py.discover_petri_net_alpha(el)
    pm4py.save_vis_petri_net(net, initial_marking, final_marking, f"{path}petri_alpha.png")

    dfg, st_acc, end_acc, = pm4py.discover_dfg(el)
    pm4py.save_vis_dfg(dfg, st_acc, end_acc, f"{path}dgfalpha.png", el)

    return net, initial_marking, final_marking

def social_net(el, path):
    '''
    Create and view hand over and working together social net works and saves them in a given path
    :param el: event log to analyse social net
    :param path: location to save social net
    :return: - Saves graph in a corresponding path
    '''
    hw_values = pm4py.discover_handover_of_work_network(el)
    pm4py.save_vis_sna(hw_values, f"{path}/ho.html")

    wt_values = pm4py.discover_working_together_network(el)
    pm4py.save_vis_sna(wt_values, f"{path}/wt.html")