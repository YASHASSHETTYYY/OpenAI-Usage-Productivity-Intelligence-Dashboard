import streamlit as st
import pandas as pd
import numpy as np
import os

PLOTLY_IMPORT_ERROR = None
try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
except ModuleNotFoundError as exc:
    go = None
    make_subplots = None
    PLOTLY_IMPORT_ERROR = exc

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="OpenAI Productivity Intelligence",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# THEME / CSS
# ─────────────────────────────────────────────
ACCENT      = "#10a37f"
BG_DARK     = "#0d0d0d"
BG_CARD     = "#1a1a1a"
BG_CARD2    = "#222222"
BORDER      = "#2a2a2a"
TEXT_PRI    = "#ffffff"
TEXT_SEC    = "#a0a0a0"
GRID_COLOR  = "#2a2a2a"

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=TEXT_PRI, family="Inter, sans-serif", size=12),
    margin=dict(l=10, r=10, t=36, b=10),
    xaxis=dict(gridcolor=GRID_COLOR, linecolor=BORDER, tickcolor=TEXT_SEC, tickfont=dict(color=TEXT_SEC, size=10)),
    yaxis=dict(gridcolor=GRID_COLOR, linecolor=BORDER, tickcolor=TEXT_SEC, tickfont=dict(color=TEXT_SEC, size=10)),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT_SEC, size=10)),
    coloraxis_colorbar=dict(tickfont=dict(color=TEXT_SEC)),
)

DEPT_COLORS = {
    "IT":         ACCENT,
    "Marketing":  "#a855f7",
    "Sales":      "#f59e0b",
    "Finance":    "#3b82f6",
    "HR":         "#ef4444",
    "Operations": "#06b6d4",
}


def rgba(hex_color: str, alpha: float) -> str:
    hex_color = hex_color.lstrip("#")
    red = int(hex_color[0:2], 16)
    green = int(hex_color[2:4], 16)
    blue = int(hex_color[4:6], 16)
    return f"rgba({red}, {green}, {blue}, {alpha})"

