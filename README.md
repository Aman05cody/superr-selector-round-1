# SupeRR Selector Season 2 — Round 1

**Identify the Most Reliable Players Under Pressure**
Rajasthan Royals IPL 2027 auction strategy — Aman Prasad Bari, 12 November 2026.

This repo holds the complete code and outputs behind the Round 1 submission
(the "v1" pure rankings): every number in the report was computed from the
official data pack by the scripts in this folder. No outside statistics, no
reputation, no price guesses.

## Results (the submission)

**Top 10 batters:** 1 Naman Dhir (92.6), 2 Suryakumar Yadav (85.5),
3 Shreyas Iyer (81.3), 4 Tim David (79.8), 5 Jos Buttler (79.7),
6 Liam Livingstone (74.7), 7 William Jacks (74.1), 8 Marcus Stoinis (73.5),
9 Rinku Singh (69.6), 10 Nicholas Pooran (70.1).

**Top 10 bowlers:** 1 Jasprit Bumrah (85.2), 2 Maheesh Theekshana (85.4),
3 Matheesha Pathirana (82.1), 4 Sunil Narine (82.7), 5 Noor Ahmad (80.3),
6 Mustafizur Rahman (76.1), 7 Corbin Bosch (74.6), 8 Gerald Coetzee (74.4),
9 Varun Chakravarthy (72.0), 10 Eshan Malinga (71.1).

## The data

The official data pack: 883 matches (22 Jan 2022 – 1 Nov 2026), 371 IPL
(IPL 2022–2026) and 512 T20 internationals. `ball_by_ball.csv` has 200,999
rows; after removing 38 super-over balls, the working set is 200,961 balls
across innings 1 and 2, of which 193,251 are legal balls (wides excluded).
The pack's `format` field calls several domestic tournaments "T20", so a ball
counts as IPL only when its competition name starts with "IPL ".

## Method (what the code does)

1. **Pressure definition — `analyze.py` + `analyze2.py`.** A ball is
   high-pressure if ANY of five rules applies: (A) death — overs 18–20 in
   the 2nd innings / 19–20 in the 1st; (B) tight finish — 2nd innings,
   ≤30 balls left, 1–36 runs needed; (C) late high RRR — 2nd innings,
   over ≥13, RRR ≥10; (D) collapse — 4+ wickets down by over 10;
   (E) knockout death — knockout match, overs 17–20. That flags 42,009
   balls, 21.7% of legal balls. (`analyze.py` first used a broader
   definition that flagged 43.4%; it was rejected as too broad and
   `analyze2.py` replaces it with the five rules above.)
2. **Par for the situation — `analyze3.py`.** Every pressure ball gets a
   subtype (priority: tight > death > late-RRR > collapse > knockout-death)
   and a par strike rate / economy for that exact subtype × format.
   Death overs in the IPL average SR 177.9 / econ 10.70; a collapse in the
   IPL averages only 112.9 / 6.79. Adjusted SR = pressure SR minus par;
   adjusted economy = pressure economy minus par.
3. **Player stats — `analyze2.py` (batters), `analyze3.py` (bowlers).**
   Per player: pressure balls, runs, strike rate, adjusted SR, uplift vs
   own non-pressure baseline, pressure average, consistency (share of
   pressure innings beating par), IPL-only pressure balls, and the same
   for bowling (economy, adjusted economy, wickets per 24 balls, dot %).
4. **Pressure Rating — `rank.py`.** Each component is normalised 0–100
   across the eligible pool (2nd–98th percentile). Batting: adjusted SR
   40%, pressure SR 20%, consistency 15%, uplift 10%, volume 10%,
   pressure average 5%. Bowling: adjusted economy 40%, wicket rate 20%,
   pressure economy 15%, consistency 10%, volume 10%, dot % 5%.
   Eligibility gates: ≥70 pressure balls, ≥300 total balls,
   ≥10 pressure innings.
5. **Final Score — `blend.py`.**
   Final = 0.60 × Pressure Rating + 0.25 × IPL-only score + 0.15 × recent
   (2025–26) score. The IPL-only and recent scores use the same adjusted
   figures restricted to IPL pressure balls and to 2025–26 pressure balls,
   shrunk towards neutral by n/(n+60). Players with too little IPL or
   recent evidence get neutral scores of 30 and 40.
