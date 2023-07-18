def get_team_records(df):
    team1, team2 = list(df['team'].unique())
    df['mod_time'] = df['minute']*60 + df['second']
    pass_columns = ['location', 'player', 'pass_recipient',
                    'pass_length', 'pass_end_location', 'timestamp', 'mod_time']
    return df[df['team'] == team1][pass_columns].to_dict('records'), df[df['team'] == team2][pass_columns].to_dict('records')


def create_pass_sequences_from_pass_events(records, threshold=5):
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