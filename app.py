import os

import numpy as np
import pandas as pd
import streamlit as st

PLOTLY_IMPORT_ERROR = None
try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
except ModuleNotFoundError as exc:
    go = None
    make_subplots = None
    PLOTLY_IMPORT_ERROR = exc


st.set_page_config(
    page_title="OpenAI Productivity Intelligence",
    layout="wide",
    initial_sidebar_state="expanded",
)


ACCENT = "#F4F4F4"
ACCENT_SOFT = "#C2C2C2"
BG_DARK = "#080808"
BG_PANEL = "#101010"
BG_PANEL_ALT = "#171717"
BORDER = "#232323"
TEXT_PRI = "#FFFFFF"
TEXT_SEC = "#A6A6A6"
TEXT_TERT = "#6D6D6D"
GRID_COLOR = "#1E1E1E"

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=TEXT_PRI, family="Manrope, sans-serif", size=12),
    margin=dict(l=10, r=10, t=36, b=10),
    xaxis=dict(
        gridcolor=GRID_COLOR,
        linecolor=BORDER,
        tickcolor=TEXT_SEC,
        tickfont=dict(color=TEXT_SEC, size=10),
    ),
    yaxis=dict(
        gridcolor=GRID_COLOR,
        linecolor=BORDER,
        tickcolor=TEXT_SEC,
        tickfont=dict(color=TEXT_SEC, size=10),
    ),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT_SEC, size=10)),
    coloraxis_colorbar=dict(tickfont=dict(color=TEXT_SEC)),
    hoverlabel=dict(
        bgcolor=BG_PANEL_ALT,
        bordercolor=BORDER,
        font=dict(color=TEXT_PRI, family="Manrope, sans-serif"),
    ),
)

DEPT_COLORS = {
    "IT": "#F2F2F2",
    "Marketing": "#D4D4D4",
    "Sales": "#BABABA",
    "Finance": "#9D9D9D",
    "HR": "#7E7E7E",
    "Operations": "#606060",
}


def rgba(hex_color: str, alpha: float) -> str:
    hex_color = hex_color.lstrip("#")
    red = int(hex_color[0:2], 16)
    green = int(hex_color[2:4], 16)
    blue = int(hex_color[4:6], 16)
    return f"rgba({red}, {green}, {blue}, {alpha})"