6. **Final lists — `final_tables.py`.** Active in 2025–26, not a Pakistan
   player (IPL-ineligible), not in RR's IPL 2026 squad, not Sanju Samson
   (traded to CSK) or Dinesh Karthik, and at least 50 IPL total balls.
   Tie-break: within 1.0 Final Score point of the group leader, more IPL
   pressure balls ranks higher.
7. **Checks — `checks.py`.** Independent re-computation of every
   finalist's IPL vs T20I and 2022–24 vs 2025–26 splits, plus RR's own
   squad pressure numbers.
8. **Export + report — `export_numbers.py`, `make_charts.py`,
   `build_report.py`.** `finalists.json` (all Top 10 details),
   charts, and the 9-page methodology report PDF.

## How to run

Needs Python 3 with `pandas`, `numpy`, `matplotlib`, `reportlab`, and the
data pack in a folder called `Data Pack` next to the scripts
(`ball_by_ball.csv`, `matches.csv`, `competitions.csv`, `teams.csv`,
`competition_team_player_mapping.csv`, `playing_eleven.csv`). Run in order:

```
python3 analyze.py
python3 analyze2.py
python3 analyze3.py
python3 rank.py
python3 blend.py
python3 final_tables.py
python3 checks.py
python3 export_numbers.py
python3 make_charts.py
python3 build_report.py
```

That regenerates every CSV, `finalists.json`, the charts, and the report PDF.

## Files

| File | Does |
|---|---|
| `analyze.py` | Loads the pack, builds match context (target, RRR, balls left, wickets down), first pressure definition, saves `balls_enriched.pkl` |
| `analyze2.py` | Final 5-rule pressure definition, per-batter stats, saves `balls_v2.pkl`, `bat_stats2.csv` |
| `analyze3.py` | Pressure subtypes, par table (`par_subtype_format.csv`), per-bowler stats, saves `balls_v3.pkl`, `bowl_stats2.csv` |
| `rank.py` | Pressure Rating (0–100) for batters and bowlers, eligibility gates, saves `bat_ranked.csv`, `bowl_ranked.csv` |
| `blend.py` | IPL-only + recent (2025–26) scores, Final Score, saves `bat_final.csv`, `bowl_final.csv` |
| `final_tables.py` | Filters (active, not Pakistan, not RR 2026 squad, ≥50 IPL balls) + tie-break, saves `bat_submitted.csv`, `bowl_submitted.csv` |
| `checks.py` | Independent verification of every finalist and RR's squad |
| `export_numbers.py` | Top 10 details with IPL/recent splits, saves `finalists.json` |
| `make_charts.py` | Pressure SR/econ charts |
| `build_report.py` | Builds the 9-page methodology report PDF |
| `data/` | Computed outputs: `finalists.json`, `bat_final.csv`, `bowl_final.csv`, `par_subtype_format.csv`, charts |

## Key findings

- Naman Dhir is the No. 1 batter under pressure: 163 pressure balls,
  SR 224.5, adjusted +68.9, and he lifts his game by 77.6 SR points
  under pressure.
- Akeal Hosein was pure-rating No. 1 (88.5) but fell to 12th once IPL
  evidence and recent form were weighted: only 16 of his 162 pressure
  balls were bowled in the IPL.
- RR's death bowling was worse than par (Sandeep Sharma +1.13, Tushar
  Deshpande +0.98, Sam Curran +1.16); the top order is not the problem
  (Jaiswal 1,485 IPL balls at SR 155.2; Vaibhav Sooryavanshi 449 IPL
  balls at SR 229.0) — both fail the pressure gates because openers
  rarely face defined pressure situations.
- Vignesh Puthur, last season's winning pick, fails the gates (18
  pressure balls, economy 14.67).

## Limitations

Small samples for some players (e.g. William Jacks, 75 pressure balls);
T20I par is lower than IPL par, so T20I-heavy records are flattered;
the pressure definition under-rates top-order batters; and the lists are
the best players under pressure, not an availability filter — the brief
asks for the best performers, period.
