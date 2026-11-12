import pandas as pd, numpy as np, json
b=pd.read_pickle("balls_v3.pkl")
legal=b[b['is_legal']].copy()
print("subtype counts (legal):")
print(legal.groupby(['subtype']).size().to_dict())
print("pressure by subtype x format:")
print(legal[legal['pressure']].groupby(['subtype','is_ipl']).size().to_dict())
par=pd.read_csv("par_subtype_format.csv")
print(par.to_string())
# finalist details: IPL-PR SR/econ, recent SR/econ, 2026 team, role
_mm=pd.read_csv('Data Pack/matches.csv'); _cc=pd.read_csv('Data Pack/competitions.csv')
_smap=_mm.set_index('match_id')['comp_id'].map(_cc.set_index('comp_id')['season']).to_dict()
legal['season']=legal['match_id'].map(_smap); legal['yr']=legal['season'].astype(str).str[:4].astype(float)
mp=pd.read_csv("Data Pack/competition_team_player_mapping.csv")
def team26(name):
    r=mp[(mp.comp_id==3298)&(mp.player_name==name)]['team_name'].values
    return r[0] if len(r) else "Not in IPL 2026"
bat=pd.read_csv("bat_submitted.csv"); bowl=pd.read_csv("bowl_submitted.csv")
out={"batters":[],"bowlers":[]}
for i,row in bat.head(12).iterrows():
    n=row['name']; d=legal[legal['striker_name']==n]; pr=d[d['pressure']]
    ipl=pr[pr['is_ipl']]; rec=pr[pr['yr']>=2025]
    def sr(x): return round(x['runs'].sum()/len(x)*100,1) if len(x) else None
    out["batters"].append(dict(rank=len(out["batters"])+1,name=n,final=round(row['final'],1),rating=round(row['rating'],1),
        pr_balls=int(row['pr_balls']),pr_runs=int(row['pr_runs']),pr_sr=round(row['pr_sr'],1),adj=round(row['adj_sr'],1),
        uplift=round(row['uplift'],1),avg=round(row['pr_avg'],1) if pd.notna(row['pr_avg']) else None,cons=round(row['cons'],1),
        ipl_pr=int(row['ipl_pr_balls']),ipl_sr=sr(ipl),rec_sr=sr(rec),rec_balls=int(len(rec)),team26=team26(n),
        bat_order=int(d['batting_order'].median()) if len(d) else None))
for i,row in bowl.head(12).iterrows():
    n=row['name']; d=legal[legal['bowler_name']==n]; pr=d[d['pressure']]
    ipl=pr[pr['is_ipl']]; rec=pr[pr['yr']>=2025]
    def ec(x): return round(x['bowler_runs'].sum()/len(x)*6,2) if len(x) else None
    out["bowlers"].append(dict(rank=len(out["bowlers"])+1,name=n,final=round(row['final'],1),rating=round(row['rating'],1),
        pr_balls=int(row['pr_balls']),pr_wk=int(row['pr_wk']),pr_econ=round(row['pr_econ'],2),adj=round(row['adj_econ'],2),
        wk_rate=round(row['wk_rate'],2),dot=round(row['pr_dot'],1),cons=round(row['cons'],1),
        ipl_pr=int(row['ipl_pr_balls']),ipl_econ=ec(ipl),rec_econ=ec(rec),rec_balls=int(len(rec)),team26=team26(n),
        style=f"{d['bowling_type'].mode().iloc[0]} ({d['pace_or_spin'].mode().iloc[0]})" if len(d) else ""))
json.dump(out, open("finalists.json","w"), indent=1)
print(json.dumps(out, indent=1))
