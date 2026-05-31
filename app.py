# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import base64
import os

# --- 1. PREMIUM LIGHT UI CONFIGURATION (GOOGLE TABS & SEPHORA LIGHT STYLE) ---
st.set_page_config(
    page_title="Sephora Strategic Hub • VGU",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if 'started' not in st.session_state:
    st.session_state.started = False

# Default state variables mapping to avoid widget collisions during reset
defaults = {
    "sb_brand": "All Brands",
    "sb_price": 100.0,
    "sb_rating": 3.5,
    "d_bins": 35,
    "d_price": 150.0,
    "d_brand": "All Brands",
    "a_sort": "love",
    "a_limit": 10,
    "a_cat": "All Categories",
    "exp_cat": "All Categories",
    "exp_search": "",
    "exp_x": "brand",
    "exp_y": "love",
    "exp_chart": "Treemap"
}

# Safely inject missing defaults into st.session_state without overriding active states
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# Safe Image Base64 encoder for secure background rendering (Using newest uploaded backdrop)
def get_image_base64(file_name):
    try:
        if os.path.exists(file_name):
            with open(file_name, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode()
    except Exception:
        pass
    return ""

# Read the uploaded background image dynamically
sephora_bg_base64 = get_image_base64("image_238c12.jpg")
if not sephora_bg_base64:
    sephora_bg_base64 = get_image_base64("image_f68b1e.jpg")

# Premium CSS Styling: Elegant, responsive, featuring micro-interactions and smooth animations
css_style = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght=300;400;500;600;700;800&display=swap');

* { 
    font-family: 'Plus Jakarta Sans', sans-serif; 
}

/* Keyframe Animations */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(24px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes pulseGlow {
    0% {
        box-shadow: 0 0 0 0 rgba(233, 30, 99, 0.45);
        transform: scale(1);
    }
    50% {
        transform: scale(1.02);
    }
    70% {
        box-shadow: 0 0 0 16px rgba(233, 30, 99, 0);
    }
    100% {
        box-shadow: 0 0 0 0 rgba(233, 30, 99, 0);
        transform: scale(1);
    }
}

/* App background default */
.stApp { 
    background-color: #FAFAFB;
    color: #2D3748;
}

/* Sidebar Pastel Pink Elegance */
section[data-testid="stSidebar"] { 
    background-color: #FFF2F5 !important; 
    border-right: 1px solid #FCDDEC; 
}

/* Glassmorphic Rounded Cards with Hover Scale & Glow Animation */
.premium-card {
    background: #FFFFFF;
    padding: 24px;
    border-radius: 20px;
    box-shadow: 0 8px 30px rgba(233, 30, 99, 0.03);
    border: 1px solid rgba(244, 143, 177, 0.15);
    margin-bottom: 20px;
    animation: fadeInUp 0.7s cubic-bezier(0.165, 0.84, 0.44, 1) both;
    transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
}

.premium-card:hover {
    transform: translateY(-4px) scale(1.005);
    box-shadow: 0 18px 45px rgba(233, 30, 99, 0.08);
    border-color: rgba(233, 30, 99, 0.3);
}

/* Sephora Signature Gradient Titles */
.main-title {
    background: linear-gradient(90deg, #E91E63 0%, #B71C1C 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800; 
    font-size: 2.5rem !important;
    letter-spacing: -1px;
    margin-bottom: 4px;
    margin-top: -10px;
}

/* Premium Metric Widgets */
.stat-box {
    text-align: center; 
    padding: 18px;
    background: #FFFFFF; 
    border-radius: 16px;
    border: 1px solid rgba(244, 143, 177, 0.15);
    box-shadow: 0 6px 20px rgba(233, 30, 99, 0.02);
    animation: fadeInUp 0.6s cubic-bezier(0.165, 0.84, 0.44, 1) both;
    transition: all 0.3s cubic-bezier(0.165, 0.84, 0.44, 1);
}
.stat-box:hover {
    border-color: rgba(233, 30, 99, 0.35);
    box-shadow: 0 12px 35px rgba(233, 30, 99, 0.06);
    transform: translateY(-3px);
}
.stat-val { 
    font-size: 2rem; 
    font-weight: 800; 
    color: #E91E63; 
}
.stat-lbl { 
    font-size: 0.75rem; 
    color: #718096; 
    font-weight: 700; 
    text-transform: uppercase; 
    letter-spacing: 1px;
    margin-top: 3px;
}

/* Premium Button Design with Active Glow Pulse */
.stButton>button {
    border-radius: 50px !important;
    background: linear-gradient(90deg, #E91E63 0%, #B71C1C 100%) !important;
    color: white !important; 
    font-weight: 700 !important;
    border: none !important; 
    padding: 14px 40px !important;
    font-size: 1.1rem !important;
    animation: pulseGlow 2.5s infinite;
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
}
.stButton>button:hover { 
    transform: scale(1.05) !important;
    box-shadow: 0 15px 35px rgba(233, 30, 99, 0.45) !important;
}

.badge {
    background-color: #FFF0F3; 
    color: #E91E63;
    padding: 6px 16px; 
    border-radius: 50px;
    font-weight: 700; 
    font-size: 0.8rem;
    display: inline-block; 
    margin-bottom: 12px; 
    border: 1px solid #FCDDEC;
}

/* Hide default Radio Labels for visual spacing */
div[data-testid="stRadio"] > label {
    display: none !important;
    height: 0px !important;
    margin: 0 !important;
    padding: 0 !important;
}

div[data-testid="stRadio"] {
    margin-top: 0px !important;
    padding-top: 0px !important;
}

/* Horizontal Tab Menu (Google Chrome Style) */
div[role="radiogroup"] {
    gap: 6px !important;
    background-color: #FFF0F3 !important;
    padding: 6px 10px !important;
    border-radius: 14px !important;
    border: 1px solid #FCDDEC !important;
    margin-top: 0px !important;
    margin-bottom: 20px !important;
    display: flex !important;
    flex-direction: row !important;
    justify-content: center !important;
}

div[role="radiogroup"] label {
    background-color: transparent !important;
    border-radius: 10px 10px 0px 0px !important;
    color: #4A5568 !important;
    font-size: 0.9rem !important;
    font-weight: 700 !important;
    padding: 8px 16px !important;
    border: none !important;
    transition: all 0.2s ease !important;
    margin: 0 !important;
}

div[role="radiogroup"] label[data-checked="true"] {
    background-color: #FFFFFF !important;
    color: #E91E63 !important;
    border-radius: 10px 10px 0px 0px !important;
    border-top: 3px solid #E91E63 !important;
    box-shadow: 0 -3px 10px rgba(233, 30, 99, 0.08) !important;
}

/* Hide default streamlit radio circles */
div[role="radiogroup"] [data-testid="stRadioSquare"] {
    display: none !important;
}
</style>
"""
st.markdown(css_style, unsafe_allow_html=True)

# --- 2. THE BRAND COLOR PALETTE (GRADIENT PINK-TO-RED SEPHORA) ---
SEPHORA_COLORS = ["#F48FB1", "#F06292", "#EC407A", "#E91E63", "#EF5350", "#E53935", "#B71C1C"]

# --- 3. DATA LOAD & PREPROCESSING ---
@st.cache_data
def load_data():
    df = pd.read_csv("sephora_website_dataset.csv")
    df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(df['price'].median())
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce').fillna(df['rating'].median())
    df['love'] = pd.to_numeric(df['love'], errors='coerce').fillna(df['love'].median())
    df['number_of_reviews'] = pd.to_numeric(df['number_of_reviews'], errors='coerce').fillna(0)
    df['vfm_score'] = (df['love'] / (df['price'] + 1)).round(2)
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"⚠️ Error: Unable to read 'sephora_website_dataset.csv'. Details: {e}")
    st.stop()


# --- 4. START SCREEN HERO LAYOUT (STABLE & IMMERSIVE DESIGN) ---
if not st.session_state.started:
    st.markdown("<style>section[data-testid='stSidebar'] { display: none !important; }</style>", unsafe_allow_html=True)
    
    # Render immersive photographic backdrop using base64 dynamically if available
    if sephora_bg_base64:
        bg_css = f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.65)), url("data:image/jpeg;base64,{sephora_bg_base64}") no-repeat center center fixed !important;
            background-size: cover !important;
        }}
        </style>
        """
    else:
        bg_css = """
        <style>
        .stApp {
            background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.65)), url("https://images.unsplash.com/photo-1596462502278-27bfdc403348?auto=format&fit=crop&w=1200&q=80") no-repeat center center fixed !important;
            background-size: cover !important;
        }
        </style>
        """
    st.markdown(bg_css, unsafe_allow_html=True)

    # Frosted glass panel styling for absolute symmetry, glowing outline, and premium float animation
    st.markdown("""
    <style>
    .glass-panel {
        background: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(35px) !important;
        -webkit-backdrop-filter: blur(35px) !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
        border-radius: 32px;
        padding: 50px 40px;
        max-width: 900px;
        margin: 40px auto 20px auto;
        text-align: center;
        box-shadow: 0 30px 70px rgba(0, 0, 0, 0.45), inset 0 1px 0 rgba(255,255,255,0.15);
        position: relative;
        animation: fadeInUp 1s cubic-bezier(0.16, 1, 0.3, 1) both, floatAnimation 6s ease-in-out infinite;
    }
    .glass-title {
        color: #FFFFFF !important;
        font-size: 2.7rem !important;
        font-weight: 800 !important;
        letter-spacing: -1px;
        margin: 25px 0 5px 0 !important;
        text-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    .glass-subtitle {
        color: #FF8A9A !important;
        font-size: 1.45rem !important;
        font-weight: 700 !important;
        margin: 0 0 10px 0 !important;
        text-shadow: 0 3px 10px rgba(0,0,0,0.4);
    }
    .glass-desc {
        color: #F7FAFC !important;
        font-size: 0.98rem;
        line-height: 1.75;
        text-align: justify;
        text-shadow: 0 1px 4px rgba(0,0,0,0.3);
    }
    .glow-text {
        background: linear-gradient(120deg, #FF8A9A 0%, #E91E63 50%, #FFC107 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shineGlow 4s linear infinite;
        font-weight: 900;
        letter-spacing: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Simplified Start Screen Layout (Sát lề trái, tuyệt đối không thụt lề để tránh hiển thị thành code block)
    st.markdown(f"""
<div class="glass-panel">
<div style='height: 12px; background: repeating-linear-gradient(-45deg, #000, #000 10px, #fff 10px, #fff 20px); width: 100%; position: absolute; top: 0; left: 0; border-radius: 32px 32px 0 0;'></div>
<div style='margin-bottom: 10px; margin-top: 15px;'>
<h1 class="glow-text" style='font-size: 3.8rem; margin: 0; text-shadow: 0 4px 20px rgba(233,30,99,0.3);'>SEPHORA</h1>
<div style='height: 3px; background: linear-gradient(90deg, #E91E63, #FF8A9A); width: 160px; margin: 15px auto 0 auto; box-shadow: 0 2px 10px rgba(233, 30, 99, 0.6);'></div>
</div>
<h1 class="glass-title">Sephora Website's Products</h1>
<h3 class="glass-subtitle">Sephora Product Analysis Data</h3>
<p style='font-size: 0.9rem; color: #E2E8F0; font-weight: 700; text-transform: uppercase; letter-spacing: 3px; margin-bottom: 35px; text-shadow: 0 2px 6px rgba(0,0,0,0.4);'>
Vietnamese-German University • Group 1 (D4)
</p>
<div style="background: rgba(0, 0, 0, 0.35); padding: 30px; border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.15); margin-bottom: 15px; box-shadow: inset 0 2px 4px rgba(0,0,0,0.2);">
<h4 style='color: #FF8A9A; margin-top: 0; font-weight: 800; font-size: 1.25rem; margin-bottom: 12px; text-align: left; text-shadow: 0 1px 4px rgba(0,0,0,0.3);'>📖 Project Introduction</h4>
<p class="glass-desc">
In the highly competitive cosmetic retail space, Sephora stands as a global trendsetter. Understanding customer loyalty behaviors, pricing dynamics, and catalog quality indices is crucial for maintaining market superiority.
</p>
<p class="glass-desc" style="margin-top: 12px; margin-bottom: 0px;">
This business intelligence system parses thousands of active Sephora listings to offer streamlined corporate decision support, discovering hidden correlations between <b>Price matrixes</b>, <b>Love Index values</b>, and <b>Rating distributions</b>.
</p>
</div>
</div>
""", unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Beautifully aligned Enter Button with active pulse glow
    col_btn_l, col_btn_c, col_btn_r = st.columns([1.2, 1, 1.2])
    with col_btn_c:
        if st.button("🚀 LET'S START", use_container_width=True):
            st.session_state.started = True
            st.rerun()



# --- 5. MAIN PORTAL (INSIDE DASHBOARD) ---
else:
    # Safely clear page-wide photographic background to render analytical charts with optimal light-contrast
    st.markdown("""
    <style>
    .stApp {
        background: #FAFAFB !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Sidebar Logo Header
    st.sidebar.markdown("<div style='text-align: center; padding: 10px 0;'><h2 style='color: #E91E63; font-weight: 800; margin-bottom: 0;'>SEPHORA BI</h2><p style='color: #880E4F; font-size: 0.8rem; letter-spacing: 2px; font-weight: 700;'>DECISION ENGINE</p></div>", unsafe_allow_html=True)
    st.sidebar.markdown("<hr style='margin: 8px 0; border-color: #FCDDEC;'>", unsafe_allow_html=True)

    # Main Header Panel
    st.markdown("<h1 class='main-title'>Strategic Decision Support Hub</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #880E4F; font-weight:600; font-size:0.92rem; margin-bottom: 15px;'>Vietnamese-German University (VGU) • Business Information Systems Project</p>", unsafe_allow_html=True)

    # Navigation options
    tab_selection = st.radio(
        "Navigation",
        [
            "🏠 Executive Home",
            "🔮 Strategy Sandbox",
            "📊 Customizable Price Densities",
            "📈 Flexible Area Trend Leaders",
            "💎 Cosmetics Explorer",
            "👥 Research Team"
        ],
        label_visibility="collapsed"
    )

    # -------------------------------------------------------------
    # PER-TAB DYNAMIC SIDEBAR FILTERS WITH CALLBACK-FREE SAFEST STATE RESET
    # -------------------------------------------------------------
    if tab_selection == "🔮 Strategy Sandbox":
        st.sidebar.markdown("### 🔮 Sandbox Filter System")
        
        # Reset mechanics: triggers immediately, safely mutating target states without jumping tabs
        if st.sidebar.button("🔄 Reset filters for this tab", use_container_width=True, key="reset_sandbox"):
            st.session_state.sb_brand = defaults["sb_brand"]
            st.session_state.sb_price = defaults["sb_price"]
            st.session_state.sb_rating = defaults["sb_rating"]
            st.rerun()

        brand_opt = ['All Brands'] + df['brand'].value_counts().head(25).index.tolist()
        
        # Ensure values exist in arrays to avoid index/ValueError crashes
        sb_b_val = st.session_state.sb_brand if st.session_state.sb_brand in brand_opt else "All Brands"
        sandbox_brand = st.sidebar.selectbox("Filter Brand Segment:", options=brand_opt, index=brand_opt.index(sb_b_val), key="sb_brand")
        
        sandbox_max_price = st.sidebar.slider("Maximum Price Target ($):", 5.0, 400.0, float(st.session_state.sb_price), step=5.0, key="sb_price")
        sandbox_min_rating = st.sidebar.slider("Minimum Rating Standard (⭐):", 1.0, 5.0, float(st.session_state.sb_rating), step=0.1, key="sb_rating")

    elif tab_selection == "📊 Customizable Price Densities":
        st.sidebar.markdown("### 📊 Density Curve Settings")
        
        if st.sidebar.button("🔄 Reset filters for this tab", use_container_width=True, key="reset_density"):
            st.session_state.d_bins = defaults["d_bins"]
            st.session_state.d_price = defaults["d_price"]
            st.session_state.d_brand = defaults["d_brand"]
            st.rerun()

        bin_count = st.sidebar.slider("Adjust Bins (Granularity):", 10, 100, int(st.session_state.d_bins), key="d_bins")
        max_price_slider = st.sidebar.slider("Max Retail Price Limit ($):", 20.0, 500.0, float(st.session_state.d_price), step=5.0, key="d_price")
        
        brand_opt_density = ['All Brands'] + df['brand'].value_counts().head(30).index.tolist()
        d_b_val = st.session_state.d_brand if st.session_state.d_brand in brand_opt_density else "All Brands"
        brand_filter = st.sidebar.selectbox("Select Brand Segment:", brand_opt_density, index=brand_opt_density.index(d_b_val), key="d_brand")

    elif tab_selection == "📈 Flexible Area Trend Leaders":
        st.sidebar.markdown("### 📈 Ranking Configuration")
        
        if st.sidebar.button("🔄 Reset filters for this tab", use_container_width=True, key="reset_leaders"):
            st.session_state.a_sort = defaults["a_sort"]
            st.session_state.a_limit = defaults["a_limit"]
            st.session_state.a_cat = defaults["a_cat"]
            st.rerun()

        sort_opts = ['love', 'number_of_reviews', 'price', 'rating']
        a_s_val = st.session_state.a_sort if st.session_state.a_sort in sort_opts else "love"
        ranking_var = st.sidebar.selectbox("Rank Products Based On:", sort_opts, index=sort_opts.index(a_s_val), key="a_sort")
        
        item_limit = st.sidebar.slider("Number of Products to Show:", 5, 30, int(st.session_state.a_limit), key="a_limit")
        
        cat_opts = ['All Categories'] + df['category'].value_counts().head(20).index.tolist()
        a_c_val = st.session_state.a_cat if st.session_state.a_cat in cat_opts else "All Categories"
        target_category = st.sidebar.selectbox("Select Category Sector:", cat_opts, index=cat_opts.index(a_c_val), key="a_cat")

    elif tab_selection == "💎 Cosmetics Explorer":
        st.sidebar.markdown("### 💎 Explorer Custom Controls")
        
        if st.sidebar.button("🔄 Reset filters for this tab", use_container_width=True, key="reset_explorer"):
            st.session_state.exp_cat = defaults["exp_cat"]
            st.session_state.exp_search = defaults["exp_search"]
            st.session_state.exp_x = defaults["exp_x"]
            st.session_state.exp_y = defaults["exp_y"]
            st.session_state.exp_chart = defaults["exp_chart"]
            st.rerun()

        cat_opts_explorer = ['All Categories'] + df['category'].dropna().unique().tolist()
        exp_c_val = st.session_state.exp_cat if st.session_state.exp_cat in cat_opts_explorer else "All Categories"
        sel_category = st.sidebar.selectbox("Base Catalog Category:", cat_opts_explorer, index=cat_opts_explorer.index(exp_c_val), key="exp_cat")
        
        search_kw = st.sidebar.text_input("Formula or Name Keyword search:", value=st.session_state.exp_search, key="exp_search")
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📊 Axis & Chart Settings")
        x_opts = ['brand', 'category', 'rating']
        exp_x_val = st.session_state.exp_x if st.session_state.exp_x in x_opts else "brand"
        x_axis_var = st.sidebar.selectbox("X-Axis Selector:", x_opts, index=x_opts.index(exp_x_val), key="exp_x")
        
        y_opts = ['love', 'price', 'number_of_reviews']
        exp_y_val = st.session_state.exp_y if st.session_state.exp_y in y_opts else "love"
        y_axis_var = st.sidebar.selectbox("Y-Axis Selector:", y_opts, index=y_opts.index(exp_y_val), key="exp_y")
        
        chart_opts = ['Treemap', 'Bar', 'Scatter']
        exp_chart_val = st.session_state.exp_chart if st.session_state.exp_chart in chart_opts else "Treemap"
        chart_type_sel = st.sidebar.selectbox("Chart Type Selector:", chart_opts, index=chart_opts.index(exp_chart_val), key="exp_chart")

    # Back to Landing screen trigger
    st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
    if st.sidebar.button("⬅️ Back to Start Screen", use_container_width=True):
        st.session_state.started = False
        st.rerun()

    # -------------------------------------------------------------
    # TAB 1: EXECUTIVE HOME (MỤC TIÊU CHIẾN LƯỢC + HÌNH CỌ TRANG TRÍ)
    # -------------------------------------------------------------
    if tab_selection == "🏠 Executive Home":
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.markdown(f"<div class='stat-box'><div class='stat-val'>{df.shape[0]:,}</div><div class='stat-lbl'>Catalog Assortments</div></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='stat-box'><div class='stat-val'>{df['brand'].nunique()}</div><div class='stat-lbl'>Unique Brands</div></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='stat-box'><div class='stat-val'>${df['price'].mean():.2f}</div><div class='stat-lbl'>Average Price</div></div>", unsafe_allow_html=True)
        with c4: st.markdown(f"<div class='stat-box'><div class='stat-val'>{df['rating'].mean():.2f}⭐</div><div class='stat-lbl'>Satisfaction Score</div></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        col_home_txt1, col_home_txt2 = st.columns(2)
        with col_home_txt1:
            st.markdown("""
            <div class='premium-card' style='height: 100%; border-right: 4px solid #E91E63; margin-bottom: 0px;'>
                <h3 style='margin-top: 0; color: #111827;'>✨ Strategic Hub Operating Instructions</h3>
                <p style='color: #4A5568; line-height: 1.75;'>
                    Welcome to the <b>Sephora Corporate Decision Support Portal</b>. This space has been carefully optimized to avoid unnecessary whitespace, offering lightning-fast database loads and high-fidelity layouts.
                </p>
                <p style='color: #4A5568; line-height: 1.75;'>
                    <b>Active Functional Modules:</b>
                </p>
                <ul style='color: #4A5568; line-height: 1.7; padding-left: 20px;'>
                    <li><b>Strategy Sandbox:</b> Explores cross-metric behaviors (Price, Reviews, Sentiment) under targeted brand standards.</li>
                    <li><b>Price Distributions:</b> Charts continuous price levels to pinpoint pricing gaps and margin strategies.</li>
                    <li><b>Assortment Leaders:</b> Displays rapid market power drops and lists viral products driven by community engagement.</li>
                    <li><b>Cosmetics Explorer (Dynamic):</b> Gives you complete analytical freedom to search ingredients, filter categories, and map bespoke multi-axis projections.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        with col_home_txt2:
            st.markdown("""
            <div class='premium-card' style='height: 100%; border-left: 5px solid #B71C1C; margin-bottom: 0px;'>
                <h3 style='margin-top: 0; color: #111827;'>🎯 Strategic Objectives</h3>
                <p style='color: #4A5568; line-height: 1.6; font-weight: 600; margin-bottom: 12px;'>
                    What key insights do we explore from this dataset?
                </p>
                <ul style='font-size: 0.9rem; line-height: 1.6; color: #4A5568; padding-left: 20px; margin-bottom: 0;'>
                    <li><b>Pricing Sweet Spots:</b> Finding perfect value targets that balance brand prestige and volume sales.</li>
                    <li><b>Love Index vs Rating Frequencies:</b> Investigating whether social loyalty translates directly into higher rating stars.</li>
                    <li><b>Assortment Strength:</b> Benchmarking market footprints across sectors like Makeup, Skincare, Fragrances, and Tools.</li>
                    <li><b>Value for Money Index:</b> Uncovering the best consumer-voted returns per dollar spent.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Luxury decorative image beside raw preview data table
        col_img_decor, col_table_decor = st.columns([1, 2])
        with col_img_decor:
            st.image(
                "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?auto=format&fit=crop&w=600&q=80",
                caption="Sephora Professional Brushes & Toolkits",
                use_container_width=True
            )
        with col_table_decor:
            st.markdown("### 📋 Primary Dataset Preview")
            rows = st.slider("Select row limit for catalog preview:", 5, 100, 15, key="home_rows")
            st.dataframe(df.head(rows), use_container_width=True)

    # -------------------------------------------------------------
    # TAB 2: STRATEGY SANDBOX (SCATTER / HISTOGRAM + PALETTE IMAGE)
    # -------------------------------------------------------------
    elif tab_selection == "🔮 Strategy Sandbox":
        st.markdown("<span class='badge'>INTERACTIVE EXPERIMENT</span>", unsafe_allow_html=True)
        st.markdown("<h2>Dynamic Performance & Customer Loyalty Sandbox</h2>", unsafe_allow_html=True)
        
        filtered_sandbox = df[df['price'] <= sandbox_max_price]
        if sandbox_brand != "All Brands":
            filtered_sandbox = filtered_sandbox[filtered_sandbox['brand'] == sandbox_brand]
        filtered_sandbox = filtered_sandbox[filtered_sandbox['rating'] >= sandbox_min_rating]
            
        col_plot1, col_plot2 = st.columns(2)
        with col_plot1:
            st.markdown("<div class='premium-card' style='padding: 15px; margin-bottom: 0px;'>", unsafe_allow_html=True)
            st.markdown("<h4>Scatter Projection: Price vs. Love Metric</h4>", unsafe_allow_html=True)
            fig_scatter = px.scatter(
                filtered_sandbox, x='price', y='love', color='category',
                size='number_of_reviews', color_discrete_sequence=SEPHORA_COLORS,
                hover_data=['brand', 'name', 'price', 'rating'], template="simple_white", opacity=0.75
            )
            fig_scatter.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                font_family="Plus Jakarta Sans", margin=dict(l=10, r=10, t=30, b=10)
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_plot2:
            st.markdown("<div class='premium-card' style='padding: 15px; margin-bottom: 0px;'>", unsafe_allow_html=True)
            st.markdown("<h4>Satisfaction Frequency: Product Star Ratings</h4>", unsafe_allow_html=True)
            fig_hist = px.histogram(
                filtered_sandbox, x='rating', color_discrete_sequence=[SEPHORA_COLORS[3]],
                template="simple_white", opacity=0.85
            )
            fig_hist.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                font_family="Plus Jakarta Sans", margin=dict(l=10, r=10, t=30, b=10)
            )
            st.plotly_chart(fig_hist, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        st.success(f"📈 **Live Sandbox Insights:** Query resolved successfully. Found **{filtered_sandbox.shape[0]}** matching listings.")

        col_desc_sandbox, col_img_sandbox = st.columns([2, 1])
        with col_desc_sandbox:
            st.markdown("""
            <div class='premium-card' style='margin-bottom: 0px; height: 100%;'>
                <h4 style='color: #E91E63; font-weight: 700;'>💡 Sandbox Strategic Intelligence</h4>
                <p style='color: #4A5568; line-height:1.7; font-size: 0.92rem;'>
                    <b>1. Pricing Sweet Spot Optimization:</b> On the scatter plot, items nestled in the <i>upper-left segment</i> represent Sephora's viral customer acquisition magnets. They trigger extensive organic reach ("Love score") while maintaining an affordable entry barrier.
                </p>
                <p style='color: #4A5568; line-height:1.7; font-size: 0.92rem;'>
                    <b>2. Consumer Satisfaction Distribution:</b> The strong leftward skew toward 4.0 and 4.5 stars confirms that Sephora’s selection process successfully guarantees catalog quality. Double peaks usually represent chemical components or formulation shifts within brand segments.
                </p>
            </div>
            """, unsafe_allow_html=True)
        with col_img_sandbox:
            st.image(
                "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?auto=format&fit=crop&w=600&q=80",
                caption="Palette & Shading Formulation Analysis",
                use_container_width=True
            )

    # -------------------------------------------------------------
    # TAB 3: CUSTOMIZABLE PRICE DENSITIES
    # -------------------------------------------------------------
    elif tab_selection == "📊 Customizable Price Densities":
        st.markdown("<span class='badge'>PRICING STRUCTURE</span>", unsafe_allow_html=True)
        st.markdown("<h2>Continuous Market Retail Pricing Densities</h2>", unsafe_allow_html=True)
        
        density_df = df[df['price'] <= max_price_slider]
        if brand_filter != 'All Brands':
            density_df = density_df[density_df['brand'] == brand_filter]
            
        fig_price_hist = px.histogram(
            density_df, x='price', nbins=bin_count,
            color_discrete_sequence=[SEPHORA_COLORS[5]], marginal="box",
            template="simple_white", opacity=0.85
        )
        fig_price_hist.update_layout(
            xaxis_title="Retail Price Point ($)", yaxis_title="Product Inventory Count",
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font_family="Plus Jakarta Sans", font_color="#2D3748",
            margin=dict(l=10, r=10, t=20, b=10)
        )
        st.plotly_chart(fig_price_hist, use_container_width=True)

        col_desc_densities, col_img_densities = st.columns([2, 1])
        with col_desc_densities:
            st.markdown(f"""
            <div class='premium-card' style='margin-bottom: 0px; height: 100%;'>
                <h4 style='color: #B71C1C; font-weight: 700;'>💼 Pricing Strategy Analysis for: {brand_filter}</h4>
                <p style='color: #4A5568; line-height:1.7;'>
                    Most cosmetic brands exhibit a distinct <b>Right-Skewed pricing pattern</b>. Sub-40 dollar entries handle the vast majority of volume and brand introduction, whereas high-margin premium products generate bulk retail net profits. Low-density pockets represent opportunities where new product lines can be introduced without cannibalizing current sales.
                </p>
            </div>
            """, unsafe_allow_html=True)
        with col_img_densities:
            st.image(
                "https://images.unsplash.com/photo-1596462502278-27bfdc403348?auto=format&fit=crop&w=600&q=80",
                caption="Premium Liquid Cosmetic Textures",
                use_container_width=True
            )

    # -------------------------------------------------------------
    # TAB 4: FLEXIBLE AREA TREND LEADERS
    # -------------------------------------------------------------
    elif tab_selection == "📈 Flexible Area Trend Leaders":
        st.markdown("<span class='badge'>ASSORTMENT POWER</span>", unsafe_allow_html=True)
        st.markdown("<h2>Category Leaders and Market Concentration Curves</h2>", unsafe_allow_html=True)
        
        area_df = df.copy()
        if target_category != 'All Categories':
            area_df = area_df[area_df['category'] == target_category]
            
        area_plot_data = area_df.sort_values(by=ranking_var, ascending=False).head(item_limit)
        
        fig_area = px.area(
            area_plot_data, x='name', y=ranking_var,
            color_discrete_sequence=[SEPHORA_COLORS[3]], template="simple_white"
        )
        fig_area.update_layout(
            xaxis={'categoryorder':'total descending'},
            xaxis_title="Assortment Listing Name", yaxis_title=ranking_var.replace('_', ' ').title(),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font_family="Plus Jakarta Sans", font_color="#2D3748",
            margin=dict(l=10, r=10, t=20, b=10)
        )
        st.plotly_chart(fig_area, use_container_width=True)

        col_desc_leaders, col_img_leaders = st.columns([2, 1])
        with col_desc_leaders:
            st.markdown(f"""
            <div class='premium-card' style='margin-bottom: 0px; height: 100%;'>
                <h4 style='color: #E91E63; font-weight: 700;'>⭐ Power Law Dynamics in Modern Cosmetics</h4>
                <p style='color: #4A5568; line-height:1.7;'>
                    The rapid decline in the area curve outside the top 3-5 entries confirms a strong <b>Power Law concentration</b> in beauty retail. A few "Hero Products" often shoulder the weight of an entire category segment's engagement. Instead of distributing budget equally, brands should focus their marketing efforts on establishing single category-leading formulations that organically drive interest to secondary lines.
                </p>
            </div>
            """, unsafe_allow_html=True)
        with col_img_leaders:
            st.image(
                "https://images.unsplash.com/photo-1608248597481-496100c80836?auto=format&fit=crop&w=600&q=80",
                caption="Organic Sephora Product Catalog",
                use_container_width=True
            )

    # -------------------------------------------------------------
    # TAB 5: COSMETICS EXPLORER (CUSTOM COMPREHENSIVE QUERY SYSTEM)
    # -------------------------------------------------------------
    elif tab_selection == "💎 Cosmetics Explorer":
        st.markdown("<span class='badge'>EXPLORATIVE ENGINE</span>", unsafe_allow_html=True)
        st.markdown("<h2>💎 Cosmetics Multidimensional Strategy Explorer</h2>", unsafe_allow_html=True)
        
        exp_df = df.copy()
        
        # Categorical Filter Logic
        if sel_category != 'All Categories':
            exp_df = exp_df[exp_df['category'] == sel_category]
            
        # Free-form search matching (Brand, Ingredients, Name)
        if search_kw:
            search_clean = search_kw.lower()
            mask_brand = exp_df['brand'].astype(str).str.lower().str.contains(search_clean)
            mask_name = exp_df['name'].astype(str).str.lower().str.contains(search_clean)
            
            # Use 'ingredients' column if available in dataset
            if 'ingredients' in exp_df.columns:
                mask_ing = exp_df['ingredients'].astype(str).str.lower().str.contains(search_clean)
                combined_mask = mask_brand | mask_name | mask_ing
            else:
                combined_mask = mask_brand | mask_name
                
            exp_df = exp_df[combined_mask]

        if not exp_df.empty:
            # Aggregate the metrics to guarantee legible data trends
            chart_data = exp_df.groupby(x_axis_var)[y_axis_var].mean().reset_index()
            chart_data = chart_data.sort_values(by=y_axis_var, ascending=False).head(30)

            # Conditional Plot Rendering Engine
            if chart_type_sel == 'Treemap':
                fig_custom = px.treemap(
                    chart_data, path=[x_axis_var], values=y_axis_var,
                    color=y_axis_var, color_continuous_scale=SEPHORA_COLORS[2:6]
                )
            elif chart_type_sel == 'Bar':
                fig_custom = px.bar(
                    chart_data, x=x_axis_var, y=y_axis_var,
                    color=y_axis_var, color_continuous_scale=SEPHORA_COLORS[2:6],
                    template="simple_white"
                )
            else:  # Scatter Setup
                fig_custom = px.scatter(
                    exp_df.head(250), x=x_axis_var, y=y_axis_var, color='category',
                    color_discrete_sequence=SEPHORA_COLORS, template="simple_white"
                )

            fig_custom.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font_family="Plus Jakarta Sans", font_color="#2D3748",
                margin=dict(l=10, r=10, t=30, b=10)
            )
            st.plotly_chart(fig_custom, use_container_width=True)

            st.success(f"🎯 **Explorer Execution Matrix:** Identified **{exp_df.shape[0]}** matching assortments.")
        else:
            st.warning("⚠️ No products matching your keyword or selected categorical criteria are present in our dataset. Try adapting your filters on the Sidebar.")

        st.markdown(f"""
        <div class='premium-card' style='margin-bottom: 0px;'>
            <h4 style='color: #E91E63; font-weight: 700;'>📊 Cosmetic Strategy Insights</h4>
            <p style='color: #4A5568; line-height:1.7;'>
                <b>Multidimensional Analysis:</b> By allowing variable re-projection, this module bridges the gap between raw metrics and business decisions. For example, setting <b>X-Axis</b> to 'brand' and <b>Y-Axis</b> to 'price' while searching for clean markers like 'glycol' or 'organic' immediately reveals which premium brands are leveraging clean-beauty ingredients to command higher market price points.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # -------------------------------------------------------------
    # TAB 6: RESEARCH TEAM
    # -------------------------------------------------------------
    elif tab_selection == "👥 Research Team":
        st.markdown("<span class='badge'>PROJECT DIRECTORY</span>", unsafe_allow_html=True)
        st.markdown("<h2>Group Research Contributors & Responsibility Matrices</h2>", unsafe_allow_html=True)

        st.markdown("""
        <div class='premium-card' style='margin-bottom: 0px;'>
            <h3>🎓 Research Group 1 (Class D4)</h3>
            <p style='color: #4A5568;'>This professional business intelligence application was built, structured, and presented for the Python Data Science & Systems Project at the Vietnamese-German University.</p>
            <table style='width: 100%; border-collapse: collapse; margin-top: 20px; color: #2D3748; font-size: 0.95rem;'>
                <thead>
                    <tr style='background-color: #FFF0F3; border-bottom: 2px solid #E91E63;'>
                        <th style='padding: 14px; text-align: left; color: #E91E63; font-weight: 800;'>Full Name</th>
                        <th style='padding: 14px; text-align: left; color: #E91E63; font-weight: 800;'>Student ID</th>
                        <th style='padding: 14px; text-align: left; color: #E91E63; font-weight: 800;'>Primary Project Contribution Matrix</th>
                    </tr>
                </thead>
                <tbody>
                    <tr style='border-bottom: 1px solid rgba(244, 143, 177, 0.15);'>
                        <td style='padding: 14px; font-weight: 600;'>Lê Thanh Đông Nghi</td>
                        <td style='padding: 14px;'>10625015</td>
                        <td style='padding: 14px; color: #4A5568;'><b>Group Leader:</b> Directed system orchestration, managed git pipeline, implemented Plot 7 & Plot 8, and structured UI/UX landing page controls.</td>
                    </tr>
                    <tr style='border-bottom: 1px solid rgba(244, 143, 177, 0.15);'>
                        <td style='padding: 14px; font-weight: 600;'>Phạm Hồng Minh</td>
                        <td style='padding: 14px;'>10625075</td>
                        <td style='padding: 14px; color: #4A5568;'><b>Business Strategist:</b> Conducted market analysis, authored system introduction documentation, and engineered Plot 1 & Plot 2 modules.</td>
                    </tr>
                    <tr style='border-bottom: 1px solid rgba(244, 143, 177, 0.15);'>
                        <td style='padding: 14px; font-weight: 600;'>Nguyễn Mai Thanh</td>
                        <td style='padding: 14px;'>10325040</td>
                        <td style='padding: 14px; color: #4A5568;'><b>Core UX Architect:</b> Established exploratory research structures, configured objectives, and developed Plot 3 & Plot 4 widgets.</td>
                    </tr>
                    <tr style='border-bottom: 1px solid rgba(244, 143, 177, 0.15);'>
                        <td style='padding: 14px; font-weight: 600;'>Nguyễn Minh Yến Phương</td>
                        <td style='padding: 14px;'>10625041</td>
                        <td style='padding: 14px; color: #4A5568;'><b>Data Engineer:</b> Designed data ingestion pipeline, cleaned raw dataset, executed median imputer schemas, and developed Plot 9 & Plot 10.</td>
                    </tr>
                    <tr style='border-bottom: 1px solid rgba(244, 143, 177, 0.15);'>
                        <td style='padding: 14px; font-weight: 600;'>Dương Thị Bình Minh</td>
                        <td style='padding: 14px;'>10625079</td>
                        <td style='padding: 14px; color: #4A5568;'><b>Visual Identity Designer:</b> Created the pink-to-red corporate color palette, optimized style tokens, and built Plot 5 & Plot 6 modules.</td>
                    </tr>
                </tbody>
            </table>
            <br>
            <p style='color: #E91E63; font-weight: 700; font-size: 1rem;'>Officially submitted to Senior Lecturer Dr. Tan Do • Vietnamese-German University (VGU).</p>
        </div>
        """, unsafe_allow_html=True)