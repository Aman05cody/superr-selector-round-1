import pandas as pd, numpy as np
b=pd.read_pickle("balls_v3.pkl")
legal=b[b['is_legal']].copy()
_mm=pd.read_csv('Data Pack/matches.csv'); _cc=pd.read_csv('Data Pack/competitions.csv')
_smap=_mm.set_index('match_id')['comp_id'].map(_cc.set_index('comp_id')['season']).to_dict()
legal['season']=legal['match_id'].map(_smap)
legal['match_inn']=legal['match_id'].astype(str)+'_'+legal['innings'].astype(str)
def yr(s):
    try: return int(str(s)[:4])
    except: return np.nan
legal['yr']=legal['season'].apply(yr)
legal['period']=np.where(legal['yr']>=2025,'2025-26','2022-24')
bat_final=["Naman Dhir","Suryakumar Yadav","Jos Buttler","Phil Salt","Glenn Phillips","Liam Livingstone","Rinku Singh","Tim David","Shreyas Iyer","Tristan Stubbs","William Jacks","Nicholas Pooran"]
bowl_final=["Akeal Hosein","Matheesha Pathirana","Gerald Coetzee","Maheesh Theekshana","Jasprit Bumrah","Corbin Bosch","Sunil Narine","Mustafizur Rahman","Noor Ahmad","Kuldeep Yadav","Rashid Khan","Eshan Malinga"]
def bat_check(name):
    d=legal[(legal['striker_name']==name)]
    pr=d[d['pressure']]
    def sr(x): return x['runs'].sum()/len(x)*100 if len(x) else np.nan
    ipl=pr[pr['is_ipl']]; t20=pr[~pr['is_ipl']]
    e1=pr[pr['period']=='2022-24']; e2=pr[pr['period']=='2025-26']
    print(f"{name}: PR {len(pr)}b SR {sr(pr):.1f} | IPL-PR {len(ipl)}b SR {sr(ipl):.1f} | T20I-PR {len(t20)}b SR {sr(t20):.1f} | 22-24 {len(e1)}b SR {sr(e1):.1f} | 25-26 {len(e2)}b SR {sr(e2):.1f} | death-share {(pr['subtype']=='death').mean()*100:.0f}% | IPL tot balls {len(d[d['is_ipl']])}")
def bowl_check(name):
    d=legal[(legal['bowler_name']==name)]
    pr=d[d['pressure']]
    def ec(x): return x['bowler_runs'].sum()/len(x)*6 if len(x) else np.nan
    def wr(x): return x['bowler_wkt'].sum()/len(x)*24 if len(x) else np.nan
    ipl=pr[pr['is_ipl']]; t20=pr[~pr['is_ipl']]
    e1=pr[pr['period']=='2022-24']; e2=pr[pr['period']=='2025-26']
    print(f"{name}: PR {len(pr)}b Ec {ec(pr):.2f} Wk/24 {wr(pr):.2f} | IPL-PR {len(ipl)}b Ec {ec(ipl):.2f} | T20I-PR {len(t20)}b Ec {ec(t20):.2f} | 22-24 {len(e1)}b Ec {ec(e1):.2f} | 25-26 {len(e2)}b Ec {ec(e2):.2f} | death-share {(pr['subtype']=='death').mean()*100:.0f}% | IPL tot balls {len(d[d['is_ipl']])}")
print("=== BAT finalists ===")
for n in bat_final: bat_check(n)
print("\n=== BOWL finalists ===")
for n in bowl_final: bowl_check(n)
print("\n=== RR 2026 squad pressure (bat) ===")
rr26=["Yashasvi Jaiswal","Vaibhav Sooryavanshi","Riyan Parag","Dhruv Jurel","Shimron Hetmyer","Ravindra Jadeja","Sam Curran","Donovan Ferreira","Dasun Shanaka","Shubham Dubey","Lhuan Pretorius"]
bat=pd.read_csv("bat_stats2.csv")
print(bat[bat.name.isin(rr26)][['name','tot_balls','pr_balls','pr_runs','pr_sr','adj_sr','uplift','pr_avg','cons','ipl_pr_balls']].round(1).sort_values('adj_sr',ascending=False).to_string(index=False))
print("\n=== RR 2026 squad pressure (bowl) ===")
bowl=pd.read_csv("bowl_stats2.csv")
rrb=["Jofra Archer","Sandeep Sharma","Tushar Deshpande","Nandre Burger","Kwena Maphaka","Kuldeep Sen","Ravi Bishnoi","Vignesh Puthur","Ravindra Jadeja","Sam Curran","Adam Milne","Yudhvir Singh"]
print(bowl[bowl.name.isin(rrb)][['name','tot_balls','pr_balls','pr_wk','pr_econ','adj_econ','wk_rate','pr_dot','cons','ipl_pr_balls']].round(2).sort_values('adj_econ').to_string(index=False))
print("\n=== Dataset summary ===")
print("matches:", len(pd.read_csv('Data Pack/matches.csv')), "balls inn1-2:", len(b), "legal:", len(legal), "pressure legal:", legal['pressure'].sum())
print("IPL matches:", pd.read_csv('Data Pack/matches.csv').merge(pd.read_csv('Data Pack/competitions.csv'),on='comp_id').query("match_format=='T20'").shape[0])