st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

  html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
    background-color: {BG_DARK};
    color: {TEXT_PRI};
  }}

  /* hide default streamlit chrome */
  #MainMenu, footer, header {{ visibility: hidden; }}
  .block-container {{ padding: 0.8rem 1.2rem 0.5rem 1.2rem !important; max-width: 100% !important; }}

  /* sidebar */
  [data-testid="stSidebar"] {{
    background-color: #111111 !important;
    border-right: 1px solid {BORDER};
  }}
  [data-testid="stSidebar"] * {{ color: {TEXT_PRI} !important; }}
  [data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {{
    background-color: {ACCENT}33 !important;
    border: 1px solid {ACCENT} !important;
  }}

  /* KPI cards */
  .kpi-card {{
    background: linear-gradient(135deg, {BG_CARD} 0%, {BG_CARD2} 100%);
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 16px 20px;
    position: relative;
    overflow: hidden;
    height: 110px;
  }}
  .kpi-card::before {{
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, {ACCENT}, #0d8f6f);
    border-radius: 12px 12px 0 0;
  }}
  .kpi-label {{
    font-size: 11px;
    font-weight: 500;
    color: {TEXT_SEC};
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 6px;
  }}
  .kpi-value {{
    font-size: 26px;
    font-weight: 700;
    color: {TEXT_PRI};
    line-height: 1.1;
  }}
  .kpi-delta {{
    font-size: 11px;
    color: {ACCENT};
    margin-top: 4px;
    font-weight: 500;
  }}
  .kpi-icon {{
    position: absolute;
    top: 14px; right: 16px;
    font-size: 22px;
    opacity: 0.3;
  }}

  /* chart card */
  .chart-card {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 2px 6px 4px 6px;
  }}
  .chart-title {{
    font-size: 12px;
    font-weight: 600;
    color: {TEXT_SEC};
    letter-spacing: 0.05em;
    text-transform: uppercase;
    padding: 10px 8px 4px 8px;
  }}

  /* dashboard header */
  .dash-header {{
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 6px 0 10px 0;
    border-bottom: 1px solid {BORDER};
    margin-bottom: 12px;
  }}
  .dash-title {{
    font-size: 20px;
    font-weight: 700;
    color: {TEXT_PRI};
    letter-spacing: -0.02em;
  }}
  .dash-subtitle {{
    font-size: 12px;
    color: {TEXT_SEC};
    margin-top: 1px;
  }}
  .dash-badge {{
    background: {ACCENT}22;
    border: 1px solid {ACCENT}55;
    color: {ACCENT};
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    margin-left: auto;
  }}

  /* divider */
  .section-divider {{
    border: none;
    border-top: 1px solid {BORDER};
    margin: 8px 0;
  }}

  /* Streamlit element overrides */
  div[data-testid="stPlotlyChart"] {{ border-radius: 8px; overflow: hidden; }}
  .stMultiSelect div[data-baseweb="select"] {{ background-color: #1a1a1a !important; border-color: {BORDER} !important; }}
  .stDateInput input {{ background-color: #1a1a1a !important; border-color: {BORDER} !important; color: {TEXT_PRI} !important; }}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA LOADER
# ─────────────────────────────────────────────
@st.cache_data
def load_data() -> pd.DataFrame:
    paths = [
        "OpenAI_Usage_Productivity_Dataset.csv",
        os.path.join(os.path.dirname(__file__), "OpenAI_Usage_Productivity_Dataset.csv"),
        "/mnt/user-data/uploads/OpenAI_Usage_Productivity_Dataset.csv",
    ]
    df = None
    for p in paths:
        if os.path.exists(p):
            df = pd.read_csv(p)
            break

    if df is None:
        # ── fallback: generate synthetic data matching the same schema ──
        np.random.seed(42)
        n = 2000
        depts       = ["IT", "Marketing", "Sales", "Finance", "HR", "Operations"]
        exp_levels  = ["Junior", "Mid", "Senior"]
        adopt_lvls  = ["Low", "Medium", "High"]
        trust_lvls  = ["Low", "Medium", "High"]
        complexity  = ["Low", "Medium", "High"]

        dept_arr  = np.random.choice(depts,      n, p=[0.22, 0.20, 0.20, 0.15, 0.13, 0.10])
        exp_arr   = np.random.choice(exp_levels, n, p=[0.35, 0.40, 0.25])
        adopt_arr = np.random.choice(adopt_lvls, n, p=[0.25, 0.40, 0.35])
        trust_arr = np.random.choice(trust_lvls, n, p=[0.20, 0.40, 0.40])
        comp_arr  = np.random.choice(complexity, n, p=[0.25, 0.45, 0.30])

        adopt_num = np.array([{"Low":1,"Medium":2,"High":3}[a] for a in adopt_arr])
        trust_num = np.array([{"Low":1,"Medium":2,"High":3}[t] for t in trust_arr])
        comp_num  = np.array([{"Low":1,"Medium":2,"High":3}[c] for c in comp_arr])
        exp_num   = np.array([{"Junior":1,"Mid":2,"Senior":3}[e] for e in exp_arr])

        usage     = 30 + adopt_num*20 + (dept_arr=="IT")*20 + (dept_arr=="Marketing")*15 + np.random.normal(0,15,n)
        usage     = np.clip(usage, 5, 180)

        prod      = 15 + adopt_num*6 + comp_num*4 + trust_num*2 + np.random.normal(0,5,n)
        prod      = np.clip(prod, 5, 60)

        rev       = (5000 + adopt_num*1500 + (dept_arr=="Sales")*4000 + exp_num*500
                     + comp_num*800 + np.random.normal(0,1500,n))
        rev       = np.clip(rev, 500, 20000)

        cost      = (1000 + adopt_num*600 + comp_num*400 + trust_num*200 + np.random.normal(0,700,n))
        cost      = np.clip(cost, 100, 8000)

        dec       = 10 + trust_num*6 + comp_num*4 + adopt_num*3 + np.random.normal(0,8,n)
        dec       = np.clip(dec, 2, 55)

        sat       = 5 + trust_num*1.2 + adopt_num*0.5 + np.random.normal(0,0.8,n)
        sat       = np.clip(sat, 1, 10)

        dates = pd.date_range("2024-01-01", "2024-12-31", periods=n)
        df = pd.DataFrame({
            "Date": dates,
            "Department": dept_arr,
            "Experience_Level": exp_arr,
            "Adoption_Level": adopt_arr,
            "AI_Trust_Level": trust_arr,
            "Prompt_Complexity": comp_arr,
            "Daily_AI_Usage_Minutes": usage.round(1),
            "Productivity_Improvement_%": prod.round(2),
            "Revenue_Impact_USD": rev.round(2),
            "Cost_Savings_USD": cost.round(2),
            "Decision_Speed_Improvement_%": dec.round(2),
            "Satisfaction_Score": sat.round(1),
        })

    # ── normalise columns ──────────────────────────────────────────────
    df["Date"] = pd.to_datetime(df["Date"])

    col_map = {
        "Productivity_Improvement_%":    "Productivity_Improvement_%",
        "Productivity Improvement %":    "Productivity_Improvement_%",
        "Decision_Speed_Improvement_%":  "Decision_Speed_Improvement_%",
        "Decision Speed Improvement %":  "Decision_Speed_Improvement_%",
    }
    df.rename(columns=col_map, inplace=True)

    if "Adoption_Level" not in df.columns and "Adoption Level" in df.columns:
        df.rename(columns={"Adoption Level": "Adoption_Level"}, inplace=True)

    # keep only the departments we colorise
    if "Department" in df.columns:
        df = df[df["Department"].isin(list(DEPT_COLORS.keys()))].copy()

    return df


# ─────────────────────────────────────────────
# HELPER: apply plotly theme
# ─────────────────────────────────────────────
def apply_theme(fig, height=260, title=""):
    fig.update_layout(
        **{k: v for k, v in PLOTLY_LAYOUT.items()},
        height=height,
        title=dict(text=title),  # titles are rendered via HTML outside Plotly
    )
    return fig


def ensure_plotly_available():
    if PLOTLY_IMPORT_ERROR is None:
        return

    st.error("Plotly is required to render this dashboard.")
    st.code("py -3.12 -m pip install -r requirements.txt", language="bash")
    st.info(f"Import error: {PLOTLY_IMPORT_ERROR}")
    st.stop()


# ─────────────────────────────────────────────
# CHART BUILDERS
# ─────────────────────────────────────────────
def kpi_html(label, value, delta, icon):
    return f"""
    <div class="kpi-card">
      <div class="kpi-icon">{icon}</div>
      <div class="kpi-label">{label}</div>
      <div class="kpi-value">{value}</div>
      <div class="kpi-delta">{delta}</div>
    </div>"""


def chart_wrap(title, fig_html):
    return f"""
    <div class="chart-card">
      <div class="chart-title">{title}</div>
      {fig_html}
    </div>"""


def build_line_chart(df: pd.DataFrame):
    ts = (df.groupby("Date")["Productivity_Improvement_%"]
            .mean().reset_index())
    ts = ts.sort_values("Date")
    # 7-day rolling
    ts["Rolling"] = ts["Productivity_Improvement_%"].rolling(7, min_periods=1).mean()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=ts["Date"], y=ts["Productivity_Improvement_%"],
        mode="lines", name="Daily",
        line=dict(color=rgba(ACCENT, 0.4), width=1),
        showlegend=True,
    ))
    fig.add_trace(go.Scatter(
        x=ts["Date"], y=ts["Rolling"],
        mode="lines", name="7-day Avg",
        line=dict(color=ACCENT, width=2),
        fill="tozeroy", fillcolor=rgba(ACCENT, 0.09),
    ))
    apply_theme(fig, height=240)
    fig.update_layout(
        xaxis_title="", yaxis_title="Productivity %",
        legend=dict(orientation="h", y=1.08, x=0),
    )
    return fig


def build_funnel_chart(df: pd.DataFrame):
    adopt_order = ["High", "Medium", "Low"]
    trust_order = ["High", "Medium", "Low"]

    adopt_counts = df["Adoption_Level"].value_counts().reindex(adopt_order, fill_value=0)
    trust_counts = df["AI_Trust_Level"].value_counts().reindex(trust_order, fill_value=0)

    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{"type":"funnel"}, {"type":"funnel"}]],
        subplot_titles=["Adoption Level", "AI Trust Level"],
    )
    fig.add_trace(go.Funnel(
        y=adopt_order, x=adopt_counts.values,
        textposition="inside", textinfo="value+percent total",
        marker=dict(color=[ACCENT, rgba(ACCENT, 0.6), rgba(ACCENT, 0.27)]),
        connector=dict(line=dict(color=BORDER, width=1)),
    ), row=1, col=1)
    fig.add_trace(go.Funnel(
        y=trust_order, x=trust_counts.values,
        textposition="inside", textinfo="value+percent total",
        marker=dict(color=["#a855f7", rgba("#a855f7", 0.6), rgba("#a855f7", 0.27)]),
        connector=dict(line=dict(color=BORDER, width=1)),
    ), row=1, col=2)
    apply_theme(fig, height=240)
    fig.update_layout(showlegend=False)
    fig.update_annotations(font=dict(color=TEXT_SEC, size=10))
    return fig


