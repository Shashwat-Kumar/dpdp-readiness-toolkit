"""Sample 3 – DPDP readiness for 'Acme Learning Pvt Ltd' (FICTIONAL). Uses tool/dpdp_scorer.py on the SYNTHETIC inventory,
then renders a cover PNG (1600x900) and a 6-page PDF. Readiness work, not legal advice."""
import os, sys, subprocess, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(HERE, "..", "common")); sys.path.insert(0, os.path.join(ROOT, "tool"))
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Rectangle, FancyBboxPatch
from style import *
import dpdp_scorer as ds
mpl_setup()
INV = os.path.join(ROOT, "tool", "sample", "SYNTHETIC_inventory.csv")
MD = os.path.join(HERE, "SAMPLE_dpdp_scorer_output.md")
out = subprocess.run([sys.executable, os.path.join(ROOT, "tool", "dpdp_scorer.py"), INV, MD], capture_output=True, text=True, check=True).stdout.strip()
txt = open(MD).read()
open(MD, "w").write('> **SAMPLE DELIVERABLE built from SYNTHETIC data for "Acme Learning Pvt Ltd (fictional)". Not a real company. Readiness work, not legal advice.**\n\n' + txt)
# --- recompute structured results with the scorer's own CHECKS / yes() ---
rows = pd.read_csv(INV, dtype=str).fillna("")
SHORT = {"notice_given": "Notice", "consent_recorded": "Consent", "withdrawal_easy": "Withdraw", "purpose_defined": "Purpose",
         "retention_defined": "Retention", "processor_contract": "Processor DPA", "security_controls": "Security",
         "breach_process": "Breach", "rights_channel": "Rights", "children_check": "Children"}
acts, matrix, gaps = [], [], []
tot = got = 0
for _, r in rows.iterrows():
    s = mx = 0; line = {}
    for col, ref, w, fix in ds.CHECKS:
        if col == "children_check" and r.get("child_data", "n").lower() not in ("y", "yes"): line[col] = "n/a"; continue
        mx += w
        if ds.yes(r.get(col, "")): s += w; line[col] = "Met"
        else: line[col] = "Gap"; gaps.append(dict(w=w, prio="P1" if w == 3 else "P2", activity=r["activity"].replace(" (SYNTHETIC)", ""), system=r["system"], ref=ref, fix=fix, col=col))
    tot += mx; got += s; pct = 100 * s / mx
    acts.append(dict(activity=r["activity"].replace(" (SYNTHETIC)", ""), system=r["system"], data=r["data_categories"], score=pct,
                     rag="GREEN" if pct >= 80 else "AMBER" if pct >= 50 else "RED", child=r["child_data"]))
    matrix.append(line)
acts = pd.DataFrame(acts); overall = 100 * got / tot
gaps = pd.DataFrame(gaps).sort_values("w", ascending=False, kind="stable").reset_index(drop=True)
RAGC = {"GREEN": GREEN, "AMBER": AMBER, "RED": RED}
print(out, "| P1:", (gaps.prio == "P1").sum(), "P2:", (gaps.prio == "P2").sum())
# enrichment (SYNTHETIC) for the data inventory page
ENR = {"Customer signup": ("Learners, parents", "48,000", "AWS Mumbai", "None (in-house)", "Indefinite"),
       "Marketing WhatsApp campaigns": ("Prospects, learners", "1,20,000", "BSP vendor, India", "WhatsApp BSP", "Indefinite"),
       "Payroll": ("Employees", "85", "HRMS SaaS, India", "HRMS provider", "8 yrs (statutory)"),
       "Student learning app": ("Students (approx. 60% under 18)", "31,000", "AWS Mumbai + analytics SDK (US)", "Analytics SDK", "Not defined"),
       "Support tickets": ("Learners, parents", "9,500 / yr", "Helpdesk SaaS (EU)", "Helpdesk provider", "Not defined")}
