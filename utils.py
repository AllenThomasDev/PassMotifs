import plotly.graph_objects as go


def get_team_records(df, team):
    df['mod_time'] = df['minute']*60 + df['second']
    pass_columns = ['player', 'pass_recipient', 'location',
                    'pass_length', 'pass_end_location', 'timestamp', 'mod_time']
    return df[df['team'] == team][pass_columns].to_dict('records')


def create_possession_sequences_from_pass_events(records, threshold=5):
    """Records is a list of records made like this ->
    sb.events(match_id=15986, split=True, flatten_attrs=True)["passes"].to_dict('records')
    threshold is number of seconds after which a pass is considered separate from a pass sequence"""
    sublists = []
    current_sublist = []
    for record in records:
        if len(current_sublist) == 0 or (record['mod_time'] - current_sublist[-1]['mod_time']) < threshold:
            current_sublist.append(record)
        else:
            sublists.append(current_sublist)
            current_sublist = [record]
    sublists.append(current_sublist)
    return sublists


def extract_three_pass_sub_possessions(passes):
    """Extracts all the three-pass long sub-possessions from the ball possession.

    Args:
      passes: A list of passes.

    Returns:
      A list of three-pass long sub-possessions.
    """

    sub_possessions = []
    for i in range(len(passes)):
        if i + 2 < len(passes):
            sub_possession = passes[i:i + 3]
            sub_possessions.append(sub_possession)
    return sub_possessions


def get_flow_for_sequence(sub_possession):
    """Converts the player identifiers in the sub-possession to A, B, C, and D labels.

    Args:
      sub_possession: A three-pass long sub-possession.

    Returns:
      A list of A, B, C, and D labels.
    """
    flow = []
    origin_player = sub_possession[0]['player']
    flow.append(origin_player)
    for entry in sub_possession:
        flow.append(entry['pass_recipient'])
    return flow


def convert_pass_flow(pass_flow):
    """Converts the pass flow to A->B->C->B.

    Args:
      pass_flow: The pass flow.

    Returns:
      The pass flow in A->B->C->B format.
    """
    flow_string = ''
    # maintain order while dropping dupes
    players = list(dict.fromkeys(pass_flow))
    labels = ['A', 'B', 'C', 'D'][:len(players)]
    players_to_labels = dict(zip(players, labels))
    converted_pass_flow = [players_to_labels[player] for player in pass_flow]
    for label in converted_pass_flow:
        flow_string += label
    return flow_string


statsbomb_competitions = {'Champions League': ['2018/2019',
                                               '2017/2018',
                                               '2016/2017',
                                               '2015/2016',
                                               '2014/2015',
                                               '2013/2014',
                                               '2012/2013',
                                               '2011/2012',
                                               '2010/2011',
                                               '2009/2010',
                                               '2008/2009',
                                               '2006/2007',
                                               '2004/2005',
                                               '2003/2004',
                                               '1999/2000'],
                          "FA Women's Super League": ['2020/2021', '2019/2020', '2018/2019'],
                          'FIFA World Cup': ['2022', '2018'],
                          'Indian Super league': ['2021/2022'],
                          'La Liga': ['2020/2021',
                                      '2019/2020',
                                      '2018/2019',
                                      '2017/2018',
                                      '2016/2017',
                                      '2015/2016',
                                      '2014/2015',
                                      '2013/2014',
                                      '2012/2013',
                                      '2011/2012',
                                      '2010/2011',
                                      '2009/2010',
                                      '2008/2009',
                                      '2007/2008',
                                      '2006/2007',
                                      '2005/2006',
                                      '2004/2005'],
                          'NWSL': ['2018'],
                          'Premier League': ['2015/2016', '2003/2004'],
                          'UEFA Euro': ['2020'],
                          "UEFA Women's Euro": ['2022'],
                          "Women's World Cup": ['2019']}

season_name_to_id = {'1999/2000': 76,
                     '2003/2004': 44,
                     '2004/2005': 37,
                     '2005/2006': 38,
                     '2006/2007': 39,
                     '2007/2008': 40,
                     '2008/2009': 41,
                     '2009/2010': 21,
                     '2010/2011': 22,
                     '2011/2012': 23,
                     '2012/2013': 24,
                     '2013/2014': 25,
                     '2014/2015': 26,
                     '2015/2016': 27,
                     '2016/2017': 2,
                     '2017/2018': 1,
                     '2018': 3,
                     '2018/2019': 4,
                     '2019': 30,
                     '2019/2020': 42,
                     '2020': 43,
                     '2020/2021': 90,
                     '2021/2022': 108,
                     '2022': 106}


competition_name_to_id = {'Champions League': 16,
                          "FA Women's Super League": 37,
                          'FIFA World Cup': 43,
                          'Indian Super league': 1238,
                          'La Liga': 11,
                          'NWSL': 49,
                          'Premier League': 2,
                          'UEFA Euro': 55,
                          "UEFA Women's Euro": 53,
                          "Women's World Cup": 72}


def football_match_to_table(match_row):
    """Converts a football match row into a neat table with home team stats in one column and corresponding away team stats in another column.

    Args:
      match_row: A Pandas DataFrame row containing the data of a football match.

    Returns:
      A string containing the table.
    """
    home_team_stats = [match_row[x]
                       for x in ['home_team', 'home_score', 'home_managers']]
    away_team_stats = [match_row[x]
                       for x in ['away_team', 'away_score', 'away_managers']]
    team_names = match_row['home_team'], match_row['away_team']
    team_scores = match_row['home_score'], match_row['away_score']
    return [team_names, team_scores]


def df_to_pass_flow(df, team, threshold):
    team_pass_events = get_team_records(df, team)
    team_pass_sequences = create_possession_sequences_from_pass_events(
        team_pass_events, threshold)
    l = []
    for subpossession in team_pass_sequences:
        three_pass_sequences = extract_three_pass_sub_possessions(
            subpossession)
        for sequence in three_pass_sequences:
            flow = get_flow_for_sequence(sequence)
            l.append(convert_pass_flow(flow))
    filtered_flows = [
        flow for flow in l if (("AA" not in flow) and ("BB" not in flow) and ("CC" not in flow))]
    return filtered_flows



def flow_to_chart(flow, team_name):
    fig = go.Pie(
        values=flow['vals'],
        labels=flow['keys'],
        name='Motif distribution',  # This name will be displayed in the legend
        showlegend=True,  # Set showlegend to True to display the legend
    )

    layout = go.Layout(
        title="Pass Motif distribution for " + team_name,
        legend=dict(
            orientation="v",  # "v" stands for vertical, which places the legend on the left
            x=0,  # Adjust the x position to control the distance from the left edge
            y=1,   # Adjust the y position to control the vertical centering
        ),
    )
    fig = go.Figure(data=[fig], layout=layout)

    return fig