def build_bar_chart(df: pd.DataFrame):
    agg = (df.groupby("Department")["Daily_AI_Usage_Minutes"]
             .mean().reset_index().sort_values("Daily_AI_Usage_Minutes", ascending=True))
    colors = [DEPT_COLORS.get(d, ACCENT) for d in agg["Department"]]
    fig = go.Figure(go.Bar(
        x=agg["Daily_AI_Usage_Minutes"],
        y=agg["Department"],
        orientation="h",
        marker=dict(color=colors, line=dict(width=0)),
        text=agg["Daily_AI_Usage_Minutes"].round(1).astype(str) + " min",
        textposition="outside",
        textfont=dict(color=TEXT_SEC, size=10),
    ))
    apply_theme(fig, height=240)
    fig.update_layout(xaxis_title="Avg Daily Usage (min)", yaxis_title="")
    return fig


def build_scatter_chart(df: pd.DataFrame):
    sample = df.sample(min(800, len(df)), random_state=42)
    colors = [DEPT_COLORS.get(d, "#888") for d in sample["Department"]]

    fig = go.Figure()
    for dept, col in DEPT_COLORS.items():
        mask = sample["Department"] == dept
        if mask.sum() == 0:
            continue
        sub = sample[mask]
        fig.add_trace(go.Scatter(
            x=sub["Revenue_Impact_USD"],
            y=sub["Cost_Savings_USD"],
            mode="markers",
            name=dept,
            marker=dict(color=col, size=5, opacity=0.75,
                        line=dict(width=0.3, color="#000")),
        ))
    apply_theme(fig, height=240)
    fig.update_layout(
        xaxis_title="Revenue Impact ($)",
        yaxis_title="Cost Savings ($)",
        legend=dict(orientation="h", y=1.08, x=0, font=dict(size=9)),
    )
    return fig


