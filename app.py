import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import google.generativeai as genai
import json
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Aurora Executive Dashboard",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --ink:     #0D0F12;
    --paper:   #F5F3EE;
    --gold:    #C8A96E;
    --gold2:   #E8C98A;
    --slate:   #2B3240;
    --muted:   #7A8394;
    --accent:  #3D6B8C;
    --danger:  #B85450;
    --success: #4A7C59;
    --border:  #DDD9D0;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--paper);
    color: var(--ink);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: var(--ink) !important;
    border-right: 1px solid #1E2330;
}
[data-testid="stSidebar"] * {
    color: #C8CDD8 !important;
}
[data-testid="stSidebar"] h1, 
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: var(--gold) !important;
    font-family: 'Syne', sans-serif !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stDateInput label,
[data-testid="stSidebar"] .stSlider label {
    color: #8A9AB0 !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    font-family: 'DM Mono', monospace !important;
}

/* KPI cards */
.kpi-card {
    background: white;
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 20px 24px;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--gold);
}
.kpi-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 8px;
}
.kpi-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.9rem;
    font-weight: 700;
    color: var(--ink);
    line-height: 1;
}
.kpi-delta {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    margin-top: 6px;
}
.kpi-delta.pos { color: var(--success); }
.kpi-delta.neg { color: var(--danger); }
.kpi-delta.neu { color: var(--muted); }

/* Section headers */
.section-header {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--muted);
    border-bottom: 1px solid var(--border);
    padding-bottom: 8px;
    margin-bottom: 16px;
    margin-top: 32px;
}

/* AI insight panel */
.insight-panel {
    background: var(--ink);
    border-radius: 4px;
    padding: 28px 32px;
    color: #C8CDD8;
    position: relative;
    overflow: hidden;
}
.insight-panel::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    background: linear-gradient(180deg, var(--gold), var(--accent));
}
.insight-tag {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 12px;
}
.insight-content {
    font-size: 0.88rem;
    line-height: 1.7;
    color: #C8CDD8;
}
.insight-section-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--gold2);
    margin-top: 16px;
    margin-bottom: 6px;
    letter-spacing: 0.05em;
}

/* Page title */
.dash-title {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: var(--ink);
    letter-spacing: -0.02em;
    line-height: 1.1;
}
.dash-subtitle {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.1em;
    color: var(--muted);
    text-transform: uppercase;
    margin-top: 4px;
}

/* Upload area */
.upload-hero {
    text-align: center;
    padding: 80px 40px;
    background: white;
    border: 2px dashed var(--border);
    border-radius: 8px;
    margin: 40px auto;
    max-width: 600px;
}
.upload-icon {
    font-size: 3rem;
    margin-bottom: 16px;
}
.upload-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--ink);
    margin-bottom: 8px;
}
.upload-hint {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: var(--muted);
    letter-spacing: 0.05em;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: transparent;
    border-bottom: 1px solid var(--border);
    gap: 0;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
    padding: 10px 20px !important;
    border-bottom: 2px solid transparent !important;
}
.stTabs [aria-selected="true"] {
    color: var(--ink) !important;
    border-bottom: 2px solid var(--gold) !important;
    background: transparent !important;
}

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--paper); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }

.stButton>button {
    background: var(--ink) !important;
    color: var(--gold) !important;
    border: 1px solid #2E3545 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    border-radius: 2px !important;
    padding: 10px 24px !important;
    transition: all 0.2s !important;
}
.stButton>button:hover {
    background: #1E2330 !important;
    border-color: var(--gold) !important;
}

/* Number input, text input */
.stTextInput input, .stNumberInput input {
    background: white !important;
    border: 1px solid var(--border) !important;
    border-radius: 2px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.85rem !important;
}

