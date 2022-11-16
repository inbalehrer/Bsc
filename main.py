import pm4py
import pandas as pd
from Conformance import Conformance
from Enhancment import Statistics, Plots
from Discovery import Filters

def to_eventlog(df, title):
    # el = pm4py.format_dataframe(df, case_id='ticket', activity_key='newstring', timestamp_key='created')
    el = pm4py.format_dataframe(df, case_id='ticket', activity_key='phase', timestamp_key='created')
    event_log = pm4py.convert_to_event_log(el)
    pm4py.write_xes(el, f"Data/xes/{title}.xes")
    return event_log


if __name__ == "__main__":
    df_a = pd.read_csv("Data/csv/a.csv", ";")
    df_b = pd.read_csv("Data/csv/b.csv", ";")
    df_c = pd.read_csv("Data/csv/c.csv", ";")

    el_a, el_b, el_c = to_eventlog(df_a, "el_a"), to_eventlog(df_b, "el_b"), to_eventlog(df_c, "el_c")
    data_frames = {"a": df_a, "b": df_b, "c": df_c}
    event_logs = {"a": el_a, "b": el_b, "c": el_c}
    start_acc = {"a": ["Plan", "RF", "RFW"], "b": ["Plan", "RF", "RFW"],
                 "c": ["Plan", "RF", "RFW"]}
    end_acc = {"a": ["Closed", "AcD"], "b": ["Closed", "AcD"], "c": ["Closed", "AcD"]}

    for i in event_logs:
        print(f"----------------------Project {i}----------------------")

        # Paths for results
        path_models = f"Results/models/{i}/"
        path_plots = f"Results/plots/{i}/"
        path_socialnet = f"Results/socialnet/{i}/"
        path_hm = f"Results/heatmaps/{i}/"

        # Filter skipped activities

        event_logs[i] = Filters.start_end_activities(event_logs[i], start_acc[i], end_acc[i])
        tickets_skipped, skipped_el = Filters.short_activity(event_logs[i], 10)
        event_logs[i] = Filters.el_skipped(skipped_el)
        data_frames[i] = pm4py.convert_to_dataframe(event_logs[i])

        # Discovery - inductive miner bpmn, dfg, petri net
        from Discovery import Visual, Model, Types, Filters

        # BPMN, DFG, Petri nets discovery
        net, initial_marking, final_marking = Visual.discovery_inductive(event_logs[i], path_models)
        net_a, initial_marking_a, final_marking_a = Visual.discovery_alpha(event_logs[i], path_models)

        # Conformance checking - Footprint analysis
        Conformance.footprint(event_logs[i])

        # Enhancement
        # Variant analysis
        num_var = pm4py.get_variants_as_tuples(event_logs[i])
        el_top = pm4py.filter_variants_top_k(event_logs[i], 5)
        net_top, initial_marking_top, final_marking_top = Visual.discovery_inductive(el_top, f"{path_models}top_")
        print(f"({i}) Variants - {len(num_var)} \n Top 5 variants cases - {len(el_top)}")

        import Enhancment.Statistics as statistics
        import Enhancment.Plots as plots

        rework_dict = Statistics.rework(event_logs[i])
        sojo_time = Statistics.sojo(event_logs[i])

        # Create plots and visualisations of statistics
        Statistics.statistics_event_duration(data_frames[i])
        Plots.time_for_activity(data_frames[i], 140, path_plots, i)
        Plots.dist_event(event_logs[i], path_plots)
        Plots.dist_activity(data_frames[i], path_plots)

        # Batches analysis, collect and calculate time differences between batches
        batches = Statistics.batch(event_logs[i])
        Statistics.batch_time_diff(pm4py.convert_to_dataframe(event_logs[i]), batches)

        Statistics.social_net(event_logs[i], f"{path_socialnet}")

        # Create heat map for each phase in the project
        phases = Model.get_phases(data_frames[i])
        from Enhancment.HeatMap import heatmap_average_values as heatmap

        for p in phases:
            heatmap(data_frames[i], p, f"{path_hm}{p}.png")

        # Analysis of event log excluding waiting phases (Plan, RFW, AcP)
        el_wpf = Filters.filter_waiting_phases(event_logs[i])
        net_wpf, initial_marking_wpf, final_marking_wpf = Visual.discovery_inductive(el_wpf, f"{path_models}wpt_")
        var_wpf = pm4py.get_variants_as_tuples(el_wpf)
        # Review top 5 variants excluding waiting phases
        el_wpf_top = pm4py.filter_variants_top_k(el_wpf, 5)
        net_wpft, initial_marking_wpft, final_marking_wpft = Visual.discovery_inductive(el_wpf_top, f"{path_models}wptop_")

        # Analysis of event log based on issuetype
        issuetype_str = Types.mining_types(event_logs[i],f"{path_models}types/")
