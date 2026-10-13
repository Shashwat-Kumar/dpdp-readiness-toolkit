#!/usr/bin/env python3
"""DPDP personal-data inventory gap scorer (prototype). Readiness aid, NOT legal advice.
Usage: python3 dpdp_scorer.py inventory.csv out_report.md
Each CSV row = one processing activity. Yes/No columns are checked against DPDP Act 2023 / Rules 2025 obligations."""
import csv, sys, datetime
CHECKS = [  # column, obligation reference, weight, remediation
 ("notice_given","s.5 / Rule 3: itemised notice in plain language",3,"Issue a standalone notice listing data, purpose, rights, and how to withdraw consent"),
 ("consent_recorded","s.6: free, specific, unambiguous consent + record",3,"Capture affirmative consent per purpose and store logs"),
 ("withdrawal_easy","s.6(4): withdrawal as easy as giving consent",2,"Add a one-step withdrawal path in the same channel"),
 ("purpose_defined","s.4/s.6: lawful, specified purpose",2,"Document a specific purpose for each activity"),
 ("retention_defined","s.8(7) / Rule 8 + Third Schedule: erase when purpose ends",2,"Set a retention period and an erasure job"),
 ("processor_contract","s.8(2): processor engaged under a valid contract",2,"Sign a DPA with the vendor that covers security and breach cooperation"),
 ("security_controls","s.8(5) / Rule 6: reasonable security safeguards",3,"Encryption, access control, logs retained 1 yr, backups"),
 ("breach_process","s.8(6) / Rule 7: notify Board + principals, 72h report",3,"Write and rehearse a breach playbook"),
 ("rights_channel","s.11-13 / Rule 14: access, correction, erasure, grievance",2,"Publish a rights/grievance channel with an SLA"),
 ("children_check","s.9 / Rule 10: verifiable parental consent if child data",3,"Age-gate and get verifiable parental consent, or confirm no child data"),
]
def yes(v): return str(v).strip().lower() in ("y","yes","true","1","na","n/a")
def main(inp,out):
    rows=list(csv.DictReader(open(inp))); lines=[]; total=got=0; gaps=[]
    for r in rows:
        s=m=0
        for col,ref,w,fix in CHECKS:
            if col=="children_check" and r.get("child_data","n").lower() not in ("y","yes"): continue
            m+=w
            if yes(r.get(col,"")): s+=w
            else: gaps.append((w,r["activity"],r.get("system",""),ref,fix))
        total+=m; got+=s; pct=100*s/m if m else 100
        rag="GREEN" if pct>=80 else "AMBER" if pct>=50 else "RED"
        lines.append(f"| {r['activity']} | {r.get('system','')} | {r.get('data_categories','')} | {pct:.0f}% | {rag} |")
    o=[f"# DPDP Readiness Gap Report (prototype output)\nGenerated {datetime.date.today()} | Input: {inp}\n",
       "> Readiness assessment against DPDP Act 2023 / Rules 2025 (core obligations in force 13 May 2027). Not legal advice; client counsel to review.\n",
       f"**Overall readiness score: {100*got/total:.0f}%** across {len(rows)} processing activities.\n",
       "## Activity scores\n| Activity | System | Data | Score | RAG |\n|---|---|---|---|---|",*lines,
       "\n## Gap register (highest weight first)\n| # | Priority | Activity | System | Obligation | Remediation |\n|---|---|---|---|---|---|"]
    for i,(w,a,sy,ref,fix) in enumerate(sorted(gaps,key=lambda g:-g[0]),1):
        o.append(f"| {i} | {'P1' if w==3 else 'P2'} | {a} | {sy} | {ref} | {fix} |")
    o.append("\n## Roadmap to 13 May 2027\n- By Dec 2026: close every P1 gap (notice, consent, security, breach, children)\n- By Feb 2027: close P2 gaps (processor DPAs, retention, rights channel)\n- Mar–Apr 2027: tabletop breach drill, re-notice existing users, evidence pack\n")
    open(out,"w").write("\n".join(o)); print(f"score={100*got/total:.0f}% gaps={len(gaps)} -> {out}")
if __name__=="__main__": main(sys.argv[1],sys.argv[2])
