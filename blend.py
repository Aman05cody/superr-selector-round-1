import pandas as pd, numpy as np
b=pd.read_pickle("balls_v3.pkl")
legal=b[b['is_legal']].copy()
# par IPL-only per subtype
par = legal[(legal['pressure'])&(legal['is_ipl'])].groupby('subtype').agg(balls=('runs','size'), bat_runs=('runs','sum'), bowl_runs=('bowler_runs','sum'))
par['par_sr']=par['bat_runs']/par['balls']*100; par['par_econ']=par['bowl_runs']/par['balls']*6
print("IPL-only par:\n", par.to_string())
psr=par['par_sr'].to_dict(); pec=par['par_econ'].to_dict()
def ipl_bat(df):
    out={}
    d=df[df['is_ipl'] & df['pressure']]
    for (pid,name), x in d.groupby(['striker_id','striker_name']):
        if len(x)<20: continue
        exp = sum(psr.get(s,150) for s in x['subtype'])/len(x)
        sr = x['runs'].sum()/len(x)*100
        out[pid]=(len(x), sr, sr-exp)
    return out
def ipl_bowl(df):
    out={}
    d=df[df['is_ipl'] & df['pressure']]
    for (pid,name), x in d.groupby(['bowler_id','bowler_name']):
        if len(x)<20: continue
        exp = sum(pec.get(s,9.0) for s in x['subtype'])/len(x)
        ec = x['bowler_runs'].sum()/len(x)*6
        out[pid]=(len(x), ec, ec-exp)
    return out
ib=ipl_bat(legal); iw=ipl_bowl(legal)
bat=pd.read_csv("bat_ranked.csv"); bowl=pd.read_csv("bowl_ranked.csv")
# recent 2025-26 adj: use full par (subtype x format) already in balls_v3 par_sr/par_econ
legal['yr']=legal['match_id'].map(pd.read_csv('Data Pack/matches.csv').set_index('match_id')['comp_id'].map(pd.read_csv('Data Pack/competitions.csv').set_index('comp_id')['season']).to_dict()).astype(str).str[:4].astype(float)
def recent_bat(df):
    out={}
    d=df[(df['yr']>=2025)&df['pressure']]
    for (pid,name), x in d.groupby(['striker_id','striker_name']):
        if len(x)<30: continue
        exp=x['par_sr'].mean(); sr=x['runs'].sum()/len(x)*100
        out[pid]=(len(x), sr, sr-exp)
    return out
def recent_bowl(df):
    out={}
    d=df[(df['yr']>=2025)&df['pressure']]
    for (pid,name), x in d.groupby(['bowler_id','bowler_name']):
        if len(x)<30: continue
        exp=x['par_econ'].mean(); ec=x['bowler_runs'].sum()/len(x)*6
        out[pid]=(len(x), ec, ec-exp)
    return out
rb=recent_bat(legal); rw=recent_bowl(legal)
# blended: final = 0.6*rating + 0.25*ipl_score + 0.15*recent_score ; scores normalised 0-100 within eligible pool
def norm_dict(vals, higher=True):
    s=pd.Series(vals); lo,hi=s.quantile(0.05),s.quantile(0.95); x=((s-lo)/(hi-lo)*100).clip(0,100)
    return (x if higher else 100-x).to_dict()
# BAT
e=bat[(bat.pr_balls>=70)&(bat.tot_balls>=300)&(bat.pr_inn>=10)].copy()
e['ipl_adj_raw']=[ib.get(p,(np.nan,np.nan,np.nan))[2] if p in ib else np.nan for p in e.pid]
e['ipl_adj']=[(ib[p][2]*ib[p][0]/(ib[p][0]+60)) if p in ib else np.nan for p in e.pid]
e['ipl_balls2']=[ib.get(p,(0,0,0))[0] if p in ib else 0 for p in e.pid]
e['rec_adj']=[(rb[p][2]*rb[p][0]/(rb[p][0]+60)) if p in rb else np.nan for p in e.pid]
e['ipl_score']=pd.Series(norm_dict(e['ipl_adj'].dropna(),True)).reindex(e.index)
# fill missing ipl score with 30 (penalty for no IPL pressure evidence)
e['ipl_score']=e['ipl_score'].fillna(30)
e['rec_score']=pd.Series(norm_dict(e['rec_adj'].dropna(),True)).reindex(e.index).fillna(40)
e['final']=0.60*e['rating']+0.25*e['ipl_score']+0.15*e['rec_score']
e=e.sort_values('final',ascending=False)
e.to_csv("bat_final.csv",index=False)
print("\nBAT blended top 20:")
print(e[['name','rating','final','pr_balls','pr_sr','adj_sr','ipl_balls2','ipl_adj','rec_adj','ipl_pr_balls','tot_last']].head(20).round(1).to_string(index=False))
# BOWL
w=bowl[(bowl.pr_balls>=70)&(bowl.tot_balls>=300)&(bowl.pr_inn>=10)].copy()
w['ipl_adj']=[(iw[p][2]*iw[p][0]/(iw[p][0]+60)) if p in iw else np.nan for p in w.pid]
w['ipl_balls2']=[iw.get(p,(0,0,0))[0] if p in iw else 0 for p in w.pid]
w['rec_adj']=[(rw[p][2]*rw[p][0]/(rw[p][0]+60)) if p in rw else np.nan for p in w.pid]
w['ipl_score']=pd.Series(norm_dict(w['ipl_adj'].dropna(),False)).reindex(w.index).fillna(30)
w['rec_score']=pd.Series(norm_dict(w['rec_adj'].dropna(),False)).reindex(w.index).fillna(40)
w['final']=0.60*w['rating']+0.25*w['ipl_score']+0.15*w['rec_score']
w=w.sort_values('final',ascending=False)
w.to_csv("bowl_final.csv",index=False)
print("\nBOWL blended top 20:")
print(w[['name','rating','final','pr_balls','pr_econ','adj_econ','ipl_balls2','ipl_adj','rec_adj','ipl_pr_balls','pace_spin','tot_last']].head(20).round(2).to_string(index=False))
