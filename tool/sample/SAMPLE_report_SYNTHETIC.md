> **SAMPLE DELIVERABLE built from SYNTHETIC data for "Acme Learning Pvt Ltd (fictional)". Not a real client.**

# DPDP Readiness Gap Report (prototype output)
Generated 2026-10-12 | Input: tool/sample/SYNTHETIC_inventory.csv

> Readiness assessment against DPDP Act 2023 / Rules 2025 (core obligations in force 13 May 2027). Not legal advice; client counsel to review.

**Overall readiness score: 50%** across 5 processing activities.

## Activity scores
| Activity | System | Data | Score | RAG |
|---|---|---|---|---|
| Customer signup (SYNTHETIC) | Web app + Postgres | name,email,phone | 59% | AMBER |
| Marketing WhatsApp campaigns (SYNTHETIC) | WhatsApp BSP vendor | phone,name | 23% | RED |
| Payroll (SYNTHETIC) | HRMS SaaS | PAN,bank a/c,salary | 86% | GREEN |
| Student learning app (SYNTHETIC) | Mobile app | name,age,progress | 40% | RED |
| Support tickets (SYNTHETIC) | Helpdesk SaaS | name,email,issue text | 45% | RED |

## Gap register (highest weight first)
| # | Priority | Activity | System | Obligation | Remediation |
|---|---|---|---|---|---|
| 1 | P1 | Customer signup (SYNTHETIC) | Web app + Postgres | s.8(6) / Rule 7: notify Board + principals, 72h report | Write and rehearse a breach playbook |
| 2 | P1 | Marketing WhatsApp campaigns (SYNTHETIC) | WhatsApp BSP vendor | s.5 / Rule 3: itemised notice in plain language | Issue a standalone notice listing data, purpose, rights, and how to withdraw consent |
| 3 | P1 | Marketing WhatsApp campaigns (SYNTHETIC) | WhatsApp BSP vendor | s.6: free, specific, unambiguous consent + record | Capture affirmative consent per purpose and store logs |
| 4 | P1 | Marketing WhatsApp campaigns (SYNTHETIC) | WhatsApp BSP vendor | s.8(6) / Rule 7: notify Board + principals, 72h report | Write and rehearse a breach playbook |
| 5 | P1 | Payroll (SYNTHETIC) | HRMS SaaS | s.8(6) / Rule 7: notify Board + principals, 72h report | Write and rehearse a breach playbook |
| 6 | P1 | Student learning app (SYNTHETIC) | Mobile app | s.8(5) / Rule 6: reasonable security safeguards | Encryption, access control, logs retained 1 yr, backups |
| 7 | P1 | Student learning app (SYNTHETIC) | Mobile app | s.8(6) / Rule 7: notify Board + principals, 72h report | Write and rehearse a breach playbook |
| 8 | P1 | Student learning app (SYNTHETIC) | Mobile app | s.9 / Rule 10: verifiable parental consent if child data | Age-gate and get verifiable parental consent, or confirm no child data |
| 9 | P1 | Support tickets (SYNTHETIC) | Helpdesk SaaS | s.6: free, specific, unambiguous consent + record | Capture affirmative consent per purpose and store logs |
| 10 | P1 | Support tickets (SYNTHETIC) | Helpdesk SaaS | s.8(6) / Rule 7: notify Board + principals, 72h report | Write and rehearse a breach playbook |
| 11 | P2 | Customer signup (SYNTHETIC) | Web app + Postgres | s.6(4): withdrawal as easy as giving consent | Add a one-step withdrawal path in the same channel |
| 12 | P2 | Customer signup (SYNTHETIC) | Web app + Postgres | s.8(7) / Rule 8 + Third Schedule: erase when purpose ends | Set a retention period and an erasure job |
| 13 | P2 | Customer signup (SYNTHETIC) | Web app + Postgres | s.11-13 / Rule 14: access, correction, erasure, grievance | Publish a rights/grievance channel with an SLA |
| 14 | P2 | Marketing WhatsApp campaigns (SYNTHETIC) | WhatsApp BSP vendor | s.6(4): withdrawal as easy as giving consent | Add a one-step withdrawal path in the same channel |
| 15 | P2 | Marketing WhatsApp campaigns (SYNTHETIC) | WhatsApp BSP vendor | s.8(7) / Rule 8 + Third Schedule: erase when purpose ends | Set a retention period and an erasure job |
| 16 | P2 | Marketing WhatsApp campaigns (SYNTHETIC) | WhatsApp BSP vendor | s.8(2): processor engaged under a valid contract | Sign a DPA with the vendor that covers security and breach cooperation |
| 17 | P2 | Marketing WhatsApp campaigns (SYNTHETIC) | WhatsApp BSP vendor | s.11-13 / Rule 14: access, correction, erasure, grievance | Publish a rights/grievance channel with an SLA |
| 18 | P2 | Student learning app (SYNTHETIC) | Mobile app | s.6(4): withdrawal as easy as giving consent | Add a one-step withdrawal path in the same channel |
| 19 | P2 | Student learning app (SYNTHETIC) | Mobile app | s.8(7) / Rule 8 + Third Schedule: erase when purpose ends | Set a retention period and an erasure job |
| 20 | P2 | Student learning app (SYNTHETIC) | Mobile app | s.11-13 / Rule 14: access, correction, erasure, grievance | Publish a rights/grievance channel with an SLA |
| 21 | P2 | Support tickets (SYNTHETIC) | Helpdesk SaaS | s.6(4): withdrawal as easy as giving consent | Add a one-step withdrawal path in the same channel |
| 22 | P2 | Support tickets (SYNTHETIC) | Helpdesk SaaS | s.8(7) / Rule 8 + Third Schedule: erase when purpose ends | Set a retention period and an erasure job |
| 23 | P2 | Support tickets (SYNTHETIC) | Helpdesk SaaS | s.8(2): processor engaged under a valid contract | Sign a DPA with the vendor that covers security and breach cooperation |

## Roadmap to 13 May 2027
- By Dec 2026: close every P1 gap (notice, consent, security, breach, children)
- By Feb 2027: close P2 gaps (processor DPAs, retention, rights channel)
- Mar–Apr 2027: tabletop breach drill, re-notice existing users, evidence pack