def build_box_chart(df: pd.DataFrame):
    order = ["Junior", "Mid", "Senior"]
    fig = go.Figure()
    for exp in order:
        sub = df[df["Experience_Level"] == exp]
        fig.add_trace(go.Box(
            y=sub["Revenue_Impact_USD"],
            name=exp,
            marker_color={"Junior": "#3b82f6", "Mid": ACCENT, "Senior": "#f59e0b"}[exp],
            line=dict(width=1.5),
            fillcolor={
                "Junior": rgba("#3b82f6", 0.27),
                "Mid": rgba(ACCENT, 0.27),
                "Senior": rgba("#f59e0b", 0.27),
            }[exp],
            boxmean="sd",
        ))
    apply_theme(fig, height=240)
    fig.update_layout(yaxis_title="Revenue Impact ($)", showlegend=False)
    return fig


def build_heatmap(df: pd.DataFrame):
    num_cols = [
        "Daily_AI_Usage_Minutes",
        "Productivity_Improvement_%",
        "Revenue_Impact_USD",
        "Cost_Savings_USD",
        "Decision_Speed_Improvement_%",
        "Satisfaction_Score",
    ]
    labels = ["AI Usage", "Productivity", "Revenue", "Cost Savings", "Decision Speed", "Satisfaction"]
    corr = df[num_cols].corr().round(2)
    corr.index   = labels
    corr.columns = labels

    fig = go.Figure(go.Heatmap(
        z=corr.values,
        x=labels, y=labels,
        colorscale=[[0, "#1a0a0a"], [0.5, "#0d3328"], [1, ACCENT]],
        zmid=0, zmin=-1, zmax=1,
        text=corr.values.round(2),
        texttemplate="%{text}",
        textfont=dict(size=10, color=TEXT_PRI),
        hoverongaps=False,
        colorbar=dict(thickness=10, tickfont=dict(color=TEXT_SEC, size=9)),
    ))
    apply_theme(fig, height=220)
    fig.update_layout(
        xaxis=dict(tickfont=dict(size=9, color=TEXT_SEC), side="bottom"),
        yaxis=dict(tickfont=dict(size=9, color=TEXT_SEC), autorange="reversed"),
    )
    return fig