st.markdown(
    f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');

  html, body, [class*="css"] {{
    font-family: 'Manrope', sans-serif;
    color: {TEXT_PRI};
  }}

  html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], .stApp {{
    background:
      radial-gradient(circle at top left, rgba(255,255,255,0.10), transparent 26%),
      radial-gradient(circle at top right, rgba(255,255,255,0.06), transparent 22%),
      linear-gradient(180deg, #111111 0%, {BG_DARK} 38%, {BG_DARK} 100%);
  }}

  #MainMenu, footer, header {{
    visibility: hidden;
  }}

  .block-container {{
    padding: 1.2rem 1.4rem 1rem 1.4rem !important;
    max-width: 100% !important;
  }}

  [data-testid="stSidebar"] {{
    background:
      radial-gradient(circle at top center, rgba(255,255,255,0.08), transparent 28%),
      linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
    border-right: 1px solid {BORDER};
    backdrop-filter: blur(18px);
  }}

  [data-testid="stSidebar"] * {{
    color: {TEXT_PRI} !important;
  }}

  [data-testid="stSidebar"] label,
  [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{
    color: {TEXT_SEC} !important;
  }}

  [data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {{
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    color: {TEXT_PRI} !important;
  }}

  [data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"],
  [data-testid="stSidebar"] .stDateInput input,
  [data-testid="stSidebar"] .stDateInput [data-baseweb="input"] {{
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 14px !important;
  }}

  [data-testid="stSidebar"] .stDateInput [data-baseweb="input"] {{
    padding-left: 0.25rem;
  }}

  .sidebar-shell {{
    padding: 0.1rem 0 1rem 0;
    margin-bottom: 1rem;
    border-bottom: 1px solid {BORDER};
  }}

  .sidebar-kicker {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: {TEXT_SEC};
    margin-bottom: 0.65rem;
  }}

  .sidebar-title {{
    font-size: 1.15rem;
    font-weight: 700;
    color: {TEXT_PRI};
    letter-spacing: -0.03em;
  }}

  .sidebar-copy {{
    margin-top: 0.35rem;
    font-size: 0.86rem;
    color: {TEXT_SEC};
    line-height: 1.55;
  }}

  .hero-panel {{
    position: relative;
    overflow: hidden;
    margin-bottom: 1rem;
    padding: 1.35rem 1.4rem;
    border-radius: 28px;
    border: 1px solid rgba(255,255,255,0.08);
    background:
      radial-gradient(circle at 12% 18%, rgba(255,255,255,0.12), transparent 24%),
      radial-gradient(circle at 82% 20%, rgba(255,255,255,0.07), transparent 24%),
      linear-gradient(135deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02) 45%, rgba(0,0,0,0.18));
    box-shadow: 0 28px 70px rgba(0, 0, 0, 0.34);
  }}

  .hero-grid {{
    display: grid;
    grid-template-columns: minmax(0, 2.1fr) minmax(280px, 1fr);
    gap: 1rem;
    align-items: end;
  }}

  .hero-overline {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: {TEXT_SEC};
    margin-bottom: 0.65rem;
  }}

  .hero-title {{
    max-width: 11ch;
    font-size: clamp(2.25rem, 4vw, 4.4rem);
    line-height: 0.98;
    font-weight: 800;
    letter-spacing: -0.07em;
    color: {TEXT_PRI};
  }}

  .hero-copy {{
    margin-top: 0.9rem;
    max-width: 58ch;
    font-size: 0.97rem;
    line-height: 1.7;
    color: {TEXT_SEC};
  }}

  .hero-meta {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.6rem;
    margin-top: 1rem;
  }}

  .hero-chip {{
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    padding: 0.5rem 0.8rem;
    border-radius: 999px;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.04);
    color: {TEXT_PRI};
    font-size: 0.76rem;
    font-weight: 600;
    letter-spacing: 0.01em;
  }}

  .hero-side {{
    padding: 1rem;
    border-radius: 22px;
    border: 1px solid rgba(255,255,255,0.08);
    background: linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02));
    backdrop-filter: blur(14px);
  }}

  .hero-stat-label {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: {TEXT_SEC};
  }}

  .hero-stat-value {{
    margin-top: 0.55rem;
    font-size: 2.7rem;
    line-height: 1;
    font-weight: 800;
    letter-spacing: -0.06em;
    color: {TEXT_PRI};
  }}

  .hero-stat-copy {{
    margin-top: 0.65rem;
    color: {TEXT_SEC};
    font-size: 0.88rem;
    line-height: 1.6;
  }}

  .kpi-card {{
    background:
      linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02)),
      linear-gradient(135deg, {BG_PANEL_ALT} 0%, {BG_PANEL} 100%);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 22px;
    padding: 1rem 1.1rem;
    position: relative;
    overflow: hidden;
    min-height: 138px;
    box-shadow: 0 22px 40px rgba(0, 0, 0, 0.28);
  }}

  .kpi-card::before {{
    content: "";
    position: absolute;
    inset: 0;
    background:
      radial-gradient(circle at top left, rgba(255,255,255,0.12), transparent 40%),
      linear-gradient(180deg, rgba(255,255,255,0.06), transparent 45%);
    pointer-events: none;
  }}

  .kpi-label {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    font-weight: 500;
    color: {TEXT_SEC};
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin: 0.95rem 0 0.65rem 0;
  }}

  .kpi-value {{
    font-size: 1.9rem;
    font-weight: 800;
    color: {TEXT_PRI};
    line-height: 1.05;
    letter-spacing: -0.04em;
  }}

  .kpi-delta {{
    font-size: 12px;
    color: {TEXT_SEC};
    margin-top: 0.5rem;
    font-weight: 500;
    line-height: 1.5;
  }}

  .kpi-tag {{
    position: absolute;
    top: 1rem;
    right: 1rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 2.1rem;
    height: 2.1rem;
    padding: 0 0.65rem;
    border-radius: 999px;
    border: 1px solid rgba(255,255,255,0.10);
    background: rgba(255,255,255,0.04);
    color: {TEXT_PRI};
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.16em;
    text-transform: uppercase;
  }}

  .section-head {{
    margin: 0.15rem 0 0.55rem 0;
  }}

  .section-eyebrow {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: {TEXT_TERT};
    margin-bottom: 0.35rem;
  }}

  .section-title {{
    font-size: 1rem;
    font-weight: 600;
    color: {TEXT_PRI};
    letter-spacing: -0.03em;
  }}

  div[data-testid="stPlotlyChart"] {{
    background:
      linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02)),
      linear-gradient(135deg, {BG_PANEL_ALT}, {BG_PANEL});
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 24px;
    padding: 0.2rem 0.25rem 0.15rem 0.25rem;
    box-shadow: 0 24px 48px rgba(0, 0, 0, 0.26);
    overflow: hidden;
  }}

  div[data-testid="stPlotlyChart"] > div {{
    border-radius: 18px;
  }}

  .stMultiSelect div[data-baseweb="select"] {{
    background-color: rgba(255,255,255,0.03) !important;
    border-color: rgba(255,255,255,0.08) !important;
  }}

  .stDateInput input {{
    background-color: rgba(255,255,255,0.03) !important;
    border-color: rgba(255,255,255,0.08) !important;
    color: {TEXT_PRI} !important;
  }}

  [data-baseweb="popover"] * {{
    color: {TEXT_PRI} !important;
  }}

  [data-baseweb="menu"] {{
    background: {BG_PANEL_ALT} !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
  }}

  @media (max-width: 980px) {{
    .hero-grid {{
      grid-template-columns: 1fr;
    }}

    .hero-title {{
      max-width: 100%;
      font-size: 2.6rem;
    }}
  }}
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_data
def load_data() -> pd.DataFrame:
    paths = [
        "OpenAI_Usage_Productivity_Dataset.csv",
        os.path.join(os.path.dirname(__file__), "OpenAI_Usage_Productivity_Dataset.csv"),
        "/mnt/user-data/uploads/OpenAI_Usage_Productivity_Dataset.csv",
    ]
    df = None
    for path in paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            break

    if df is None:
        np.random.seed(42)
        n = 2000
        departments = ["IT", "Marketing", "Sales", "Finance", "HR", "Operations"]
        experience_levels = ["Junior", "Mid", "Senior"]
        adoption_levels = ["Low", "Medium", "High"]
        trust_levels = ["Low", "Medium", "High"]
        complexity_levels = ["Low", "Medium", "High"]

        department_array = np.random.choice(
            departments, n, p=[0.22, 0.20, 0.20, 0.15, 0.13, 0.10]
        )
        experience_array = np.random.choice(
            experience_levels, n, p=[0.35, 0.40, 0.25]
        )
        adoption_array = np.random.choice(adoption_levels, n, p=[0.25, 0.40, 0.35])
        trust_array = np.random.choice(trust_levels, n, p=[0.20, 0.40, 0.40])
        complexity_array = np.random.choice(complexity_levels, n, p=[0.25, 0.45, 0.30])

        adoption_numeric = np.array([{"Low": 1, "Medium": 2, "High": 3}[value] for value in adoption_array])
        trust_numeric = np.array([{"Low": 1, "Medium": 2, "High": 3}[value] for value in trust_array])
        complexity_numeric = np.array([{"Low": 1, "Medium": 2, "High": 3}[value] for value in complexity_array])
        experience_numeric = np.array([{"Junior": 1, "Mid": 2, "Senior": 3}[value] for value in experience_array])

        usage = (
            30
            + adoption_numeric * 20
            + (department_array == "IT") * 20
            + (department_array == "Marketing") * 15
            + np.random.normal(0, 15, n)
        )
        usage = np.clip(usage, 5, 180)

        productivity = (
            15
            + adoption_numeric * 6
            + complexity_numeric * 4
            + trust_numeric * 2
            + np.random.normal(0, 5, n)
        )
        productivity = np.clip(productivity, 5, 60)

        revenue = (
            5000
            + adoption_numeric * 1500
            + (department_array == "Sales") * 4000
            + experience_numeric * 500
            + complexity_numeric * 800
            + np.random.normal(0, 1500, n)
        )
        revenue = np.clip(revenue, 500, 20000)

        cost_savings = (
            1000
            + adoption_numeric * 600
            + complexity_numeric * 400
            + trust_numeric * 200
            + np.random.normal(0, 700, n)
        )
        cost_savings = np.clip(cost_savings, 100, 8000)

        decision_speed = (
            10
            + trust_numeric * 6
            + complexity_numeric * 4
            + adoption_numeric * 3
            + np.random.normal(0, 8, n)
        )
        decision_speed = np.clip(decision_speed, 2, 55)

        satisfaction = 5 + trust_numeric * 1.2 + adoption_numeric * 0.5 + np.random.normal(0, 0.8, n)
        satisfaction = np.clip(satisfaction, 1, 10)

        dates = pd.date_range("2024-01-01", "2024-12-31", periods=n)
        df = pd.DataFrame(
            {
                "Date": dates,
                "Department": department_array,
                "Experience_Level": experience_array,
                "Adoption_Level": adoption_array,
                "AI_Trust_Level": trust_array,
                "Prompt_Complexity": complexity_array,
                "Daily_AI_Usage_Minutes": usage.round(1),
                "Productivity_Improvement_%": productivity.round(2),
                "Revenue_Impact_USD": revenue.round(2),
                "Cost_Savings_USD": cost_savings.round(2),
                "Decision_Speed_Improvement_%": decision_speed.round(2),
                "Satisfaction_Score": satisfaction.round(1),
            }
        )

    df["Date"] = pd.to_datetime(df["Date"])

    column_map = {
        "Productivity_Improvement_%": "Productivity_Improvement_%",
        "Productivity Improvement %": "Productivity_Improvement_%",
        "Decision_Speed_Improvement_%": "Decision_Speed_Improvement_%",
        "Decision Speed Improvement %": "Decision_Speed_Improvement_%",
    }
    df.rename(columns=column_map, inplace=True)

    if "Adoption_Level" not in df.columns and "Adoption Level" in df.columns:
        df.rename(columns={"Adoption Level": "Adoption_Level"}, inplace=True)

    if "Department" in df.columns:
        df = df[df["Department"].isin(list(DEPT_COLORS.keys()))].copy()

    return df


