import pandas as pd, numpy as np
bat=pd.read_csv("bat_stats2.csv"); bowl=pd.read_csv("bowl_stats2.csv")
# pakistan players (IPL-ineligible) - by name, verify via teams? hardcode from knowledge, cross-check with T20I teams
PAK = {"Babar Azam","Shaheen Afridi","Abrar Ahmed","Mohammad Nawaz","Mohammad Wasim","Abbas Afridi","Fakhar Zaman","Saim Ayub","Sufiyan Muqeem","Mohammad Rizwan","Haris Rauf","Naseem Shah","Shadab Khan","Iftikhar Ahmed","Salman Mirza","Usman Khan","Mohammad Haris","Azam Khan"}
RR_CORE = {"Sanju Samson","Yashasvi Jaiswal","Riyan Parag","Dhruv Jurel","Shimron Hetmyer","Jofra Archer","Sandeep Sharma","Tushar Deshpande","Wanindu Hasaranga","Maheesh Theekshana"}
# note Theekshana was RR 2025-26? He played for RR in 2025. Check later; keep flag only Samson for now in final filter, others noted
def norm(s, higher_better=True):
    s=s.astype(float)
    lo,hi=s.quantile(0.02), s.quantile(0.98)
    x=(s-lo)/(hi-lo)*100
    x=x.clip(0,100)
    return x if higher_better else 100-x

def bat_rating(df):
    e=df[(df.pr_balls>=70)&(df.tot_balls>=300)&(df.pr_inn>=10)].copy()
    e['n_adj']=norm(e['adj_sr'],True); e['n_sr']=norm(e['pr_sr'],True); e['n_cons']=e['cons'].clip(0,100)
    e['n_uplift']=norm(e['uplift'],True); e['n_vol']=norm(np.log(e['pr_balls']),True)
    e['n_avg']=norm(e['pr_avg'].fillna(e['pr_avg'].median()).clip(upper=60),True)
    e['rating']=0.40*e['n_adj']+0.20*e['n_sr']+0.15*e['n_cons']+0.10*e['n_uplift']+0.10*e['n_vol']+0.05*e['n_avg']
    return e.sort_values('rating',ascending=False)
def bowl_rating(df):
    e=df[(df.pr_balls>=70)&(df.tot_balls>=300)&(df.pr_inn>=10)].copy()
    e['n_adj']=norm(e['adj_econ'],False); e['n_econ']=norm(e['pr_econ'],False); e['n_wk']=norm(e['wk_rate'],True)
    e['n_cons']=e['cons'].clip(0,100); e['n_vol']=norm(np.log(e['pr_balls']),True); e['n_dot']=norm(e['pr_dot'],True)
    e['rating']=0.40*e['n_adj']+0.15*e['n_econ']+0.20*e['n_wk']+0.10*e['n_cons']+0.10*e['n_vol']+0.05*e['n_dot']
    return e.sort_values('rating',ascending=False)

br=bat_rating(bat); wr=bowl_rating(bowl)
br.to_csv("bat_ranked.csv",index=False); wr.to_csv("bowl_ranked.csv",index=False)
pd.set_option('display.width',250)
print("=== BAT composite top 25 (all eligible) ===")
print(br[['name','rating','pr_balls','pr_runs','pr_sr','adj_sr','uplift','pr_avg','cons','ipl_pr_balls','tot_last']].head(25).round(1).to_string(index=False))
print("\n=== BOWL composite top 25 (all eligible) ===")
print(wr[['name','rating','pr_balls','pr_wk','pr_econ','adj_econ','wk_rate','pr_dot','cons','ipl_pr_balls','pace_spin','tot_last']].head(25).round(2).to_string(index=False))
print("\n=== BAT filtered: active>=2025, not PAK, not Samson ===")
f=br[(pd.to_numeric(br.tot_last, errors='coerce')>=2025)&(~br.name.isin(PAK))&(~br.name.isin(["Sanju Samson","Dinesh Karthik"]))]
print(f[['name','rating','pr_balls','pr_runs','pr_sr','adj_sr','uplift','pr_avg','cons','ipl_pr_balls','tot_last']].head(15).round(1).to_string(index=False))
print("\n=== BOWL filtered: active>=2025, not PAK ===")
fw=wr[(pd.to_numeric(wr.tot_last, errors='coerce')>=2025)&(~wr.name.isin(PAK))]
print(fw[['name','rating','pr_balls','pr_wk','pr_econ','adj_econ','wk_rate','pr_dot','cons','ipl_pr_balls','pace_spin','tot_last']].head(15).round(2).to_string(index=False))
print("\n=== RR core check ===")
print("bat RR:", bat[bat.name.isin(RR_CORE)][['name','pr_balls','pr_sr','adj_sr','tot_last']].to_string(index=False))
print("bowl RR:", bowl[bowl.name.isin(RR_CORE)][['name','pr_balls','pr_econ','adj_econ','tot_last']].to_string(index=False))
