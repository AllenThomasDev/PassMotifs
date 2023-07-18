def get_team_records(df):
    team1, team2 = list(df['team'].unique())
    df['mod_time'] = df['minute']*60 + df['second']
    pass_columns = ['player', 'pass_recipient', 'location',
                    'pass_length', 'pass_end_location', 'timestamp', 'mod_time']
    return df[df['team'] == team1][pass_columns].to_dict('records'), df[df['team'] == team2][pass_columns].to_dict('records')


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
        flow_string+=label
    return flow_string