DEADLINE = dt.date(2027, 5, 13)
SHORTPH = ["Discovery", "Close P1 gaps", "Close P2 gaps", "Drill, re-notice, evidence", "Buffer"]
GAPNAME = {"notice_given": "notice", "consent_recorded": "consent records", "withdrawal_easy": "withdrawal", "purpose_defined": "purpose",
           "retention_defined": "retention", "processor_contract": "vendor DPA", "security_controls": "security", "breach_process": "breach playbook",
           "rights_channel": "rights channel", "children_check": "parental consent"}
PHASES = [("Discovery & inventory", dt.date(2026, 10, 1), dt.date(2026, 10, 31), TEAL_L),
          ("Close P1 gaps: notice, consent, security, breach, children", dt.date(2026, 11, 1), dt.date(2026, 12, 31), TEAL_D),
          ("Close P2 gaps: DPAs, retention, rights channel, withdrawal", dt.date(2027, 1, 1), dt.date(2027, 2, 28), TEAL),
          ("Breach drill, re-notice users, evidence pack", dt.date(2027, 3, 1), dt.date(2027, 4, 30), TEAL_L),
          ("Buffer & sign-off", dt.date(2027, 5, 1), DEADLINE, "#9CC4C6")]

def gauge(ax, val, r=1.0, w=0.28, fs=46):
    ax.set_aspect("equal"); ax.axis("off")
    for lo, hi, c in ((0, 50, RED), (50, 80, AMBER), (80, 100, GREEN)):
        ax.add_patch(Wedge((0, 0), r, 180 - hi * 1.8, 180 - lo * 1.8, width=w, fc=c, ec="white", lw=2, alpha=0.22))
    ax.add_patch(Wedge((0, 0), r, 180 - val * 1.8, 180, width=w, fc=TEAL, ec="white", lw=2))
    a = np.radians(180 - val * 1.8); ax.plot([0, 0.66 * r * np.cos(a)], [0, 0.66 * r * np.sin(a)], color=INK, lw=3, solid_capstyle="round")
    ax.add_patch(plt.Circle((0, 0), 0.05, color=INK))
    ax.text(0, -0.25, f"{val:.0f}%", ha="center", va="center", fontsize=fs, weight="black", color=TEAL_D)
    for v in (0, 50, 80, 100):
        aa = np.radians(180 - v * 1.8); ax.text(1.13 * r * np.cos(aa), 1.13 * r * np.sin(aa), f"{v}", ha="center", va="center", fontsize=fs * 0.24, color=GREY)
    ax.set_xlim(-1.25, 1.25); ax.set_ylim(-0.5, 1.2)

def roadmap(ax, fs=11, today=dt.date(2026, 10, 13), labels=True, short=False):
    start = dt.date(2026, 10, 1); n = lambda d: (d - start).days
    for i, (lab, a, b, c) in enumerate(PHASES):
        ax.barh(i, n(b) - n(a), left=n(a), color=c, height=0.62)
        if labels: ax.text(n(a) + 4, i, SHORTPH[i] if short else lab, va="center", fontsize=fs, color="white" if c in (TEAL_D, TEAL) else INK, weight="bold")
    ax.axvline(n(DEADLINE), color=RED, lw=2); ax.text(n(DEADLINE) - 3, -0.75, "13 May 2027\nobligations in force", ha="right", va="center", fontsize=fs * 0.9, color=RED, weight="bold")
    ax.axvline(n(today), color=GREY, ls=":", lw=1.2); ax.text(n(today) + 2, len(PHASES) - 0.35, "today", fontsize=fs * 0.85, color=GREY)
    ticks = pd.date_range("2026-10-01", "2027-05-01", freq="MS")
    ax.set_xticks([n(t.date()) for t in ticks]); ax.set_xticklabels([t.strftime("%b %y") for t in ticks], fontsize=fs * 0.9)
    ax.set_yticks([]); ax.invert_yaxis(); ax.set_xlim(0, n(DEADLINE) + 6); ax.set_ylim(len(PHASES) - 0.4, -1.3)
    ax.grid(axis="y", visible=False); ax.spines["left"].set_visible(False)

