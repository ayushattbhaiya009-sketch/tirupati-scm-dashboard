"""
Tirupati Medicare – SCM Order Analysis Dashboard
A production-ready Streamlit app for daily SCM order analysis.
Upgraded: Category Analytics, Multi-CSV, Overall Comparison
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SCM Dashboard – Tirupati Medicare",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* ── Global text contrast fixes ── */
/* Main app text */
.main .block-container { color: #0f172a; }
p, span, div, label, li { color: inherit; }

/* Ensure all Streamlit text elements are readable */
.stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown span { color: #0f172a !important; }
.stText { color: #0f172a !important; }
.stCaption, [data-testid="stCaptionContainer"] { color: #374151 !important; font-weight: 500; }
.stAlert p { color: inherit !important; }

/* Headings */
h1, h2, h3, h4, h5, h6 { color: #0f172a !important; font-weight: 700; }

/* Sidebar text – force dark text on light sidebar background */
[data-testid="stSidebar"] { background: #f8fafc; border-right: 1px solid #e2e8f0; }
[data-testid="stSidebar"] * { color: #0f172a !important; }
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] .stMarkdown { color: #0f172a !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #0f172a !important; font-weight: 700; }
[data-testid="stSidebar"] .stCaption { color: #374151 !important; }
[data-testid="stSidebar"] [data-testid="stWidgetLabel"],
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stRadio label,
[data-testid="stSidebar"] .stDateInput label { color: #0f172a !important; font-weight: 600; }

/* Tab labels */
.stTabs [data-baseweb="tab"] {
    font-size: 0.875rem;
    font-weight: 600;
    color: #1e293b !important;
}
.stTabs [data-baseweb="tab"][aria-selected="true"] { color: #0f172a !important; font-weight: 700; }
.stTabs [data-baseweb="tab-list"] { background: #f8fafc; border-radius: 10px; padding: 4px; }

/* Widget labels (filters, sliders, selectboxes) */
[data-testid="stWidgetLabel"],
.stSelectbox label, .stMultiSelect label,
.stRadio label, .stSlider label,
.stDateInput label, .stTextInput label { color: #0f172a !important; font-weight: 600; }

/* Radio button options */
.stRadio [data-testid="stMarkdownContainer"] p { color: #0f172a !important; font-weight: 500; }

/* Multiselect tags */
[data-baseweb="tag"] span { color: #1e293b !important; font-weight: 600; }

/* Selectbox and multiselect dropdown text */
[data-baseweb="select"] [data-testid="stMarkdownContainer"] p { color: #0f172a !important; }

/* Info / warning / success / error messages */
[data-testid="stAlert"] { }
[data-testid="stAlert"] p,
[data-testid="stAlert"] div { font-weight: 500; }
.stAlert [data-testid="stMarkdownContainer"] p { color: inherit !important; }

/* Download button */
.stDownloadButton button { color: #0f172a !important; font-weight: 600; }

/* Button */
.stButton button { color: #0f172a !important; font-weight: 600; }

/* Dataframe / table text */
[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }
[data-testid="stDataFrame"] td,
[data-testid="stDataFrame"] th { color: #0f172a !important; font-weight: 500; }
[data-testid="stDataFrame"] th { font-weight: 700 !important; background-color: #f1f5f9 !important; }

/* Metric container */
div[data-testid="metric-container"] {
    background: #fff;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 16px;
}
div[data-testid="metric-container"] label,
div[data-testid="metric-container"] [data-testid="stMetricLabel"] { color: #374151 !important; font-weight: 600; }
div[data-testid="metric-container"] [data-testid="stMetricValue"] { color: #0f172a !important; font-weight: 700; }
div[data-testid="metric-container"] [data-testid="stMetricDelta"] { font-weight: 600; }

/* KPI Cards – white background, dark text always */
.kpi-card {
    background: #ffffff;
    border: 1px solid #e8edf2;
    border-radius: 12px;
    padding: 20px 24px;
    text-align: center;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
}
.kpi-value { font-size: 2rem; font-weight: 700; color: #0f172a; line-height: 1; }
.kpi-label { font-size: 0.78rem; font-weight: 600; color: #374151; margin-top: 6px; text-transform: uppercase; letter-spacing: 0.05em; }
.kpi-delta { font-size: 0.82rem; margin-top: 4px; font-weight: 600; }
.kpi-good { color: #15803d; }
.kpi-bad  { color: #b91c1c; }
.kpi-warn { color: #b45309; }
.kpi-blue { border-top: 3px solid #3b82f6; }
.kpi-green{ border-top: 3px solid #22c55e; }
.kpi-red  { border-top: 3px solid #ef4444; }
.kpi-amber{ border-top: 3px solid #f59e0b; }
.kpi-purple{border-top: 3px solid #a855f7; }
.kpi-teal { border-top: 3px solid #14b8a6; }
.kpi-orange{border-top: 3px solid #f97316; }
.kpi-indigo{border-top: 3px solid #6366f1; }

/* Insight cards – light backgrounds with rich dark text */
.insight-card {
    background: #e0f2fe;
    border-left: 4px solid #0284c7;
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 10px;
    font-size: 0.875rem;
    color: #0c3d5e;
    font-weight: 500;
}
.insight-card.warn   { background: #fef3c7; border-left-color: #d97706; color: #6b3300; }
.insight-card.danger { background: #fee2e2; border-left-color: #dc2626; color: #7f1d1d; }
.insight-card.good   { background: #dcfce7; border-left-color: #16a34a; color: #14532d; }
.insight-card b, .insight-card strong { font-weight: 700; }

/* Section headers */
.section-title {
    font-size: 1.1rem; font-weight: 700; color: #0f172a;
    border-bottom: 2px solid #cbd5e1; padding-bottom: 8px;
    margin-bottom: 20px; margin-top: 10px;
}

/* Quality indicators */
.quality-warn { background: #fef3c7; border: 1px solid #f59e0b; border-radius: 8px; padding: 10px 14px; margin: 4px 0; font-size: 0.84rem; color: #6b3300; font-weight: 500; }
.quality-ok   { background: #dcfce7; border: 1px solid #4ade80; border-radius: 8px; padding: 10px 14px; margin: 4px 0; font-size: 0.84rem; color: #14532d; font-weight: 500; }

/* Category badge colors */
.cat-powder  { background: #dbeafe; color: #1d4ed8; border-radius: 6px; padding: 2px 8px; font-size: 0.78rem; font-weight: 700; }
.cat-tablets { background: #dcfce7; color: #15803d; border-radius: 6px; padding: 2px 8px; font-size: 0.78rem; font-weight: 700; }
.cat-liquid  { background: #fef3c7; color: #92400e; border-radius: 6px; padding: 2px 8px; font-size: 0.78rem; font-weight: 700; }
.cat-ayurveda{ background: #f3e8ff; color: #6b21a8; border-radius: 6px; padding: 2px 8px; font-size: 0.78rem; font-weight: 700; }
.cat-other   { background: #e2e8f0; color: #334155; border-radius: 6px; padding: 2px 8px; font-size: 0.78rem; font-weight: 700; }

/* Upload status */
.upload-success { background: #dcfce7; border: 1px solid #4ade80; border-radius: 8px; padding: 10px 14px; font-size: 0.84rem; color: #14532d; font-weight: 600; margin: 4px 0; }
.upload-error   { background: #fee2e2; border: 1px solid #fca5a5; border-radius: 8px; padding: 10px 14px; font-size: 0.84rem; color: #7f1d1d; font-weight: 600; margin: 4px 0; }

/* Spinner text */
[data-testid="stSpinner"] p { color: #0f172a !important; font-weight: 500; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════

# Target pharma categories for Tirupati Medicare
PHARMA_CATEGORIES = ["Powder", "Tablets", "Liquid", "Ayurveda"]

# Default product-to-category mapping (auto-detected by keywords)
DEFAULT_PRODUCT_CATEGORY_RULES = {
    "Powder":   ["powder", "granules", "sachet"],
    "Tablets":  ["tablet", "tab", "mg", "capsule", "cap", "pill"],
    "Liquid":   ["syrup", "suspension", "solution", "injection", "drops", "sucrose",
                 "glargine", "insulin", "liquid", "ml", "iv"],
    "Ayurveda": ["ayur", "herbal", "tulsi", "ashwagandha", "triphala", "neem",
                 "haritaki", "chyawan", "brahmi", "shatavar", "giloy"],
}

CORP_COLORS     = ["#3b82f6","#22c55e","#f59e0b","#ef4444","#a855f7","#14b8a6","#f97316","#6366f1"]
CATEGORY_COLORS = {"Powder": "#3b82f6", "Tablets": "#22c55e", "Liquid": "#f59e0b",
                   "Ayurveda": "#a855f7", "Other": "#94a3b8"}

# ══════════════════════════════════════════════════════════════════════════════
# COLUMN MAPPING ENGINE
# ══════════════════════════════════════════════════════════════════════════════

COLUMN_MAP = {
    "order_id":       ["order id", "order_id", "order no", "order number", "orderid", "orderno",
                        "order ref", "sales order", "so no", "so number", "reference", "ref no"],
    "client":         ["client", "customer", "party", "party name", "buyer", "account",
                        "customer name", "client name", "sold to", "ship to party"],
    "product":        ["product", "item", "sku", "material", "product name", "item name",
                        "description", "product description", "article", "goods"],
    "category":       ["category", "product category", "item category", "group", "product group",
                        "division", "segment"],
    "qty":            ["qty", "quantity", "units", "ordered qty", "order qty", "pieces",
                        "nos", "number", "count", "pcs"],
    "amount":         ["amount", "value", "total", "order value", "total value", "revenue",
                        "net amount", "net value", "invoice amount", "sales value", "price",
                        "total amount", "billing amount"],
    "inventory":      ["inventory", "stock", "stock qty", "available stock", "on hand",
                        "closing stock", "opening stock", "inventory level"],
    "order_date":     ["order date", "date", "created date", "booking date", "entry date",
                        "sales date", "po date", "creation date"],
    "dispatch_date":  ["dispatch date", "shipped date", "ship date", "delivery date",
                        "actual dispatch", "dispatched on", "shipping date", "shipment date"],
    "due_date":       ["due date", "expected date", "promise date", "required date",
                        "delivery due", "target date", "requested date"],
    "status":         ["status", "order status", "state", "stage", "order stage"],
    "city":           ["city", "location", "town", "place"],
    "region":         ["region", "territory", "zone", "area", "state", "district"],
    "salesperson":    ["salesperson", "sales rep", "executive", "sales executive", "rep",
                        "assigned to", "account manager", "se"],
    "remarks":        ["remarks", "notes", "comments", "reason", "note"],
}

STATUS_CATEGORIES = {
    "dispatched":  ["dispatched", "shipped", "delivered", "closed", "completed", "fulfilled", "done"],
    "pending":     ["pending", "open", "new", "created", "booked", "not started", "received"],
    "confirmed":   ["confirmed", "approved", "accepted", "processing", "in process", "in progress"],
    "partial":     ["partial", "partially dispatched", "partial delivery", "partially shipped",
                    "partially fulfilled", "part dispatch"],
    "cancelled":   ["cancelled", "canceled", "rejected", "closed-cancelled", "void", "voided"],
    "delayed":     ["delayed", "overdue", "late", "hold", "on hold", "stuck", "backorder"],
}


def normalize_colname(col: str) -> str:
    return col.strip().lower().replace("_", " ").replace("-", " ")


def map_columns(df: pd.DataFrame) -> tuple:
    """Auto-map raw column names to standard schema. Returns (df_mapped, mapping_used, warnings)."""
    col_lower = {normalize_colname(c): c for c in df.columns}
    mapping = {}
    warnings_list = []

    for std_name, variants in COLUMN_MAP.items():
        for v in variants:
            if v in col_lower:
                mapping[std_name] = col_lower[v]
                break

    rename_dict = {v: k for k, v in mapping.items()}
    df_out = df.rename(columns=rename_dict)

    mapped_originals = set(mapping.values())
    for c in df.columns:
        if c not in mapped_originals:
            df_out.rename(columns={c: c}, inplace=True)

    for must in ["order_id", "client", "product", "qty", "amount", "order_date", "status"]:
        if must not in df_out.columns:
            warnings_list.append(f"⚠ Column '{must}' not found — related metrics will be skipped.")

    return df_out, mapping, warnings_list


@st.cache_data(show_spinner=False)
def clean_data(df: pd.DataFrame) -> tuple:
    """Clean and standardize data. Returns (cleaned_df, quality_notes)."""
    notes = []
    orig_len = len(df)

    df = df.dropna(how="all")

    if "order_id" in df.columns:
        before = len(df)
        df = df.drop_duplicates(subset=["order_id"], keep="first")
        dupes = before - len(df)
        if dupes:
            notes.append(f"Removed {dupes} duplicate Order IDs.")

    for dcol in ["order_date", "dispatch_date", "due_date"]:
        if dcol in df.columns:
            df[dcol] = pd.to_datetime(df[dcol], dayfirst=True, errors="coerce")
            bad = df[dcol].isna().sum()
            if bad:
                notes.append(f"{bad} rows in '{dcol}' could not be parsed as dates.")

    for ncol in ["qty", "amount", "inventory"]:
        if ncol in df.columns:
            df[ncol] = pd.to_numeric(
                df[ncol].astype(str).str.replace(",", "").str.replace("₹", "").str.strip(),
                errors="coerce"
            )
            bad = df[ncol].isna().sum()
            if bad:
                notes.append(f"{bad} rows in '{ncol}' could not be parsed as numbers.")

    if "status" in df.columns:
        df["status_raw"] = df["status"].copy()
        df["status"] = df["status"].astype(str).str.strip().str.lower()
        def map_status(s):
            for cat, variants in STATUS_CATEGORIES.items():
                if any(v in s for v in variants):
                    return cat
            return s
        df["status_std"] = df["status"].apply(map_status)
    else:
        df["status_std"] = "unknown"

    if "dispatch_date" in df.columns and "due_date" in df.columns:
        df["delay_days"] = (df["dispatch_date"] - df["due_date"]).dt.days
        df["is_delayed"] = df["delay_days"] > 0
    elif "order_date" in df.columns:
        today = pd.Timestamp.today()
        if "status_std" in df.columns:
            df["is_delayed"] = (
                (df["status_std"].isin(["pending", "confirmed", "partial"])) &
                (today - df["order_date"]).dt.days > 7
            )
        else:
            df["is_delayed"] = False
    else:
        df["is_delayed"] = False

    if "order_date" in df.columns:
        today = pd.Timestamp.today()
        df["order_age_days"] = (today - df["order_date"]).dt.days.clip(lower=0)
        df["order_month"] = df["order_date"].dt.to_period("M").astype(str)
        df["order_week"]  = df["order_date"].dt.to_period("W").astype(str)
        df["order_day"]   = df["order_date"].dt.date

    total_rows = len(df)
    blank_amounts = df["amount"].isna().sum() if "amount" in df.columns else 0
    if blank_amounts:
        notes.append(f"{blank_amounts}/{total_rows} rows have missing 'amount' values.")

    blank_clients = df["client"].isna().sum() if "client" in df.columns else 0
    if blank_clients:
        notes.append(f"{blank_clients}/{total_rows} rows have missing 'client' values.")

    removed = orig_len - total_rows
    if removed:
        notes.append(f"{removed} fully blank rows removed.")

    return df, notes


# ══════════════════════════════════════════════════════════════════════════════
# CATEGORY CLASSIFICATION ENGINE (NEW)
# ══════════════════════════════════════════════════════════════════════════════

def auto_assign_pharma_category(product_name: str) -> str:
    """Auto-assign a product to Powder/Tablets/Liquid/Ayurveda based on name keywords."""
    name_lower = str(product_name).lower()
    # Check Liquid first (more specific keywords)
    for cat, keywords in DEFAULT_PRODUCT_CATEGORY_RULES.items():
        if any(kw in name_lower for kw in keywords):
            return cat
    return "Tablets"  # Default: most pharma products are tablets


def apply_pharma_categories(df: pd.DataFrame, custom_mapping: dict) -> pd.DataFrame:
    """
    Add 'pharma_category' column using:
    1. User-defined custom_mapping (product -> category)
    2. Auto-detection by product name keywords (vectorized)
    """
    df = df.copy()
    if "product" not in df.columns:
        df["pharma_category"] = "Tablets"
        return df

    products = df["product"].fillna("").astype(str)

    # Vectorized keyword detection: iterate categories in priority order
    result = pd.Series("Tablets", index=df.index)
    # Process in reverse priority so highest-priority overwrites last
    for cat in ["Ayurveda", "Tablets", "Powder", "Liquid"]:
        keywords = DEFAULT_PRODUCT_CATEGORY_RULES.get(cat, [])
        if keywords:
            pattern = "|".join(keywords)
            mask = products.str.lower().str.contains(pattern, na=False)
            result[mask] = cat

    # Apply custom mapping overrides (vectorized via map)
    if custom_mapping:
        override = df["product"].map(custom_mapping)
        result = result.where(override.isna(), override)

    df["pharma_category"] = result
    return df


# ══════════════════════════════════════════════════════════════════════════════
# MULTI-CSV MERGE ENGINE (NEW)
# ══════════════════════════════════════════════════════════════════════════════

def detect_merge_key(df1: pd.DataFrame, df2: pd.DataFrame):
    """Find best common column to merge on."""
    # Normalize columns for comparison
    norm1 = {normalize_colname(c): c for c in df1.columns}
    norm2 = {normalize_colname(c): c for c in df2.columns}
    common_norm = set(norm1.keys()) & set(norm2.keys())

    # Priority: order_id, product, client
    for preferred in ["order id", "order_id", "product", "client", "sku"]:
        if preferred in common_norm:
            return preferred, norm1[preferred], norm2[preferred]

    if common_norm:
        key = list(common_norm)[0]
        return key, norm1[key], norm2[key]
    return None, None, None


def normalize_merge_key(df: pd.DataFrame, key_col: str) -> pd.DataFrame:
    """Normalize a merge key column to string, stripped, lowercased to avoid type mismatches."""
    if key_col in df.columns:
        df = df.copy()
        df[key_col] = df[key_col].astype(str).str.strip().str.lower().replace("nan", pd.NA)
    return df


def merge_dataframes(df1: pd.DataFrame, df2: pd.DataFrame, merge_hint: str = "auto") -> tuple:
    """
    Safely merge two DataFrames. Returns (merged_df, merge_info, error_msg).

    Strategy:
    - If both files share the same schema (same or overlapping columns beyond the key),
      they are STACKED (pd.concat) — this is the case for "split exports" of the same data.
    - If the files have complementary/non-overlapping columns (e.g. orders + inventory),
      they are JOINED (pd.merge) on the common key.
    """
    try:
        key_norm, key1, key2 = detect_merge_key(df1, df2)
        if not key1:
            # No common key — do a concat (stack rows)
            merged = pd.concat([df1, df2], ignore_index=True)
            info = f"No common key found. Stacked {len(df1)} + {len(df2)} = {len(merged)} rows."
            return merged, info, None

        # Map to standard names first
        df1_m, _, _ = map_columns(df1)
        df2_m, _, _ = map_columns(df2)

        # Re-detect after mapping
        key_norm2, key1_mapped, key2_mapped = detect_merge_key(df1_m, df2_m)

        if key1_mapped and key2_mapped and key1_mapped == key2_mapped:
            # Normalize the merge key in both frames to avoid int/object mismatches
            df1_m = normalize_merge_key(df1_m, key1_mapped)
            df2_m = normalize_merge_key(df2_m, key1_mapped)

            # Determine whether files are same-schema (should concat) or
            # complementary-schema (should join).
            cols1 = set(df1_m.columns)
            cols2 = set(df2_m.columns)
            common_cols = cols1 & cols2
            # Non-key columns that are shared between both files
            shared_non_key = common_cols - {key1_mapped}
            # Non-key columns unique to each file
            unique_to_f2 = cols2 - cols1

            # If file2 has more unique (non-overlapping) columns than shared ones,
            # it's a complementary file → JOIN.
            # Otherwise (files mostly share the same columns) → CONCAT/STACK.
            if len(unique_to_f2) > len(shared_non_key):
                # Complementary schemas — join to widen the dataset
                merged = pd.merge(df1_m, df2_m, on=key1_mapped, how="outer", suffixes=("", "_file2"))
                info = f"Joined on '{key1_mapped}': {len(df1_m)} + {len(df2_m)} → {len(merged)} rows."
            else:
                # Same/similar schema — stack rows (concat)
                merged = pd.concat([df1_m, df2_m], ignore_index=True)
                info = f"Merged on '{key1_mapped}': {len(df1_m)} + {len(df2_m)} → {len(merged)} rows."
        else:
            merged = pd.concat([df1_m, df2_m], ignore_index=True)
            info = f"Stacked files: {len(df1_m)} + {len(df2_m)} = {len(merged)} rows."

        return merged, info, None
    except Exception as e:
        return df1, "", str(e)


def merge_all_files(raw_dfs: list, fnames: list) -> tuple:
    """
    Merge a list of DataFrames (1–5) intelligently.
    Returns (merged_df, merge_info_msg, error_msg).
    """
    if len(raw_dfs) == 0:
        return None, None, "No files provided."

    if len(raw_dfs) == 1:
        return raw_dfs[0], None, None

    # Incrementally merge: fold each subsequent file into the running result
    current, info_parts = raw_dfs[0], []
    for i in range(1, len(raw_dfs)):
        next_df = raw_dfs[i]
        merged, info, err = merge_dataframes(current, next_df)
        if err:
            merged = pd.concat([current, next_df], ignore_index=True)
            info = f"File {i+1} stacked (error: {err}): → {len(merged)} rows."
        info_parts.append(f"[+File {i+1}: {fnames[i]}] {info}")
        current = merged

    summary = f"{len(raw_dfs)} files merged → {len(current):,} total rows. " + " | ".join(info_parts)
    return current, summary, None


# ══════════════════════════════════════════════════════════════════════════════
# SAFE AGGREGATION HELPER
# ══════════════════════════════════════════════════════════════════════════════

def _first_col(df):
    """Return first non-index column name, safe for agg count."""
    return df.columns[0]

# ══════════════════════════════════════════════════════════════════════════════
# CHART HELPERS
# ══════════════════════════════════════════════════════════════════════════════

CORP_SEQ = px.colors.sequential.Blues

def corp_bar(df, x, y, title, color=None, orientation="v", text=None, height=360):
    fig = px.bar(df, x=x, y=y, title=title, color=color,
                  color_discrete_sequence=CORP_COLORS,
                  orientation=orientation, text=text, height=height)
    fig.update_layout(
        title_font_size=14, title_font_color="#0f172a",
        plot_bgcolor="#ffffff", paper_bgcolor="#ffffff",
        margin=dict(l=20, r=20, t=44, b=20),
        font=dict(family="Inter", color="#0f172a"),
        xaxis=dict(showgrid=False, color="#1e293b", tickfont=dict(color="#1e293b", size=12)),
        yaxis=dict(gridcolor="#e2e8f0", color="#1e293b", tickfont=dict(color="#1e293b", size=12)),
        showlegend=bool(color),
        legend=dict(font=dict(color="#0f172a", size=12)),
    )
    fig.update_traces(marker_line_width=0)
    return fig


def corp_line(df, x, y, title, color=None, height=320):
    fig = px.line(df, x=x, y=y, title=title, color=color,
                   color_discrete_sequence=CORP_COLORS, height=height, markers=True)
    fig.update_layout(
        title_font_size=14, title_font_color="#0f172a",
        plot_bgcolor="#ffffff", paper_bgcolor="#ffffff",
        margin=dict(l=20, r=20, t=44, b=20),
        font=dict(family="Inter", color="#0f172a"),
        xaxis=dict(showgrid=False, color="#1e293b", tickfont=dict(color="#1e293b", size=12)),
        yaxis=dict(gridcolor="#e2e8f0", color="#1e293b", tickfont=dict(color="#1e293b", size=12)),
        legend=dict(font=dict(color="#0f172a", size=12)),
    )
    return fig


def corp_donut(labels, values, title, height=340):
    fig = go.Figure(go.Pie(
        labels=labels, values=values, hole=0.55,
        marker_colors=CORP_COLORS, textinfo="percent+label",
        hovertemplate="%{label}: %{value} (%{percent})<extra></extra>",
        textfont=dict(color="#0f172a", size=12),
    ))
    fig.update_layout(
        title_text=title, title_font_size=14, title_font_color="#0f172a",
        paper_bgcolor="#ffffff", margin=dict(l=20, r=20, t=44, b=20),
        font=dict(family="Inter", color="#0f172a"), height=height,
        legend=dict(orientation="v", x=1.02, font=dict(color="#0f172a", size=12)),
    )
    return fig


def kpi_card(value, label, color_cls="kpi-blue", delta=None, delta_good=True):
    delta_html = ""
    if delta is not None:
        cls = "kpi-good" if delta_good else "kpi-bad"
        delta_html = f'<div class="kpi-delta {cls}">{delta}</div>'
    return f"""
    <div class="kpi-card {color_cls}">
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{label}</div>
        {delta_html}
    </div>
    """


def fmt_inr(val):
    if pd.isna(val): return "N/A"
    if val >= 1e7:  return f"₹{val/1e7:.2f}Cr"
    if val >= 1e5:  return f"₹{val/1e5:.2f}L"
    if val >= 1e3:  return f"₹{val/1e3:.1f}K"
    return f"₹{val:,.0f}"


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR – Upload & Filters
# ══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("## 💊 Tirupati Medicare")
    st.markdown("**SCM Order Dashboard**")
    st.markdown("---")

    # ── Multi-CSV Upload ──────────────────────────────────────────
    st.markdown("### 📂 Upload Order Data")
    st.caption("Upload 1–5 CSV/Excel files. Multiple files are auto-merged intelligently.")

    uploaded_files = st.file_uploader(
        "Drop CSV or Excel files here",
        type=["csv", "xlsx", "xls"],
        accept_multiple_files=True,
        help="Supports .csv, .xlsx, .xls. Upload up to 5 files for auto-merge.",
    )

    merge_info_msg = None

    if uploaded_files:
        if len(uploaded_files) > 5:
            st.warning("Only the first 5 files will be used.")
            uploaded_files = uploaded_files[:5]
        for i, uf in enumerate(uploaded_files):
            st.markdown(f'<div class="upload-success">✅ File {i+1}: {uf.name}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📈 Sales Order Data (Trends)")
    st.caption("Upload the Sales Order Excel/CSV for monthly trend analysis.")
    sales_file = st.file_uploader(
        "Sales order file (SO Date, Customer Name, Product Name, Sales Qty, Net Value)",
        type=["csv", "xlsx", "xls"],
        accept_multiple_files=False,
        key="sales_upload",
        help="Powers the Product Trends and Customer Trends tabs.",
    )

    st.markdown("---")
    st.markdown("### 🔧 Filters")
    filter_placeholder = st.empty()
    reset_btn = st.button("🔄 Reset All Filters", use_container_width=True)

    st.markdown("---")
    st.markdown("### 📊 View Mode")
    view_mode = st.radio("Select view", ["Summary", "Detailed"], index=0, horizontal=True)
    st.markdown("---")
    st.caption("Built for Tirupati Medicare SCM Team")


# ══════════════════════════════════════════════════════════════════════════════
# LOAD & PROCESS DATA
# ══════════════════════════════════════════════════════════════════════════════

@st.cache_data(show_spinner=False)
def load_file(file_bytes: bytes, fname: str):
    if fname.endswith(".csv"):
        try:
            return pd.read_csv(io.BytesIO(file_bytes), encoding="utf-8")
        except UnicodeDecodeError:
            return pd.read_csv(io.BytesIO(file_bytes), encoding="latin1")
    else:
        xf = pd.ExcelFile(io.BytesIO(file_bytes))
        sheets = xf.sheet_names
        chosen = sheets[0]  # Default to first sheet; sidebar select handled below
        return pd.read_excel(io.BytesIO(file_bytes), sheet_name=chosen)


@st.cache_data(show_spinner=False)
def load_sales_data(file_bytes: bytes, fname: str) -> pd.DataFrame:
    """Load and clean sales order data for trend analysis."""
    if fname.endswith(".csv"):
        try:
            raw = pd.read_csv(io.BytesIO(file_bytes), encoding="utf-8", low_memory=False)
        except UnicodeDecodeError:
            raw = pd.read_csv(io.BytesIO(file_bytes), encoding="latin1", low_memory=False)
    else:
        raw = pd.read_excel(io.BytesIO(file_bytes))

    # Normalize column names
    raw.columns = raw.columns.str.strip()

    # Map expected columns flexibly
    col_aliases = {
        "so_date":       ["SO Date", "SO First Date", "Order Date", "Date"],
        "customer":      ["Customer Name", "Customer", "Client", "Party Name"],
        "product":       ["Product Name", "Product", "Item", "Material"],
        "sales_qty":     ["Sales Qty", "Qty", "Quantity", "Ordered Qty"],
        "net_value":     ["Net Value", "Value", "Amount", "Net Amount", "Order Value"],
    }
    rename = {}
    for std, variants in col_aliases.items():
        for v in variants:
            if v in raw.columns:
                rename[v] = std
                break

    df = raw.rename(columns=rename)

    # Parse date
    if "so_date" in df.columns:
        df["so_date"] = pd.to_datetime(df["so_date"], dayfirst=True, errors="coerce")
        df["month_period"] = df["so_date"].dt.to_period("M")
        df["month_label"] = df["so_date"].dt.strftime("%b %Y")
        df["month_sort"] = df["so_date"].dt.to_period("M").astype(str)

    # Parse numeric — strip commas / currency
    for col in ["sales_qty", "net_value"]:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace(",", "").str.replace("₹", "").str.strip(),
                errors="coerce"
            )

    # Drop rows with no date, no customer, or no product
    for req in ["so_date", "customer", "product"]:
        if req in df.columns:
            df = df.dropna(subset=[req])

    return df


if not uploaded_files:
    st.markdown("""
    <div style="text-align:center; padding: 80px 20px 40px;">
        <div style="font-size:3rem;">💊</div>
        <h1 style="color:#0f172a; font-weight:700; margin-top:16px;">SCM Order Analysis Dashboard</h1>
        <p style="color:#1e293b; font-size:1.1rem; max-width:560px; margin:16px auto 0;">
            Upload your daily order export (CSV or Excel) using the sidebar to instantly
            generate a complete order analysis with KPIs, client insights, product performance,
            delay tracking, and category-wise analytics.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    for col, icon, title, desc in [
        (col1, "📊", "Automatic Analysis", "KPIs, charts, and trends from your file"),
        (col2, "🚨", "Exception Tracking", "Delayed, partial, and at-risk orders flagged"),
        (col3, "🗂", "Category Analytics", "Powder · Tablets · Liquid · Ayurveda breakdown"),
        (col4, "📂", "Multi-CSV Merge", "Upload up to 5 files — auto-merged on common keys"),
    ]:
        with col:
            st.markdown(f"""
            <div class="kpi-card" style="text-align:left; padding:24px;">
                <div style="font-size:1.8rem;">{icon}</div>
                <div style="font-weight:700; color:#0f172a; margin-top:8px;">{title}</div>
                <div style="color:#1e293b; font-size:0.875rem; margin-top:4px;">{desc}</div>
            </div>""", unsafe_allow_html=True)
    st.stop()


