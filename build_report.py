#!/usr/bin/env python3
"""SupeRR Selector Season 2 — Round 1 methodology report (PDF)."""
import json
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                Image, PageBreak, KeepTogether, HRFlowable)
from reportlab.lib import colors

PINK = HexColor("#E4007C"); NAVY = HexColor("#12263F"); GREY = HexColor("#5A6B80")
LIGHT = HexColor("#FDEEF5"); MID = HexColor("#E8EDF2"); GOLD = HexColor("#B98A1D")
OUT = "/home/hatch/workspace/your_files/SupeRR-Selector-Round1-RR-Auction-Strategy.pdf"
FIN = json.load(open("/home/hatch/workspace/superR-selector/finalists.json"))

S = {}
S["h1"] = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=15, leading=18, textColor=NAVY, spaceBefore=10, spaceAfter=6)
S["h2"] = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=12, leading=15, textColor=PINK, spaceBefore=10, spaceAfter=4)
S["h3"] = ParagraphStyle("h3", fontName="Helvetica-Bold", fontSize=10.5, leading=13, textColor=NAVY, spaceBefore=8, spaceAfter=3)
S["body"] = ParagraphStyle("body", fontName="Helvetica", fontSize=9.5, leading=13.5, textColor=HexColor("#1F2A37"), spaceAfter=5)
S["small"] = ParagraphStyle("small", fontName="Helvetica", fontSize=8.5, leading=12, textColor=GREY, spaceAfter=4)
S["bullet"] = ParagraphStyle("bullet", parent=S["body"], leftIndent=12, bulletIndent=4, spaceAfter=3)
S["cell"] = ParagraphStyle("cell", fontName="Helvetica", fontSize=8, leading=10.5, textColor=HexColor("#1F2A37"))
S["cellB"] = ParagraphStyle("cellB", parent=S["cell"], fontName="Helvetica-Bold")
S["cellW"] = ParagraphStyle("cellW", parent=S["cell"], textColor=white, fontName="Helvetica-Bold")
S["cellC"] = ParagraphStyle("cellC", parent=S["cell"], alignment=TA_CENTER)
S["cellBC"] = ParagraphStyle("cellBC", parent=S["cellB"], alignment=TA_CENTER)
S["coverT"] = ParagraphStyle("coverT", fontName="Helvetica-Bold", fontSize=26, leading=30, textColor=NAVY)
S["coverS"] = ParagraphStyle("coverS", fontName="Helvetica", fontSize=13, leading=18, textColor=PINK)