# ---------------- cover 1600x900 ----------------
fig = plt.figure(figsize=(16, 9), dpi=100)
fig.text(0.04, 0.905, "DPDP ACT READINESS ASSESSMENT", fontsize=13, color=TEAL, weight="bold")
fig.text(0.04, 0.84, "Acme Learning: are we ready for 13 May 2027?", fontsize=30, weight="black", color=INK)
fig.text(0.04, 0.79, "Fictional ed-tech company  ·  5 processing activities  ·  10 obligations under the DPDP Act 2023 and Rules 2025  ·  readiness work, not legal advice",
         fontsize=13.5, color=GREY)
sample_badge(fig, y=0.955)
ax = fig.add_axes([0.03, 0.40, 0.27, 0.34]); gauge(ax, overall, fs=50)
fig.text(0.165, 0.37, "Overall readiness score", ha="center", fontsize=14, color=INK, weight="bold")
fig.text(0.165, 0.34, f"{len(gaps)} gaps: {(gaps.prio=='P1').sum()} high priority (P1), {(gaps.prio=='P2').sum()} medium (P2)", ha="center", fontsize=12, color=GREY)
# gap register snapshot
ax = fig.add_axes([0.335, 0.33, 0.625, 0.41]); ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
ax.text(0, 0.97, "Gap register snapshot", fontsize=16, weight="bold", color=INK, va="top")
cols_x = [0.0, 0.31, 0.43, 0.57]; hdr = ["Activity", "Score", "Gaps", "High-priority gaps"]
y = 0.82
ax.add_patch(Rectangle((0, y - 0.05), 1, 0.1, fc=TEAL, ec="none"))
for x, h in zip(cols_x, hdr): ax.text(x + 0.01, y, h, color="white", fontsize=12, weight="bold", va="center")
for i, a in acts.iterrows():
    y = 0.82 - 0.135 * (i + 1)
    if i % 2 == 0: ax.add_patch(Rectangle((0, y - 0.0675), 1, 0.135, fc=TEAL_XXL, ec="none"))
    g = gaps[gaps.activity == a.activity]
    ax.text(0.01, y, a.activity, fontsize=12, va="center", color=INK)
    ax.add_patch(FancyBboxPatch((0.315, y - 0.035), 0.09, 0.07, boxstyle="round,pad=0.005,rounding_size=0.02", fc=RAGC[a.rag], ec="none"))
    ax.text(0.36, y, f"{a.score:.0f}%", fontsize=12, va="center", ha="center", color="white", weight="bold")
    ax.text(0.44, y, f"{(g.prio=='P1').sum()} × P1  ·  {(g.prio=='P2').sum()} × P2", fontsize=11.5, va="center", color=INK)
    p1 = [GAPNAME[c] for c in g[g.prio == "P1"].col]
    ax.text(0.58, y, "P1: " + ", ".join(p1), fontsize=11.5, va="center", color=GREY)
ax = fig.add_axes([0.04, 0.085, 0.92, 0.2]); roadmap(ax, fs=11.5, short=True)
ax.set_title("Roadmap to 13 May 2027", fontsize=16, pad=6)
footer(fig, "Acme Learning is fictional · readiness work, not legal advice", size=11)
fig.savefig(os.path.join(HERE, "dpdp_readiness_cover.png"), dpi=100); plt.close(fig)