# ─── Load files ──────────────────────────────────────────────────────────────
with st.spinner("Loading and processing your data…"):
    # Cap at 5 files (already trimmed in sidebar, but guard here too)
    files_to_use = uploaded_files[:5]

    raw_dfs = []
    for uf in files_to_use:
        raw_dfs.append(load_file(uf.getvalue(), uf.name))

    fnames = [uf.name for uf in files_to_use]
    raw_df, merge_info_msg, merge_error = merge_all_files(raw_dfs, fnames)

    if merge_error:
        st.error(f"Merge error: {merge_error}. Using first file only.")
        raw_df = raw_dfs[0]

    df_mapped, col_mapping, map_warnings = map_columns(raw_df)

    # Safety: coalesce any _file2 suffixed columns back into their base columns.
    # This handles edge cases where the merge path produced split columns.
    for col in list(df_mapped.columns):
        if col.endswith("_file2"):
            base_col = col[:-6]  # strip "_file2"
            if base_col in df_mapped.columns:
                df_mapped[base_col] = df_mapped[base_col].combine_first(df_mapped[col])
                df_mapped.drop(columns=[col], inplace=True)
            else:
                df_mapped.rename(columns={col: base_col}, inplace=True)

    df, quality_notes = clean_data(df_mapped)

# Show merge info if applicable
if merge_info_msg:
    st.info(f"🔗 **Multi-file merge:** {merge_info_msg}")


