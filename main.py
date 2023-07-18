from statsbombpy import sb
import pandas as pd
from utils import *
import pprint as pp


def main():
    """Calculates passflow motifs from a list of passes.

    Args:
      passes: A list of passes, where each pass is a tuple of (sender, receiver).
      motif_length: The length of the motifs to calculate.

    Returns:
      A dictionary of passflow motifs, where the key is the motif and the value
      is the number of times the motif appears.
    """
    threshold = 5
    df = sb.events(match_id=15986, split=True, flatten_attrs=True)["passes"]
    team_1_records, team_2_records = get_team_records(df)
    team_1_pass_sequences = create_possession_sequences_from_pass_events(
        team_1_records, threshold)
    team_2_pass_sequences = create_possession_sequences_from_pass_events(
        team_2_records, threshold)
    three_passes = extract_three_pass_sub_possessions(team_1_pass_sequences[111])
    for sequence in three_passes:
        flow = get_flow_for_sequence(sequence)
        print(flow, convert_pass_flow(flow))



if __name__ == "__main__":
    main()
