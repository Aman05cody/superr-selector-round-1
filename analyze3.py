import pandas as pd, numpy as np
b=pd.read_pickle("balls_v2.pkl")
legal=b[b['is_legal']].copy()
# subtype priority: tight > death > lateRRR > collapse > KOdeath > none ; death = over>=18 inn2 or >=19 inn1
def subtype(row):
    if not row['pressure']: return 'non-pressure'
    if row['innings']==2 and row['balls_remaining']<=30 and 1<=row['runs_needed']<=36: return 'tight-finish'
    if (row['innings']==2 and row['over_num']>=18) or (row['innings']==1 and row['over_num']>=19): return 'death'
    if row['innings']==2 and row['over_num']>=13 and row['rrr']>=10: return 'late-high-RRR'
    if row['wkts_down']>=4 and row['over_num']<=10: return 'collapse'
    if row['knock_out']==1 and row['over_num']>=17: return 'knockout-death'
    return 'pressure-other'
legal['subtype']=legal.apply(subtype,axis=1)
print(legal.groupby(['subtype','is_ipl']).size())
# par per subtype x format: batting SR, bowling econ
par = legal[legal['pressure']].groupby(['subtype','is_ipl']).agg(balls=('runs','size'), bat_runs=('runs','sum'), bowl_runs=('bowler_runs','sum'), wk=('bowler_wkt','sum'))
par['par_sr']=par['bat_runs']/par['balls']*100
par['par_econ']=par['bowl_runs']/par['balls']*6
par['par_wk_rate']=par['wk']/par['balls']*24
print(par.to_string())
par.to_csv("par_subtype_format.csv")
legal.to_pickle("balls_v3.pkl")

# attach par to each ball
par_sr = par['par_sr'].to_dict(); par_ec = par['par_econ'].to_dict()
legal['par_sr'] = [par_sr.get((s,f), np.nan) for s,f in zip(legal['subtype'], legal['is_ipl'])]
legal['par_econ'] = [par_ec.get((s,f), np.nan) for s,f in zip(legal['subtype'], legal['is_ipl'])]
legal['exp_runs_bat'] = legal['par_sr']/100  # expected batter runs per ball in that context
legal['exp_runs_bowl'] = legal['par_econ']/6
legal.to_pickle("balls_v3.pkl")

bat=pd.read_csv("bat_stats.csv"); bowl=pd.read_csv("bowl_stats.csv")
# last season + IPL totals per player
m=pd.read_csv("Data Pack/matches.csv"); comp=pd.read_csv("Data Pack/competitions.csv")
season_map=m.set_index('match_id')['comp_id'].map(comp.set_index('comp_id')['season']).to_dict()
legal['season']=legal['match_id'].map(season_map)
legal['match_inn']=legal['match_id'].astype(str)+'_'+legal['innings'].astype(str)
for df, idcol, namecol in [(bat,'pid','name'),(bowl,'pid','name')]:
    pass
# compute adjusted metrics per batter
def adj_bat(df):
    out=[]
    for (pid,name), d in df.groupby(['striker_id','striker_name']):
        pr=d[d['pressure']]
        if len(pr)==0: continue
        exp_sr = (pr['par_sr']/100*1)  # per ball expected runs
        # expected SR given mix = total expected runs / balls *100
        exp_runs = pr['par_sr'].sum()/100
        adj_sr = pr['runs'].sum()/len(pr)*100 - exp_runs/len(pr)*100  # player SR minus mix-expected SR
        # also pressure SR
        out.append(dict(pid=pid,name=name,pr_balls=len(pr),pr_runs=pr['runs'].sum(),pr_sr=pr['runs'].sum()/len(pr)*100,
                       exp_sr=exp_runs/len(pr)*100, adj_sr=adj_sr, last_season=pr['season'].max(), tot_last=d['season'].max(),
                       ipl_pr=(pr['is_ipl']).sum(), pr_inn=pr['match_inn'].nunique()))
    return pd.DataFrame(out)
def adj_bowl(df):
    out=[]
    for (pid,name), d in df.groupby(['bowler_id','bowler_name']):
        pr=d[d['pressure']]
        if len(pr)==0: continue
        exp_econ = pr['par_econ'].mean()  # approx weighted by balls (each ball equal) -> mean par econ
        # weighted expected econ = sum(par_econ/6)/balls*6 = mean par_econ
        pecon = pr['bowler_runs'].sum()/len(pr)*6
        out.append(dict(pid=pid,name=name,pr_balls=len(pr),pr_runs=pr['bowler_runs'].sum(),pr_wk=pr['bowler_wkt'].sum(),pr_econ=pecon,
                       exp_econ=exp_econ, adj_econ=pecon-exp_econ, last_season=pr['season'].max(), tot_last=d['season'].max(),
                       ipl_pr=(pr['is_ipl']).sum(), pr_inn=pr['match_inn'].nunique()))
    return pd.DataFrame(out)

ab=adj_bat(legal); aw=adj_bowl(legal)
ab.to_csv("bat_adj.csv",index=False); aw.to_csv("bowl_adj.csv",index=False)
# merge with bat_stats
bat2=bat.merge(ab[['pid','exp_sr','adj_sr','last_season','tot_last']], on='pid', how='left', suffixes=('','_adj'))
bowl2=bowl.merge(aw[['pid','exp_econ','adj_econ','last_season','tot_last']], on='pid', how='left', suffixes=('','_adj'))
bat2.to_csv("bat_stats2.csv",index=False); bowl2.to_csv("bowl_stats2.csv",index=False)
print("\nBAT adj_sr top (eligible gates):")
e=bat2[(bat2.pr_balls>=70)&(bat2.tot_balls>=300)&(bat2.pr_inn>=10)]
print(e.sort_values('adj_sr',ascending=False)[['name','pr_balls','pr_sr','exp_sr','adj_sr','uplift','pr_avg','cons','ipl_pr_balls','seasons','tot_last']].head(30).to_string(index=False))
print("\nBOWL adj_econ top (eligible gates):")
eb=bowl2[(bowl2.pr_balls>=70)&(bowl2.tot_balls>=300)&(bowl2.pr_inn>=10)]
print(eb.sort_values('adj_econ')[['name','pr_balls','pr_econ','exp_econ','adj_econ','econ_gain','pr_wk','wk_rate','pr_dot','cons','ipl_pr_balls','pace_spin','tot_last']].head(30).to_string(index=False))