# ══════════════════════════════════════════════════════════════════════════════
# CATEGORY MAPPING UI (NEW)
# ══════════════════════════════════════════════════════════════════════════════

# Build default auto-mapping for all products
if "product" in df.columns:
    all_products = sorted(df["product"].dropna().unique())
    # Initialize session state for custom mapping
    if "custom_cat_map" not in st.session_state:
        st.session_state.custom_cat_map = {
            p: auto_assign_pharma_category(p) for p in all_products
        }
    custom_cat_map = st.session_state.custom_cat_map
else:
    custom_cat_map = {}

# Apply pharma categories
df = apply_pharma_categories(df, custom_cat_map)


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR FILTERS (df is now available)
# ══════════════════════════════════════════════════════════════════════════════

with filter_placeholder.container():
    if "order_date" in df.columns:
        min_d = df["order_date"].min()
        max_d = df["order_date"].max()
        if pd.notna(min_d) and pd.notna(max_d):
            date_range = st.date_input(
                "Order Date Range",
                value=(min_d.date(), max_d.date()),
                min_value=min_d.date(), max_value=max_d.date(),
            )
        else:
            date_range = None
    else:
        date_range = None

    if "status_std" in df.columns:
        statuses = sorted(df["status_std"].dropna().unique())
        sel_status = st.multiselect("Order Status", statuses, default=statuses)
    else:
        sel_status = []

    if "client" in df.columns:
        clients = sorted(df["client"].dropna().unique())
        sel_clients = st.multiselect("Client", clients, default=[])
    else:
        sel_clients = []

    # Pharma category filter (NEW)
    pharma_cats = sorted(df["pharma_category"].dropna().unique()) if "pharma_category" in df.columns else []
    sel_pharma_cats = st.multiselect("Pharma Category", pharma_cats, default=pharma_cats)

    if "region" in df.columns:
        regions = sorted(df["region"].dropna().unique())
        sel_regions = st.multiselect("Region / Zone", regions, default=[])
    else:
        sel_regions = []


def apply_filters(df):
    dff = df.copy()
    if reset_btn:
        return dff
    if date_range and len(date_range) == 2 and "order_date" in dff.columns:
        s, e = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
        dff = dff[(dff["order_date"] >= s) & (dff["order_date"] <= e)]
    if sel_status and "status_std" in dff.columns:
        dff = dff[dff["status_std"].isin(sel_status)]
    if sel_clients and "client" in dff.columns:
        dff = dff[dff["client"].isin(sel_clients)]
    if sel_pharma_cats and "pharma_category" in dff.columns:
        dff = dff[dff["pharma_category"].isin(sel_pharma_cats)]
    if sel_regions and "region" in dff.columns:
        dff = dff[dff["region"].isin(sel_regions)]
    return dff


dff = apply_filters(df)

if len(dff) == 0:
    st.warning("⚠ No data matches the current filters. Please adjust the filters.")
    st.stop()


# ══════════════════════════════════════════════════════════════════════════════
# LOAD SALES ORDER DATA (for trend tabs)
# ══════════════════════════════════════════════════════════════════════════════

sales_df = None
if sales_file is not None:
    with st.spinner("Loading sales order data…"):
        sales_df = load_sales_data(sales_file.getvalue(), sales_file.name)



total_orders    = len(dff)
total_value     = dff["amount"].sum()       if "amount" in dff.columns else None
total_value     = total_value if (total_value is not None and not pd.isna(total_value) and total_value > 0) else None
unique_clients  = dff["client"].nunique()   if "client" in dff.columns else None
unique_products = dff["product"].nunique()  if "product" in dff.columns else None
total_inventory = dff["inventory"].sum()    if "inventory" in dff.columns else None

status_counts = dff["status_std"].value_counts() if "status_std" in dff.columns else pd.Series(dtype=int)
n_dispatched  = status_counts.get("dispatched", 0)
n_pending     = status_counts.get("pending", 0) + status_counts.get("confirmed", 0)
n_partial     = status_counts.get("partial", 0)
n_cancelled   = status_counts.get("cancelled", 0)
n_delayed     = dff["is_delayed"].sum() if "is_delayed" in dff.columns else 0

fill_rate    = round(n_dispatched / total_orders * 100, 1) if total_orders else 0
on_time_rate = round((n_dispatched - n_delayed) / max(n_dispatched, 1) * 100, 1) if n_dispatched else None


# ══════════════════════════════════════════════════════════════════════════════
# AUTO-GENERATED INSIGHTS
# ══════════════════════════════════════════════════════════════════════════════

def safe_idxmax(series):
    """Return idxmax safely; return None if series is empty or all-NaN."""
    s = series.dropna()
    if s.empty:
        return None
    return s.idxmax()


def safe_idxmin(series):
    """Return idxmin safely; return None if series is empty or all-NaN."""
    s = series.dropna()
    if s.empty:
        return None
    return s.idxmin()


def generate_insights(dff):
    insights = []

    try:
        if "client" in dff.columns and "amount" in dff.columns:
            cl_sum = dff.groupby("client")["amount"].sum()
            top_c = safe_idxmax(cl_sum)
            if top_c is not None:
                top_c_val = cl_sum[top_c]
                insights.append(("info", f"🏆 Top Client: <b>{top_c}</b> contributing {fmt_inr(top_c_val)} in order value."))
    except Exception:
        pass

    try:
        if "product" in dff.columns and "amount" in dff.columns:
            pr_sum = dff.groupby("product")["amount"].sum()
            top_p = safe_idxmax(pr_sum)
            if top_p is not None:
                insights.append(("info", f"📦 Highest Value Product: <b>{top_p}</b>"))
    except Exception:
        pass

    try:
        if n_delayed > 0:
            delay_pct = round(n_delayed / total_orders * 100, 1)
            cls = "danger" if delay_pct > 20 else "warn"
            insights.append((cls, f"⚠ <b>{n_delayed} orders ({delay_pct}%)</b> are delayed or at risk of delay."))
    except Exception:
        pass

    try:
        if n_pending > 0:
            pct = round(n_pending / total_orders * 100, 1)
            cls = "danger" if pct > 40 else "warn"
            insights.append((cls, f"🕐 <b>{n_pending} open orders ({pct}%)</b> are pending or awaiting dispatch."))
    except Exception:
        pass

    if n_partial > 0:
        insights.append(("warn", f"📊 <b>{n_partial} orders</b> are partially fulfilled — may need follow-up."))

    try:
        if "client" in dff.columns and total_value and total_value > 0:
            cl_sum2 = dff.groupby("client")["amount"].sum()
            if not cl_sum2.empty:
                top5_share = cl_sum2.nlargest(5).sum() / total_value * 100
                if top5_share > 70:
                    insights.append(("warn", f"⚡ High client concentration: Top 5 clients = {top5_share:.0f}% of order value."))
                else:
                    insights.append(("good", f"✅ Client portfolio well-distributed. Top 5 = {top5_share:.0f}% of value."))
    except Exception:
        pass

    try:
        if "order_age_days" in dff.columns and "status_std" in dff.columns:
            old = dff[(dff["status_std"].isin(["pending","confirmed"])) & (dff["order_age_days"] > 14)]
            if len(old):
                insights.append(("danger", f"🔴 <b>{len(old)} orders</b> have been open for more than 14 days."))
    except Exception:
        pass

    try:
        if fill_rate >= 80:
            insights.append(("good", f"✅ Fill rate is healthy at <b>{fill_rate}%</b>."))
        elif fill_rate >= 50:
            insights.append(("warn", f"⚠ Fill rate is moderate at <b>{fill_rate}%</b>. Review pending orders."))
        else:
            insights.append(("danger", f"🔴 Fill rate is low at <b>{fill_rate}%</b>. Significant pending backlog."))
    except Exception:
        pass

    try:
        if "pharma_category" in dff.columns and "amount" in dff.columns:
            cat_sum = dff.groupby("pharma_category")["amount"].sum()
            top_cat = safe_idxmax(cat_sum)
            if top_cat is not None:
                top_cat_val = cat_sum[top_cat]
                insights.append(("info", f"🏷 Highest Revenue Category: <b>{top_cat}</b> — {fmt_inr(top_cat_val)}"))
    except Exception:
        pass

    return insights


insights_list = generate_insights(dff)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN DASHBOARD TABS (9 tabs: 7 original + 2 new category tabs)
# ══════════════════════════════════════════════════════════════════════════════

st.markdown(
    f"### 📊 Order Analysis Dashboard &nbsp; "
    f"<span style='font-size:0.9rem; color:#374151; font-weight:500'>— {len(dff):,} orders loaded</span>",
    unsafe_allow_html=True
)

tab1, tab_cat_overview, tab_cat_detail, tab_prod_trends, tab_cust_trends, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🏠 Overview",
    "🗂 Category Comparison",
    "🔬 Category Analysis",
    "📈 Product Trends",       # NEW – monthly product value/volume bar charts
    "👤 Customer Trends",      # NEW – monthly customer value/volume bar charts
    "👥 Clients",
    "📦 Products",
    "🔄 Order Status",
    "⚠ Delays & Exceptions",
    "📋 Data Table",
    "🔍 Data Quality",
])


