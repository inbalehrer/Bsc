import pm4py


def discovery_inductive(el, path):
    bpmn_model = pm4py.discover_bpmn_inductive(el)
    pm4py.save_vis_bpmn(bpmn_model, f"{path}bpmn_inductive.png")

    net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(el)
    pm4py.save_vis_petri_net(net, initial_marking, final_marking, f"{path}petri_inductive.png")

    dfg, st_acc, end_acc, = pm4py.discover_dfg(el)
    pm4py.save_vis_dfg(dfg, st_acc, end_acc, f"{path}dgf.png", el)

    return net, initial_marking, final_marking


def discovery_alpha(el, path):
    net, initial_marking, final_marking = pm4py.discover_petri_net_alpha(el)
    pm4py.save_vis_petri_net(net, initial_marking, final_marking, f"{path}petri_alpha.png")

    dfg, st_acc, end_acc, = pm4py.discover_dfg(el)
    pm4py.save_vis_dfg(dfg, st_acc, end_acc, f"{path}dgfalpha.png", el)

    return net, initial_marking, final_marking
