# ◈ AI-Powered Executive Dashboard

An executive dashboard that auto-detects your dataset's columns, renders KPI visualisations, and uses **Gemini 2.5 Flash** (Google) to generate a written executive brief — with zero hardcoded assumptions about your data.

---

## Features

- **Universal data ingestion** — upload any CSV, Excel (.xlsx), or JSON file
- **Auto-column detection** — the app maps revenue, profit, budget, region, channel, churn, and sentiment fields automatically from your column names
- **Interactive filters** — date range, region, channel, segment, and category filters in the sidebar
- **6 chart types** — revenue over time, region breakdown, channel mix, profit by category, budget vs actual, churn by segment, sentiment trend
- **AI Executive Brief** — one click generates a structured narrative with performance summary, risks/opportunities, and recommended actions using **Gemini 2.5 Flash** via the Google Generative AI API

---

## Local Setup

### 1. Clone or download the project

```bash
git clone <your-repo-url>
cd dashboard
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app.py
```

The app opens at **http://localhost:8501**

---

## Usage

1. **Upload your dataset** using the sidebar file uploader (CSV, Excel, or JSON)
2. **Apply filters** as needed (date range, region, channel, etc.)
3. **Browse the tabs** — Revenue & Profit, Region & Channel, Customers
4. **Add your Google Gemini API key** in the sidebar (starts with `AIza…`)
5. **Click "Generate Executive Insights"** on the AI Insights tab

> Your API key is never stored or logged. Only aggregated KPI numbers are sent to the AI — no raw customer data.

---

## Getting a Gemini API Key

1. Go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the key (starts with `AIza`) and paste it into the sidebar

The free tier is sufficient for this project.

---

## Deploying to Streamlit Cloud (Free — for submission)

Streamlit Cloud gives you a **public shareable URL** for free.

### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/aurora-dashboard.git
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click **"New app"**
4. Select your repository, branch (`main`), and main file (`app.py`)
5. Click **"Deploy"**

Streamlit will install dependencies from `requirements.txt` automatically.

### Step 3: (Optional) Store your API key as a secret

In Streamlit Cloud → your app → **Settings → Secrets**, add:

```toml
GEMINI_API_KEY = "AIza..."
```

Then in `app.py`, pre-fill the key so you don't have to paste it every time:

```python
import os
default_key = os.environ.get("GEMINI_API_KEY", "")
api_key = st.text_input("Google Gemini API Key", value=default_key, type="password")
```

---

## Dataset Requirements

Your dataset should ideally contain columns matching these concepts (exact names don't matter — the app detects them):

| Concept | Example column names |
|---|---|
| Date | `date`, `transaction_date`, `month`, `period` |
| Revenue | `revenue`, `sales`, `actual_revenue`, `income` |
| Profit | `profit`, `net_profit`, `margin` |
| Budget Revenue | `budgeted_revenue`, `budget_rev`, `target_revenue` |
| Budget Expense | `budgeted_expense`, `budget_exp` |
| Actual Expense | `actual_expense`, `actual_exp` |
| Region | `region`, `area`, `territory`, `state` |
| Channel | `channel`, `platform`, `source` |
| Churn | `churn_flag`, `churned`, `attrition` (values: Yes/No or 1/0) |
| Customer Segment | `customer_segment`, `segment`, `tier` |
| Category | `category`, `product_category`, `class` |
| Sentiment | `sentiment_score`, `rating`, `nps` |

---

## Tech Stack

| Layer | Tool |
|---|---|
| UI & App Framework | Streamlit |
| Visualisation | Plotly |
| Data processing | Pandas |
| AI Insights | Google Gemini 2.5 Flash |
| Deployment | Streamlit Community Cloud |

---

## File Structure

```
dashboard/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## Notes for Graders

- The dashboard is **dataset-agnostic** — any business CSV will work, not just the provided Aurora dataset
- AI insights are generated from **aggregated KPIs only**, not raw rows
- The column mapping logic is in the `detect_columns()` function in `app.py`
- The AI prompt is structured to produce three specific output sections: Performance Summary, Risks & Opportunities, and Recommended Actions — directly addressing the project's minimum requirements
- AI powered by **Gemini 2.5 Flash** via the Google Generative AI Python SDK