# ─────────────────────────────── TAB 1: OVERVIEW ─────────────────────────────
with tab1:
    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: st.markdown(kpi_card(f"{total_orders:,}", "Total Orders", "kpi-blue"), unsafe_allow_html=True)
    with c2: st.markdown(kpi_card(fmt_inr(total_value) if total_value else "N/A", "Total Order Value", "kpi-green"), unsafe_allow_html=True)
    with c3: st.markdown(kpi_card(f"{unique_clients:,}" if unique_clients else "N/A", "Unique Clients", "kpi-purple"), unsafe_allow_html=True)
    with c4: st.markdown(kpi_card(f"{unique_products:,}" if unique_products else "N/A", "Unique Products", "kpi-teal"), unsafe_allow_html=True)
    with c5: st.markdown(kpi_card(f"{fill_rate}%", "Fill Rate", "kpi-green" if fill_rate >= 80 else "kpi-amber"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: st.markdown(kpi_card(f"{n_dispatched:,}", "Dispatched", "kpi-green"), unsafe_allow_html=True)
    with c2: st.markdown(kpi_card(f"{n_pending:,}", "Pending / Open", "kpi-amber"), unsafe_allow_html=True)
    with c3: st.markdown(kpi_card(f"{n_partial:,}", "Partially Done", "kpi-blue"), unsafe_allow_html=True)
    with c4: st.markdown(kpi_card(f"{n_cancelled:,}", "Cancelled", "kpi-red"), unsafe_allow_html=True)
    with c5: st.markdown(kpi_card(f"{n_delayed:,}", "Delayed / At Risk", "kpi-red"), unsafe_allow_html=True)

    st.markdown("---")

    st.markdown('<div class="section-title">🤖 Auto-Generated Insights</div>', unsafe_allow_html=True)
    icols = st.columns(2)
    for i, (cls, text) in enumerate(insights_list):
        with icols[i % 2]:
            st.markdown(f'<div class="insight-card {cls}">{text}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-title">📈 Order Trends Over Time</div>', unsafe_allow_html=True)

    if "order_date" in dff.columns:
        granularity = st.radio("Trend Granularity", ["Daily", "Weekly", "Monthly"], index=2, horizontal=True)
        if granularity == "Daily":
            t_col = "order_day"
        elif granularity == "Weekly":
            t_col = "order_week"
        else:
            t_col = "order_month"

        if "amount" in dff.columns:
            trend = dff.groupby(t_col).size().reset_index(name="Orders")
            trend["Value"] = dff.groupby(t_col)["amount"].sum().values
        else:
            trend = dff.groupby(t_col).size().reset_index(name="Orders")
        trend = trend.sort_values(t_col)

        col_l, col_r = st.columns(2)
        with col_l:
            fig = corp_line(trend, t_col, "Orders", "Order Volume Trend")
            st.plotly_chart(fig, use_container_width=True)
        with col_r:
            if "Value" in trend.columns:
                fig2 = corp_line(trend, t_col, "Value", "Order Value Trend (₹)")
                st.plotly_chart(fig2, use_container_width=True)
            elif "status_std" in dff.columns:
                sc = dff.groupby(["order_month","status_std"]).size().reset_index(name="count")
                fig2 = corp_bar(sc, "order_month", "count", "Orders by Status (Monthly)", color="status_std")
                st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Upload data with 'Order Date' to view trends.")


# ─────────────────────── TAB: CATEGORY COMPARISON (NEW) ──────────────────────
with tab_cat_overview:
    st.markdown('<div class="section-title">🗂 Overall Category Comparison — Powder · Tablets · Liquid · Ayurveda</div>', unsafe_allow_html=True)

    if "pharma_category" not in dff.columns:
        st.warning("Pharma category column not found.")
    else:
        try:
            cat_grp = dff.groupby("pharma_category").size().reset_index(name="Total Orders")
            cat_grp = cat_grp.rename(columns={"pharma_category": "Category"})
            if "amount" in dff.columns:
                rev_s = dff.groupby("pharma_category")["amount"].sum().reset_index()
                rev_s.columns = ["Category", "Total Revenue"]
                cat_grp = cat_grp.merge(rev_s, on="Category", how="left")
            if "qty" in dff.columns:
                qty_s = dff.groupby("pharma_category")["qty"].sum().reset_index()
                qty_s.columns = ["Category", "Total Qty"]
                cat_grp = cat_grp.merge(qty_s, on="Category", how="left")
            if "inventory" in dff.columns:
                inv_s = dff.groupby("pharma_category")["inventory"].sum().reset_index()
                inv_s.columns = ["Category", "Total Inventory"]
                cat_grp = cat_grp.merge(inv_s, on="Category", how="left")
            if "product" in dff.columns:
                uprod_s = dff.groupby("pharma_category")["product"].nunique().reset_index()
                uprod_s.columns = ["Category", "Unique Products"]
                cat_grp = cat_grp.merge(uprod_s, on="Category", how="left")
        except Exception:
            cat_grp = pd.DataFrame(columns=["Category", "Total Orders"])

        total_rev = cat_grp["Total Revenue"].sum() if "Total Revenue" in cat_grp.columns else 1
        if total_rev == 0: total_rev = 1
        total_ord = max(cat_grp["Total Orders"].sum(), 1)
        if "Total Revenue" in cat_grp.columns:
            cat_grp["Revenue %"] = (cat_grp["Total Revenue"] / total_rev * 100).round(1)
        cat_grp["Order %"] = (cat_grp["Total Orders"] / total_ord * 100).round(1)

        # ── KPI Row per Category ──────────────────────────────────────────
        num_cats = len(cat_grp)
        kpi_cols = st.columns(max(num_cats, 4))
        color_classes = ["kpi-blue", "kpi-green", "kpi-amber", "kpi-purple", "kpi-teal"]
        for i, row in cat_grp.iterrows():
            idx = list(cat_grp.index).index(i)
            if idx < len(kpi_cols):
                with kpi_cols[idx]:
                    rev_str = fmt_inr(row["Total Revenue"]) if "Total Revenue" in row else "N/A"
                    st.markdown(kpi_card(
                        rev_str,
                        row["Category"],
                        color_classes[idx % len(color_classes)],
                        delta=f"{row['Order %']}% of orders",
                        delta_good=True
                    ), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Charts Row 1: Sales + Revenue ────────────────────────────────
        col_l, col_r = st.columns(2)
        with col_l:
            fig_ord = corp_bar(
                cat_grp, "Category", "Total Orders",
                "📦 Orders by Category",
                color="Category", height=380
            )
            fig_ord.update_traces(
                marker_color=[CATEGORY_COLORS.get(c, "#94a3b8") for c in cat_grp["Category"]],
                text=cat_grp["Total Orders"], textposition="outside"
            )
            st.plotly_chart(fig_ord, use_container_width=True)

        with col_r:
            if "Total Revenue" in cat_grp.columns:
                fig_rev = corp_bar(
                    cat_grp, "Category", "Total Revenue",
                    "💰 Revenue by Category",
                    color="Category", height=380
                )
                fig_rev.update_traces(
                    marker_color=[CATEGORY_COLORS.get(c, "#94a3b8") for c in cat_grp["Category"]],
                    text=[fmt_inr(v) for v in cat_grp["Total Revenue"]],
                    textposition="outside"
                )
                st.plotly_chart(fig_rev, use_container_width=True)

        # ── Charts Row 2: Donut + Ranking ─────────────────────────────────
        col_l, col_r = st.columns(2)
        with col_l:
            if "Total Revenue" in cat_grp.columns:
                fig_donut = corp_donut(
                    cat_grp["Category"], cat_grp["Total Revenue"],
                    "Category Revenue Contribution", height=380
                )
                fig_donut.update_traces(
                    marker=dict(colors=[CATEGORY_COLORS.get(c, "#94a3b8") for c in cat_grp["Category"]])
                )
                st.plotly_chart(fig_donut, use_container_width=True)

        with col_r:
            if "Total Revenue" in cat_grp.columns:
                rank_df = cat_grp.sort_values("Total Revenue", ascending=True)
                fig_rank = go.Figure(go.Bar(
                    x=rank_df["Total Revenue"],
                    y=rank_df["Category"],
                    orientation="h",
                    marker_color=[CATEGORY_COLORS.get(c, "#94a3b8") for c in rank_df["Category"]],
                    text=[fmt_inr(v) for v in rank_df["Total Revenue"]],
                    textposition="outside"
                ))
                fig_rank.update_layout(
                    title="🏆 Category Performance Ranking",
                    plot_bgcolor="#fff", paper_bgcolor="#fff",
                    font=dict(family="Inter", color="#0f172a"), height=380,
                    margin=dict(l=20, r=80, t=44, b=20),
                    xaxis=dict(showgrid=False, color="#1e293b"),
                    yaxis=dict(gridcolor="#e2e8f0", color="#1e293b"),
                )
                st.plotly_chart(fig_rank, use_container_width=True)

        # ── Inventory by Category (if available) ─────────────────────────
        if "Total Inventory" in cat_grp.columns and cat_grp["Total Inventory"].sum() > 0:
            st.markdown('<div class="section-title">📦 Inventory by Category</div>', unsafe_allow_html=True)
            fig_inv = corp_bar(cat_grp, "Category", "Total Inventory", "Inventory Levels by Category")
            fig_inv.update_traces(
                marker_color=[CATEGORY_COLORS.get(c, "#94a3b8") for c in cat_grp["Category"]],
                text=cat_grp["Total Inventory"].apply(lambda x: f"{x:,.0f}"),
                textposition="outside"
            )
            st.plotly_chart(fig_inv, use_container_width=True)

        # ── Trend by category over time ────────────────────────────────
        if "order_month" in dff.columns:
            st.markdown('<div class="section-title">📊 Monthly Revenue Growth by Category</div>', unsafe_allow_html=True)
            if "amount" in dff.columns:
                trend_cat = dff.groupby(["order_month","pharma_category"])["amount"].sum().reset_index()
                trend_cat.columns = ["Month", "Category", "Revenue"]
                trend_cat = trend_cat.sort_values("Month")
                n_months = trend_cat["Month"].nunique()
                n_cats   = trend_cat["Category"].nunique()
                # Use stacked bars when many months × categories would crowd grouped bars
                bar_mode = "group" if (n_months * n_cats) <= 24 else "stack"
                fig_trend = px.bar(
                    trend_cat, x="Month", y="Revenue", color="Category",
                    title="Monthly Revenue Growth by Category",
                    color_discrete_map=CATEGORY_COLORS,
                    barmode=bar_mode,
                    height=420,
                    text_auto=False,
                )
                fig_trend.update_traces(
                    textposition="outside" if bar_mode == "group" else "inside",
                    texttemplate="%{y:,.0f}",
                )
                fig_trend.update_layout(
                    plot_bgcolor="#fff", paper_bgcolor="#fff", font=dict(family="Inter", color="#0f172a"),
                    xaxis=dict(showgrid=False, tickangle=-30, color="#1e293b",
                               title=None, tickfont=dict(size=11)),
                    yaxis=dict(gridcolor="#e2e8f0", color="#1e293b",
                               title="Revenue (₹)", tickformat=",.0f"),
                    legend=dict(
                        title="Category", orientation="v",
                        x=1.02, y=1, bgcolor="rgba(255,255,255,0.85)",
                        bordercolor="#e2e8f0", borderwidth=1,
                        font=dict(size=12, color="#0f172a"),
                    ),
                    margin=dict(l=20, r=140, t=52, b=60),
                    bargap=0.18,
                    bargroupgap=0.06,
                )
                st.plotly_chart(fig_trend, use_container_width=True)

        # ── Summary Table ─────────────────────────────────────────────────
        st.markdown('<div class="section-title">📋 Category Summary Table</div>', unsafe_allow_html=True)
        display_cat = cat_grp.copy()
        if "Total Revenue" in display_cat.columns:
            display_cat["Total Revenue"] = display_cat["Total Revenue"].apply(fmt_inr)
        st.dataframe(display_cat, use_container_width=True, hide_index=True)

        # Export
        buf_cat = io.BytesIO()
        with pd.ExcelWriter(buf_cat, engine="openpyxl") as writer:
            cat_grp.to_excel(writer, index=False, sheet_name="Category Summary")
        st.download_button("⬇ Download Category Summary (Excel)", buf_cat.getvalue(),
                            "category_summary.xlsx",
                            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


# ─────────────────────── TAB: CATEGORY ANALYSIS (NEW) ────────────────────────
with tab_cat_detail:
    st.markdown('<div class="section-title">🔬 Category-Wise Deep Dive</div>', unsafe_allow_html=True)

    if "pharma_category" not in dff.columns:
        st.warning("Pharma category column not found.")
    else:
        available_cats = sorted(dff["pharma_category"].dropna().unique())

        col_sel, col_info = st.columns([1, 3])
        with col_sel:
            selected_cat = st.selectbox(
                "Select Category",
                available_cats,
                help="Drill into a specific pharma category"
            )
        with col_info:
            st.markdown(f"<br><span style='color:#1e293b;font-size:0.9rem;font-weight:500;'>Showing analysis for <b>{selected_cat}</b></span>", unsafe_allow_html=True)

        cat_df = dff[dff["pharma_category"] == selected_cat].copy()

        if cat_df.empty:
            st.warning(f"No data found for category: {selected_cat}")
        else:
            # KPI Row
            cat_orders    = len(cat_df)
            cat_revenue   = cat_df["amount"].sum()   if "amount" in cat_df.columns else None
            cat_qty       = cat_df["qty"].sum()       if "qty" in cat_df.columns else None
            cat_inventory = cat_df["inventory"].sum() if "inventory" in cat_df.columns else None
            cat_products  = cat_df["product"].nunique() if "product" in cat_df.columns else None
            cat_delayed   = cat_df["is_delayed"].sum() if "is_delayed" in cat_df.columns else 0
            cat_fill      = round(
                cat_df[cat_df["status_std"] == "dispatched"]["status_std"].count() / cat_orders * 100, 1
            ) if cat_orders else 0

            c1,c2,c3,c4 = st.columns(4)
            with c1: st.markdown(kpi_card(f"{cat_orders:,}", "Total Orders", "kpi-blue"), unsafe_allow_html=True)
            with c2: st.markdown(kpi_card(fmt_inr(cat_revenue) if cat_revenue else "N/A", "Total Revenue", "kpi-green"), unsafe_allow_html=True)
            with c3: st.markdown(kpi_card(f"{cat_products:,}" if cat_products else "N/A", "Products", "kpi-purple"), unsafe_allow_html=True)
            with c4: st.markdown(kpi_card(f"{cat_fill}%", "Fill Rate", "kpi-green" if cat_fill >= 80 else "kpi-amber"), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            c1,c2,c3 = st.columns(3)
            with c1: st.markdown(kpi_card(f"{int(cat_qty):,}" if cat_qty else "N/A", "Total Qty Ordered", "kpi-teal"), unsafe_allow_html=True)
            with c2: st.markdown(kpi_card(f"{cat_delayed:,}", "Delayed Orders", "kpi-red"), unsafe_allow_html=True)
            with c3: st.markdown(kpi_card(f"{int(cat_inventory):,}" if cat_inventory else "N/A", "Inventory Level", "kpi-indigo"), unsafe_allow_html=True)

            st.markdown("---")

            # ── Top 10 Products in Category ───────────────────────────────
            if "product" in cat_df.columns:
                col_l, col_r = st.columns(2)
                with col_l:
                    if "amount" in cat_df.columns:
                        top10 = cat_df.groupby("product")["amount"].sum().nlargest(10).reset_index()
                        top10.columns = ["Product", "Revenue"]
                        top10 = top10.sort_values("Revenue")
                        fig_top = go.Figure(go.Bar(
                            x=top10["Revenue"], y=top10["Product"],
                            orientation="h",
                            marker_color=CATEGORY_COLORS.get(selected_cat, "#3b82f6"),
                            text=[fmt_inr(v) for v in top10["Revenue"]],
                            textposition="outside"
                        ))
                        fig_top.update_layout(
                            title=f"Top 10 Products by Revenue",
                            plot_bgcolor="#fff", paper_bgcolor="#fff",
                            font=dict(family="Inter", color="#0f172a"), height=400,
                            margin=dict(l=20, r=80, t=44, b=20),
                            xaxis=dict(showgrid=False, color="#1e293b"), yaxis=dict(gridcolor="#e2e8f0", color="#1e293b"),
                        )
                        st.plotly_chart(fig_top, use_container_width=True)

                with col_r:
                    if "qty" in cat_df.columns:
                        top10q = cat_df.groupby("product")["qty"].sum().nlargest(10).reset_index()
                        top10q.columns = ["Product", "Qty"]
                        top10q = top10q.sort_values("Qty")
                        fig_topq = go.Figure(go.Bar(
                            x=top10q["Qty"], y=top10q["Product"],
                            orientation="h",
                            marker_color=CATEGORY_COLORS.get(selected_cat, "#3b82f6"),
                            text=top10q["Qty"].apply(lambda x: f"{x:,.0f}"),
                            textposition="outside"
                        ))
                        fig_topq.update_layout(
                            title="Top 10 Products by Quantity",
                            plot_bgcolor="#fff", paper_bgcolor="#fff",
                            font=dict(family="Inter", color="#0f172a"), height=400,
                            margin=dict(l=20, r=80, t=44, b=20),
                            xaxis=dict(showgrid=False, color="#1e293b"), yaxis=dict(gridcolor="#e2e8f0", color="#1e293b"),
                        )
                        st.plotly_chart(fig_topq, use_container_width=True)

            # ── Trends ───────────────────────────────────────────────────
            if "order_month" in cat_df.columns:
                st.markdown('<div class="section-title">📈 Sales & Revenue Trends</div>', unsafe_allow_html=True)
                col_l, col_r = st.columns(2)
                with col_l:
                    s_trend = cat_df.groupby("order_month").size().reset_index(name="Orders")
                    s_trend = s_trend.sort_values("order_month")
                    fig_st = corp_line(s_trend, "order_month", "Orders", f"{selected_cat} — Sales Trend")
                    fig_st.update_traces(line_color=CATEGORY_COLORS.get(selected_cat, "#3b82f6"),
                                          marker_color=CATEGORY_COLORS.get(selected_cat, "#3b82f6"))
                    st.plotly_chart(fig_st, use_container_width=True)
                with col_r:
                    if "amount" in cat_df.columns:
                        r_trend = cat_df.groupby("order_month")["amount"].sum().reset_index()
                        r_trend.columns = ["Month", "Revenue"]
                        r_trend = r_trend.sort_values("Month")
                        fig_rt = corp_line(r_trend, "Month", "Revenue", f"{selected_cat} — Revenue Trend")
                        fig_rt.update_traces(line_color=CATEGORY_COLORS.get(selected_cat, "#3b82f6"),
                                              marker_color=CATEGORY_COLORS.get(selected_cat, "#3b82f6"))
                        st.plotly_chart(fig_rt, use_container_width=True)

            # ── Product Performance Ranking ───────────────────────────────
            if "product" in cat_df.columns and "amount" in cat_df.columns:
                st.markdown('<div class="section-title">🏆 Product Performance Ranking</div>', unsafe_allow_html=True)
                try:
                    _perf_agg = {"Revenue": ("amount", "sum")}
                    if "qty" in cat_df.columns: _perf_agg["Qty"] = ("qty", "sum")
                    if "is_delayed" in cat_df.columns: _perf_agg["Delayed"] = ("is_delayed", "sum")
                    perf = cat_df.groupby("product").agg(**_perf_agg).reset_index()
                    size_s = cat_df.groupby("product").size().reindex(perf["product"])
                    perf["Orders"] = size_s.values
                    perf = perf.sort_values("Revenue", ascending=False)
                    perf["Revenue_fmt"] = perf["Revenue"].apply(fmt_inr)
                    perf["Rank"] = range(1, len(perf)+1)
                    display_p = perf[["Rank","product","Orders","Revenue_fmt"] +
                                      ([c for c in ["Qty","Delayed"] if c in perf.columns])].copy()
                    display_p.columns = ["Rank","Product","Orders","Revenue"] + \
                                          [c for c in ["Qty","Delayed"] if c in perf.columns]
                    st.dataframe(display_p, use_container_width=True, hide_index=True)
                except Exception:
                    st.info("Insufficient data for product performance ranking.")

            # ── Category Mapping Editor ───────────────────────────────────
            st.markdown("---")
            st.markdown('<div class="section-title">✏️ Edit Product → Category Mapping</div>', unsafe_allow_html=True)
            st.caption("Change the category assignment for individual products. Updates take effect immediately.")

            if "product" in dff.columns:
                all_prods = sorted(dff["product"].dropna().unique())
                edit_df = pd.DataFrame({
                    "Product": all_prods,
                    "Category": [st.session_state.custom_cat_map.get(p, "Tablets") for p in all_prods]
                })
                edited = st.data_editor(
                    edit_df,
                    column_config={
                        "Category": st.column_config.SelectboxColumn(
                            "Category",
                            options=PHARMA_CATEGORIES + ["Other"],
                            required=True
                        )
                    },
                    use_container_width=True,
                    hide_index=True,
                    key="cat_editor"
                )
                if st.button("💾 Apply Category Changes", type="primary"):
                    for _, row in edited.iterrows():
                        st.session_state.custom_cat_map[row["Product"]] = row["Category"]
                    st.success("✅ Category mapping updated! Data will refresh on next interaction.")
                    st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# SHARED HELPERS FOR SALES TREND TABS
# ═══════════════════════════════════════════════════════════════════════════════

def _sales_unavailable(reason: str = ""):
    st.info(
        f"📂 **Sales Order data not loaded.**{(' ' + reason) if reason else ''}\n\n"
        "Upload your sales order file using **📈 Sales Order Data (Trends)** in the sidebar.",
        icon="📂",
    )


def _sorted_months(df: pd.DataFrame) -> list:
    """Return chronologically sorted unique month labels."""
    month_map = df[["month_sort", "month_label"]].drop_duplicates().sort_values("month_sort")
    return month_map["month_label"].tolist(), month_map["month_sort"].tolist()


def _stacked_bar(pivot_df: pd.DataFrame, title: str, yaxis_title: str,
                  color_map: dict = None, height: int = 480) -> go.Figure:
    """
    Build a stacked bar chart from a pivot table (index=months, columns=entities).
    Months are already sorted at this point.
    """
    fig = go.Figure()
    colors = color_map or {}
    palette = CORP_COLORS * 10  # repeat palette to cover many series

    for i, col in enumerate(pivot_df.columns):
        fig.add_trace(go.Bar(
            name=col,
            x=pivot_df.index,
            y=pivot_df[col],
            marker_color=colors.get(col, palette[i % len(palette)]),
            hovertemplate=f"<b>{col}</b><br>Month: %{{x}}<br>{yaxis_title}: %{{y:,.0f}}<extra></extra>",
        ))

    fig.update_layout(
        title=dict(text=title, font=dict(size=14, color="#1e293b")),
        barmode="stack",
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        font=dict(family="Inter", color="#0f172a"),
        height=height,
        margin=dict(l=20, r=20, t=52, b=60),
        xaxis=dict(showgrid=False, color="#1e293b", tickangle=-30,
                   title=None, tickfont=dict(size=11)),
        yaxis=dict(gridcolor="#e2e8f0", color="#1e293b",
                   title=yaxis_title, tickformat=",.0f"),
        legend=dict(
            orientation="v", x=1.02, y=1,
            bgcolor="rgba(255,255,255,0.9)", bordercolor="#e2e8f0",
            borderwidth=1, font=dict(size=11, color="#0f172a"),
        ),
        bargap=0.15,
    )
    return fig


def _grouped_bar(long_df: pd.DataFrame, x_col: str, y_col: str,
                  color_col: str, title: str, yaxis_title: str,
                  height: int = 480) -> go.Figure:
    """Grouped bar chart from a long-format DataFrame."""
    entities = long_df[color_col].unique()
    palette = CORP_COLORS * 10
    fig = go.Figure()
    for i, ent in enumerate(entities):
        sub = long_df[long_df[color_col] == ent]
        fig.add_trace(go.Bar(
            name=ent,
            x=sub[x_col],
            y=sub[y_col],
            marker_color=palette[i % len(palette)],
            hovertemplate=f"<b>{ent}</b><br>Month: %{{x}}<br>{yaxis_title}: %{{y:,.0f}}<extra></extra>",
        ))
    fig.update_layout(
        title=dict(text=title, font=dict(size=14, color="#1e293b")),
        barmode="group",
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        font=dict(family="Inter", color="#0f172a"),
        height=height,
        margin=dict(l=20, r=20, t=52, b=60),
        xaxis=dict(showgrid=False, color="#1e293b", tickangle=-30,
                   title=None, tickfont=dict(size=11)),
        yaxis=dict(gridcolor="#e2e8f0", color="#1e293b",
                   title=yaxis_title, tickformat=",.0f"),
        legend=dict(
            orientation="v", x=1.02, y=1,
            bgcolor="rgba(255,255,255,0.9)", bordercolor="#e2e8f0",
            borderwidth=1, font=dict(size=11, color="#0f172a"),
        ),
        bargap=0.18,
        bargroupgap=0.06,
    )
    return fig


def _build_trend_pivot(df: pd.DataFrame, entity_col: str, metric_col: str,
                        top_entities: list) -> pd.DataFrame:
    """
    Build a month × entity pivot for trend charts.
    Filters to top_entities, fills missing months with 0, sorts months chronologically.
    """
    sub = df[df[entity_col].isin(top_entities)].copy()
    grp = sub.groupby(["month_label", "month_sort", entity_col])[metric_col].sum().reset_index()
    pivot = grp.pivot_table(index=["month_sort", "month_label"],
                             columns=entity_col, values=metric_col,
                             fill_value=0)
    pivot.index = pd.MultiIndex.from_tuples(pivot.index, names=["month_sort", "month_label"])
    pivot = pivot.sort_index(level="month_sort")
    # Use only the readable month label as index for display
    pivot.index = pivot.index.get_level_values("month_label")
    pivot.columns.name = None
    return pivot


# ─────────────────────── TAB: PRODUCT MONTHLY TRENDS (NEW) ───────────────────
with tab_prod_trends:
    st.markdown('<div class="section-title">📈 Product Trends — Management View</div>',
                unsafe_allow_html=True)

    if sales_df is None:
        _sales_unavailable()
    elif "product" not in sales_df.columns or "month_label" not in sales_df.columns:
        st.error("Sales data is missing required columns (Product Name, SO Date).")
    else:
        sdf = sales_df.copy()
        TOP_N = 5  # Show only Top 5 for clean management view

        # ── Executive KPIs ────────────────────────────────────────────────
        ex1, ex2, ex3, ex4 = st.columns(4)

        if "net_value" in sdf.columns and not sdf.empty:
            prod_val_series = sdf.groupby("product")["net_value"].sum()
            top_prod_val     = prod_val_series.idxmax()
            top_prod_val_amt = prod_val_series.max()
            total_prod_value = prod_val_series.sum()
            top5_prod_share  = prod_val_series.nlargest(TOP_N).sum() / max(total_prod_value, 1) * 100
        else:
            top_prod_val = top_prod_val_amt = total_prod_value = top5_prod_share = None

        if "sales_qty" in sdf.columns and not sdf.empty:
            prod_vol_series = sdf.groupby("product")["sales_qty"].sum()
            top_prod_vol    = prod_vol_series.idxmax()
        else:
            top_prod_vol = None

        total_unique_products = sdf["product"].nunique() if not sdf.empty else 0

        with ex1:
            st.markdown(kpi_card(
                str(top_prod_val)[:26] + ("…" if top_prod_val and len(str(top_prod_val)) > 26 else "") if top_prod_val else "N/A",
                "Top Product by Value", "kpi-green",
                delta=fmt_inr(top_prod_val_amt) if top_prod_val_amt else None, delta_good=True
            ), unsafe_allow_html=True)
        with ex2:
            st.markdown(kpi_card(
                str(top_prod_vol)[:26] + ("…" if top_prod_vol and len(str(top_prod_vol)) > 26 else "") if top_prod_vol else "N/A",
                "Top Product by Volume", "kpi-blue"
            ), unsafe_allow_html=True)
        with ex3:
            st.markdown(kpi_card(
                f"{top5_prod_share:.0f}%" if top5_prod_share is not None else "N/A",
                "Top 5 Products Share", "kpi-purple"
            ), unsafe_allow_html=True)
        with ex4:
            st.markdown(kpi_card(
                f"{total_unique_products:,}",
                "Total Products", "kpi-teal"
            ), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Section 1: Top 5 by Value & Volume (horizontal bar charts) ───
        st.markdown('<div class="section-title">🏆 Top 5 Products — Value & Volume</div>',
                    unsafe_allow_html=True)
        col_l, col_r = st.columns(2)

        with col_l:
            if "net_value" in sdf.columns and not sdf.empty:
                top5_val = (
                    sdf.groupby("product")["net_value"].sum()
                    .nlargest(TOP_N).reset_index()
                )
                top5_val.columns = ["Product", "Total Value"]
                top5_val = top5_val.sort_values("Total Value", ascending=True)
                # Truncate long product names
                top5_val["Label"] = top5_val["Product"].str[:30]

                fig_t5v = go.Figure(go.Bar(
                    x=top5_val["Total Value"],
                    y=top5_val["Label"],
                    orientation="h",
                    marker_color=["#3b82f6"] * TOP_N,
                    text=[fmt_inr(v) for v in top5_val["Total Value"]],
                    textposition="outside",
                    hovertemplate="<b>%{y}</b><br>Value: ₹%{x:,.0f}<extra></extra>",
                ))
                fig_t5v.update_layout(
                    title="Top 5 Products by Total Value",
                    plot_bgcolor="#ffffff", paper_bgcolor="#ffffff",
                    font=dict(family="Inter", color="#0f172a"), height=360,
                    margin=dict(l=10, r=100, t=44, b=20),
                    xaxis=dict(showgrid=False, showticklabels=False, title=None),
                    yaxis=dict(gridcolor="#e2e8f0", color="#1e293b",
                               tickfont=dict(size=12, color="#0f172a"), title=None),
                    showlegend=False,
                )
                st.plotly_chart(fig_t5v, use_container_width=True)
            else:
                st.info("Net Value data not available.")

        with col_r:
            if "sales_qty" in sdf.columns and not sdf.empty:
                top5_vol = (
                    sdf.groupby("product")["sales_qty"].sum()
                    .nlargest(TOP_N).reset_index()
                )
                top5_vol.columns = ["Product", "Total Volume"]
                top5_vol = top5_vol.sort_values("Total Volume", ascending=True)
                top5_vol["Label"] = top5_vol["Product"].str[:30]

                fig_t5vol = go.Figure(go.Bar(
                    x=top5_vol["Total Volume"],
                    y=top5_vol["Label"],
                    orientation="h",
                    marker_color=["#22c55e"] * TOP_N,
                    text=[f"{v:,.0f}" for v in top5_vol["Total Volume"]],
                    textposition="outside",
                    hovertemplate="<b>%{y}</b><br>Volume: %{x:,.0f} units<extra></extra>",
                ))
                fig_t5vol.update_layout(
                    title="Top 5 Products by Total Volume (Units)",
                    plot_bgcolor="#ffffff", paper_bgcolor="#ffffff",
                    font=dict(family="Inter", color="#0f172a"), height=360,
                    margin=dict(l=10, r=80, t=44, b=20),
                    xaxis=dict(showgrid=False, showticklabels=False, title=None),
                    yaxis=dict(gridcolor="#e2e8f0", color="#1e293b",
                               tickfont=dict(size=12, color="#0f172a"), title=None),
                    showlegend=False,
                )
                st.plotly_chart(fig_t5vol, use_container_width=True)
            else:
                st.info("Sales Qty data not available.")

        st.markdown("---")

        # ── Section 2: Product Year-over-Year Monthly Comparison ─────────
        st.markdown('<div class="section-title">📅 Product Year-over-Year Monthly Trend</div>',
                    unsafe_allow_html=True)
        st.caption("Select a single product to compare its month-wise performance: Previous Year vs Current Year.")

        # Product selector — single product only
        _all_products_p = sorted(sdf["product"].dropna().unique().tolist())
        _selected_product = st.selectbox(
            "Select Product",
            _all_products_p,
            key="prod_yoy_select",
        )

        # Filter to selected product only
        sdf_prod = sdf[sdf["product"] == _selected_product].copy()

        # Determine years automatically from the selected product's data
        if "so_date" in sdf_prod.columns and not sdf_prod.empty:
            _years_p = sorted(sdf_prod["so_date"].dt.year.dropna().unique().astype(int))
        else:
            _years_p = []

        # Multi-year palette: green for earliest, blue for latest, others in between
        _YEAR_PALETTE = ["#22c55e", "#3b82f6", "#f59e0b", "#a855f7", "#ef4444", "#14b8a6", "#f97316", "#6366f1"]

        def _year_color(idx, total):
            """Assign color: first year=green, last year=blue, middle years from palette."""
            if total == 1:
                return "#3b82f6"
            if idx == 0:
                return "#22c55e"
            if idx == total - 1:
                return "#3b82f6"
            # Middle years cycle through remaining palette entries
            mid_palette = ["#f59e0b", "#a855f7", "#ef4444", "#14b8a6", "#f97316", "#6366f1"]
            return mid_palette[(idx - 1) % len(mid_palette)]

        # Helper: build multi-year month-vs-month grouped bar chart for a product
        def _build_intra_product_yoy_chart(metric_col, title, yaxis_title, fmt_fn=None):
            if metric_col not in sdf_prod.columns or sdf_prod.empty:
                return None

            sub = sdf_prod.copy()
            sub["year"] = sub["so_date"].dt.year
            sub["month_num"] = sub["so_date"].dt.month

            # All years present in this product's data
            all_years = sorted(sub["year"].dropna().unique().astype(int))
            if not all_years:
                return None

            grp = sub.groupby(["year", "month_num"])[metric_col].sum().reset_index()

            ALL_MONTHS_P = list(range(1, 13))
            _MONTH_ABBR = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
                           7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
            month_labels = [_MONTH_ABBR[m] for m in ALL_MONTHS_P]

            def _year_values(year):
                y_data = grp[grp["year"] == year].set_index("month_num")[metric_col]
                return [float(y_data.get(m, 0)) for m in ALL_MONTHS_P]

            fig_yoy_p = go.Figure()
            n_years = len(all_years)

            for idx, yr in enumerate(all_years):
                is_curr = (yr == all_years[-1])
                label = f"{yr} (Current Year)" if is_curr else (f"{yr} (Previous Year)" if n_years == 2 else str(yr))
                hover_tpl = (
                    f"<b>{_selected_product}</b><br>%{{x}} {yr}<br>"
                    + (f"Value: ₹%{{y:,.0f}}" if fmt_fn else f"Volume: %{{y:,.0f}} units")
                    + "<extra></extra>"
                )
                fig_yoy_p.add_trace(go.Bar(
                    name=label,
                    x=month_labels,
                    y=_year_values(yr),
                    marker_color=_year_color(idx, n_years),
                    opacity=0.88,
                    hovertemplate=hover_tpl,
                ))

            # Build legend hint string for x-axis title
            legend_hints = "  ".join(
                f"{'🟩' if idx==0 else ('🟦' if idx==n_years-1 else '🟨')} {yr}"
                for idx, yr in enumerate(all_years)
            )
            fig_yoy_p.update_layout(
                title=f"{title} — {_selected_product}",
                barmode="group",
                plot_bgcolor="#ffffff", paper_bgcolor="#ffffff",
                font=dict(family="Inter", color="#0f172a"), height=420,
                margin=dict(l=20, r=20, t=54, b=60),
                xaxis=dict(
                    showgrid=False, tickangle=0, color="#1e293b",
                    title=f"Month  |  {legend_hints}",
                    tickfont=dict(size=12, color="#0f172a"),
                    title_font=dict(size=11, color="#374151"),
                    categoryorder="array",
                    categoryarray=month_labels,
                ),
                yaxis=dict(
                    gridcolor="#e2e8f0", color="#1e293b",
                    title=yaxis_title, tickformat=",.0f",
                    tickfont=dict(size=12, color="#0f172a"),
                ),
                legend=dict(
                    orientation="h", x=0, y=1.08,
                    font=dict(size=11, color="#0f172a"),
                    bgcolor="rgba(255,255,255,0)",
                ),
                bargap=0.22, bargroupgap=0.06,
            )
            return fig_yoy_p

        if len(_years_p) >= 1 and "so_date" in sdf_prod.columns:
            trend_col_pl, trend_col_pr = st.columns(2)

            with trend_col_pl:
                fig_tpv = _build_intra_product_yoy_chart(
                    "net_value",
                    "Product Value Trend",
                    "Net Value (₹)", fmt_fn=True,
                )
                if fig_tpv:
                    st.plotly_chart(fig_tpv, use_container_width=True)
                else:
                    st.info("Net Value data not available.")

            with trend_col_pr:
                fig_tpvol = _build_intra_product_yoy_chart(
                    "sales_qty",
                    "Product Volume Trend",
                    "Sales Qty (Units)", fmt_fn=False,
                )
                if fig_tpvol:
                    st.plotly_chart(fig_tpvol, use_container_width=True)
                else:
                    st.info("Sales Qty data not available.")
        else:
            st.info("Insufficient data for year-over-year trend charts.")

        st.markdown("---")

        # ── Section 3: Product Summary Table (Top 20) ─────────────────────
        st.markdown('<div class="section-title">📋 Product Summary — Top 20</div>',
                    unsafe_allow_html=True)
        _agg_p = {}
        if "net_value" in sdf.columns:  _agg_p["Total Value"]  = ("net_value",  "sum")
        if "sales_qty" in sdf.columns:  _agg_p["Total Volume"] = ("sales_qty",  "sum")
        if _agg_p:
            prod_summary = sdf.groupby("product").agg(**_agg_p).reset_index()
            prod_summary = prod_summary.sort_values(
                "Total Value" if "Total Value" in prod_summary.columns else prod_summary.columns[-1],
                ascending=False
            ).head(20)
            if "Total Value" in prod_summary.columns:
                prod_summary["Total Value (₹)"] = prod_summary["Total Value"].apply(fmt_inr)
                prod_summary = prod_summary.drop(columns=["Total Value"])
            prod_summary = prod_summary.rename(columns={"product": "Product"})
            prod_summary.insert(0, "Rank", range(1, len(prod_summary) + 1))
            st.dataframe(prod_summary, use_container_width=True, hide_index=True)


# ─────────────────────── TAB: CUSTOMER MONTHLY TRENDS (NEW) ──────────────────
with tab_cust_trends:
    st.markdown('<div class="section-title">👤 Customer Trends — Management View</div>',
                unsafe_allow_html=True)

    if sales_df is None:
        _sales_unavailable()
    elif "customer" not in sales_df.columns or "month_label" not in sales_df.columns:
        st.error("Sales data is missing required columns (Customer Name, SO Date).")
    else:
        sdf_c = sales_df.copy()
        TOP_NC = 5  # Show only Top 5 for clean management view

        # ── Executive KPIs ────────────────────────────────────────────────
        cx1, cx2, cx3, cx4 = st.columns(4)

        if "net_value" in sdf_c.columns and not sdf_c.empty:
            cust_val_series  = sdf_c.groupby("customer")["net_value"].sum()
            top_cust_val     = cust_val_series.idxmax()
            top_cust_val_amt = cust_val_series.max()
            total_cust_value = cust_val_series.sum()
            top5_cust_share  = cust_val_series.nlargest(TOP_NC).sum() / max(total_cust_value, 1) * 100
        else:
            top_cust_val = top_cust_val_amt = total_cust_value = top5_cust_share = None

        if "sales_qty" in sdf_c.columns and not sdf_c.empty:
            cust_vol_series = sdf_c.groupby("customer")["sales_qty"].sum()
            top_cust_vol    = cust_vol_series.idxmax()
        else:
            top_cust_vol = None

        total_unique_customers = sdf_c["customer"].nunique() if not sdf_c.empty else 0

        with cx1:
            st.markdown(kpi_card(
                str(top_cust_val)[:26] + ("…" if top_cust_val and len(str(top_cust_val)) > 26 else "") if top_cust_val else "N/A",
                "Top Customer by Value", "kpi-green",
                delta=fmt_inr(top_cust_val_amt) if top_cust_val_amt else None, delta_good=True
            ), unsafe_allow_html=True)
        with cx2:
            st.markdown(kpi_card(
                str(top_cust_vol)[:26] + ("…" if top_cust_vol and len(str(top_cust_vol)) > 26 else "") if top_cust_vol else "N/A",
                "Top Customer by Volume", "kpi-blue"
            ), unsafe_allow_html=True)
        with cx3:
            st.markdown(kpi_card(
                f"{top5_cust_share:.0f}%" if top5_cust_share is not None else "N/A",
                "Top 5 Customers Share", "kpi-purple"
            ), unsafe_allow_html=True)
        with cx4:
            st.markdown(kpi_card(
                f"{total_unique_customers:,}",
                "Total Customers", "kpi-teal"
            ), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Section 1: Top 5 by Value & Volume (horizontal bar charts) ───
        st.markdown('<div class="section-title">🏆 Top 5 Customers — Value & Volume</div>',
                    unsafe_allow_html=True)
        col_cl, col_cr = st.columns(2)

        with col_cl:
            if "net_value" in sdf_c.columns and not sdf_c.empty:
                top5c_val = (
                    sdf_c.groupby("customer")["net_value"].sum()
                    .nlargest(TOP_NC).reset_index()
                )
                top5c_val.columns = ["Customer", "Total Value"]
                top5c_val = top5c_val.sort_values("Total Value", ascending=True)
                top5c_val["Label"] = top5c_val["Customer"].str[:30]

                fig_t5cv = go.Figure(go.Bar(
                    x=top5c_val["Total Value"],
                    y=top5c_val["Label"],
                    orientation="h",
                    marker_color=["#3b82f6"] * TOP_NC,
                    text=[fmt_inr(v) for v in top5c_val["Total Value"]],
                    textposition="outside",
                    hovertemplate="<b>%{y}</b><br>Value: ₹%{x:,.0f}<extra></extra>",
                ))
                fig_t5cv.update_layout(
                    title="Top 5 Customers by Total Value",
                    plot_bgcolor="#ffffff", paper_bgcolor="#ffffff",
                    font=dict(family="Inter", color="#0f172a"), height=360,
                    margin=dict(l=10, r=100, t=44, b=20),
                    xaxis=dict(showgrid=False, showticklabels=False, title=None),
                    yaxis=dict(gridcolor="#e2e8f0", color="#1e293b",
                               tickfont=dict(size=12, color="#0f172a"), title=None),
                    showlegend=False,
                )
                st.plotly_chart(fig_t5cv, use_container_width=True)
            else:
                st.info("Net Value data not available.")

        with col_cr:
            if "sales_qty" in sdf_c.columns and not sdf_c.empty:
                top5c_vol = (
                    sdf_c.groupby("customer")["sales_qty"].sum()
                    .nlargest(TOP_NC).reset_index()
                )
                top5c_vol.columns = ["Customer", "Total Volume"]
                top5c_vol = top5c_vol.sort_values("Total Volume", ascending=True)
                top5c_vol["Label"] = top5c_vol["Customer"].str[:30]

                fig_t5cvol = go.Figure(go.Bar(
                    x=top5c_vol["Total Volume"],
                    y=top5c_vol["Label"],
                    orientation="h",
                    marker_color=["#22c55e"] * TOP_NC,
                    text=[f"{v:,.0f}" for v in top5c_vol["Total Volume"]],
                    textposition="outside",
                    hovertemplate="<b>%{y}</b><br>Volume: %{x:,.0f} units<extra></extra>",
                ))
                fig_t5cvol.update_layout(
                    title="Top 5 Customers by Total Volume (Units)",
                    plot_bgcolor="#ffffff", paper_bgcolor="#ffffff",
                    font=dict(family="Inter", color="#0f172a"), height=360,
                    margin=dict(l=10, r=80, t=44, b=20),
                    xaxis=dict(showgrid=False, showticklabels=False, title=None),
                    yaxis=dict(gridcolor="#e2e8f0", color="#1e293b",
                               tickfont=dict(size=12, color="#0f172a"), title=None),
                    showlegend=False,
                )
                st.plotly_chart(fig_t5cvol, use_container_width=True)
            else:
                st.info("Sales Qty data not available.")

        st.markdown("---")

        # ── Section 2: Intra-Customer YoY Monthly Comparison ─────────────
        st.markdown('<div class="section-title">📅 Customer Year-over-Year Monthly Trend</div>',
                    unsafe_allow_html=True)
        st.caption("Select a single customer to compare their month-wise performance: Previous Year vs Current Year.")

        # Customer selector — single customer only
        _all_customers_c = sorted(sdf_c["customer"].dropna().unique().tolist())
        _selected_customer = st.selectbox(
            "Select Customer",
            _all_customers_c,
            key="cust_yoy_select",
        )

        # Filter to selected customer only
        sdf_cust = sdf_c[sdf_c["customer"] == _selected_customer].copy()

        # Determine years automatically from the selected customer's data
        if "so_date" in sdf_cust.columns and not sdf_cust.empty:
            _years_c = sorted(sdf_cust["so_date"].dt.year.dropna().unique().astype(int))
        else:
            _years_c = []

        # Multi-year palette (same as product tab for consistency)
        _YEAR_PALETTE_C = ["#22c55e", "#3b82f6", "#f59e0b", "#a855f7", "#ef4444", "#14b8a6", "#f97316", "#6366f1"]

        def _year_color_c(idx, total):
            if total == 1:
                return "#3b82f6"
            if idx == 0:
                return "#22c55e"
            if idx == total - 1:
                return "#3b82f6"
            mid_palette = ["#f59e0b", "#a855f7", "#ef4444", "#14b8a6", "#f97316", "#6366f1"]
            return mid_palette[(idx - 1) % len(mid_palette)]

        # Helper: build multi-year month-vs-month grouped bar chart for a customer
        def _build_intra_customer_yoy_chart(metric_col, title, yaxis_title, fmt_fn=None):
            if metric_col not in sdf_cust.columns or sdf_cust.empty:
                return None

            sub = sdf_cust.copy()
            sub["year"] = sub["so_date"].dt.year
            sub["month_num"] = sub["so_date"].dt.month

            all_years_c = sorted(sub["year"].dropna().unique().astype(int))
            if not all_years_c:
                return None

            grp = sub.groupby(["year", "month_num"])[metric_col].sum().reset_index()

            ALL_MONTHS = list(range(1, 13))
            _MONTH_ABBR = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
                           7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
            month_labels = [_MONTH_ABBR[m] for m in ALL_MONTHS]

            def _year_values(year):
                y_data = grp[grp["year"] == year].set_index("month_num")[metric_col]
                return [float(y_data.get(m, 0)) for m in ALL_MONTHS]

            fig_yoy_c = go.Figure()
            n_years_c = len(all_years_c)

            for idx, yr in enumerate(all_years_c):
                is_curr = (yr == all_years_c[-1])
                label = f"{yr} (Current Year)" if is_curr else (f"{yr} (Previous Year)" if n_years_c == 2 else str(yr))
                hover_tpl = (
                    f"<b>{_selected_customer}</b><br>%{{x}} {yr}<br>"
                    + (f"Value: ₹%{{y:,.0f}}" if fmt_fn else f"Volume: %{{y:,.0f}} units")
                    + "<extra></extra>"
                )
                fig_yoy_c.add_trace(go.Bar(
                    name=label,
                    x=month_labels,
                    y=_year_values(yr),
                    marker_color=_year_color_c(idx, n_years_c),
                    opacity=0.88,
                    hovertemplate=hover_tpl,
                ))

            legend_hints_c = "  ".join(
                f"{'🟩' if idx==0 else ('🟦' if idx==n_years_c-1 else '🟨')} {yr}"
                for idx, yr in enumerate(all_years_c)
            )
            fig_yoy_c.update_layout(
                title=f"{title} — {_selected_customer}",
                barmode="group",
                plot_bgcolor="#ffffff", paper_bgcolor="#ffffff",
                font=dict(family="Inter", color="#0f172a"), height=420,
                margin=dict(l=20, r=20, t=54, b=60),
                xaxis=dict(
                    showgrid=False, tickangle=0, color="#1e293b",
                    title=f"Month  |  {legend_hints_c}",
                    tickfont=dict(size=12, color="#0f172a"),
                    title_font=dict(size=11, color="#374151"),
                    categoryorder="array",
                    categoryarray=month_labels,
                ),
                yaxis=dict(
                    gridcolor="#e2e8f0", color="#1e293b",
                    title=yaxis_title, tickformat=",.0f",
                    tickfont=dict(size=12, color="#0f172a"),
                ),
                legend=dict(
                    orientation="h", x=0, y=1.08,
                    font=dict(size=11, color="#0f172a"),
                    bgcolor="rgba(255,255,255,0)",
                ),
                bargap=0.22, bargroupgap=0.06,
            )
            return fig_yoy_c

        if len(_years_c) >= 1 and "so_date" in sdf_cust.columns:
            trend_col_cl, trend_col_cr = st.columns(2)

            with trend_col_cl:
                fig_tcv = _build_intra_customer_yoy_chart(
                    "net_value",
                    "Customer Value Trend",
                    "Net Value (₹)", fmt_fn=True,
                )
                if fig_tcv:
                    st.plotly_chart(fig_tcv, use_container_width=True)
                else:
                    st.info("Net Value data not available.")

            with trend_col_cr:
                fig_tcvol = _build_intra_customer_yoy_chart(
                    "sales_qty",
                    "Customer Volume Trend",
                    "Sales Qty (Units)", fmt_fn=False,
                )
                if fig_tcvol:
                    st.plotly_chart(fig_tcvol, use_container_width=True)
                else:
                    st.info("Sales Qty data not available.")
        else:
            st.info("Insufficient data for year-over-year trend charts.")

        st.markdown("---")

        # ── Section 3: Customer Summary Table (Top 20) ────────────────────
        st.markdown('<div class="section-title">📋 Customer Summary — Top 20</div>',
                    unsafe_allow_html=True)
        _agg_c = {}
        if "net_value" in sdf_c.columns:  _agg_c["Total Value"]  = ("net_value",  "sum")
        if "sales_qty" in sdf_c.columns:  _agg_c["Total Volume"] = ("sales_qty",  "sum")
        if _agg_c:
            cust_summary = sdf_c.groupby("customer").agg(**_agg_c).reset_index()
            cust_summary = cust_summary.sort_values(
                "Total Value" if "Total Value" in cust_summary.columns else cust_summary.columns[-1],
                ascending=False
            ).head(20)
            if "Total Value" in cust_summary.columns:
                cust_summary["Total Value (₹)"] = cust_summary["Total Value"].apply(fmt_inr)
                cust_summary = cust_summary.drop(columns=["Total Value"])
            cust_summary = cust_summary.rename(columns={"customer": "Customer"})
            cust_summary.insert(0, "Rank", range(1, len(cust_summary) + 1))
            st.dataframe(cust_summary, use_container_width=True, hide_index=True)


# ──────────────────────────── TAB 2: CLIENT ANALYSIS ─────────────────────────
with tab2:
    if "client" not in dff.columns:
        st.warning("No 'client' column found in the data.")
    else:
        st.markdown('<div class="section-title">👥 Client Performance</div>', unsafe_allow_html=True)

        top_n = st.slider("Show Top N Clients", 5, 30, 10)

        try:
            _cl_agg2 = {}
            if "amount" in dff.columns:    _cl_agg2["Value"]   = ("amount",     "sum")
            if "qty" in dff.columns:       _cl_agg2["Qty"]     = ("qty",        "sum")
            if "is_delayed" in dff.columns: _cl_agg2["Delayed"] = ("is_delayed", "sum")
            client_grp = dff.groupby("client").size().reset_index(name="Orders")
            if _cl_agg2:
                _cl_extra = dff.groupby("client").agg(**_cl_agg2).reset_index()
                client_grp = client_grp.merge(_cl_extra, on="client", how="left")
            client_grp = client_grp.sort_values("Orders", ascending=False)
        except Exception:
            client_grp = pd.DataFrame(columns=["client", "Orders"])

        col_l, col_r = st.columns(2)
        with col_l:
            try:
                top_by_orders = client_grp.nlargest(top_n, "Orders")
                if not top_by_orders.empty:
                    fig = corp_bar(top_by_orders, "Orders", "client",
                                    f"Top {top_n} Clients by Order Count", orientation="h")
                    fig.update_layout(yaxis=dict(autorange="reversed"))
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Not enough data available.")
            except Exception:
                st.info("Not enough data available.")

        with col_r:
            try:
                if "Value" in client_grp.columns:
                    top_by_val = client_grp.nlargest(top_n, "Value")
                    if not top_by_val.empty:
                        fig2 = corp_bar(top_by_val, "Value", "client",
                                         f"Top {top_n} Clients by Order Value", orientation="h")
                        fig2.update_layout(yaxis=dict(autorange="reversed"))
                        fig2.update_traces(
                            text=[fmt_inr(v) for v in top_by_val["Value"]],
                            textposition="outside"
                        )
                        st.plotly_chart(fig2, use_container_width=True)
                    else:
                        st.info("Not enough data available.")
            except Exception:
                st.info("Not enough data available.")

        if "Value" in client_grp.columns:
            st.markdown('<div class="section-title">📊 Client Concentration</div>', unsafe_allow_html=True)
            try:
                c1, c2 = st.columns([1, 2])
                total_v = client_grp["Value"].sum()
                top5 = client_grp.nlargest(5, "Value")
                others_val = max(total_v - top5["Value"].sum(), 0)
                labels_pie = list(top5["client"]) + ["Others"]
                vals_pie   = list(top5["Value"]) + [others_val]
                with c1:
                    fig3 = corp_donut(labels_pie, vals_pie, "Client Value Share")
                    st.plotly_chart(fig3, use_container_width=True)
                with c2:
                    display_cols_cl = ["client","Orders"] + ([c for c in ["Value","Qty","Delayed"] if c in client_grp.columns])
                    disp = client_grp[display_cols_cl].copy()
                    if "Value" in disp.columns:
                        disp["Value"] = disp["Value"].apply(fmt_inr)
                    st.dataframe(disp.head(20), use_container_width=True, hide_index=True)
            except Exception:
                st.info("Insufficient data for concentration analysis.")

        if "is_delayed" in dff.columns and "Delayed" in client_grp.columns:
            st.markdown('<div class="section-title">⚠ Clients with Most Delayed Orders</div>', unsafe_allow_html=True)
            try:
                delay_clients = client_grp[client_grp["Delayed"] > 0].nlargest(top_n, "Delayed")
                if not delay_clients.empty:
                    fig4 = corp_bar(delay_clients, "Delayed", "client",
                                     "Delayed Orders by Client", orientation="h")
                    fig4.update_traces(marker_color="#ef4444")
                    fig4.update_layout(yaxis=dict(autorange="reversed"))
                    st.plotly_chart(fig4, use_container_width=True)
                else:
                    st.success("✅ No delayed orders found for any client.")
            except Exception:
                st.info("No valid delay data available.")

        st.markdown('<div class="section-title">🔍 Client Drilldown</div>', unsafe_allow_html=True)
        try:
            client_options = sorted(dff["client"].dropna().unique())
            if client_options:
                selected_client = st.selectbox("Select a client to inspect", client_options)
                client_detail = dff[dff["client"] == selected_client]
                st.markdown(f"**{len(client_detail)} orders** for *{selected_client}*")
                show_cols = [c for c in ["order_id","product","pharma_category","qty","amount","order_date",
                                           "dispatch_date","status_std","is_delayed","order_age_days"] if c in client_detail.columns]
                st.dataframe(client_detail[show_cols], use_container_width=True, hide_index=True)
            else:
                st.info("No client data available.")
        except Exception:
            st.info("No valid client data for drilldown.")


# ──────────────────────────── TAB 3: PRODUCT ANALYSIS ────────────────────────
with tab3:
    if "product" not in dff.columns:
        st.warning("No 'product' column found in the data.")
    else:
        st.markdown('<div class="section-title">📦 Product Performance</div>', unsafe_allow_html=True)

        top_n_p = st.slider("Show Top N Products", 5, 30, 15, key="prod_n")

        try:
            _pr_agg2 = {}
            if "amount" in dff.columns:     _pr_agg2["Value"]   = ("amount",     "sum")
            if "qty" in dff.columns:        _pr_agg2["Qty"]     = ("qty",        "sum")
            if "is_delayed" in dff.columns: _pr_agg2["Delayed"] = ("is_delayed", "sum")
            prod_grp = dff.groupby("product").size().reset_index(name="Orders")
            if _pr_agg2:
                _pr_extra2 = dff.groupby("product").agg(**_pr_agg2).reset_index()
                prod_grp = prod_grp.merge(_pr_extra2, on="product", how="left")
        except Exception:
            prod_grp = pd.DataFrame(columns=["product", "Orders"])

        c1, c2 = st.columns(2)
        with c1:
            try:
                if "Value" in prod_grp.columns and not prod_grp.empty:
                    tp = prod_grp.nlargest(top_n_p, "Value")
                    fig = corp_bar(tp, "Value", "product", f"Top {top_n_p} Products by Value", orientation="h")
                    fig.update_layout(yaxis=dict(autorange="reversed"))
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Not enough data available.")
            except Exception:
                st.info("Not enough data available.")

        with c2:
            try:
                if "Qty" in prod_grp.columns and not prod_grp.empty:
                    tq = prod_grp.nlargest(top_n_p, "Qty")
                    fig2 = corp_bar(tq, "Qty", "product", f"Top {top_n_p} Products by Quantity", orientation="h")
                    fig2.update_layout(yaxis=dict(autorange="reversed"))
                    st.plotly_chart(fig2, use_container_width=True)
                else:
                    st.info("Not enough data available.")
            except Exception:
                st.info("Not enough data available.")

        st.markdown('<div class="section-title">📉 Low-Moving Products (Bottom 10 by Orders)</div>', unsafe_allow_html=True)
        try:
            if not prod_grp.empty:
                low_movers = prod_grp.nsmallest(10, "Orders")
                st.dataframe(low_movers, use_container_width=True, hide_index=True)
            else:
                st.info("No product data available.")
        except Exception:
            st.info("Insufficient data for low-movers ranking.")

        # Pharma category breakdown (using new pharma_category column)
        if "pharma_category" in dff.columns:
            st.markdown('<div class="section-title">🗂 Pharma Category Performance</div>', unsafe_allow_html=True)
            try:
                _cat2_agg = {"Orders": ("pharma_category", "count")}
                if "amount" in dff.columns:
                    _cat2_agg["Value"] = ("amount", "sum")
                cat_grp2 = dff.groupby("pharma_category").agg(**_cat2_agg).reset_index()
                c1, c2 = st.columns(2)
                with c1:
                    fig3 = corp_bar(cat_grp2, "pharma_category", "Orders", "Orders by Pharma Category")
                    fig3.update_traces(
                        marker_color=[CATEGORY_COLORS.get(c, "#94a3b8") for c in cat_grp2["pharma_category"]]
                    )
                    st.plotly_chart(fig3, use_container_width=True)
                with c2:
                    if "Value" in cat_grp2.columns:
                        fig4 = corp_donut(cat_grp2["pharma_category"], cat_grp2["Value"], "Value by Pharma Category")
                        st.plotly_chart(fig4, use_container_width=True)
            except Exception:
                st.info("Insufficient data for category breakdown.")

        if "Delayed" in prod_grp.columns:
            st.markdown('<div class="section-title">🚨 Products with Most Delay Issues</div>', unsafe_allow_html=True)
            try:
                prob_prods = prod_grp[prod_grp["Delayed"] > 0].nlargest(10, "Delayed")
                if not prob_prods.empty:
                    fig5 = corp_bar(prob_prods, "Delayed", "product",
                                     "Products with Most Delayed Orders", orientation="h")
                    fig5.update_traces(marker_color="#ef4444")
                    fig5.update_layout(yaxis=dict(autorange="reversed"))
                    st.plotly_chart(fig5, use_container_width=True)
                else:
                    st.success("✅ No delay-linked products found.")
            except Exception:
                st.info("No valid delay data available.")


# ──────────────────────────── TAB 4: ORDER STATUS ────────────────────────────
with tab4:
    st.markdown('<div class="section-title">🔄 Order Status Breakdown</div>', unsafe_allow_html=True)

    if "status_std" not in dff.columns:
        st.warning("No status column found.")
    else:
        sc = dff["status_std"].value_counts().reset_index()
        sc.columns = ["Status", "Count"]

        c1, c2 = st.columns([1,2])
        with c1:
            fig = corp_donut(sc["Status"], sc["Count"], "Order Status Distribution")
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            sc["% Share"] = (sc["Count"] / sc["Count"].sum() * 100).round(1)
            st.dataframe(sc, use_container_width=True, hide_index=True)

            open_statuses   = ["pending","confirmed","partial","delayed"]
            closed_statuses = ["dispatched","cancelled"]
            n_open   = dff[dff["status_std"].isin(open_statuses)]["status_std"].count()
            n_closed = dff[dff["status_std"].isin(closed_statuses)]["status_std"].count()
            st.markdown(f"""
            <div style="display:flex; gap:16px; margin-top:16px;">
                <div class="kpi-card kpi-amber" style="flex:1;">
                    <div class="kpi-value">{n_open}</div>
                    <div class="kpi-label">Open Orders</div>
                </div>
                <div class="kpi-card kpi-green" style="flex:1;">
                    <div class="kpi-value">{n_closed}</div>
                    <div class="kpi-label">Closed Orders</div>
                </div>
            </div>""", unsafe_allow_html=True)

        if "order_month" in dff.columns:
            st.markdown('<div class="section-title">📅 Status Trends (Monthly)</div>', unsafe_allow_html=True)
            sm = dff.groupby(["order_month","status_std"]).size().reset_index(name="count")
            sm = sm.sort_values("order_month")
            fig2 = px.bar(sm, x="order_month", y="count", color="status_std",
                           title="Monthly Order Counts by Status",
                           color_discrete_sequence=CORP_COLORS, height=380, barmode="stack")
            fig2.update_layout(plot_bgcolor="#fff", paper_bgcolor="#fff",
                                xaxis=dict(showgrid=False, color="#1e293b"), yaxis=dict(gridcolor="#e2e8f0", color="#1e293b"),
                                font=dict(family="Inter", color="#0f172a"), margin=dict(t=44,b=20))
            st.plotly_chart(fig2, use_container_width=True)

        if "order_age_days" in dff.columns:
            st.markdown('<div class="section-title">⏳ Order Ageing (Open Orders Only)</div>', unsafe_allow_html=True)
            open_df = dff[dff["status_std"].isin(["pending","confirmed","partial"])]
            if not open_df.empty:
                try:
                    bins   = [0, 7, 14, 30, 60, 999]
                    labels = ["0-7 days","8-14 days","15-30 days","31-60 days","60+ days"]
                    open_df = open_df.copy()
                    open_df["age_bucket"] = pd.cut(open_df["order_age_days"], bins=bins, labels=labels)
                    age_grp = open_df["age_bucket"].value_counts().sort_index().reset_index()
                    age_grp.columns = ["Age Bucket","Count"]
                    age_grp["color"] = ["#22c55e","#84cc16","#f59e0b","#f97316","#ef4444"][:len(age_grp)]
                    fig3 = go.Figure(go.Bar(
                        x=age_grp["Age Bucket"], y=age_grp["Count"],
                        marker_color=age_grp["color"], text=age_grp["Count"],
                        textposition="outside",
                    ))
                    fig3.update_layout(title="Open Order Age Distribution",
                                        plot_bgcolor="#fff", paper_bgcolor="#fff",
                                        xaxis=dict(showgrid=False, color="#1e293b"), yaxis=dict(gridcolor="#e2e8f0", color="#1e293b"),
                                        font=dict(family="Inter", color="#0f172a"), height=340, margin=dict(t=44,b=20))
                    st.plotly_chart(fig3, use_container_width=True)
                except Exception:
                    st.info("Insufficient data for ageing chart.")
            else:
                st.success("No open orders in current view.")


# ──────────────────────────── TAB 5: DELAYS & EXCEPTIONS ─────────────────────
with tab5:
    st.markdown('<div class="section-title">⚠ Orders Needing Attention</div>', unsafe_allow_html=True)

    exceptions = pd.DataFrame()

    if "is_delayed" in dff.columns:
        delayed_df = dff[dff["is_delayed"] == True].copy()
        delayed_df["Exception Type"] = "Delayed"
        exceptions = pd.concat([exceptions, delayed_df], ignore_index=True)

    if "status_std" in dff.columns:
        partial_df = dff[dff["status_std"] == "partial"].copy()
        partial_df["Exception Type"] = "Partially Fulfilled"
        exceptions = pd.concat([exceptions, partial_df], ignore_index=True)

        if "order_age_days" in dff.columns:
            stuck_df = dff[(dff["status_std"].isin(["pending","confirmed"])) &
                            (dff["order_age_days"] > 14)].copy()
            stuck_df["Exception Type"] = "Stuck >14 Days"
            exceptions = pd.concat([exceptions, stuck_df], ignore_index=True)

    for missing_col, label in [("amount","Missing Amount"), ("client","Missing Client"), ("product","Missing Product")]:
        if missing_col in dff.columns:
            miss_df = dff[dff[missing_col].isna()].copy()
            miss_df["Exception Type"] = label
            exceptions = pd.concat([exceptions, miss_df], ignore_index=True)

    if "amount" in dff.columns:
        try:
            q99 = dff["amount"].quantile(0.99)
            high_val = dff[dff["amount"] > q99].copy()
            if not high_val.empty:
                high_val["Exception Type"] = "Unusually High Value"
                exceptions = pd.concat([exceptions, high_val], ignore_index=True)
        except Exception:
            pass

    if exceptions.empty:
        st.success("✅ No exceptions or at-risk orders found in the current view.")
    else:
        exceptions = exceptions.drop_duplicates()

        exc_summary = exceptions["Exception Type"].value_counts().reset_index()
        exc_summary.columns = ["Exception Type","Count"]
        fig = corp_bar(exc_summary, "Exception Type", "Count", "Exception Summary")
        fig.update_traces(marker_color="#ef4444")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"**{len(exceptions):,} exception records** across {exceptions['Exception Type'].nunique()} categories.")

        exc_filter = st.multiselect("Filter by Exception Type",
                                     exceptions["Exception Type"].unique(),
                                     default=list(exceptions["Exception Type"].unique()))
        exc_view = exceptions[exceptions["Exception Type"].isin(exc_filter)]

        display_exc_cols = ["Exception Type"] + [c for c in
            ["order_id","client","product","pharma_category","qty","amount","order_date","dispatch_date",
             "status_std","order_age_days","is_delayed","delay_days"] if c in exc_view.columns]
        st.dataframe(exc_view[display_exc_cols].reset_index(drop=True),
                      use_container_width=True, hide_index=True)

        exc_csv = exc_view[display_exc_cols].to_csv(index=False).encode("utf-8")
        st.download_button("⬇ Download Exception Report (CSV)", exc_csv,
                            "exceptions_report.csv", "text/csv")


# ──────────────────────────── TAB 6: DETAILED TABLE ──────────────────────────
with tab6:
    st.markdown('<div class="section-title">📋 Full Order Data</div>', unsafe_allow_html=True)

    search = st.text_input("🔍 Search (Client, Product, Order ID, Category…)", "")

    show_df = dff.copy()

    if search:
        mask = pd.Series(False, index=show_df.index)
        for col in ["client","product","order_id","status_std","region","salesperson","pharma_category"]:
            if col in show_df.columns:
                mask |= show_df[col].astype(str).str.lower().str.contains(search.lower(), na=False)
        show_df = show_df[mask]

    st.caption(f"Showing {len(show_df):,} records")

    priority_cols = ["order_id","client","product","pharma_category","category","qty","amount",
                      "order_date","dispatch_date","due_date","status_std",
                      "is_delayed","order_age_days","delay_days","region","salesperson","remarks"]
    display_cols = [c for c in priority_cols if c in show_df.columns]
    extra_cols = [c for c in show_df.columns if c not in priority_cols and not c.startswith("status")]
    display_cols += extra_cols[:5]

    st.dataframe(show_df[display_cols].reset_index(drop=True),
                  use_container_width=True, hide_index=True)

    # ── Export Options (expanded) ─────────────────────────────────────────
    st.markdown('<div class="section-title">⬇ Export Options</div>', unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        csv_bytes = show_df[display_cols].to_csv(index=False).encode("utf-8")
        st.download_button("⬇ Download as CSV", csv_bytes, "orders_filtered.csv", "text/csv")
    with col_b:
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as writer:
            show_df[display_cols].to_excel(writer, index=False, sheet_name="Orders")
        st.download_button("⬇ Download as Excel", buf.getvalue(),
                            "orders_filtered.xlsx",
                            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    with col_c:
        # Summary report export (NEW)
        buf_summary = io.BytesIO()
        with pd.ExcelWriter(buf_summary, engine="openpyxl") as writer:
            # Sheet 1: Overall KPIs
            kpi_rows = [
                {"Metric": "Total Orders", "Value": total_orders},
                {"Metric": "Total Revenue", "Value": fmt_inr(total_value) if total_value else "N/A"},
                {"Metric": "Unique Clients", "Value": unique_clients},
                {"Metric": "Unique Products", "Value": unique_products},
                {"Metric": "Fill Rate %", "Value": fill_rate},
                {"Metric": "Dispatched", "Value": n_dispatched},
                {"Metric": "Pending/Open", "Value": n_pending},
                {"Metric": "Cancelled", "Value": n_cancelled},
                {"Metric": "Delayed / At Risk", "Value": n_delayed},
            ]
            pd.DataFrame(kpi_rows).to_excel(writer, index=False, sheet_name="KPI Summary")

            # Sheet 2: Category Summary
            if "pharma_category" in dff.columns:
                try:
                    cat_s = dff.groupby("pharma_category").size().reset_index(name="Orders")
                    if "amount" in dff.columns:
                        rev_cs = dff.groupby("pharma_category")["amount"].sum().reset_index()
                        rev_cs.columns = ["pharma_category", "Revenue"]
                        cat_s = cat_s.merge(rev_cs, on="pharma_category", how="left")
                    if "product" in dff.columns:
                        uprod_cs = dff.groupby("pharma_category")["product"].nunique().reset_index()
                        uprod_cs.columns = ["pharma_category", "Products"]
                        cat_s = cat_s.merge(uprod_cs, on="pharma_category", how="left")
                    cat_s.to_excel(writer, index=False, sheet_name="Category Summary")
                except Exception:
                    pass

            # Sheet 3: Client Summary
            if "client" in dff.columns:
                try:
                    cl_s = dff.groupby("client").size().reset_index(name="Orders")
                    if "amount" in dff.columns:
                        rev_cls = dff.groupby("client")["amount"].sum().reset_index()
                        rev_cls.columns = ["client", "Revenue"]
                        cl_s = cl_s.merge(rev_cls, on="client", how="left")
                    cl_s = cl_s.sort_values("Orders", ascending=False)
                    cl_s.to_excel(writer, index=False, sheet_name="Client Summary")
                except Exception:
                    pass

        st.download_button("⬇ Download Summary Report", buf_summary.getvalue(),
                            "summary_report.xlsx",
                            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


# ──────────────────────────── TAB 7: DATA QUALITY ────────────────────────────
with tab7:
    st.markdown('<div class="section-title">🔍 Data Quality Report</div>', unsafe_allow_html=True)

    st.markdown("**Column Mapping Used**")
    map_data = [{"Standard Field": k, "Detected As": v} for k,v in col_mapping.items()]
    if map_data:
        st.dataframe(pd.DataFrame(map_data), use_container_width=True, hide_index=True)
    else:
        st.info("No column mapping was applied.")

    mapped_std = set(col_mapping.keys())
    all_cols = set(df_mapped.columns)
    unmapped = all_cols - mapped_std
    if unmapped:
        st.markdown("**Columns Not Mapped (passed through as-is):**")
        st.write(", ".join(sorted(unmapped)))

    # Pharma category mapping summary (NEW)
    if "pharma_category" in df.columns:
        st.markdown("---")
        st.markdown("**Pharma Category Assignment Summary**")
        cat_map_summary = df.groupby(["product","pharma_category"]).size().reset_index(name="Orders")
        cat_map_summary.columns = ["Product","Assigned Category","Orders"]
        st.dataframe(cat_map_summary, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("**Data Quality Warnings**")
    if not quality_notes and not map_warnings:
        st.markdown('<div class="quality-ok">✅ No data quality issues detected.</div>', unsafe_allow_html=True)
    for note in map_warnings + quality_notes:
        st.markdown(f'<div class="quality-warn">{note}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**Completeness Summary**")

    completeness_rows = []
    for col in df.columns:
        total = len(df)
        filled = df[col].notna().sum()
        completeness_rows.append({
            "Column": col,
            "Total": total,
            "Filled": filled,
            "Missing": total - filled,
            "Completeness %": round(filled / total * 100, 1) if total else 0,
        })
    comp_df = pd.DataFrame(completeness_rows).sort_values("Completeness %")
    st.dataframe(comp_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("**Raw Data Preview (First 10 rows before processing)**")
    st.dataframe(raw_df.head(10), use_container_width=True)
