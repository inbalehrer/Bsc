import pm4py


def roles(df):
    '''
    Collect all the unique values of the roles in a dataframe
    :param df: data frame
    :return: a list of distinct roles
    '''
    roles_list = df['author'].unique()
    return roles_list


def tasks(df):
    '''
    Collect all the unique values of the tasks in a dataframe
    :param df: data frame
    :return: a list of distinct tasks
     '''
    task_types = df['issuetype'].unique()
    return task_types


def priorities(df):
    '''
     Collect all the unique values of the priorities in a dataframe
     :param df: data frame
     :return: a list of distinct priorities
      '''
    priorities_list = df['priority'].unique()
    return priorities_list


def oldstrings(df):
    '''
     Collect all the unique values of the old statuses (transition start) in a dataframe
     :param df: data frame
     :return: a list of distinct old status
      '''
    oldstrings_list = df['oldstring'].unique()
    return oldstrings_list


def newstrings(df):
    '''
     Collect all the unique values of the new statuses (transition goal) in a dataframe
     :param df: data frame
     :return: a list of distinct new status
      '''
    newstrings_list = df['newstring'].unique()
    return newstrings_list


def get_phases(df):
    '''
     Collect all the unique values of the phases in a dataframe
     :param df: data frame
     :return: a list of distinct phases
      '''
    phase_list = df['phase'].unique()
    return phase_list


def start_activities(el):
    '''
     :param el: event log
     :return: a list of all possible start activities of an event log
      '''
    start_activities = pm4py.get_start_activities(el)
    return start_activities


def end_activities(el):
    '''
     :param el: event log
     :return: a list of all possible end activities of an event log
      '''
    end_activities = pm4py.get_start_activities(el)
    return end_activities


def get_model(df, el):
    '''
     Collect all the available values of the dataframe attributes
     :param df: data frame
     :return: readable string with all the available values in a dateframe
      '''
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