def apply_theme(fig, height=260, title=""):
    fig.update_layout(
        **{key: value for key, value in PLOTLY_LAYOUT.items()},
        height=height,
        title=dict(text=title),
    )
    return fig


def ensure_plotly_available():
    if PLOTLY_IMPORT_ERROR is None:
        return

    st.error("Plotly is required to render this dashboard.")
    st.code("py -3.12 -m pip install -r requirements.txt", language="bash")
    st.info(f"Import error: {PLOTLY_IMPORT_ERROR}")
    st.stop()


def kpi_html(label, value, delta, tag):
    return f"""
    <div class="kpi-card">
      <div class="kpi-tag">{tag}</div>
      <div class="kpi-label">{label}</div>
      <div class="kpi-value">{value}</div>
      <div class="kpi-delta">{delta}</div>
    </div>
    """


def section_header_html(eyebrow, title):
    return f"""
    <div class="section-head">
      <div class="section-eyebrow">{eyebrow}</div>
      <div class="section-title">{title}</div>
    </div>
    """


def build_line_chart(df: pd.DataFrame):
    timeseries = df.groupby("Date")["Productivity_Improvement_%"].mean().reset_index()
    timeseries = timeseries.sort_values("Date")
    timeseries["Rolling"] = timeseries["Productivity_Improvement_%"].rolling(7, min_periods=1).mean()

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=timeseries["Date"],
            y=timeseries["Productivity_Improvement_%"],
            mode="lines",
            name="Daily",
            line=dict(color=rgba(ACCENT_SOFT, 0.55), width=1),
            showlegend=True,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=timeseries["Date"],
            y=timeseries["Rolling"],
            mode="lines",
            name="7-day Avg",
            line=dict(color=ACCENT, width=2),
            fill="tozeroy",
            fillcolor=rgba(ACCENT, 0.09),
        )
    )
    apply_theme(fig, height=240)
    fig.update_layout(
        xaxis_title="",
        yaxis_title="Productivity %",
        legend=dict(orientation="h", y=1.08, x=0),
    )
    return fig