def P(t, st="body"): return Paragraph(t, S[st])
def tbl(header, rows, widths, align_center_from=1):
    data = [[Paragraph(h, S["cellW"]) for h in header]]
    for r in rows:
        data.append([Paragraph(str(c), S["cellB"] if i == 0 else S["cell"]) if i == 0 else
                     Paragraph(str(c), S["cellC"]) for i, c in enumerate(r)])
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT]),
        ("GRID", (0, 0), (-1, -1), 0.4, HexColor("#C9D2DC")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t

def footer(canvas, doc):
    canvas.saveState()
    if doc.page > 1:
        canvas.setFont("Helvetica", 7.5); canvas.setFillColor(GREY)
        canvas.drawString(15*mm, 12*mm, "SupeRR Selector Season 2  |  Round 1  |  Rajasthan Royals — IPL 2027 Auction Strategy  |  Aman Prasad Bari")
        canvas.drawRightString(A4[0]-15*mm, 12*mm, f"Page {doc.page}")
    canvas.restoreState()

story = []
# ---------- COVER ----------
story.append(Spacer(1, 38*mm))
story.append(P("RAJASTHAN ROYALS", "coverS"))
story.append(P("SupeRR Selector<br/>Season 2 — Round 1", "coverT"))
story.append(Spacer(1, 4*mm))
story.append(HRFlowable(width="22%", thickness=2.5, color=PINK, spaceAfter=5, spaceBefore=2, hAlign="LEFT"))
story.append(Paragraph("Identify the Most Reliable Players<br/>Under Pressure", ParagraphStyle("ct2", parent=S["coverT"], fontSize=17, leading=21, textColor=PINK)))
story.append(Spacer(1, 6*mm))
story.append(P("A data-driven ranking of the batters and bowlers who deliver when the game is on the line — "
               "and the players Rajasthan Royals should back at the IPL 2027 auction.", "body"))
story.append(Spacer(1, 10*mm))
cover_rows = [["Submitted by", "Aman Prasad Bari"],
              ["Email", "amanprasadbari05@gmail.com"],
              ["Competition", "SupeRR Selector Season 2 (Unstop)"],
              ["Round", "Round 1 — live 10 Nov 2026, 6:00 PM IST to 18 Nov 2026, 11:59 PM IST"],
              ["Date of report", "12 November 2026"],
              ["Data", "Official Round 1 data pack: IPL 2022–2026 + T20I 2022–2026 ball-by-ball"]]
ct = Table([[Paragraph(f"<b>{a}</b>", S["cell"]), Paragraph(b, S["cell"])] for a, b in cover_rows],
           colWidths=[32*mm, 138*mm])
ct.setStyle(TableStyle([("BACKGROUND", (0, 0), (0, -1), LIGHT), ("GRID", (0, 0), (-1, -1), 0.4, HexColor("#C9D2DC")),
                        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                        ("LEFTPADDING", (0, 0), (-1, -1), 5), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
story.append(ct)
story.append(Spacer(1, 8*mm))
story.append(P("<b>How to use this report.</b>  The two ranked Top 10 lists on page 2 are the submission — enter them in the "
               "Unstop dropdowns exactly as listed. Everything after page 2 is the evidence: how pressure was defined, "
               "how the ratings were built, what the numbers say player by player, and what RR should actually do at the auction.", "small"))
story.append(PageBreak())

# ---------- EXEC SUMMARY ----------
story.append(P("Executive summary — the two Top 10 lists", "h1"))
story.append(P("One line first: <b>RR's problem is not talent at the top, it is reliability at the end.</b> In this data, RR's regular "
               "batters score barely above par under pressure (Hetmyer +13.2, Parag +15.0, Jurel +4.6, Jaiswal −8.7 on the adjusted "
               "scale in §3), and RR's death bowlers Sandeep Sharma (+1.13) and Tushar Deshpande (+0.98) both concede <i>more</i> than par "
               "under pressure. The auction must therefore buy finishers and death bowlers — not more top-order batsmen.", "body"))
story.append(P("<b>Top 10 batters under pressure</b> — Final Score in brackets (0–100; §4 explains it). Enter in this order on Unstop.", "h3"))
brows = []
for x in FIN["batters"][:10]:
    brows.append([x["rank"], x["name"], f"{x['pr_sr']:.1f}", f"+{x['adj']:.1f}", f"{x['pr_balls']}", f"{x['ipl_sr']:.1f}", x["team26"].replace("Mumbai Indians", "MI").replace("Royal Challengers Bengaluru", "RCB").replace("Kolkata Knight Riders", "KKR").replace("Punjab Kings", "PBKS").replace("Sunrisers Hyderabad", "SRH").replace("Lucknow Super Giants", "LSG").replace("Gujarat Titans", "GT").replace("Delhi Capitals", "DC")])
story.append(tbl(["#", "Batter", "Press. SR", "Adj. SR*", "Press. balls", "IPL press. SR", "IPL 2026 team"],
                 [[r[0], r[1], r[2], r[3], r[4], r[5], r[6]] for r in brows],
                 [8*mm, 42*mm, 22*mm, 20*mm, 22*mm, 24*mm, 32*mm]))
story.append(P("* Adjusted SR = pressure strike rate minus the par strike rate for the exact situations that player faced (§3). "
               "Naman Dhir's +68.9 means he scored about 69 runs per 100 balls more than par in the same spots.", "small"))
story.append(P("<b>Top 10 bowlers under pressure</b> — Final Score in brackets. Enter in this order on Unstop.", "h3"))
wrows = []
for x in FIN["bowlers"][:10]:
    wrows.append([x["rank"], x["name"], f"{x['pr_econ']:.2f}", f"{x['adj']:.2f}", f"{x['pr_wk']}", f"{x['wk_rate']:.2f}", f"{x['ipl_econ']:.2f}" if x["ipl_econ"] else "—", x["team26"].replace("Mumbai Indians", "MI").replace("Kolkata Knight Riders", "KKR").replace("Chennai Super Kings", "CSK").replace("Sunrisers Hyderabad", "SRH").replace("Not in IPL 2026", "— (free agent)")])
story.append(tbl(["#", "Bowler", "Press. econ", "Adj. econ*", "Press. wkts", "Wkts / 24 balls", "IPL press. econ", "IPL 2026 team"],
                 wrows, [8*mm, 40*mm, 22*mm, 20*mm, 20*mm, 24*mm, 22*mm, 24*mm]))
story.append(P("* Adjusted economy = pressure economy minus the par economy for the exact situations that bowler faced. "
               "Negative is good: Bumrah's −2.29 means he conceded 2.29 runs per over fewer than par in the same spots.", "small"))
story.append(P("<b>Read the rankings with the auction in mind.</b> Most of the twenty names currently belong to other franchises, "
               "so availability matters as much as ability — §7 sorts them into "
               "<i>bid to win</i>, <i>bid if the price is right</i> and <i>pursue only if released</i>. The most valuable realistic "
               "targets are <b>Maheesh Theekshana</b> (ex-RR, not in IPL 2026 — a free agent), <b>Naman Dhir</b>, <b>Tim David</b>, "
               "<b>Rinku Singh</b> and <b>Noor Ahmad</b>.", "body"))
story.append(P("<b>One warning the data forces on us.</b> Akeal Hosein is No. 1 on the raw five-year rating (88.5) but only 16 of his "
               "162 pressure balls were bowled in the IPL, and his 2025–26 pressure economy (7.41) is far worse than his 2022–24 figure "
               "(4.47). Once IPL evidence and recent form are weighted in (§4), he falls to 12th. He is listed as first bowling alternate, "
               "not in the Top 10 — that is the method working as intended, not an oversight.", "body"))

# ---------- 1 RR PROBLEM ----------
story.append(P("1 &nbsp; Why RR need this — what the 2026 squad already shows", "h1"))
story.append(P("The data pack itself contains the IPL 2025 and 2026 squads, so RR's gaps can be measured rather than assumed. "
               "RR's IPL 2026 squad (27 players) included Jaiswal, Vaibhav Sooryavanshi, Parag, Jurel, Hetmyer, Jadeja (traded in from CSK), "
               "Sam Curran, Donovan Ferreira, Dasun Shanaka, Archer, Sandeep Sharma, Tushar Deshpande, Nandre Burger and Ravi Bishnoi. "
               "Sanju Samson — RR's captain until 2025 — was traded to CSK for IPL 2026, and Maheesh Theekshana, RR's best pressure bowler "
               "in 2025, did not play IPL 2026 at all.", "body"))
story.append(P("RR batters under pressure (adjusted SR, §3) — regulars vs bench:", "h3"))
story.append(tbl(["Player", "Role in RR 2026", "Press. balls", "Press. SR", "Adj. SR", "Verdict"],
                 [["Donovan Ferreira", "Bench / finisher", "172", "173.8", "+37.5", "Best in squad — underused"],
                  ["Shubham Dubey", "Bench / finisher", "92", "182.6", "+28.4", "Strong — underused"],
                  ["Dasun Shanaka", "Squad all-rounder", "357", "159.7", "+20.5", "Useful"],
                  ["Riyan Parag", "Regular, No. 4–5", "205", "174.6", "+15.0", "Above par, not elite"],
                  ["Shimron Hetmyer", "Regular finisher", "482", "164.7", "+13.2", "Below what a finisher needs"],
                  ["Dhruv Jurel", "Regular, keeper-batter", "291", "164.6", "+4.6", "Around par"],
                  ["Yashasvi Jaiswal", "Regular opener", "46", "156.5", "−8.7", "Rarely bats under pressure"]],
                 [34*mm, 34*mm, 22*mm, 22*mm, 20*mm, 38*mm]))
story.append(P("RR bowlers under pressure (adjusted economy — negative is better than par):", "h3"))
story.append(tbl(["Player", "Press. balls", "Press. econ", "Adj. econ", "Verdict"],
                 [["Nandre Burger", "95", "8.78", "−0.78", "Best current RR pressure bowler"],
                  ["Jofra Archer", "270", "9.02", "−0.52", "Solid, not a death lock"],
                  ["Ravindra Jadeja", "224", "7.77", "−0.39", "Control, few wickets (1.07 / 24 balls)"],
                  ["Ravi Bishnoi", "605", "8.71", "+0.39", "Around par"],
                  ["Tushar Deshpande", "312", "11.08", "+0.98", "Concedes ~1 run/over over par"],
                  ["Sandeep Sharma", "282", "11.11", "+1.13", "Concedes ~1.1 runs/over over par"],
                  ["Sam Curran", "364", "10.65", "+1.16", "Concedes ~1.2 runs/over over par"]],
                 [40*mm, 24*mm, 24*mm, 24*mm, 58*mm]))
story.append(P("Two conclusions follow. <b>First, RR's bench finishers (Ferreira, Dubey) already outperform the regulars under pressure</b> — "
               "selection, not just recruitment, is part of the fix. <b>Second, RR's death bowling is the clearest hole:</b> the three bowlers "
               "RR most often trust at the death are all worse than par there, while the one elite pressure bowler RR had (Theekshana, "
               "adjusted economy −1.79) was let go. The rankings in §5–§6 are therefore read through one lens: who fixes the finish "
               "with the bat and the death with the ball?", "body"))

# ---------- 2 DATA ----------
story.append(P("2 &nbsp; The data", "h1"))
story.append(P("All analysis uses only the supplied Round 1 data pack (downloaded from Unstop, file <i>6af458274c1e8_data_pack.zip</i>), "
               "covering 22 January 2022 to 1 November 2026:", "body"))
for b in ["<b>883 matches</b> in 141 competitions — <b>371 IPL matches</b> (IPL 2022–2026, 74–75 per season) and <b>512 T20I matches</b>.",
          "<b>200,999 ball-by-ball deliveries</b>; 200,961 in innings 1–2 (38 super-over balls excluded), of which <b>193,251 are legal balls</b> "
          "(wides excluded — a wide is not a ball faced or bowled). <b>42,009 legal balls (21.7%) are classified as pressure</b> under §3.",
          "<b>888 batters and 647 bowlers</b> appear; after the eligibility gates in §4, <b>105 batters and 148 bowlers</b> qualify for ranking.",
          "Files used: <i>ball_by_ball.csv</i>, <i>matches.csv</i>, <i>competitions.csv</i>, <i>teams.csv</i>, "
          "<i>competition_team_player_mapping.csv</i> (for IPL 2025/2026 squads) and <i>playing_eleven.csv</i> (cross-checks).",
          "Runs: a batter's runs are the <i>runs</i> column; a bowler's runs conceded are bat runs plus wide/no-ball extras "
          "(leg-byes and byes are not charged to the bowler). A bowler's wicket excludes run-outs, retire-outs and obstructing the field."]:
    story.append(P(b, "bullet", ))
story.append(P("No outside performance data was used for the rankings. Public context (2026 squads, trades) comes only from the data pack's own "
               "team–player mapping, so every squad claim in this report can be checked inside the pack.", "body"))

# ---------- 3 PRESSURE ----------
story.append(P("3 &nbsp; What counts as pressure?", "h1"))
story.append(P("Pressure is not a feeling — it is a match situation in which the cost of the next ball is unusually high. A ball is "
               "classified <b>high-pressure</b> if it meets <i>any</i> of five transparent rules. The same balls are pressure for the "
               "batter and for the bowler, so the two rankings are built on one definition, as the brief requires.", "body"))
story.append(tbl(["#", "Rule", "What it captures", "Balls"],
                 [["A", "Death finish — overs 18–20 in the 2nd innings; overs 19–20 in the 1st", "The endgame, where every ball changes the result", "12,773*"],
                  ["B", "Tight finish — 2nd innings, ≤30 balls left, 1–36 runs needed", "A game either side can still win", "8,799"],
                  ["C", "Late high required rate — 2nd innings, over ≥13, required rate ≥10", "A chase slipping away", "12,574"],
                  ["D", "Collapse — 4+ wickets down by over 10", "Rebuilding after early damage", "7,499"],
                  ["E", "Knockout death — knockout match, overs 17–20", "Elimination games at the death", "364"]],
                 [8*mm, 78*mm, 58*mm, 26*mm]))
story.append(P("* Rule A overlaps rules B–E, so the rows do not sum to 42,009; each ball is counted once, with priority B &gt; A &gt; C &gt; D &gt; E "
               "for the subtype tables below.", "small"))
story.append(P("Why these rules, and why not a simpler one? Three checks shaped them. <b>First, a single rule fails:</b> using only death overs "
               "misses chases lost in overs 13–16 and collapses; using only required rate fails because a target of 180 makes the required "
               "rate 9.00 from ball one — that is a normal chase, not pressure. That is why rule C requires over ≥13 <i>and</i> rate ≥10. "
               "<b>Second, the rules must bite:</b> an early version (death from over 17, any required rate ≥9) labelled 43.4% of all balls "
               "as pressure — too broad to distinguish anything. The final version labels 21.7%, close to one ball in five. "
               "<b>Third, the rules must be checkable:</b> every rule uses only over, innings, runs needed, balls left and wickets down — "
               "anyone with the pack can reproduce the classification exactly.", "body"))
story.append(P("Par for each situation. &nbsp; A 190 strike rate in a collapse is worth far more than a 190 strike rate at the death, "
               "because the average batter scores much slower in a collapse. So for each pressure subtype — separately for IPL and T20I — "
               "we computed the league par strike rate and par economy on pressure balls:", "body"))
story.append(tbl(["Pressure subtype", "IPL par SR", "IPL par econ", "T20I par SR", "T20I par econ"],
                 [["Collapse (4+ wkts down, ≤over 10)", "112.9", "6.79", "104.9", "6.31"],
                  ["Death (overs 18–20, 2nd inns)", "177.9", "10.70", "163.0", "9.83"],
                  ["Knockout death", "173.5", "10.43", "140.3", "8.42"],
                  ["Late high required rate (≥10, over ≥13)", "150.9", "9.08", "136.6", "8.22"],
                  ["Tight finish (≤30 balls, 1–36 needed)", "173.7", "10.45", "148.7", "8.94"]],
                 [62*mm, 27*mm, 27*mm, 27*mm, 27*mm]))
story.append(Image("/home/hatch/workspace/superR-selector/chart_par.png", width=170*mm, height=66*mm))
story.append(P("Figure 1 — Par strike rate is 65 points higher at the death than in a collapse (IPL). Any rating that compares raw strike "
               "rates across these situations without adjusting for them will simply rank death-overs specialists first. The adjusted "
               "metrics in §4 exist to stop that.", "small"))
story.append(P("A player's <b>adjusted strike rate</b> is therefore his pressure strike rate minus the par strike rate of the <i>exact mix</i> "
               "of situations he faced (same for economy). A player who only ever bats in collapses is judged against collapse par, not "
               "against death par. The same adjustment is done separately for IPL and T20I balls, because IPL par is higher in every subtype.", "body"))

# ---------- 4 METHOD ----------
story.append(P("4 &nbsp; How the ratings were built", "h1"))
story.append(P("<b>Batting — Pressure Rating (0–100).</b> For each batter: pressure strike rate (40%), uplift vs his own non-pressure "
               "strike rate (10%), pressure average (5%), consistency — the share of his pressure innings (≥5 pressure balls) in which he "
               "scored 15+ runs at a strike rate ≥120 (15%), absolute pressure strike rate (20%) and pressure-ball volume (10%). Each "
               "component is normalised across the eligible pool (2nd–98th percentile, clipped 0–100).", "body"))
story.append(P("<b>Bowling — Pressure Rating (0–100).</b> Adjusted economy (40%), wicket rate in wickets per 24 pressure balls (20%), "
               "absolute pressure economy (15%), consistency — the share of his pressure innings (≥6 pressure balls) with economy ≤8.00 (10%), "
               "pressure-ball volume (10%) and dot-ball percentage (5%).", "body"))
story.append(P("<b>Final Score — the ranking score.</b> &nbsp; Final Score = 0.60 × Pressure Rating (2022–26, IPL + T20I) + 0.25 × IPL-only "
               "pressure score + 0.15 × Recent (2025–26) pressure score. The IPL-only and recent scores use the same adjusted metric as the "
               "main rating, shrunk by n/(n+60) so that a brilliant 20-ball cameo cannot outrank 300 balls of evidence, and scored as neutral "
               "(30 / 40) when a player has fewer than 20 IPL pressure balls or 30 recent pressure balls. Rationale: the target competition "
               "is the IPL, and 2027 form matters more than 2022 form — but neither should erase five years of evidence.", "body"))
story.append(P("<b>Tie-break.</b> If two Final Scores are within 1.0 point, the player with more IPL pressure balls ranks higher. This decided "
               "three places: Bumrah over Theekshana (341 vs 150 IPL pressure balls), Pathirana over Narine (332 vs 294), and Rinku Singh "
               "over Nicholas Pooran (402 vs 346) — in each case the higher-volume IPL player is ranked first.", "body"))
story.append(P("<b>Eligibility gates (applied before ranking).</b> Batters and bowlers need ≥70 pressure balls, ≥300 total legal balls, "
               "≥10 pressure innings, and at least two seasons in the data. This removes one-match wonders: 105 batters and 148 bowlers pass.", "body"))
story.append(P("<b>Auction filters (applied after ranking, to produce the submitted lists).</b> (i) Played in 2025 or 2026. "
               "(ii) Not a Pakistan player — Pakistan players do not play in the IPL, so Babar Azam, Shaheen Afridi, Abrar Ahmed, Mohammad Nawaz "
               "and others are excluded from the submitted lists even when they rank highly on pure numbers (they appear in the Appendix). "
               "(iii) Not in RR's IPL 2026 squad — RR cannot buy players they already own. (iv) At least 50 IPL balls in the data — this "
               "excludes T20I-only names such as Taskin Ahmed (pure-rating bowling No. 6, zero IPL balls). (v) Sanju Samson is excluded: RR "
               "themselves traded him to CSK for IPL 2026, so a buy-back is not a realistic auction plan. Dinesh Karthik (retired after 2024) "
               "is excluded by filter (i). No player was excluded for reputation, age or price — only by these five stated rules.", "body"))
story.append(P("All figures in this report were computed from the data pack in Python (pandas). The ball classification, par tables and "
               "ratings are deterministic from the five rules above; the only judgement calls are the weights, which are stated here in full.", "body"))

# ---------- 5 BATTERS ----------
story.append(P("5 &nbsp; Top 10 batters under pressure", "h1"))
story.append(Image("/home/hatch/workspace/superR-selector/chart_bat.png", width=170*mm, height=74*mm))
story.append(P("Figure 2 — Every one of the Top 10 lifts his strike rate under pressure. Dhir (+78), Rinku (+57) and Livingstone (+53) "
               "improve most on their own baseline; Tim David's uplift is smallest (+24) only because his non-pressure strike rate "
               "(167.2) is already the highest of the ten.", "small"))
story.append(tbl(["#", "Batter (Final)", "Press. balls / runs", "Press. SR", "Adj. SR", "Avg", "Cons.*", "IPL press. SR"],
                 [[x["rank"], f"{x['name']} ({x['final']:.1f})", f"{x['pr_balls']} / {x['pr_runs']}", f"{x['pr_sr']:.1f}", f"+{x['adj']:.1f}", f"{x['avg']:.1f}", f"{x['cons']:.0f}%", f"{x['ipl_sr']:.1f} ({x['ipl_pr']}b)"] for x in FIN["batters"][:10]],
                 [8*mm, 44*mm, 28*mm, 18*mm, 16*mm, 14*mm, 14*mm, 28*mm]))
story.append(P("* Consistency = share of pressure innings (≥5 pressure balls) with 15+ runs at SR ≥120.", "small"))
profiles_b = [
 ("<b>1 — Naman Dhir (92.6, MI).</b> The clear No. 1, and not a small-sample artefact: 163 pressure balls, strike rate 224.5, "
  "adjusted +68.9 — about 69 runs per 100 balls above par in the same situations. IPL pressure SR 212.8 (117 balls) and recent "
  "SR 227.8 (133 balls in 2025–26) both confirm it; consistency 83% is the best in the Top 10. Median batting position 4. <b>RR fit:</b> "
  "the finisher RR do not have — bid to win."),
 ("<b>2 — Suryakumar Yadav (85.5, MI).</b> The largest proven sample after Tim David: 374 pressure balls, SR 210.4, adjusted +58.7. "
  "The one caution is recency — his 2025–26 pressure SR (174.2) is well below his 2022–24 figure (223.1). Still elite, but the price "
  "must reflect a player past his peak pressure years. <b>RR fit:</b> pursue only if MI release him, which is unlikely."),
 ("<b>3 — Shreyas Iyer (81.3, PBKS).</b> The best recent form in the Top 10: pressure SR 213.5 in 2025–26 (171 balls), IPL pressure "
  "SR 202.0. A No. 4 who anchors <i>and</i> finishes — exactly the middle-order profile RR lack. <b>RR fit:</b> bid to win if released; "
  "also the only Top 10 batter with captaincy value."),
 ("<b>4 — Tim David (79.8, RCB).</b> The most bankable finisher in the data: 536 pressure balls, 1,024 pressure runs — both the highest "
  "of any batter — SR 191.0, IPL pressure SR 197.0, recent SR 206.3. Volume is its own reliability argument. <b>RR fit:</b> bid to win; "
  "the safe pick if Dhir's price runs away."),
 ("<b>5 — Jos Buttler (79.7, GT).</b> Ex-RR, and RR know exactly what he does: pressure SR 202.8, IPL pressure SR 210.6, adjusted +40.8. "
  "Opens or finishes, and keeps wicket. <b>RR fit:</b> a buy-back only if GT release him — and only then, because Jaiswal and Vaibhav "
  "already fill the opener slots."),
 ("<b>6 — Liam Livingstone (74.7, SRH).</b> Best IPL pressure strike rate in the Top 10 (221.8), plus a bowling option. The flag is "
  "recency: only 17 pressure balls in 2025–26, so his recent score is neutral by rule — the ranking rests on 2022–24. <b>RR fit:</b> "
  "bid if the price is right, not at any price."),
 ("<b>7 — William Jacks (74.1, MI).</b> Adjusted SR +47.8 is third-best, but on only 75 pressure balls — the smallest sample in the "
  "Top 10 — and his IPL pressure SR of 274.3 rests on 35 balls. Genuine upside (also bowls off-spin), genuine variance. <b>RR fit:</b> "
  "a value bid, not a marquee bid."),
 ("<b>8 — Marcus Stoinis (73.5, PBKS).</b> 335 pressure balls, SR 181.8, IPL pressure SR 188.0, recent SR 193.4 — consistent across "
  "every cut. Ignore his bowling under pressure (economy 10.69): buy the bat. <b>RR fit:</b> bid if the price is right; the "
  "all-rounder slot is already crowded at RR (Jadeja, Curran, Parag)."),
 ("<b>9 — Rinku Singh (69.6, KKR).</b> The safest IPL-proven finisher in the data: 402 IPL pressure balls (more than any batter), "
  "SR 179.4, pressure average 42.9 — the highest average in the Top 10, because he finishes unbeaten so often. Recent SR 171.5 is "
  "softer than his 2022–24 figure (194.4), which is why he is 9th, not 4th. <b>RR fit:</b> bid to win — the lowest-risk Indian finisher available."),
 ("<b>10 — Nicholas Pooran (70.1, LSG).</b> 435 pressure balls, IPL pressure SR 192.5 (346 balls), left-handed middle order — a "
  "different look from RR's right-heavy finishers. Recent sample is small (44 balls in 2025–26), so the ranking leans on his large "
  "IPL body of work. <b>RR fit:</b> bid if the price is right."),
]
for t in profiles_b:
    story.append(P(t, "bullet"))
story.append(P("<b>First alternates:</b> Romario Shepherd (69.7) — IPL pressure SR 205.2 and recent SR 190.6, but only 97 IPL pressure "
               "balls and a poor pressure bowling record, so he ranks as a batter only; and Tristan Stubbs (66.5) — 312 IPL pressure balls, "
               "but his recent SR fell to 154.3.", "body"))

# ---------- 6 BOWLERS ----------
story.append(P("6 &nbsp; Top 10 bowlers under pressure", "h1"))
story.append(Image("/home/hatch/workspace/superR-selector/chart_bowl.png", width=170*mm, height=74*mm))
story.append(P("Figure 3 — Every Top 10 bowler beats par for the situations he bowled in. Bumrah's gap (−2.29) is the largest, and it comes "
               "mostly at the death, where par is 10.70 — the hardest place to beat par. Narine's gap comes with the lowest absolute economy (6.51).", "small"))
story.append(tbl(["#", "Bowler (Final)", "Press. balls / wkts", "Press. econ", "Adj. econ", "Wkts/24", "Dot %", "IPL press. econ"],
                 [[x["rank"], f"{x['name']} ({x['final']:.1f})", f"{x['pr_balls']} / {x['pr_wk']}", f"{x['pr_econ']:.2f}", f"{x['adj']:.2f}", f"{x['wk_rate']:.2f}", f"{x['dot']:.0f}%", f"{x['ipl_econ']:.2f} ({x['ipl_pr']}b)" if x["ipl_econ"] else "—"] for x in FIN["bowlers"][:10]],
                 [8*mm, 42*mm, 26*mm, 18*mm, 16*mm, 16*mm, 12*mm, 32*mm]))
profiles_w = [
 ("<b>1 — Jasprit Bumrah (85.2, MI).</b> Best adjusted economy in the data (−2.29) on the biggest death sample: 53% of his 475 pressure "
  "balls were at the death, IPL pressure economy 7.06 against a death par of 10.70, stable across periods (7.32 → 7.61). <b>RR fit:</b> "
  "the benchmark, not a realistic target — pursue only if MI release him. Use his number to price everyone else."),
 ("<b>2 — Maheesh Theekshana (85.4, free agent).</b> The most important name in this report: RR's own 2025 pressure bowler "
  "(adjusted −1.79, 384 balls), IPL pressure economy 6.68, and rock-steady across periods (7.10 → 7.03). He did not play IPL 2026. "
  "<b>RR fit:</b> re-sign him. He is available, he knows the franchise, and he directly replaces the spin control RR lost."),
 ("<b>3 — Matheesha Pathirana (82.1, KKR).</b> The wicket-taker: 47 pressure wickets, 2.41 per 24 balls, 468 pressure balls. The warning "
  "is recent form — pressure economy 9.74 in 2025–26 (114 balls) against 7.12 in 2022–24. <b>RR fit:</b> bid, but with a hard price "
  "ceiling; do not chase him past it."),
 ("<b>4 — Sunil Narine (82.7, KKR).</b> The reliability pick: all 294 of his pressure balls were bowled in the IPL, economy 6.51, "
  "and almost identical across periods (6.50 → 6.53). Consistency 79% is the best among the pace/spin leaders. <b>RR fit:</b> pursue only "
  "if KKR release him; the most bankable spinner in the list."),
 ("<b>5 — Noor Ahmad (80.3, CSK).</b> Left-arm wrist-spin, 276 pressure balls, IPL pressure economy 6.88, recent 6.95 — no decline "
  "anywhere in his profile, and the youngest of the spin options. <b>RR fit:</b> bid to win; a long-term asset, not a one-season fix."),
 ("<b>6 — Mustafizur Rahman (76.1, KKR).</b> The form pick: pressure economy improved from 8.79 (2022–24) to 6.47 (2025–26), and 53% of "
  "his pressure balls are at the death. The counter-flag is his IPL pressure economy (9.23) — the improvement is partly T20I-driven. "
  "<b>RR fit:</b> bid if the price is right; verify the IPL-death number before going big."),
 ("<b>7 — Corbin Bosch (74.6, MI).</b> All 127 of his pressure balls came in 2025–26 — a genuine newcomer, not a five-year record — with "
  "the best dot-ball rate in the Top 10 (53.5%). IPL pressure economy 8.81 tempers the enthusiasm. <b>RR fit:</b> a value pace bid."),
 ("<b>8 — Gerald Coetzee (74.4, SRH).</b> Best wicket rate in the Top 10 (3.05 per 24 balls) on 118 pressure balls. But his IPL pressure "
  "economy is 9.39 — the T20I numbers (6.21) flatter him. <b>RR fit:</b> bid if the price is right, as a wicket-taking change-up, "
  "not as a death-overs lock."),
 ("<b>9 — Varun Chakravarthy (72.0, KKR).</b> 472 pressure balls, and the recent trend is the story: pressure economy 6.32 in 2025–26 "
  "(222 balls) against 8.36 in the IPL overall. A mystery spinner peaking now. <b>RR fit:</b> bid to win if the price stays sane."),
 ("<b>10 — Eshan Malinga (71.1, SRH).</b> Steady rather than spectacular: 292 pressure balls, economy 8.01, IPL pressure economy 8.57, "
  "recent 8.50. No red flags, no fireworks. <b>RR fit:</b> the sensible last pick — a death-overs workhorse at a workhorse price."),
]
for t in profiles_w:
    story.append(P(t, "bullet"))
story.append(P("<b>First alternates:</b> Lungi Ngidi (71.7) — wicket rate 2.57 per 24 balls, but economy 8.49 and consistency only 40%; "
               "and Akeal Hosein (71.1) — No. 1 on the raw five-year rating, 12th on the Final Score (see Executive Summary). "
               "Taskin Ahmed, pure-rating No. 6, is excluded entirely: he has bowled zero balls in the IPL.", "body"))

# ---------- 7 AUCTION PLAN ----------
story.append(P("7 &nbsp; What RR should do at the IPL 2027 auction", "h1"))
story.append(P("<b>Bid to win (realistic and fills the gap).</b> Theekshana (re-sign), Naman Dhir, Tim David, Rinku Singh, Noor Ahmad, "
               "Varun Chakravarthy, Eshan Malinga. These seven are either free agents, plausibly released, or Indian players RR can "
               "actually buy — and each one directly fixes the finish or the death.", "body"))
story.append(P("<b>Bid if the price is right.</b> Shreyas Iyer, Marcus Stoinis, Nicholas Pooran, Liam Livingstone, William Jacks, "
               "Mustafizur Rahman, Corbin Bosch, Gerald Coetzee. All would help; none is worth breaking the purse for, and each carries a "
               "flag in §5–§6 (recency, sample size or IPL-death economy) that should cap the bid.", "body"))
story.append(P("<b>Pursue only if released.</b> Suryakumar Yadav, Jos Buttler, Jasprit Bumrah, Matheesha Pathirana, Sunil Narine. "
               "Five of the best pressure players in the data — and five players their franchises have no reason to release. RR should "
               "register interest and move on; the plan must not depend on them.", "body"))
story.append(P("<b>The overseas-slot constraint.</b> Only three of the Top 10 batters (Dhir, Shreyas, Rinku) and two of the Top 10 bowlers "
               "(Bumrah, Varun) are Indian. An IPL squad holds at most 8 overseas players and an XI at most 4. RR cannot buy the whole "
               "list — the Indian core (Dhir, Shreyas, Rinku) plus two or three overseas picks (Theekshana, Noor, David) is the realistic "
               "shape of the shopping list. That is also why Dhir and Rinku matter more than their raw ranks suggest: Indian finishers "
               "under pressure are the scarcest resource in this data.", "body"))
story.append(P("<b>Price discipline.</b> Do not pay a marquee price for Pathirana (recent economy 9.74), Coetzee (IPL pressure economy 9.39) "
               "or Hosein (16 IPL pressure balls). Do not pay for reputation over the adjusted numbers: the whole point of this exercise is "
               "that a bowler with a famous name and a pressure economy of 11.08 (Tushar Deshpande, already at RR) is worse than a quiet "
               "one at 7.08 (Theekshana). Finally, fix selection too: Ferreira (+37.5) and Dubey (+28.4) already outperform RR's regular "
               "finishers under pressure and should play more, whatever the auction delivers.", "body"))

# ---------- 8 RELIABILITY ----------
story.append(P("8 &nbsp; Reliability checks — and where the model is less certain", "h1"))
story.append(P("<b>Split-half (2022–24 vs 2025–26).</b> The headline names survive the split. Dhir: 210.0 → 227.8. Tim David: 184.6 → 206.3. "
               "Shreyas: 151.9 → 213.5. Theekshana: 7.10 → 7.03. Narine: 6.50 → 6.53. Bumrah: 7.32 → 7.61. The names that do <i>not</i> survive "
               "it are flagged, not hidden: Suryakumar (223.1 → 174.2), Stubbs (200.9 → 154.3), Pathirana (7.12 → 9.74), Kuldeep Yadav "
               "(6.86 → 9.42 — which is why Kuldeep, pure-rating No. 11 among bowlers, does not make the Top 10).", "body"))
story.append(P("<b>IPL vs T20I.</b> Every Top 10 player has his IPL-only pressure number printed in §5–§6. The Final Score weights IPL "
               "evidence at 25% precisely because T20I opposition is weaker (par SR is lower in every subtype, §3) and because some "
               "T20I stars never face IPL pressure. The biggest IPL/T20I gaps in the near-misses are instructive: Hosein's IPL pressure "
               "economy is 7.88 on 16 balls against a 5.38 T20I figure; Babar Azam (pure-rating batting No. 4) has zero IPL balls and is "
               "excluded as a Pakistan player in any case.", "body"))
story.append(P("<b>Consistency.</b> The consistency column is the share of a player's pressure innings that were genuinely good. "
               "Dhir 83%, Narine 79%, Hosein 79%, Theekshana 73%, SKY 69%, Livingstone 70% — the Top 10 are not one-innings wonders. "
               "The lowest consistency in either Top 10 is Jacks (43%) and Bosch (54%), both flagged in their profiles.", "body"))
story.append(P("9 &nbsp; Limitations and reproducibility", "h1"))
for b in ["<b>Pressure is defined, not discovered.</b> The five rules are reasoned choices (§3), not a fitted model. A different "
          "definition (e.g. win-probability leverage) would shuffle the middle of the rankings, though the top names are robust: "
          "Dhir, SKY, Bumrah and Theekshana lead under the pure rating, the IPL-only rating and the Final Score alike.",
          "<b>Sample sizes are small for some finalists.</b> Jacks (75 pressure balls), Bosch (127), Coetzee (118) — their scores carry "
          "wide uncertainty, and the shrinkage in §4 only partly corrects for it. Treat their ranks as ±3, not exact.",
          "<b>Availability is as of the data pack.</b> Retention and release decisions for IPL 2027 are not in the pack and were not "
          "assumed, except for the five stated auction filters. If a 'pursue only if released' player is retained, RR should move to "
          "the first alternate in the same category.",
          "<b>What the data cannot see:</b> fitness, form after 1 November 2026, price, auction dynamics, team balance beyond the "
          "overseas cap, and match-ups (e.g. a bowler's record against specific batters). The report ranks pressure performance; "
          "the auction room must add price and fit.",
          "<b>Reproduce it:</b> take <i>ball_by_ball.csv</i> (innings 1–2, wides excluded), rebuild runs-needed, balls-left, wickets-down "
          "and required rate ball by ball, apply the five rules in §3, compute par by subtype × format, then the ratings in §4 with the "
          "gates and filters stated. Every number in §5–§6 follows from those steps; no step uses data outside the pack."]:
    story.append(P(b, "bullet"))
story.append(P("Appendix — for the record", "h1"))
story.append(P("<b>Pure five-year Pressure Rating, unfiltered (Top 10).</b> Batters: 1 Naman Dhir (88.6), 2 Suryakumar Yadav (87.3), "
               "3 Najibullah Zadran (85.8), 4 Babar Azam (79.3), 5 Dinesh Karthik (75.8), 6 Jos Buttler (75.1), 7 Phil Salt (74.7), "
               "8 Glenn Phillips (74.0), 9 Liam Livingstone (72.9), 10 Rinku Singh (72.2). Bowlers: 1 Akeal Hosein (88.5), "
               "2 Sufiyan Muqeem (82.9), 3 Mohammad Nawaz (82.2), 4 Matheesha Pathirana (81.1), 5 Riley Meredith (80.6), "
               "6 Abrar Ahmed (79.2), 7 Gerald Coetzee (78.3), 8 Abbas Afridi (76.9), 9 Maheesh Theekshana (76.3), 10 Jasprit Bumrah (75.4). "
               "The Final Score moves Hosein, Nawaz, Sufiyan, Abrar, Meredith and Abbas out of the submitted Top 10 for the reasons stated "
               "in §4 and §8 (Pakistan ineligibility, no IPL evidence, or retired/inactive) — the pure list is kept here so the effect of "
               "every filter is auditable.", "body"))
story.append(P("<b>Excluded notables, and why.</b> Babar Azam (batting pure No. 4) and Shaheen Afridi — Pakistan players, IPL-ineligible. "
               "Najibullah Zadran (pure No. 3) — last played 2024, zero IPL balls. Dinesh Karthik (pure No. 5) — retired after IPL 2024. "
               "Sanju Samson (adjusted SR +39.5, would rank near the Top 10) — traded by RR to CSK for IPL 2026. Taskin Ahmed (bowling pure "
               "No. 6) — zero IPL balls. Glenn Phillips (pure No. 8) and Phil Salt (pure No. 7) — their pressure evidence is mostly T20I; "
               "once IPL and recent form are weighted they fall just outside the submitted Top 10 (Phillips Final 65.3).", "body"))
story.append(P("<b>Submission checklist for Unstop.</b> Batters, Rank 1–10: Naman Dhir, Suryakumar Yadav, Shreyas Iyer, Tim David, "
               "Jos Buttler, Liam Livingstone, William Jacks, Marcus Stoinis, Rinku Singh, Nicholas Pooran. Bowlers, Rank 1–10: "
               "Jasprit Bumrah, Maheesh Theekshana, Matheesha Pathirana, Sunil Narine, Noor Ahmad, Mustafizur Rahman, Corbin Bosch, "
               "Gerald Coetzee, Varun Chakravarthy, Eshan Malinga. Upload this report as the methodology document. Deadline: "
               "18 November 2026, 11:59 PM IST.", "body"))
story.append(Spacer(1, 6*mm))
story.append(HRFlowable(width="100%", thickness=0.7, color=MID, spaceAfter=4, spaceBefore=4))
story.append(P("Prepared by Aman Prasad Bari for SupeRR Selector Season 2, Round 1. Data: official Round 1 data pack "
               "(IPL 2022–2026 and T20I 2022–2026). Analysis and report completed 12 November 2026.", "small"))

doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=15*mm, rightMargin=15*mm, topMargin=14*mm, bottomMargin=16*mm,
                        title="SupeRR Selector Season 2 — Round 1: Most Reliable Players Under Pressure (Rajasthan Royals)",
                        author="Aman Prasad Bari")
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print("built", OUT)