# ---------------- charts for PDF ----------------
FIG = os.path.join(HERE, "figures"); os.makedirs(FIG, exist_ok=True)
fig, ax = plt.subplots(figsize=(7.2, 2.7), dpi=200)
ax.barh(acts.activity, acts.score, color=[RAGC[r] for r in acts.rag], height=0.58)
for i, v in enumerate(acts.score): ax.text(v + 1.2, i, f"{v:.0f}%", va="center", fontsize=9.5, weight="bold", color=INK)
ax.axvline(80, color=GREEN, ls="--", lw=1); ax.axvline(50, color=AMBER, ls="--", lw=1); ax.axvline(overall, color=TEAL, lw=1.6)
ax.text(overall + 1, -0.55, f"overall {overall:.0f}%", fontsize=8.5, color=TEAL, va="center")
ax.set_xlim(0, 105); ax.set_ylim(4.5, -0.9); ax.set_xlabel("Weighted readiness score"); ax.set_title("Readiness by processing activity", fontsize=11)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "activity_scores.png")); plt.close(fig)
fig, ax = plt.subplots(figsize=(7.4, 2.8), dpi=200); roadmap(ax, fs=8.5, short=True); fig.tight_layout(); fig.savefig(os.path.join(FIG, "roadmap.png")); plt.close(fig)
fig, ax = plt.subplots(figsize=(3.2, 2.0), dpi=200); gauge(ax, overall, fs=26); fig.savefig(os.path.join(FIG, "gauge.png"), bbox_inches="tight"); plt.close(fig)

# ---------------- PDF ----------------
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from PIL import Image as PI
rl_setup(); S = rl_styles(); W = A4[0] - 80; C = colors.HexColor
P = lambda t, s="body": Paragraph(t, S[s]); B = lambda t: Paragraph(t, S["bullet"], bulletText="•")
def IMG(path, w):
    path = path if os.path.isabs(path) else os.path.join(FIG, path); iw, ih = PI.open(path).size; return Image(path, width=w, height=w * ih / iw)
doc = SimpleDocTemplate(os.path.join(HERE, "dpdp_readiness_report.pdf"), pagesize=A4, leftMargin=40, rightMargin=40, topMargin=46, bottomMargin=54,
                        title="Acme Learning – DPDP readiness assessment (SAMPLE)", author="Shashwat Kumar")
deco = rl_page_decor("Acme Learning · DPDP readiness assessment")
st = []
disc = ("<b>Readiness work, not legal advice.</b> This assessment maps processing activities against core obligations of the Digital Personal Data "
        "Protection Act 2023 and the DPDP Rules 2025 to prioritise operational fixes. It is not a legal opinion; the organisation's counsel should review "
        "interpretations, especially on children's data and cross-border transfers.")
n_p1 = (gaps.prio == "P1").sum(); n_p2 = (gaps.prio == "P2").sum()
breach_all = (gaps.col == "breach_process").sum()
# 1
st += [P("SAMPLE DELIVERABLE · DPDP READINESS", "kicker"), P("Acme Learning Pvt Ltd: DPDP readiness assessment", "h1"),
       P(f"Fictional ed-tech company · assessment date 13 Oct 2026 · scored with the DPDP gap scorer on a synthetic inventory", "small"), Spacer(1, 8),
       IMG(os.path.join(HERE, "dpdp_readiness_cover.png"), W), Spacer(1, 4), P("Executive summary", "h2"),
       P(f"Acme Learning is <b>{overall:.0f}% ready</b> across its five main processing activities. Three activities are RED, one is AMBER and one is GREEN. "
         f"We logged <b>{len(gaps)} gaps</b>: {n_p1} high priority (P1) and {n_p2} medium (P2). Core obligations take effect on <b>13 May 2027</b>, "
         "seven months from now. That is enough time if P1 work starts this quarter."),
       B(f"<b>No breach playbook anywhere</b> ({breach_all} of 5 activities). The Rules expect prompt notice to the Data Protection Board and affected people, with a detailed report within 72 hours."),
       B("<b>Children's data is the biggest legal exposure.</b> The student app processes data of minors without verifiable parental consent (s.9, Rule 10)."),
       B("<b>WhatsApp marketing has no valid notice or consent</b> and no contract with the messaging vendor. It is the lowest-scoring activity (23%)."),
       B("<b>Retention is undefined</b> for four of five activities, so data is kept indefinitely."),
       P(disc, "callout"), PageBreak()]