def build_funnel_chart(df: pd.DataFrame):
    adoption_order = ["High", "Medium", "Low"]
    trust_order = ["High", "Medium", "Low"]

    adoption_counts = df["Adoption_Level"].value_counts().reindex(adoption_order, fill_value=0)
    trust_counts = df["AI_Trust_Level"].value_counts().reindex(trust_order, fill_value=0)
    total_records = max(len(df), 1)

    fig = make_subplots(
        rows=1,
        cols=2,
        specs=[[{"type": "funnel"}, {"type": "funnel"}]],
        subplot_titles=["Adoption Level", "AI Trust Level"],
        horizontal_spacing=0.22,
    )
    fig.add_trace(
        go.Funnel(
            y=adoption_order,
            x=adoption_counts.values,
            textposition="outside",
            text=[f"{value:,}<br>{value / total_records:.0%}" for value in adoption_counts.values],
            textinfo="text",
            marker=dict(color=["#E4E4E4", "#AAAAAA", "#616161"]),
            connector=dict(line=dict(color=BORDER, width=1)),
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Funnel(
            y=trust_order,
            x=trust_counts.values,
            textposition="outside",
            text=[f"{value:,}<br>{value / total_records:.0%}" for value in trust_counts.values],
            textinfo="text",
            marker=dict(color=["#FFFFFF", "#CFCFCF", "#7A7A7A"]),
            connector=dict(line=dict(color=BORDER, width=1)),
        ),
        row=1,
        col=2,
    )
    apply_theme(fig, height=260)
    fig.update_layout(
        showlegend=False,
        margin=dict(l=28, r=34, t=54, b=10),
    )
    fig.update_traces(
        textfont=dict(size=11, color=TEXT_PRI),
        outsidetextfont=dict(size=11, color=TEXT_PRI),
    )
    fig.update_annotations(font=dict(color=TEXT_SEC, size=10))
    return fig


def build_bar_chart(df: pd.DataFrame):
    aggregate = (
        df.groupby("Department")["Daily_AI_Usage_Minutes"]
        .mean()
        .reset_index()
        .sort_values("Daily_AI_Usage_Minutes", ascending=True)
    )
    colors = [DEPT_COLORS.get(department, ACCENT_SOFT) for department in aggregate["Department"]]

    fig = go.Figure(
        go.Bar(
            x=aggregate["Daily_AI_Usage_Minutes"],
            y=aggregate["Department"],
            orientation="h",
            marker=dict(color=colors, line=dict(width=0)),
            text=aggregate["Daily_AI_Usage_Minutes"].round(1).astype(str) + " min",
            textposition="outside",
            textfont=dict(color=TEXT_SEC, size=10),
        )
    )
    apply_theme(fig, height=240)
    fig.update_layout(xaxis_title="Avg daily usage (min)", yaxis_title="")
    return fig


def build_scatter_chart(df: pd.DataFrame):
    sample = df.sample(min(800, len(df)), random_state=42)

    fig = go.Figure()
    for department, color in DEPT_COLORS.items():
        mask = sample["Department"] == department
        if mask.sum() == 0:
            continue
        subset = sample[mask]
        fig.add_trace(
            go.Scatter(
                x=subset["Revenue_Impact_USD"],
                y=subset["Cost_Savings_USD"],
                mode="markers",
                name=department,
                marker=dict(
                    color=color,
                    size=5,
                    opacity=0.75,
                    line=dict(width=0.3, color=rgba(TEXT_PRI, 0.18)),
                ),
            )
        )

    apply_theme(fig, height=240)
    fig.update_layout(
        xaxis_title="Revenue impact ($)",
        yaxis_title="Cost savings ($)",
        legend=dict(orientation="h", y=1.08, x=0, font=dict(size=9)),
    )
    return fig


def build_box_chart(df: pd.DataFrame):
    experience_order = ["Junior", "Mid", "Senior"]
    experience_colors = {"Junior": "#8D8D8D", "Mid": "#DADADA", "Senior": "#F3F3F3"}

    fig = go.Figure()
    for level in experience_order:
        subset = df[df["Experience_Level"] == level]
        fig.add_trace(
            go.Box(
                y=subset["Revenue_Impact_USD"],
                name=level,
                marker_color=experience_colors[level],
                line=dict(width=1.5),
                fillcolor=rgba(experience_colors[level], 0.24),
                boxmean="sd",
            )
        )

    apply_theme(fig, height=240)
    fig.update_layout(yaxis_title="Revenue impact ($)", showlegend=False)
    return fig


def build_heatmap(df: pd.DataFrame):
    numeric_columns = [
        "Daily_AI_Usage_Minutes",
        "Productivity_Improvement_%",
        "Revenue_Impact_USD",
        "Cost_Savings_USD",
        "Decision_Speed_Improvement_%",
        "Satisfaction_Score",
    ]
    labels = ["AI Usage", "Productivity", "Revenue", "Cost Savings", "Decision Speed", "Satisfaction"]
    correlation = df[numeric_columns].corr().round(2)
    correlation.index = labels
    correlation.columns = labels

    fig = go.Figure(
        go.Heatmap(
            z=correlation.values,
            x=labels,
            y=labels,
            colorscale=[[0, "#0B0B0B"], [0.5, "#3B3B3B"], [1, "#D9D9D9"]],
            zmid=0,
            zmin=-1,
            zmax=1,
            text=correlation.values.round(2),
            texttemplate="%{text}",
            textfont=dict(size=10, color=TEXT_PRI),
            hoverongaps=False,
            colorbar=dict(thickness=10, tickfont=dict(color=TEXT_SEC, size=9)),
        )
    )
    apply_theme(fig, height=220)
    fig.update_layout(
        xaxis=dict(tickfont=dict(size=9, color=TEXT_SEC), side="bottom"),
        yaxis=dict(tickfont=dict(size=9, color=TEXT_SEC), autorange="reversed"),
    )
    return fig


def render_sidebar(df: pd.DataFrame):
    st.sidebar.markdown(
        f"""
        <div class="sidebar-shell">
          <div class="sidebar-kicker">OpenAI-inspired view</div>
          <div class="sidebar-title">Control Panel</div>
          <div class="sidebar-copy">
            Narrow the dashboard by department, seniority, adoption level, and date range.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    departments = sorted(df["Department"].unique().tolist())
    selected_departments = st.sidebar.multiselect("Department", departments, default=departments)

    experience_options = ["Junior", "Mid", "Senior"]
    selected_experience = st.sidebar.multiselect(
        "Experience Level", experience_options, default=experience_options
    )

    adoption_options = ["Low", "Medium", "High"]
    selected_adoption = st.sidebar.multiselect("Adoption Level", adoption_options, default=adoption_options)

    min_date = df["Date"].min().date()
    max_date = df["Date"].max().date()
    date_range = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    st.sidebar.markdown(f"<hr style='border-color:{BORDER};margin:16px 0;'>", unsafe_allow_html=True)
    st.sidebar.markdown(
        f"""
        <div style="font-size:10px; color:{TEXT_SEC}; line-height:1.6;">
          <b style="color:{TEXT_PRI};">Dataset</b><br>
          {len(df):,} records | {df['Department'].nunique()} departments<br>
          {df['Date'].min().strftime('%b %Y')} to {df['Date'].max().strftime('%b %Y')}
        </div>
        """,
        unsafe_allow_html=True,
    )

    return selected_departments, selected_experience, selected_adoption, date_range


def filter_data(df, selected_departments, selected_experience, selected_adoption, date_range):
    filtered = df.copy()
    if selected_departments:
        filtered = filtered[filtered["Department"].isin(selected_departments)]
    if selected_experience:
        filtered = filtered[filtered["Experience_Level"].isin(selected_experience)]
    if selected_adoption:
        filtered = filtered[filtered["Adoption_Level"].isin(selected_adoption)]
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered = filtered[
            (filtered["Date"].dt.date >= start_date) & (filtered["Date"].dt.date <= end_date)
        ]
    return filtered


def main():
    ensure_plotly_available()
    df = load_data()

    selected_departments, selected_experience, selected_adoption, date_range = render_sidebar(df)
    filtered_df = filter_data(
        df,
        selected_departments,
        selected_experience,
        selected_adoption,
        date_range,
    )

    if filtered_df.empty:
        st.warning("No data matches the selected filters. Please broaden your selection.")
        return

    avg_productivity = filtered_df["Productivity_Improvement_%"].mean()
    total_revenue = filtered_df["Revenue_Impact_USD"].sum()
    avg_satisfaction = filtered_df["Satisfaction_Score"].mean()
    avg_usage = filtered_df["Daily_AI_Usage_Minutes"].mean()
    total_cost_savings = filtered_df["Cost_Savings_USD"].sum()
    avg_decision_speed = filtered_df["Decision_Speed_Improvement_%"].mean()

    date_start = filtered_df["Date"].min().strftime("%b %d, %Y")
    date_end = filtered_df["Date"].max().strftime("%b %d, %Y")

    st.markdown(
        f"""
        <div class="hero-panel">
          <div class="hero-grid">
            <div>
              <div class="hero-overline">OpenAI productivity intelligence</div>
              <div class="hero-title">Quiet, focused analytics for AI performance.</div>
              <div class="hero-copy">
                The dashboard now uses a Cod Gray foundation, bright white typography, and soft
                gradients to echo the visual feel of OpenAI's website while keeping the data easy to read.
              </div>
              <div class="hero-meta">
                <div class="hero-chip">Live filtered view</div>
                <div class="hero-chip">{len(filtered_df):,} records</div>
                <div class="hero-chip">{date_start} to {date_end}</div>
              </div>
            </div>
            <div class="hero-side">
              <div class="hero-stat-label">Average productivity lift</div>
              <div class="hero-stat-value">{avg_productivity:.1f}%</div>
              <div class="hero-stat-copy">
                Supported by {avg_usage:.0f} minutes of daily AI usage and
                {avg_decision_speed:.1f}% average decision-speed improvement in the selected cohort.
              </div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    kpi_1, kpi_2, kpi_3, kpi_4 = st.columns(4)
    with kpi_1:
        st.markdown(
            kpi_html(
                "Average Productivity Gain",
                f"{avg_productivity:.1f}%",
                f"{avg_productivity - 25:+.1f} pp versus benchmark",
                "K01",
            ),
            unsafe_allow_html=True,
        )
    with kpi_2:
        st.markdown(
            kpi_html(
                "Total Revenue Impact",
                f"${total_revenue / 1_000_000:.1f}M",
                f"${total_revenue / len(filtered_df):,.0f} per employee",
                "K02",
            ),
            unsafe_allow_html=True,
        )
    with kpi_3:
        st.markdown(
            kpi_html(
                "Average Satisfaction Score",
                f"{avg_satisfaction:.1f} / 10",
                f"{avg_decision_speed:.1f}% faster decisions",
                "K03",
            ),
            unsafe_allow_html=True,
        )
    with kpi_4:
        st.markdown(
            kpi_html(
                "Average Daily AI Usage",
                f"{avg_usage:.0f} min",
                f"${total_cost_savings / 1_000_000:.1f}M total cost savings",
                "K04",
            ),
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

    row_2a, row_2b = st.columns([2.8, 2.2], gap="small")
    with row_2a:
        st.markdown(section_header_html("Trend", "Productivity over time"), unsafe_allow_html=True)
        st.plotly_chart(build_line_chart(filtered_df), use_container_width=True, config={"displayModeBar": False})

    with row_2b:
        st.markdown(section_header_html("Distribution", "Adoption versus trust"), unsafe_allow_html=True)
        st.plotly_chart(
            build_funnel_chart(filtered_df),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    row_3a, row_3b, row_3c = st.columns([1, 1.4, 1], gap="small")
    with row_3a:
        st.markdown(section_header_html("Departments", "AI usage by team"), unsafe_allow_html=True)
        st.plotly_chart(build_bar_chart(filtered_df), use_container_width=True, config={"displayModeBar": False})

    with row_3b:
        st.markdown(section_header_html("Economics", "Revenue versus cost savings"), unsafe_allow_html=True)
        st.plotly_chart(
            build_scatter_chart(filtered_df),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    with row_3c:
        st.markdown(section_header_html("Experience", "Revenue by seniority"), unsafe_allow_html=True)
        st.plotly_chart(build_box_chart(filtered_df), use_container_width=True, config={"displayModeBar": False})

    st.markdown(section_header_html("Correlation", "Metric relationship matrix"), unsafe_allow_html=True)
    st.plotly_chart(build_heatmap(filtered_df), use_container_width=True, config={"displayModeBar": False})

    st.markdown(
        f"""
        <div style="text-align:center; padding:10px 0 2px 0; font-size:10px; color:{TEXT_SEC};
                    border-top:1px solid {BORDER}; margin-top:6px;">
          OpenAI Productivity Intelligence | Built with Streamlit and Plotly |
          {len(filtered_df):,} records rendered
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
