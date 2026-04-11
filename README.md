# OpenAI Usage & Productivity Intelligence Dashboard

A business intelligence dashboard built to measure the organizational impact of AI adoption — across productivity, revenue, cost savings, and decision-making — using a dataset of 2,000 employee records from 2024.

**[View Live Dashboard](https://openai-usage-appuctivity-intelligence-dashboard-vvxwbbtywnejgq.streamlit.app/)**

---

## Overview

Most organizations adopt AI without a clear way to measure whether it's working. This project addresses that gap by building an end-to-end BI platform that ties AI usage data directly to business outcomes. The goal was to move beyond anecdotal claims and surface evidence-based insights that leadership can act on.

---

## Results

| Metric | Value |
|---|---|
| Productivity improvement | ~30% |
| Faster decision-making | ~26% |
| Total revenue impact | $15M |
| Cost savings identified | $5.77M |

---

## What the Dashboard Covers

**Productivity trends over time** — tracks how productivity shifts month-over-month as AI adoption increases across the organization.

**Department-wise AI usage and impact** — compares adoption rates and resulting productivity and revenue outcomes by department.

**Revenue contribution by role and experience** — breaks down revenue generation by job function and seniority to identify where AI delivers the most value.

**Adoption segmentation** — classifies employees into high, medium, and low adoption tiers and benchmarks their performance across all KPIs.

---

## Key Findings

**Adoption outperforms trust as a performance driver.** There is a measurable gap between employees who trust AI and employees who actually use it. The data shows that usage — not perception — is what drives results. Organizations investing only in awareness campaigns without hands-on adoption programs are leaving performance gains unrealized.

**High adopters consistently outperform across every KPI** — productivity, revenue generation, decision-making speed, and employee satisfaction. The gap between high and low adopters is significant enough to treat adoption rate as a leading indicator of team performance.

**Sales generates the highest revenue impact per AI interaction** despite having relatively lower overall usage. This points to high efficiency in how the Sales team applies AI, and suggests their workflows are worth replicating elsewhere.

**IT and Marketing lead in operational productivity**, making them natural candidates for internal AI center-of-excellence roles.

**Medium adopters represent the largest untapped opportunity.** They are the biggest segment by headcount and sit closest to the high-adopter threshold. Targeted upskilling for this group is likely to yield the highest return on investment.

---

## Recommendations

| Finding | Action |
|---|---|
| Adoption drives performance more than trust | Prioritize hands-on AI training over awareness campaigns |
| Sales has the highest ROI per AI interaction | Document and replicate Sales AI workflows across revenue teams |
| IT and Marketing are productivity leaders | Position them as internal champions and best-practice references |
| Medium adopters are the biggest growth lever | Design targeted upskilling programs specifically for this segment |

---

## Tech Stack

- **Dashboard:** Streamlit
- **Data processing:** Python, Pandas
- **Visualization:** Plotly, Matplotlib
- **Dataset:** 2,000 synthetic enterprise records (2024)

---

## Project Structure

```
OpenAI-Usage-Productivity-Intelligence-Dashboard/
├── app.py
├── requirements.txt
├── OpenAI_Usage_Productivity_Dataset.csv
├── .gitignore
└── README.md
```

---

## Running Locally

```bash
git clone https://github.com/YASHASSHETTYYY/OpenAI-Usage-Productivity-Intelligence-Dashboard.git
cd OpenAI-Usage-Productivity-Intelligence-Dashboard
pip install -r requirements.txt
streamlit run app.py
```

Opens at `http://localhost:8501`

---

## Author

**Yashas Shetty**
[GitHub](https://github.com/YASHASSHETTYYY) · [LinkedIn](www.linkedin.com/in/yashas-shetty)
