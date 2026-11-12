import pandas as pd, numpy as np
bat=pd.read_csv("bat_final.csv"); bowl=pd.read_csv("bowl_final.csv")
# apply tie-break: within 1.0 of group leader, order by IPL pressure balls desc
def tiebreak(df, score='final', ipl='ipl_pr_balls'):
    df=df.sort_values(score,ascending=False).reset_index(drop=True)
    out=[]; i=0
    while i<len(df):
        j=i+1
        while j<len(df) and df.loc[i,score]-df.loc[j,score]<=1.0:
            j+=1
        grp=df.iloc[i:j].sort_values(ipl,ascending=False)
        out.append(grp); i=j
    return pd.concat(out).reset_index(drop=True)
PAK={"Babar Azam","Shaheen Afridi","Abrar Ahmed","Mohammad Nawaz","Mohammad Wasim","Abbas Afridi","Fakhar Zaman","Saim Ayub","Sufiyan Muqeem","Mohammad Rizwan","Haris Rauf","Naseem Shah","Shadab Khan","Iftikhar Ahmed","Salman Mirza"}
RR26={"Adam Milne","Aman Rao Perala","Brijesh Sharma","Dasun Shanaka","Dhruv Jurel","Donovan Ferreira","Emanjot Singh Chahal","Jofra Archer","Kuldeep Sen","Kwena Maphaka","Lhuan Pretorius","Nandre Burger","Ravi Bishnoi","Ravi Singh","Ravindra Jadeja","Riyan Parag","Sam Curran","Sandeep Sharma","Shimron Hetmyer","Shubham Dubey","Sushant Mishra","Tushar Deshpande","Vaibhav Sooryavanshi","Vignesh Puthur","Yash Punja","Yashasvi Jaiswal","Yudhvir Singh"}
def filt(df):
    d=df[(pd.to_numeric(df['tot_last'],errors='coerce')>=2025)&(~df['name'].isin(PAK))&(~df['name'].isin(RR26))&(~df['name'].isin(["Sanju Samson","Dinesh Karthik"]))].copy()
    # IPL experience: at least 50 IPL total balls (use ipl_tot_balls)
    d=d[d['ipl_tot_balls']>=50]
    return tiebreak(d)
bf=filt(bat); wf=tiebreak(bowl[(pd.to_numeric(bowl['tot_last'],errors='coerce')>=2025)&(~bowl['name'].isin(PAK))&(~bowl['name'].isin(RR26))&(bowl['ipl_tot_balls']>=50)])
bf.to_csv("bat_submitted.csv",index=False); wf.to_csv("bowl_submitted.csv",index=False)
print("=== SUBMITTED BATTERS Top 12 ===")
print(bf[['name','final','rating','pr_balls','pr_runs','pr_sr','adj_sr','uplift','pr_avg','cons','ipl_pr_balls','ipl_tot_balls']].head(12).round(1).to_string(index=False))
print("\n=== SUBMITTED BOWLERS Top 12 ===")
print(wf[['name','final','rating','pr_balls','pr_wk','pr_econ','adj_econ','wk_rate','pr_dot','cons','ipl_pr_balls','ipl_tot_balls','pace_spin']].head(12).round(2).to_string(index=False))
# IPL-only SR/econ + recent for finalists: merge from checks data via bat_stats2/bowl_stats2 + blend cols
for f in ["bat_submitted.csv","bowl_submitted.csv"]:
    d=pd.read_csv(f); print(f, len(d))