# 2 data inventory
inv = [["Activity", "Data principals", "Data categories", "Est. records", "System / location", "Processor", "Current retention", "Child data"]]
for _, a in acts.iterrows():
    e = ENR[a.activity]; inv.append([a.activity, e[0], a.data.replace(",", ", "), e[1], e[2], e[3], e[4], "Yes" if a.child.lower().startswith("y") else "No"])
cs = ParagraphStyle("cs", parent=S["cell"], fontSize=7.8, leading=9.6); chs = ParagraphStyle("chs", parent=S["cellh"], fontSize=7.8, leading=9.6)
inv_t = [[Paragraph(x, chs) for x in inv[0]]] + [[Paragraph(x, cs) for x in r] for r in inv[1:]]
chk = [["#", "Obligation checked", "Reference", "Weight"]] + [[str(i + 1), SHORT[c], ref, str(w)] for i, (c, ref, w, _) in enumerate(ds.CHECKS)]
chk_t = [[Paragraph(x, chs) for x in chk[0]]] + [[Paragraph(x, cs) for x in r] for r in chk[1:]]
st += [P("SCOPE &amp; DATA INVENTORY", "kicker"), P("What personal data Acme holds, and where", "h1"),
       P("Over two weeks of interviews and system walkthroughs we listed every processing activity that touches personal data, then picked the five with the highest "
         "volume or risk. For each one we record who the data is about, what is collected, where it sits, which vendors process it and how long it is kept."),
       rl_table(inv_t, [W * f for f in (0.15, 0.14, 0.13, 0.09, 0.16, 0.12, 0.12, 0.09)]), Spacer(1, 4),
       P("Record counts and locations are synthetic illustrations.", "small"),
       P("Method: ten weighted checks per activity", "h2"),
       P("Each activity is tested against ten obligations. High-impact items (notice, consent, security, breach, children) carry weight 3 and the rest weight 2. "
         "The score is the weighted share of checks met. 'n/a' items, such as the children check where no child data is processed, are excluded. "
         "RAG bands: GREEN ≥ 80%, AMBER 50–79%, RED &lt; 50%."),
       rl_table(chk_t, [W * 0.05, W * 0.2, W * 0.63, W * 0.12]), PageBreak()]
# 3 scores + matrix
mh = ["Activity"] + [SHORT[c] for c, *_ in ds.CHECKS] + ["Score"]
mrows = [[Paragraph(x, ParagraphStyle("mh", parent=chs, fontSize=6.6, leading=8)) for x in mh]]
ext = []
for i, (line, (_, a)) in enumerate(zip(matrix, acts.iterrows()), 1):
    rr = [Paragraph(a.activity, cs)]
    for j, (c, *_r) in enumerate(ds.CHECKS, 1):
        v = line[c]; rr.append(v)
        ext.append(("BACKGROUND", (j, i), (j, i), C("#E4F1E8") if v == "Met" else C("#F6DEDB") if v == "Gap" else C("#F2F4F5")))
        ext.append(("TEXTCOLOR", (j, i), (j, i), C(GREEN) if v == "Met" else C(RED) if v == "Gap" else C(GREY)))
    rr.append(f"{a.score:.0f}%"); ext += [("BACKGROUND", (11, i), (11, i), C(RAGC[a.rag])), ("TEXTCOLOR", (11, i), (11, i), colors.white), ("FONTNAME", (11, i), (11, i), "Lato-Bold")]
    mrows.append(rr)
