import pm4py


def footprint(el):
    from pm4py.algo.discovery.footprints import algorithm as footprints
    from pm4py.visualization.footprints import visualizer as fp_visualizer
    fp_log = footprints.apply(el, variant=footprints.Variants.ENTIRE_EVENT_LOG)
    print(
        f"Footprint (entire log):\n DFG: {fp_log['dfg']} \n SEQUENCE: {fp_log['sequence']} \n PARALLEL: {fp_log['parallel']}")

    # visualize single footprint table - model
    f, im, fm = pm4py.discover_petri_net_inductive(el)
    fp_net = footprints.apply(f, im, fm)
    gviz = fp_visualizer.apply(fp_net, parameters={fp_visualizer.Variants.SINGLE.value.Parameters.FORMAT: "svg"})
    fp_visualizer.view(gviz)

    # Compare fp of entire log and a net
    #gviz = fp_visualizer.apply(fp_log, fp_net,parameters={fp_visualizer.Variants.COMPARISON.value.Parameters.FORMAT: "svg"})
    #fp_visualizer.view(gviz)

def conformance(el, el_top, net, initial_marking, final_marking):
    # List with the corresponding alignment and fitness note
    print(f"Token replay")
    tr =  pm4py.conformance_diagnostics_token_based_replay(el, net, initial_marking, final_marking)
    for i in tr:
        # TODO: check results / works? meaning?
        print(tr[i])
    print(f"=======================  Alignment =======================")
    aligned_traces = pm4py.conformance_diagnostics_alignments(el, net, initial_marking, final_marking)
    from pm4py.algo.evaluation.replay_fitness import algorithm as fitness
    log_fitness = fitness.evaluate(aligned_traces, variant=fitness.Variants.ALIGNMENT_BASED)
    print(f"Alignment fitness: \n {log_fitness}")

    print(f"=======================  Log Skeleton =======================")
    from pm4py.algo.discovery.log_skeleton import algorithm as lsk
    from pm4py.algo.conformance.log_skeleton import algorithm as lsk_conf
    skeleton = lsk.apply(el_top, parameters={lsk.Variants.CLASSIC.value.Parameters.NOISE_THRESHOLD: 0.0})
    conf_result = lsk_conf.apply(el, skeleton)
    fit = 0
    for r in conf_result:
        if r['is_fit'] == True: fit += 1
    print(f"Fit traces: {fit} - {round((fit * 100) / len(conf_result), 3)} %")