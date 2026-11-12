import pandas as pd, numpy as np
b=pd.read_pickle("balls_enriched.pkl")
# --- PRESSURE v2 ---
b['pressure'] = (
  ((b['over_num']>=18)&(b['innings']==2)) |
  ((b['over_num']>=19)&(b['innings']==1)) |
  ((b['innings']==2)&(b['balls_remaining']<=30)&(b['runs_needed']>=1)&(b['runs_needed']<=36)) |
  ((b['innings']==2)&(b['over_num']>=13)&(b['rrr']>=10)) |
  ((b['wkts_down']>=4)&(b['over_num']<=10)) |
  ((b['knock_out']==1)&(b['over_num']>=17))
)
b['pressure'] = b['pressure'].fillna(False)
legal = b[b['is_legal']].copy()
print("pressure share legal:", round(legal['pressure'].mean(),3), legal['pressure'].sum(), "of", len(legal))
# season per match
m=pd.read_csv("Data Pack/matches.csv")
comp=pd.read_csv("Data Pack/competitions.csv")
season_map = m.set_index('match_id')['comp_id'].map(comp.set_index('comp_id')['season']).to_dict()
legal['season'] = legal['match_id'].map(season_map)
legal['match_inn'] = legal['match_id'].astype(str)+"_"+legal['innings'].astype(str)

def bat_stats(df):
    g=df.groupby(['striker_id','striker_name'])
    rows=[]
    for (pid,name), d in g:
        tot=d; pr=d[d['pressure']]; base=d[~d['pressure']]
        def s(x):
            balls=len(x); runs=x['runs'].sum(); outs=x['batter_out'].sum()
            return balls, runs, outs, (runs/balls*100 if balls else 0), (runs/outs if outs else np.nan), ((x['is_four']|x['is_six']).mean()*100 if balls else 0), ((x['runs']==0).mean()*100 if balls else 0)
        tb,tr,to,tsr,tavg,tbnd,tdot=s(tot); pb,pr_,po,psr,pavg,pbnd,pdot=s(pr); bb,br,bo,bsr,bavg,bbnd,bdot=s(base)
        # pressure innings
        pi = pr['match_inn'].nunique(); ti = tot['match_inn'].nunique()
        # consistency: pressure innings with >=5 pressure balls and SR>=120 or 15+ runs
        good=0; pin_n=0
        for _,x in pr.groupby('match_inn'):
            if len(x)>=5:
                pin_n+=1
                if x['runs'].sum()>=15 and (x['runs'].sum()/len(x)*100>=120): good+=1
        cons = good/pin_n*100 if pin_n else 0
        ipl_pr = pr['is_ipl'].sum(); ipl_tot = tot['is_ipl'].sum()
        seasons = tot['season'].nunique()
        rows.append(dict(pid=pid,name=name,tot_balls=tb,tot_runs=tr,tot_outs=to,tot_sr=tsr,tot_avg=tavg,
            pr_balls=pb,pr_runs=pr_,pr_outs=po,pr_sr=psr,pr_avg=pavg,pr_bnd=pbnd,pr_dot=pdot,
            base_sr=bsr,base_avg=bavg,uplift=psr-bsr,pr_inn=pi,tot_inn=ti,cons=cons,good_inn=good,pin_n=pin_n,
            ipl_pr_balls=ipl_pr,ipl_tot_balls=ipl_tot,seasons=seasons))
    return pd.DataFrame(rows)

def bowl_stats(df):
    g=df.groupby(['bowler_id','bowler_name'])
    rows=[]
    for (pid,name), d in g:
        tot=d; pr=d[d['pressure']]; base=d[~d['pressure']]
        def s(x):
            balls=len(x); runs=x['bowler_runs'].sum(); wk=x['bowler_wkt'].sum()
            econ=runs/balls*6 if balls else 0; avg=runs/wk if wk else np.nan; sr=balls/wk if wk else np.nan
            return balls,runs,wk,econ,avg,sr,((x['runs']==0)&(x['bowler_runs']==0)).mean()*100 if balls else 0, ((x['is_four']|x['is_six']).mean()*100 if balls else 0)
        tb,tr,tw,te,ta,ts,tdot,tbnd=s(tot); pb,pr_,pw,pe,pa,ps,pdot,pbnd=s(pr); bb,br,bw,be,ba,bs,bdot,bbnd=s(base)
        pi=pr['match_inn'].nunique()
        good=0; pin_n=0
        for _,x in pr.groupby('match_inn'):
            if len(x)>=6:
                pin_n+=1
                if x['bowler_runs'].sum()/len(x)*6<=8.0: good+=1
        cons=good/pin_n*100 if pin_n else 0
        rows.append(dict(pid=pid,name=name,tot_balls=tb,tot_runs=tr,tot_wk=tw,tot_econ=te,tot_avg=ta,tot_sr=ts,
            pr_balls=pb,pr_runs=pr_,pr_wk=pw,pr_econ=pe,pr_avg=pa,pr_sr=ps,pr_dot=pdot,pr_bnd=pbnd,
            base_econ=be,econ_gain=be-pe,wk_rate=pw/pb*24 if pb else 0,pr_inn=pi,cons=cons,good_inn=good,pin_n=pin_n,
            ipl_pr_balls=pr['is_ipl'].sum(),ipl_tot_balls=tot['is_ipl'].sum(),seasons=tot['season'].nunique(),
            pace_spin=tot['pace_or_spin'].mode().iloc[0] if len(tot) else '', bowl_type=tot['bowling_type'].mode().iloc[0] if len(tot) else ''))
    return pd.DataFrame(rows)

bat=bat_stats(legal); bowl=bowl_stats(legal)
bat.to_csv("bat_stats.csv",index=False); bowl.to_csv("bowl_stats.csv",index=False)
print("\nBAT eligible >=70 pr balls, >=300 tot, >=10 pr inn:")
e=bat[(bat.pr_balls>=70)&(bat.tot_balls>=300)&(bat.pr_inn>=10)]
print(len(e),"eligible")
print(e.sort_values('pr_sr',ascending=False)[['name','pr_balls','pr_runs','pr_outs','pr_sr','pr_avg','base_sr','uplift','pr_bnd','cons','ipl_pr_balls','seasons']].head(25).to_string(index=False))
print("\nBOWL eligible >=70 pr balls, >=300 tot, >=10 pr inn:")
eb=bowl[(bowl.pr_balls>=70)&(bowl.tot_balls>=300)&(bowl.pr_inn>=10)]
print(len(eb),"eligible")
print(eb.sort_values('pr_econ')[['name','pr_balls','pr_wk','pr_econ','base_econ','econ_gain','pr_avg','wk_rate','pr_dot','cons','ipl_pr_balls','pace_spin']].head(25).to_string(index=False))
b.to_pickle("balls_v2.pkl")