# ─────────────────────────────────────────────
# SIDEBAR FILTERS
# ─────────────────────────────────────────────
def render_sidebar(df: pd.DataFrame):
    st.sidebar.markdown(f"""
    <div style="padding:12px 0 16px 0; border-bottom:1px solid {BORDER}; margin-bottom:16px;">
      <div style="font-size:16px; font-weight:700; color:{TEXT_PRI};">🤖 AI Insights</div>
      <div style="font-size:11px; color:{TEXT_SEC}; margin-top:2px;">Filter & Explore</div>
    </div>
    """, unsafe_allow_html=True)

    depts = sorted(df["Department"].unique().tolist())
    sel_dept = st.sidebar.multiselect("Department", depts, default=depts)

    exp_opts = ["Junior", "Mid", "Senior"]
    sel_exp  = st.sidebar.multiselect("Experience Level", exp_opts, default=exp_opts)

    adopt_opts = ["Low", "Medium", "High"]
    sel_adopt  = st.sidebar.multiselect("Adoption Level", adopt_opts, default=adopt_opts)

    min_date = df["Date"].min().date()
    max_date = df["Date"].max().date()
    date_range = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    st.sidebar.markdown(f"<hr style='border-color:{BORDER};margin:16px 0;'>", unsafe_allow_html=True)
    st.sidebar.markdown(f"""
    <div style="font-size:10px; color:{TEXT_SEC}; line-height:1.6;">
      <b style="color:{ACCENT};">Dataset</b><br>
      {len(df):,} records · {df['Department'].nunique()} departments<br>
      {df['Date'].min().strftime('%b %Y')} – {df['Date'].max().strftime('%b %Y')}
    </div>
    """, unsafe_allow_html=True)

    return sel_dept, sel_exp, sel_adopt, date_range


