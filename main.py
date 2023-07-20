from statsbombpy import sb
import pandas as pd
from utils import *
import pprint as pp
from collections import Counter
import streamlit as st
import plotly.express as px
st.set_page_config(layout="wide")
leagues = list(statsbomb_competitions.keys())

def main():
    # Create the drop downs
    selected_comp = st.sidebar.selectbox('Competition', leagues, index= 0)
    selected_season = st.sidebar.selectbox('Season', statsbomb_competitions[selected_comp])
    comp_id = competition_name_to_id[selected_comp]
    season_id = season_name_to_id[selected_season]
    matches =  sb.matches(competition_id=comp_id, season_id=season_id)
    home_teams = matches['home_team'].unique()
    home_team = st.sidebar.selectbox('Home Team', home_teams)
    away_teams = matches[matches['home_team'] == home_team]['away_team'].unique()
    away_team = st.sidebar.selectbox('Away Team', away_teams)
    eligible_matches = matches[matches["home_team"] == home_team][matches["away_team"] == away_team]
    match_id = int(eligible_matches["match_id"].iloc[0])
    print(eligible_matches.columns)
    df = sb.events(match_id=match_id, split=True, flatten_attrs=True)["passes"]
    threshold = 5
    home_flows = df_to_pass_flow(df, home_team, threshold)
    away_flows = df_to_pass_flow(df, away_team, threshold)
    home_flows_dist = dict(Counter(home_flows))
    away_flows_dist = dict(Counter(away_flows))
    home_df = pd.DataFrame(list(home_flows_dist.items()), columns=['keys', 'vals'])
    away_df = pd.DataFrame(list(away_flows_dist.items()), columns=['keys', 'vals'])
    # home_df = pd.DataFrame.from_dict(home_flows_dist, orient="index", columns=["Count"])
    # away_df = pd.DataFrame.from_dict(away_flows_dist, orient="index", columns=["Count"])
    home_df = home_df.reset_index()
    home_chart = flow_to_chart(home_df, home_team)
    away_chart = flow_to_chart(away_df, away_team)
    st.sidebar.write("This is a WIP app, please let me know @Allenytics on Twitter if you find anything breaking.")
    st.sidebar.write("https://twitter.com/Allenytics")
    st.sidebar.write("Read more about PassMotifs here - ")
    st.sidebar.write("https://cafetactiques.com/2023/07/11/pass-flow-motifs-examining-team-passing-style/")
    st.sidebar.write("Further reading - ")
    st.sidebar.write("https://arxiv.org/pdf/1409.0308.pdf")
    columns = st.columns([1,1])
    with columns[0]:
        st.plotly_chart(home_chart)
    with columns[1]:
        st.plotly_chart(away_chart)



if __name__ == '__main__':
    main()