div[data-testid="metric-container"] {
    background: white;
    border: 1px solid var(--border);
    padding: 16px;
    border-radius: 4px;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def fmt_currency(val):
    if val >= 1_000_000:
        return f"${val/1_000_000:.2f}M"
    elif val >= 1_000:
        return f"${val/1_000:.1f}K"
    return f"${val:.0f}"

def fmt_pct(val):
    return f"{val:.1f}%"

def delta_class(val):
    if val > 0: return "pos", f"▲ {abs(val):.1f}%"
    if val < 0: return "neg", f"▼ {abs(val):.1f}%"
    return "neu", "— 0.0%"

CHART_COLORS = ["#C8A96E", "#3D6B8C", "#4A7C59", "#B85450", "#7B6EA8", "#D4875A"]
CHART_LAYOUT = dict(
    paper_bgcolor="white",
    plot_bgcolor="white",
    font_family="DM Sans",
    font_color="#0D0F12",
    title_font_family="Syne",
    title_font_size=13,
    margin=dict(t=40, b=30, l=30, r=20),
    legend=dict(
        bgcolor="white",
        bordercolor="#DDD9D0",
        borderwidth=1,
        font=dict(size=11),
    ),
)

def apply_layout(fig, **kwargs):
    fig.update_layout(**CHART_LAYOUT, **kwargs)
    fig.update_xaxes(showgrid=False, linecolor="#DDD9D0", tickfont=dict(size=10, family="DM Mono"))
    fig.update_yaxes(showgrid=True, gridcolor="#F0EDE8", linecolor="#DDD9D0", tickfont=dict(size=10, family="DM Mono"))
    return fig


# ── Column detection ───────────────────────────────────────────────────────────
def detect_columns(df):
    """
    Auto-detect semantic column mappings from any uploaded dataset.
    Returns a dict with keys: date, revenue, profit, budget_rev, actual_rev,
    budget_exp, actual_exp, region, channel, churn, segment, category, sentiment
    """
    cols = {c.lower(): c for c in df.columns}
    mapping = {}

    def find(keywords, numeric=False):
        for kw in keywords:
            for lc, orig in cols.items():
                if kw in lc:
                    if numeric:
                        try:
                            pd.to_numeric(df[orig], errors='raise')
                            return orig
                        except Exception:
                            continue
                    else:
                        return orig
        return None

    mapping["date"]       = find(["date", "time", "month", "period", "day"])
    mapping["revenue"]    = find(["revenue", "sales", "income", "turnover"], numeric=True)
    mapping["profit"]     = find(["profit", "margin", "net", "earnings"], numeric=True)
    mapping["budget_rev"] = find(["budgeted_rev", "budget_rev", "budget_sales", "rev_budget", "target_rev"], numeric=True)
    mapping["actual_rev"] = find(["actual_rev", "actual_revenue", "actual_sales"], numeric=True)
    mapping["budget_exp"] = find(["budgeted_exp", "budget_exp", "budget_cost", "exp_budget"], numeric=True)
    mapping["actual_exp"] = find(["actual_exp", "actual_expense", "actual_cost"], numeric=True)
    mapping["region"]     = find(["region", "area", "territory", "location", "geo", "state", "country"])
    mapping["channel"]    = find(["channel", "medium", "platform", "source"])
    mapping["churn"]      = find(["churn", "attrition", "cancel", "churned"])
    mapping["segment"]    = find(["segment", "tier", "type", "customer_type", "client_type"])
    mapping["category"]   = find(["category", "product_cat", "prod_cat", "class", "group"])
    mapping["sentiment"]  = find(["sentiment", "score", "rating", "nps", "satisfaction"], numeric=True)
    mapping["variance_rev"] = find(["variance_rev", "var_rev", "rev_variance"], numeric=True)

    # fallback: actual_rev → revenue
    if not mapping["revenue"] and mapping["actual_rev"]:
        mapping["revenue"] = mapping["actual_rev"]

    return mapping


def load_data(uploaded_file):
    name = uploaded_file.name.lower()
    if name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif name.endswith((".xlsx", ".xls")):
        df = pd.read_excel(uploaded_file)
    elif name.endswith(".json"):
        df = pd.read_json(uploaded_file)
    else:
        st.error("Unsupported file type. Please upload CSV, Excel, or JSON.")
        return None, None

    mapping = detect_columns(df)

    # Parse date
    if mapping["date"]:
        df[mapping["date"]] = pd.to_datetime(df[mapping["date"]], errors="coerce")

    # Numeric coercion for all mapped numeric cols
    for key in ["revenue", "profit", "budget_rev", "actual_rev", "budget_exp", "actual_exp", "sentiment", "variance_rev"]:
        col = mapping.get(key)
        if col:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df, mapping


# ── KPI computation ───────────────────────────────────────────────────────────
def compute_kpis(df, m):
    kpis = {}

    rev_col    = m.get("revenue")
    profit_col = m.get("profit")
    brev_col   = m.get("budget_rev")
    arev_col   = m.get("actual_rev")
    bexp_col   = m.get("budget_exp")
    aexp_col   = m.get("actual_exp")
    churn_col  = m.get("churn")
    sent_col   = m.get("sentiment")
    date_col   = m.get("date")

    if rev_col:
        kpis["total_revenue"] = df[rev_col].sum()
    elif arev_col:
        kpis["total_revenue"] = df[arev_col].sum()
    else:
        kpis["total_revenue"] = None

    if profit_col:
        kpis["total_profit"] = df[profit_col].sum()
        if kpis["total_revenue"] and kpis["total_revenue"] != 0:
            kpis["profit_margin"] = (kpis["total_profit"] / kpis["total_revenue"]) * 100
        else:
            kpis["profit_margin"] = None
    else:
        kpis["total_profit"] = None
        kpis["profit_margin"] = None

    # Revenue vs Budget
    if brev_col and arev_col:
        total_budget = df[brev_col].sum()
        total_actual = df[arev_col].sum()
        kpis["budget_rev"]  = total_budget
        kpis["actual_rev"]  = total_actual
        kpis["rev_vs_budget_pct"] = ((total_actual - total_budget) / total_budget * 100) if total_budget else None
    elif m.get("variance_rev"):
        kpis["rev_vs_budget_pct"] = None  # can't compute cleanly

    # Expense variance
    if bexp_col and aexp_col:
        total_bexp = df[bexp_col].sum()
        total_aexp = df[aexp_col].sum()
        kpis["budget_exp"] = total_bexp
        kpis["actual_exp"] = total_aexp
        kpis["exp_vs_budget_pct"] = ((total_aexp - total_bexp) / total_bexp * 100) if total_bexp else None

    # Churn rate
    if churn_col:
        churn_vals = df[churn_col].astype(str).str.strip().str.lower()
        churned = churn_vals.isin(["yes", "1", "true", "churned"]).sum()
        total = len(churn_vals.dropna())
        kpis["churn_count"] = int(churned)
        kpis["churn_rate"]  = (churned / total * 100) if total else None

    # Avg sentiment
    if sent_col:
        kpis["avg_sentiment"] = df[sent_col].mean()

    # Date range
    if date_col:
        valid_dates = df[date_col].dropna()
        if len(valid_dates):
            kpis["date_from"] = valid_dates.min().strftime("%b %d, %Y")
            kpis["date_to"]   = valid_dates.max().strftime("%b %d, %Y")

    return kpis


# ── AI insights ───────────────────────────────────────────────────────────────
def build_kpi_summary(kpis, m, df):
    lines = ["DATASET KPI SUMMARY\n"]
    if kpis.get("date_from"):
        lines.append(f"Period: {kpis['date_from']} – {kpis['date_to']}")
    if kpis.get("total_revenue") is not None:
        lines.append(f"Total Revenue: {fmt_currency(kpis['total_revenue'])}")
    if kpis.get("total_profit") is not None:
        lines.append(f"Total Profit: {fmt_currency(kpis['total_profit'])}")
    if kpis.get("profit_margin") is not None:
        lines.append(f"Profit Margin: {fmt_pct(kpis['profit_margin'])}")
    if kpis.get("rev_vs_budget_pct") is not None:
        lines.append(f"Revenue vs Budget: {'+' if kpis['rev_vs_budget_pct']>0 else ''}{kpis['rev_vs_budget_pct']:.1f}%")
    if kpis.get("churn_rate") is not None:
        lines.append(f"Churn Rate: {fmt_pct(kpis['churn_rate'])} ({kpis['churn_count']} customers churned)")
    if kpis.get("avg_sentiment") is not None:
        lines.append(f"Avg Sentiment Score: {kpis['avg_sentiment']:.2f}")

    # Top region
    if m.get("region") and m.get("revenue"):
        top_region = df.groupby(m["region"])[m["revenue"]].sum().idxmax()
        lines.append(f"Top Revenue Region: {top_region}")

    # Top channel
    if m.get("channel") and m.get("revenue"):
        top_channel = df.groupby(m["channel"])[m["revenue"]].sum().idxmax()
        lines.append(f"Top Revenue Channel: {top_channel}")

    # Expense efficiency
    if kpis.get("exp_vs_budget_pct") is not None:
        sign = "over" if kpis["exp_vs_budget_pct"] > 0 else "under"
        lines.append(f"Expenses: {abs(kpis['exp_vs_budget_pct']):.1f}% {sign} budget")

    return "\n".join(lines)


def generate_ai_insights(kpi_summary, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        generation_config=genai.types.GenerationConfig(
            max_output_tokens=900,
            temperature=0.4,
        )
    )
    prompt = f"""You are a senior business intelligence analyst preparing an executive briefing.

Below is a KPI summary extracted from a business dataset:

{kpi_summary}

Write a concise, professional executive insight report with exactly THREE sections:

**PERFORMANCE SUMMARY**
A 3–4 sentence overview of overall business performance. Be specific about numbers where available. Explain what the data reveals about the business trajectory.

**KEY RISKS & OPPORTUNITIES**
Identify 2–3 risks and 2–3 opportunities evident from the data. Be specific and business-minded. Use bullet points (•).

**RECOMMENDED EXECUTIVE ACTIONS**
Provide 3–4 concrete, prioritized actions an executive should consider. Reference specific KPIs. Use bullet points (•).

Keep the tone authoritative, succinct, and decision-oriented. Avoid generic platitudes. Respond ONLY with the three sections above."""

    response = model.generate_content(prompt)
    return response.text


# ── Charts ────────────────────────────────────────────────────────────────────
def chart_revenue_over_time(df, m):
    date_col = m.get("date")
    rev_col  = m.get("revenue") or m.get("actual_rev")
    if not date_col or not rev_col:
        return None
    tmp = df.dropna(subset=[date_col, rev_col]).copy()
    tmp["__month"] = tmp[date_col].dt.to_period("M").dt.to_timestamp()
    agg = tmp.groupby("__month")[rev_col].sum().reset_index()
    agg.columns = ["Month", "Revenue"]
    fig = px.area(agg, x="Month", y="Revenue",
                  color_discrete_sequence=[CHART_COLORS[0]])
    fig.update_traces(line_color=CHART_COLORS[0], fillcolor="rgba(200,169,110,0.12)")
    apply_layout(fig, title="Revenue Over Time")
    return fig


def chart_revenue_by_region(df, m):
    region_col = m.get("region")
    rev_col    = m.get("revenue") or m.get("actual_rev")
    if not region_col or not rev_col:
        return None
    agg = df.groupby(region_col)[rev_col].sum().reset_index().sort_values(rev_col, ascending=True)
    fig = px.bar(agg, x=rev_col, y=region_col, orientation="h",
                 color_discrete_sequence=[CHART_COLORS[1]])
    apply_layout(fig, title="Revenue by Region")
    return fig


def chart_revenue_by_channel(df, m):
    channel_col = m.get("channel")
    rev_col     = m.get("revenue") or m.get("actual_rev")
    if not channel_col or not rev_col:
        return None
    agg = df.groupby(channel_col)[rev_col].sum().reset_index()
    fig = px.pie(agg, names=channel_col, values=rev_col,
                 color_discrete_sequence=CHART_COLORS,
                 hole=0.5)
    fig.update_traces(textfont_family="DM Mono", textfont_size=11)
    apply_layout(fig, title="Revenue by Channel")
    return fig


def chart_profit_by_category(df, m):
    cat_col    = m.get("category") or m.get("segment")
    profit_col = m.get("profit")
    if not cat_col or not profit_col:
        return None
    agg = df.groupby(cat_col)[profit_col].sum().reset_index().sort_values(profit_col, ascending=False)
    fig = px.bar(agg, x=cat_col, y=profit_col,
                 color_discrete_sequence=[CHART_COLORS[2]])
    apply_layout(fig, title="Profit by Category")
    return fig


def chart_revenue_vs_budget(df, m):
    brev_col = m.get("budget_rev")
    arev_col = m.get("actual_rev")
    date_col = m.get("date")
    if not brev_col or not arev_col or not date_col:
        return None
    tmp = df.dropna(subset=[date_col]).copy()
    tmp["__month"] = tmp[date_col].dt.to_period("M").dt.to_timestamp()
    agg = tmp.groupby("__month")[[brev_col, arev_col]].sum().reset_index()
    agg.columns = ["Month", "Budget", "Actual"]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=agg["Month"], y=agg["Budget"], name="Budget",
                         marker_color="rgba(200,169,110,0.3)",
                         marker_line_color=CHART_COLORS[0],
                         marker_line_width=1.5))
    fig.add_trace(go.Bar(x=agg["Month"], y=agg["Actual"], name="Actual",
                         marker_color=CHART_COLORS[1]))
    apply_layout(fig, title="Actual vs Budgeted Revenue", barmode="group")
    return fig


