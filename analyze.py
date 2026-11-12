import pandas as pd, numpy as np

b = pd.read_csv("Data Pack/ball_by_ball.csv", low_memory=False)
m = pd.read_csv("Data Pack/matches.csv", parse_dates=["match_date"])
comp = pd.read_csv("Data Pack/competitions.csv")
# keep innings 1-2 only (exclude super overs: 38 balls)
b = b[b['innings'].isin([1,2])].copy()
b['total_runs_ball'] = b['runs'] + b['extras1_runs'] + b['extras_2_runs']
b['is_wide'] = (b['extras_type']=='wide')
b['is_legal'] = ~b['is_wide']   # legal ball for batter/bowler counting
b['bowler_runs'] = b['runs'] + np.where(b['extras_type'].isin(['wide','Overstep']), b['extras1_runs']+b['extras_2_runs'], 0)
# bowler wicket: bowler credited unless RunOut / Retire / Obstructing
b['bowler_wkt'] = b['is_wicket'] & (~b['dismissal_type'].isin(['RunOut','Retire Out','Obstracting the field','Obstructing the field']))
b['batter_out'] = b['is_wicket'] & (b['dismissed_player_id']==b['striker_id'])
# sort for cumulative context
b = b.sort_values(['match_id','innings','innings_ball_num']).reset_index(drop=True)
# first innings total per match
first_tot = b[b['innings']==1].groupby('match_id')['total_runs_ball'].sum().rename('first_inn_total')
b = b.merge(first_tot, on='match_id', how='left')
b['target'] = b['first_inn_total'] + 1
# cumulative before ball: per match+innings
b['cum_runs_before'] = b.groupby(['match_id','innings'])['total_runs_ball'].cumsum() - b['total_runs_ball']
b['cum_wk_before'] = b.groupby(['match_id','innings'])['is_wicket'].cumsum() - b['is_wicket']
# legal balls before (approx: innings_ball_num is delivery count incl wides? use overid)
b['over_num'] = b['overid']  # 1..20
# balls remaining (legal balls): 120 - legal balls bowled before. Approx via innings_ball_num is messy with wides; use count of legal balls before
b['legal_before'] = b.groupby(['match_id','innings'])['is_legal'].cumsum() - b['is_legal'].astype(int)
b['balls_remaining'] = 120 - b['legal_before']
b['runs_needed'] = np.where(b['innings']==2, b['target'] - b['cum_runs_before'], np.nan)
b['rrr'] = np.where((b['innings']==2)&(b['balls_remaining']>0), b['runs_needed']/(b['balls_remaining']/6.0), np.nan)
b['wkts_down'] = b['cum_wk_before']
b['wkts_in_hand'] = 10 - b['cum_wk_before']
# knockout flag
ko = m.set_index('match_id')['knock_out'].to_dict()
stage = m.set_index('match_id')['stage'].to_dict()
b['knock_out'] = b['match_id'].map(ko).fillna(0)
b['stage'] = b['match_id'].map(stage)
b['is_ipl'] = b['match_id'].map(m.set_index('match_id')['comp_id']).isin(comp[comp['comp_name'].str.startswith('IPL ')]['comp_id'])
# PRESSURE DEFINITION (transparent, same balls for bat & ball)
# A death overs 17-20 | B high-RRR chase RRR>=9 | C tight finish: <=36 balls left, 1-45 needed | D collapse: >=4 wkts down before over 12
b['p_death'] = b['over_num']>=17
b['p_rrr'] = (b['innings']==2) & (b['rrr']>=9.0)
b['p_tight'] = (b['innings']==2) & (b['balls_remaining']<=36) & (b['runs_needed']>=1) & (b['runs_needed']<=45)
b['p_collapse'] = (b['wkts_down']>=4) & (b['over_num']<=12)
b['pressure'] = b['p_death'] | b['p_rrr'] | b['p_tight'] | b['p_collapse']
b['pressure_reason'] = np.where(b['p_death'],'death',np.where(b['p_rrr'],'rrr',np.where(b['p_tight'],'tight',np.where(b['p_collapse'],'collapse','none'))))
print("Total legal balls:", b['is_legal'].sum(), "pressure legal balls:", (b['pressure']&b['is_legal']).sum(), "share:", round((b['pressure']&b['is_legal']).mean(),3))
print("Pressure by reason (legal balls):")
print(b[b['is_legal']].groupby('pressure_reason').size())
print("Pressure by innings:", b[b['is_legal']].groupby(['innings','pressure']).size())
print("Pressure by IPL/T20I:", b[b['is_legal']].groupby(['is_ipl','pressure']).size())
print("Knockout balls:", b['knock_out'].sum(), "knockout pressure share:", b[b['knock_out']==1]['pressure'].mean())
b.to_pickle("balls_enriched.pkl")
print("saved balls_enriched.pkl", len(b))