# ─────────────────────────────────────────────
# FILTER
# ─────────────────────────────────────────────
def filter_data(df, sel_dept, sel_exp, sel_adopt, date_range):
    fdf = df.copy()
    if sel_dept:
        fdf = fdf[fdf["Department"].isin(sel_dept)]
    if sel_exp:
        fdf = fdf[fdf["Experience_Level"].isin(sel_exp)]
    if sel_adopt:
        fdf = fdf[fdf["Adoption_Level"].isin(sel_adopt)]
    if len(date_range) == 2:
        start, end = date_range
        fdf = fdf[(fdf["Date"].dt.date >= start) & (fdf["Date"].dt.date <= end)]
    return fdf


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    ensure_plotly_available()
    df = load_data()

    # sidebar
    sel_dept, sel_exp, sel_adopt, date_range = render_sidebar(df)
    fdf = filter_data(df, sel_dept, sel_exp, sel_adopt, date_range)

    if fdf.empty:
        st.warning("No data matches the selected filters. Please broaden your selection.")
        return

    # ── HEADER ──────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="dash-header">
      <div style="background:{ACCENT}22; border:1px solid {ACCENT}55; border-radius:8px;
                  width:36px; height:36px; display:flex; align-items:center; justify-content:center;
                  font-size:18px;">🤖</div>
      <div>
        <div class="dash-title">OpenAI Productivity Intelligence</div>
        <div class="dash-subtitle">Enterprise AI Adoption & Performance Analytics</div>
      </div>
      <div class="dash-badge">● LIVE · {len(fdf):,} records</div>
    </div>
    """, unsafe_allow_html=True)

    # ── ROW 1 – KPI CARDS ───────────────────────────────────────────────
    avg_prod  = fdf["Productivity_Improvement_%"].mean()
    tot_rev   = fdf["Revenue_Impact_USD"].sum()
    avg_sat   = fdf["Satisfaction_Score"].mean()
    avg_usage = fdf["Daily_AI_Usage_Minutes"].mean()
    avg_cost  = fdf["Cost_Savings_USD"].sum()
    avg_dec   = fdf["Decision_Speed_Improvement_%"].mean()

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(kpi_html(
            "Avg Productivity Gain",
            f"{avg_prod:.1f}%",
            f"↑ {avg_prod - 25:.1f}pp vs benchmark",
            "📈"
        ), unsafe_allow_html=True)
    with k2:
        st.markdown(kpi_html(
            "Total Revenue Impact",
            f"${tot_rev/1_000_000:.1f}M",
            f"${tot_rev/len(fdf):,.0f} per employee",
            "💰"
        ), unsafe_allow_html=True)
    with k3:
        st.markdown(kpi_html(
            "Avg Satisfaction Score",
            f"{avg_sat:.1f} / 10",
            f"↑ {avg_dec:.1f}% decision speed",
            "⭐"
        ), unsafe_allow_html=True)
    with k4:
        st.markdown(kpi_html(
            "Avg Daily AI Usage",
            f"{avg_usage:.0f} min",
            f"${avg_cost/1_000_000:.1f}M total cost savings",
            "⏱️"
        ), unsafe_allow_html=True)

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

    # ── ROW 2 – Line + Funnel ───────────────────────────────────────────
    r2a, r2b = st.columns([3, 2], gap="small")
    with r2a:
        st.markdown(f"<div class='chart-title'>📊 Productivity Trend Over Time</div>", unsafe_allow_html=True)
        with st.container():
            st.plotly_chart(build_line_chart(fdf), use_container_width=True, config={"displayModeBar": False})

    with r2b:
        st.markdown(f"<div class='chart-title'>🔀 Adoption vs Trust Funnel</div>", unsafe_allow_html=True)
        st.plotly_chart(build_funnel_chart(fdf), use_container_width=True, config={"displayModeBar": False})

    # ── ROW 3 – Bar + Scatter + Box ─────────────────────────────────────
    r3a, r3b, r3c = st.columns([1, 1.4, 1], gap="small")
    with r3a:
        st.markdown(f"<div class='chart-title'>🏢 Dept · AI Usage</div>", unsafe_allow_html=True)
        st.plotly_chart(build_bar_chart(fdf), use_container_width=True, config={"displayModeBar": False})

    with r3b:
        st.markdown(f"<div class='chart-title'>💡 Revenue vs Cost Savings</div>", unsafe_allow_html=True)
        st.plotly_chart(build_scatter_chart(fdf), use_container_width=True, config={"displayModeBar": False})

    with r3c:
        st.markdown(f"<div class='chart-title'>🎯 Experience vs Revenue</div>", unsafe_allow_html=True)
        st.plotly_chart(build_box_chart(fdf), use_container_width=True, config={"displayModeBar": False})

    # ── ROW 4 – Correlation Heatmap ─────────────────────────────────────
    st.markdown(f"<div class='chart-title'>🔥 Metric Correlation Heatmap</div>", unsafe_allow_html=True)
    st.plotly_chart(build_heatmap(fdf), use_container_width=True, config={"displayModeBar": False})

    # ── FOOTER ──────────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="text-align:center; padding:10px 0 2px 0;
                font-size:10px; color:{TEXT_SEC}; border-top:1px solid {BORDER}; margin-top:6px;">
      OpenAI Productivity Intelligence · Built with Streamlit + Plotly ·
      <span style="color:{ACCENT};">●</span> {len(fdf):,} records rendered
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