def chart_churn_by_segment(df, m):
    churn_col   = m.get("churn")
    segment_col = m.get("segment") or m.get("region")
    if not churn_col or not segment_col:
        return None
    tmp = df.copy()
    tmp["__churned"] = tmp[churn_col].astype(str).str.strip().str.lower().isin(["yes", "1", "true", "churned"]).astype(int)
    agg = tmp.groupby(segment_col)["__churned"].agg(["sum", "count"]).reset_index()
    agg.columns = [segment_col, "Churned", "Total"]
    agg["Churn Rate %"] = (agg["Churned"] / agg["Total"] * 100).round(1)
    fig = px.bar(agg, x=segment_col, y="Churn Rate %",
                 color="Churn Rate %",
                 color_continuous_scale=["#4A7C59", "#C8A96E", "#B85450"])
    apply_layout(fig, title="Churn Rate by Segment")
    return fig


def chart_sentiment(df, m):
    sent_col   = m.get("sentiment")
    date_col   = m.get("date")
    if not sent_col:
        return None
    if date_col:
        tmp = df.dropna(subset=[date_col, sent_col]).copy()
        tmp["__month"] = tmp[date_col].dt.to_period("M").dt.to_timestamp()
        agg = tmp.groupby("__month")[sent_col].mean().reset_index()
        agg.columns = ["Month", "Avg Sentiment"]
        fig = px.line(agg, x="Month", y="Avg Sentiment",
                      color_discrete_sequence=[CHART_COLORS[4]])
        fig.add_hline(y=0, line_dash="dash", line_color="#DDD9D0")
        apply_layout(fig, title="Average Sentiment Over Time")
    else:
        fig = px.histogram(df, x=sent_col, nbins=30,
                           color_discrete_sequence=[CHART_COLORS[4]])
        apply_layout(fig, title="Sentiment Score Distribution")
    return fig