ext += [("LEFTPADDING", (1, 0), (-1, -1), 2), ("RIGHTPADDING", (1, 0), (-1, -1), 2), ("ALIGN", (1, 1), (-1, -1), "CENTER"), ("FONTSIZE", (1, 1), (-1, -1), 7.6), ("GRID", (0, 0), (-1, -1), 0.6, colors.white)]
mt = rl_table(mrows, [W * 0.17] + [W * 0.073] * 10 + [W * 0.1], zebra=False, extra=ext)
st += [P("READINESS SCORES", "kicker"), P("Where Acme stands today", "h1"), IMG("activity_scores.png", W * 0.95), Spacer(1, 4),
       P("Obligation-by-activity matrix", "h2"), mt, Spacer(1, 8),
       P("Reading the matrix", "h2"),
       B("<b>Breach</b> is a gap in every column. That is a company-wide control, so one playbook, one incident log and one drill fix it everywhere."),
       B("<b>Withdrawal</b> and <b>retention</b> fail almost everywhere. Consent can be given in one tap but cannot be withdrawn the same way, and nothing is ever deleted."),
       B("<b>Purpose</b> is met everywhere, a good base for writing itemised notices quickly."),
       B("<b>Payroll</b> is GREEN because employment processing rests on legitimate uses rather than consent, which the scorer marks as n/a."),
       PageBreak()]
# 4 gap register
gr = [["#", "Pri.", "Activity", "Obligation", "Remediation", "Owner"]]
OWN = {"notice_given": "Legal + Product", "consent_recorded": "Product + Eng", "withdrawal_easy": "Product", "purpose_defined": "Legal", "retention_defined": "Eng + Legal",
       "processor_contract": "Procurement", "security_controls": "CTO / InfoSec", "breach_process": "InfoSec + DPO", "rights_channel": "Support + DPO", "children_check": "Product + Legal"}
gs = ParagraphStyle("gs", parent=S["cell"], fontSize=7.4, leading=8.9)
for i, g in gaps.iterrows():
    gr.append([str(i + 1), g.prio, g.activity, g.ref, g.fix, OWN[g.col]])
ext = []
for i, g in gaps.iterrows():
    ext += [("BACKGROUND", (1, i + 1), (1, i + 1), C(RED) if g.prio == "P1" else C(AMBER)), ("TEXTCOLOR", (1, i + 1), (1, i + 1), colors.white), ("FONTNAME", (1, i + 1), (1, i + 1), "Lato-Bold")]
grt = [[Paragraph(x, ParagraphStyle("gh", parent=chs, fontSize=7.4, leading=8.9)) for x in gr[0]]] + \
      [[r[0], r[1]] + [Paragraph(x, gs) for x in r[2:]] for r in gr[1:]]
ext += [("TOPPADDING", (0, 0), (-1, -1), 2.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2), ("FONTSIZE", (0, 1), (1, -1), 7.4), ("ALIGN", (1, 1), (1, -1), "CENTER")]
st += [P("GAP REGISTER", "kicker"), P(f"{len(gaps)} gaps, ranked by weight", "h1"),
       P(f"Generated by the DPDP gap scorer and reviewed by hand. P1 = weight-3 obligation ({n_p1} items, close by Dec 2026); P2 = weight-2 obligation ({n_p2} items, close by Feb 2027).", "small"), Spacer(1, 4),
       rl_table(grt, [W * f for f in (0.04, 0.06, 0.18, 0.30, 0.30, 0.12)], extra=ext, font_size=7.4), PageBreak()]
# 5 roadmap
ms = [["Milestone", "Target date", "Evidence of completion"],
      ["Inventory and RoPA signed off by leadership", "31 Oct 2026", "Signed record of processing; data-flow diagrams"],
      ["Breach playbook live; incident log in place", "30 Nov 2026", "Playbook v1, 72-hour report template, on-call list"],
      ["Itemised notices and consent capture with logs", "15 Dec 2026", "Notice text per activity; consent records in the database"],
      ["Age-gating and verifiable parental consent in student app", "31 Dec 2026", "Release notes; consent artefacts; test evidence"],
      ["Security baseline: encryption, access reviews, 1-year logs", "31 Dec 2026", "Configuration screenshots; access review sign-off"],
      ["DPAs signed with WhatsApp vendor, helpdesk and analytics SDK", "31 Jan 2027", "Executed DPAs with breach-cooperation clauses"],
      ["Retention schedule and automated erasure jobs", "15 Feb 2027", "Retention policy; job run logs"],
      ["Rights and grievance channel with SLA; one-tap withdrawal", "28 Feb 2027", "Published page; ticket workflow; SLA dashboard"],
      ["Tabletop breach drill; re-notice existing users", "15 Apr 2027", "Drill report; re-notice campaign metrics"],
      ["Evidence pack and readiness re-score ≥ 85%", "30 Apr 2027", "Re-run of scorer; evidence index for counsel review"]]
