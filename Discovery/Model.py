import pm4py


def roles(df):
    roles_list = df['author'].unique()
    return roles_list


def tasks(df):
    task_types = df['issuetype'].unique()
    return task_types


def priorities(df):
    priorities_list = df['priority'].unique()
    return priorities_list


def oldstrings(df):
    oldstrings_list = df['oldstring'].unique()
    return oldstrings_list


def newstrings(df):
    newstrings_list = df['newstring'].unique()
    return newstrings_list


def get_phases(df):
    phase_list = df['phase'].unique()
    return phase_list


def start_activities(el):
    start_activities = pm4py.get_start_activities(el)
    return start_activities


def end_activities(el):
    end_activities = pm4py.get_start_activities(el)
    return end_activities


def get_model(df, el):
    role_list = roles(df)
    task_list = tasks(df)
    prio_list = priorities(df)
    # old_str = oldstrings(df)
    # new_str = newstrings(df)
    phase = get_phases(df)
    start_acc = start_activities(el)
    end_acc = end_activities(el)
    print("roles: ", role_list,
          "\n tasks: ", task_list,
          "\n priorities: ", prio_list,
          # "\n old strings: ", old_str,
          # "\n new strings: ", new_str,
          "\n activities: ", phase,
          "\n start activities: ", start_acc,
          "\n end activities: ", end_acc)