def chart_revenue_by_segment(df, m):
    seg_col = m.get("segment")
    rev_col = m.get("revenue") or m.get("actual_rev")
    if not seg_col or not rev_col:
        return None
    agg = df.groupby(seg_col)[rev_col].sum().reset_index().sort_values(rev_col, ascending=False)
    fig = px.bar(agg, x=seg_col, y=rev_col, color=seg_col,
                 color_discrete_sequence=CHART_COLORS)
    apply_layout(fig, title="Revenue by Customer Segment", showlegend=False)
    return fig


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ◈ AURORA")
    st.markdown("<div style='font-family:DM Mono;font-size:0.65rem;letter-spacing:0.1em;color:#4A5568;margin-bottom:24px'>EXECUTIVE INTELLIGENCE PLATFORM</div>", unsafe_allow_html=True)

    st.markdown("### Upload Dataset")
    uploaded_file = st.file_uploader(
        "Drop a CSV, Excel, or JSON file",
        type=["csv", "xlsx", "xls", "json"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### AI Insights")
    api_key = st.text_input("Google Gemini API Key", type="password",
                            placeholder="AIza…",
                            help="Your key is never stored or logged.")

    st.markdown("---")
    st.markdown("### Filters")
    filter_state = {}


# ── MAIN ──────────────────────────────────────────────────────────────────────
if uploaded_file is None:
    st.markdown("""
    <div style='padding: 48px 0 20px 0'>
        <div class='dash-title'>Executive Intelligence<br>Dashboard</div>
        <div class='dash-subtitle'>Upload your dataset to begin · AI-powered insights on demand</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='upload-hero'>
        <div class='upload-icon'>◈</div>
        <div class='upload-title'>Drop your dataset here</div>
        <div class='upload-hint' style='margin-bottom:12px'>CSV · XLSX · JSON</div>
        <div style='font-size:0.8rem;color:#9AA5B4;max-width:360px;margin:0 auto;line-height:1.6'>
            The dashboard auto-detects your columns and maps them to KPIs. 
            Any business dataset works — sales, operations, finance, CRM.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class='kpi-card'>
            <div class='kpi-label'>Revenue & Profit</div>
            <div style='font-size:0.82rem;color:#7A8394;margin-top:6px;line-height:1.6'>
                Automatic KPI extraction, trend analysis, and budget variance tracking
            </div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='kpi-card'>
            <div class='kpi-label'>Region & Channel</div>
            <div style='font-size:0.82rem;color:#7A8394;margin-top:6px;line-height:1.6'>
                Performance breakdowns across geographies and distribution channels
            </div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class='kpi-card'>
            <div class='kpi-label'>AI Executive Brief</div>
            <div style='font-size:0.82rem;color:#7A8394;margin-top:6px;line-height:1.6'>
                One-click narrative summaries with risks, opportunities, and recommended actions
            </div>
        </div>""", unsafe_allow_html=True)
    st.stop()


# ── Load & detect ─────────────────────────────────────────────────────────────
df_raw, mapping = load_data(uploaded_file)
if df_raw is None:
    st.stop()

# ── SIDEBAR FILTERS ───────────────────────────────────────────────────────────
df = df_raw.copy()

with st.sidebar:
    # Date range filter
    if mapping.get("date"):
        dc = mapping["date"]
        valid = df[dc].dropna()
        if len(valid):
            min_d = valid.min().date()
            max_d = valid.max().date()
            date_range = st.date_input("Date Range", value=(min_d, max_d),
                                       min_value=min_d, max_value=max_d)
            if len(date_range) == 2:
                df = df[(df[dc].dt.date >= date_range[0]) & (df[dc].dt.date <= date_range[1])]

    # Categorical filters
    for key, label in [("region","Region"), ("channel","Channel"), ("segment","Segment"), ("category","Category")]:
        col = mapping.get(key)
        if col and col in df.columns:
            opts = sorted(df[col].dropna().unique().tolist())
            sel  = st.multiselect(label, opts, default=opts)
            if sel:
                df = df[df[col].isin(sel)]


# ── KPIs ──────────────────────────────────────────────────────────────────────
kpis = compute_kpis(df, mapping)

# ── Header ────────────────────────────────────────────────────────────────────
col_title, col_btn = st.columns([4, 1])
with col_title:
    st.markdown(f"""
    <div style='padding-bottom: 4px'>
        <div class='dash-title'>Executive Dashboard</div>
        <div class='dash-subtitle'>
            {uploaded_file.name.upper()} &nbsp;·&nbsp; 
            {len(df):,} ROWS &nbsp;·&nbsp;
            {kpis.get('date_from','—')} → {kpis.get('date_to','—')}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── KPI CARDS ─────────────────────────────────────────────────────────────────
st.markdown("<div class='section-header'>Key Performance Indicators</div>", unsafe_allow_html=True)

kpi_items = []

if kpis.get("total_revenue") is not None:
    kpi_items.append(("Total Revenue", fmt_currency(kpis["total_revenue"]), None, None))

if kpis.get("total_profit") is not None:
    kpi_items.append(("Total Profit", fmt_currency(kpis["total_profit"]), None, None))

if kpis.get("profit_margin") is not None:
    kpi_items.append(("Profit Margin", fmt_pct(kpis["profit_margin"]), None, None))

if kpis.get("rev_vs_budget_pct") is not None:
    v = kpis["rev_vs_budget_pct"]
    cls, txt = delta_class(v)
    kpi_items.append(("Revenue vs Budget", f"{'+' if v>0 else ''}{v:.1f}%", cls, txt))

if kpis.get("churn_rate") is not None:
    v = kpis["churn_rate"]
    kpi_items.append(("Churn Rate", fmt_pct(v), "neg" if v > 10 else "pos", f"{kpis['churn_count']:,} churned"))

if kpis.get("avg_sentiment") is not None:
    v = kpis["avg_sentiment"]
    kpi_items.append(("Avg Sentiment", f"{v:.2f}", "pos" if v > 0 else "neg", "positive" if v > 0 else "negative"))

if kpis.get("actual_rev") is not None and kpis.get("actual_exp") is not None:
    kpi_items.append(("Actual Revenue", fmt_currency(kpis["actual_rev"]), None, None))

# Render KPI cards in rows of 4
for i in range(0, len(kpi_items), 4):
    cols = st.columns(min(4, len(kpi_items) - i))
    for j, col in enumerate(cols):
        if i + j < len(kpi_items):
            label, val, cls, delta = kpi_items[i + j]
            delta_html = f"<div class='kpi-delta {cls or 'neu'}'>{delta}</div>" if delta else ""
            col.markdown(f"""
            <div class='kpi-card'>
                <div class='kpi-label'>{label}</div>
                <div class='kpi-value'>{val}</div>
                {delta_html}
            </div>
            """, unsafe_allow_html=True)


# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📈 Revenue & Profit", "🌍 Region & Channel", "👥 Customers", "🤖 AI Insights"])

with tab1:
    c1, c2 = st.columns([2, 1])
    with c1:
        fig = chart_revenue_over_time(df, mapping)
        if fig: st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with c2:
        fig = chart_profit_by_category(df, mapping)
        if fig: st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    fig = chart_revenue_vs_budget(df, mapping)
    if fig: st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


with tab2:
    c1, c2 = st.columns(2)
    with c1:
        fig = chart_revenue_by_region(df, mapping)
        if fig: st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    with c2:
        fig = chart_revenue_by_channel(df, mapping)
        if fig: st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


with tab3:
    c1, c2 = st.columns(2)
    with c1:
        fig = chart_churn_by_segment(df, mapping)
        if fig: st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    with c2:
        fig = chart_revenue_by_segment(df, mapping)
        if fig: st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    fig = chart_sentiment(df, mapping)
    if fig: st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


with tab4:
    st.markdown("<div class='section-header'>AI-Generated Executive Brief</div>", unsafe_allow_html=True)

    if not api_key:
        st.info("Enter your Google Gemini API key in the sidebar to generate AI insights.")
    else:
        if st.button("⚡ Generate Executive Insights"):
            with st.spinner("Analysing your data…"):
                try:
                    kpi_summary = build_kpi_summary(kpis, mapping, df)
                    insights = generate_ai_insights(kpi_summary, api_key)
                    st.session_state["insights"]    = insights
                    st.session_state["kpi_summary"] = kpi_summary
                except Exception as e:
                    st.error(f"AI generation failed: {e}")

        if "insights" in st.session_state:
            # Parse and display sections nicely
            raw = st.session_state["insights"]

            # Show KPI context used
            with st.expander("📊 Data context sent to AI"):
                st.code(st.session_state.get("kpi_summary", ""), language=None)

            # Render the insight panel
            # Split into sections for better rendering
            sections = []
            current_title = ""
            current_body  = []
            for line in raw.split("\n"):
                stripped = line.strip()
                if stripped.startswith("**") and stripped.endswith("**"):
                    if current_title:
                        sections.append((current_title, "\n".join(current_body).strip()))
                    current_title = stripped.strip("*").strip()
                    current_body  = []
                else:
                    current_body.append(line)
            if current_title:
                sections.append((current_title, "\n".join(current_body).strip()))

            if sections:
                inner_html = ""
                for title, body in sections:
                    body_html = body.replace("\n", "<br>")
                    inner_html += f"""
                    <div class='insight-section-title'>{title}</div>
                    <div class='insight-content'>{body_html}</div>
                    """
                st.markdown(f"""
                <div class='insight-panel'>
                    <div class='insight-tag'>◈ AURORA AI · GEMINI 2.5 FLASH</div>
                    {inner_html}
                </div>
                """, unsafe_allow_html=True)
            else:
                # Fallback: render raw
                st.markdown(f"""
                <div class='insight-panel'>
                    <div class='insight-tag'>◈ AURORA AI · GEMINI 2.5 FLASH</div>
                    <div class='insight-content'>{raw.replace(chr(10), '<br>')}</div>
                </div>
                """, unsafe_allow_html=True)

            st.caption("AI insights are powered by Gemini 2.5 Flash. Only aggregated KPI numbers are sent — no raw customer data.")

        elif api_key:
            st.markdown("""
            <div style='text-align:center;padding:60px 0;color:#9AA5B4;font-family:DM Mono;font-size:0.75rem;letter-spacing:0.1em'>
                CLICK GENERATE TO PRODUCE YOUR EXECUTIVE BRIEF
            </div>
            """, unsafe_allow_html=True)