mst = [[Paragraph(x, chs) for x in ms[0]]] + [[Paragraph(x, cs) for x in r] for r in ms[1:]]
st += [P("ROADMAP", "kicker"), P("Seven months to 13 May 2027", "h1"),
       P("The plan does the high-risk, high-weight work first. P1 gaps close before the end of December, so January to April is left for contracts, "
         "retention engineering and rehearsal. A two-week buffer protects the deadline."),
       IMG("roadmap.png", W), Spacer(1, 6), rl_table(mst, [W * 0.47, W * 0.14, W * 0.39]), Spacer(1, 6),
       P(f"Expected outcome: closing every P1 and P2 gap takes the readiness score from {overall:.0f}% to 100% on the ten checks. A re-score of 85% or more "
         "by end-April is the go/no-go threshold.", "callout"), PageBreak()]
# 6 governance, next steps, disclaimer
ra = [["Workstream", "Responsible", "Accountable", "Consulted"],
      ["Notices, consent, withdrawal", "Product + Engineering", "CEO", "Legal counsel"],
      ["Children's data (age-gate, parental consent)", "Product", "CEO", "Legal counsel, Customer Success"],
      ["Security baseline and breach playbook", "CTO / InfoSec", "CTO", "Cloud vendor, DPO"],
      ["Vendor DPAs", "Procurement", "CFO", "Legal counsel"],
      ["Retention and erasure", "Engineering", "CTO", "Finance (statutory records)"],
      ["Rights and grievance channel", "Support", "DPO / Grievance Officer", "Product"]]
rat = [[Paragraph(x, chs) for x in ra[0]]] + [[Paragraph(x, cs) for x in r] for r in ra[1:]]
st += [P("GOVERNANCE &amp; NEXT STEPS", "kicker"), P("Making it stick", "h1"),
       P("Who does what", "h2"), rl_table(rat, [W * 0.34, W * 0.2, W * 0.2, W * 0.26]), Spacer(1, 6),
       P("Next 30 days", "h2"),
       B("Appoint an accountable owner for DPDP readiness and a Grievance Officer contact."),
       B("Freeze new WhatsApp campaigns to cold lists until the notice and consent flow is live."),
       B("Start the breach playbook and the age-gating design in parallel; both are on the critical path."),
       B("Send DPA templates to the three processors identified in the inventory."),
       P("Assumptions &amp; limitations", "h2"),
       B("Scope covers the five highest-risk activities. HR recruitment, CCTV and website analytics should be inventoried next."),
       B("Answers come from interviews and walkthroughs; technical controls were not penetration-tested."),
       B("Cross-border transfer analysis (the analytics SDK in the US, helpdesk in the EU) is flagged for counsel and not scored."),
       B("Whether Acme could be notified as a Significant Data Fiduciary is not assessed."),
       Spacer(1, 4), P(disc, "callout"),
       P("About this sample: Acme Learning Pvt Ltd is a fictional company. The inventory is synthetic and was scored with an open DPDP gap-scorer prototype "
         "(dpdp_scorer.py). Prepared by Shashwat Kumar as an illustrative work sample.", "small")]
doc.build(st, onFirstPage=deco, onLaterPages=deco)
print("overall", round(overall, 1), "gaps", len(gaps))
