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


# Initialize Session State for page and starting control
if 'started' not in st.session_state:
    st.session_state.started = False


# Default state variables mapping to avoid widget collisions during reset
defaults = {
    "sb_brands": [],
    "sb_categories": [],
    "sb_price": (5.0, 150.0),
    "sb_rating": (3.5, 5.0),
    "sb_min_reviews": 0,
    "sb_x_axis": "price",
    "sb_y_axis": "love",
    "d_bins": 35,
    "d_price": (5.0, 150.0),
    "d_brands": [],
    "d_categories": [],
    "d_rating": (1.0, 5.0),
    "d_x_axis": "category",      
    "d_y_axis": "price",        
    "d_color_by": "category",
    "a_sort": "love",
    "a_limit": 10,
    "a_cats": [],
    "a_brands": [],
    "a_price_range": (0.0, 300.0),
    "a_rating_range": (1.0, 5.0),
    "a_x_axis": "name",
    "a_y_axis": "love",
    "exp_cats": [],
    "exp_brands": [],
    "exp_search": "",
    "exp_x": "brand",
    "exp_y": "love",
    "exp_chart": "Treemap",
    "exp_rating": (1.0, 5.0),
    "exp_love": (0, 500000),
    "exp_price": (5.0, 300.0)
}


# Safely inject missing defaults into st.session_state
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


# Read background image dynamically if available
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


/* FIX OVER-BOLD TEXT ISSUE ONLY FOR CARD PARAGRAPHS & DESCRIPTION LINES */
.premium-card p, .premium-card li, .glass-desc, .glass-panel p {
    font-weight: 400 !important;
}


/* Restores natural rich bold styling to headers, labels, KPIs, and general elements */
h1, h2, h3, h4, h5, h6, strong, b, .main-title, .stat-val, .stat-lbl, .badge {
    font-weight: 700 !important;
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
    background-color: #F3F4F6;
    color: #1F2937;
}


/* Sidebar Pastel Pink Elegance */
section[data-testid="stSidebar"] {
    background-color: #FFE5EC !important;
    border-right: 1px solid #FFCCD5;
}


/* Glassmorphic Rounded Cards with Hover Scale & Glow Animation */
.premium-card {
    background: #FFFFFF;
    padding: 24px;
    border-radius: 20px;
    box-shadow: 0 10px 35px rgba(233, 30, 99, 0.06);
    border: 1px solid rgba(233, 30, 99, 0.22);
    margin-bottom: 20px;
    animation: fadeInUp 0.7s cubic-bezier(0.165, 0.84, 0.44, 1) both;
    transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
}


.premium-card:hover {
    transform: translateY(-4px) scale(1.005);
    box-shadow: 0 20px 50px rgba(233, 30, 99, 0.12);
    border-color: rgba(233, 30, 99, 0.45);
}


/* Sephora Signature Gradient Titles */
.main-title {
    background: linear-gradient(90deg, #E91E63 0%, #B71C1C 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
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
    border: 1px solid rgba(233, 30, 99, 0.2);
    box-shadow: 0 6px 20px rgba(233, 30, 99, 0.03);
    animation: fadeInUp 0.6s cubic-bezier(0.165, 0.84, 0.44, 1) both;
    transition: all 0.3s cubic-bezier(0.165, 0.84, 0.44, 1);
}
.stat-box:hover {
    border-color: rgba(233, 30, 99, 0.45);
    box-shadow: 0 12px 35px rgba(233, 30, 99, 0.08);
    transform: translateY(-3px);
}
.stat-val {
    font-size: 2rem;
    color: #C2185B;
}
.stat-lbl {
    font-size: 0.75rem;
    color: #374151;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 3px;
}


/* Premium Button Design with Active Glow Pulse */
.stButton>button {
    border-radius: 50px !important;
    background: linear-gradient(90deg, #E91E63 0%, #B71C1C 100%) !important;
    color: white !important;
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
    background-color: #FFE5EC;
    color: #C2185B;
    padding: 6px 16px;
    border-radius: 50px;
    font-size: 0.8rem;
    display: inline-block;
    margin-bottom: 12px;
    border: 1px solid #FFA2B6;
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
    background-color: #FFE5EC !important;
    padding: 6px 10px !important;
    border-radius: 14px !important;
    border: 1px solid #FFA2B6 !important;
    margin-top: 0px !important;
    margin-bottom: 20px !important;
    display: flex !important;
    flex-direction: row !important;
    justify-content: center !important;
}


div[role="radiogroup"] label {
    background-color: transparent !important;
    border-radius: 10px 10px 0px 0px !important;
    color: #374151 !important;
    font-size: 0.9rem !important;
    padding: 8px 16px !important;
    border: none !important;
    transition: all 0.2s ease !important;
    margin: 0 !important;
}


div[role="radiogroup"] label[data-checked="true"] {
    background-color: #FFFFFF !important;
    color: #C2185B !important;
    border-radius: 10px 10px 0px 0px !important;
    border-top: 3px solid #C2185B !important;
    box-shadow: 0 -3px 12px rgba(233, 30, 99, 0.12) !important;
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


# High Contrast Spectrum for premium visualization elements
HIGH_CONTRAST_BURGUNDY = [
    "#FFB3C1",  # Clear light pink
    "#FF4D6D",  # Warm Coral Pink
    "#E0115F",  # Brilliant Ruby Pink
    "#C2185B",  # Sephora Brand Crimson
    "#A01A40",  # Dark Crimson Berry
    "#700C25",  # Vintage Red Plum
    "#3D001B"   # Deep Royal Burgundy
]


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
<h4 style='color: #FF8A9A; margin-top: 0; font-weight: 800; font-size: 1.25rem; margin-bottom: 12px; text-align: left; text-shadow: 0 1px 4px rgba(0,0,0,0.3);'> PROJECT INTRODUCTION</h4>
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
    st.markdown("""
    <style>
    .stApp {
        background: #FAFAFB !important;
    }
    </style>
    """, unsafe_allow_html=True)


    # Sidebar Logo Header
    st.sidebar.markdown("<div style='text-align: center; padding: 10px 0;'><h2 style='color: #E91E63; font-weight: 800; margin-bottom: 0;'>SEPHORA PRODUCT ANALYSE</h2><p style='color: #880E4F; font-size: 0.8rem; letter-spacing: 2px; font-weight: 700;'>DECISION ENGINE</p></div>", unsafe_allow_html=True)
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


    # --- UNIFIED & SYNCHRONIZED SIDEBAR FILTER LAYOUT FOR PERFECT CONSISTENCY ---
    if tab_selection == "🔮 Strategy Sandbox":
        st.sidebar.markdown("### 🔮 Sandbox Filter System")
        if st.sidebar.button("🔄 Reset filters for this tab", use_container_width=True, key="reset_sandbox"):
            st.session_state.sb_brands = defaults["sb_brands"]
            st.session_state.sb_categories = defaults["sb_categories"]
            st.session_state.sb_price = defaults["sb_price"]
            st.session_state.sb_rating = defaults["sb_rating"]
            st.session_state.sb_min_reviews = defaults["sb_min_reviews"]
            st.session_state.sb_x_axis = defaults["sb_x_axis"]
            st.session_state.sb_y_axis = defaults["sb_y_axis"]
            st.rerun()


        # Part 1: Scope Filters (Brand & Category)
        brand_opt = df['brand'].value_counts().head(50).index.tolist()
        sandbox_brands = st.sidebar.multiselect("Filter Brand Segments (Multi):", options=brand_opt, default=st.session_state.sb_brands, key="sb_brands")
       
        cat_opt_sandbox = df['category'].dropna().unique().tolist()
        sandbox_categories = st.sidebar.multiselect("Filter Product Categories (Multi):", options=cat_opt_sandbox, default=st.session_state.sb_categories, key="sb_categories")
       
        # Part 2: Range Sliders (Price & Rating)
        sandbox_price_range = st.sidebar.slider("Price Target Range ($):", 5.0, 400.0, st.session_state.sb_price, key="sb_price")
        sandbox_rating_range = st.sidebar.slider("Rating Target Range (⭐):", 1.0, 5.0, st.session_state.sb_rating, step=0.1, key="sb_rating")
       
        # Part 3: Specific Parameters
        sandbox_min_reviews = st.sidebar.number_input("Minimum Reviews Count:", min_value=0, max_value=5000, value=int(st.session_state.sb_min_reviews), step=10, key="sb_min_reviews")


        # Part 4: Axis & Chart Configurations
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📊 Interactive Axis Settings")
        axis_choices = ['price', 'love', 'rating', 'number_of_reviews', 'vfm_score']
        sandbox_x_axis = st.sidebar.selectbox("Select X-Axis Metric:", options=axis_choices, index=axis_choices.index(st.session_state.sb_x_axis), key="sb_x_axis")
        sandbox_y_axis = st.sidebar.selectbox("Select Y-Axis Metric:", options=axis_choices, index=axis_choices.index(st.session_state.sb_y_axis), key="sb_y_axis")


    elif tab_selection == "📊 Customizable Price Densities":
        st.sidebar.markdown("### 📊 Density Matrix Settings")
        if st.sidebar.button("🔄 Reset filters for this tab", use_container_width=True, key="reset_density"):
            st.session_state.d_bins = defaults["d_bins"]
            st.session_state.d_price = defaults["d_price"]
            st.session_state.d_brands = defaults["d_brands"]
            st.session_state.d_categories = defaults["d_categories"]
            st.session_state.d_rating = defaults["d_rating"]
            st.session_state.d_x_axis = defaults["d_x_axis"]
            st.session_state.d_y_axis = defaults["d_y_axis"]
            st.session_state.d_color_by = defaults["d_color_by"]
            st.rerun()


        # Part 1: Scope Filters (Brand & Category)
        brand_opt_density = df['brand'].value_counts().head(40).index.tolist()
        density_brands = st.sidebar.multiselect("Select Brand Segments (Multi):", brand_opt_density, default=st.session_state.d_brands, key="d_brands")
       
        cat_opt_density = df['category'].dropna().unique().tolist()
        density_categories = st.sidebar.multiselect("Select Product Categories (Multi):", cat_opt_density, default=st.session_state.d_categories, key="d_categories")
       
        # Part 2: Range Sliders (Price & Rating)
        density_price_range = st.sidebar.slider("Retail Price Limits ($):", 5.0, 500.0, st.session_state.d_price, step=5.0, key="d_price")
        density_rating_range = st.sidebar.slider("Satisfaction Rating Range (⭐):", 1.0, 5.0, st.session_state.d_rating, step=0.1, key="d_rating")
       
        # Part 3: Specific Parameters
        bin_count = st.sidebar.slider("Adjust Bins (Granularity):", 10, 100, int(st.session_state.d_bins), key="d_bins")


        # Part 4: Axis & Chart Configurations
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📊 Matrix Style Settings")
        density_x_choices = ['category', 'brand', 'rating']
        density_x_axis = st.sidebar.selectbox("Select Grouping Axis (X-Axis):", options=density_x_choices, index=density_x_choices.index(st.session_state.d_x_axis), key="d_x_axis")
       
        density_y_choices = ['price', 'love', 'number_of_reviews', 'vfm_score']
        density_y_axis = st.sidebar.selectbox("Select Analytical Metric (Y-Axis):", options=density_y_choices, index=density_y_choices.index(st.session_state.d_y_axis), key="d_y_axis")
       
        density_color_by = st.sidebar.selectbox("Segment Color By:", options=['category', 'brand', 'rating'], index=['category', 'brand', 'rating'].index(st.session_state.d_color_by), key="d_color_by")


    elif tab_selection == "📈 Flexible Area Trend Leaders":
        st.sidebar.markdown("### 📈 Ranking Configuration")
        if st.sidebar.button("🔄 Reset filters for this tab", use_container_width=True, key="reset_leaders"):
            st.session_state.a_sort = defaults["a_sort"]
            st.session_state.a_limit = defaults["a_limit"]
            st.session_state.a_cats = defaults["a_cats"]
            st.session_state.a_brands = defaults["a_brands"]
            st.session_state.a_price_range = defaults["a_price_range"]
            st.session_state.a_rating_range = defaults["a_rating_range"]
            st.session_state.a_x_axis = defaults["a_x_axis"]
            st.session_state.a_y_axis = defaults["a_y_axis"]
            st.rerun()


        # Part 1: Scope Filters (Brand & Category)
        brand_opts_leaders = df['brand'].value_counts().head(50).index.tolist()
        leaders_brands = st.sidebar.multiselect("Select Brand Targets (Multi):", brand_opts_leaders, default=st.session_state.a_brands, key="a_brands")
       
        cat_opts = df['category'].value_counts().head(30).index.tolist()
        leaders_categories = st.sidebar.multiselect("Select Category Sectors (Multi):", cat_opts, default=st.session_state.a_cats, key="a_cats")
       
        # Part 2: Range Sliders (Price & Rating)
        leaders_price_range = st.sidebar.slider("Price Bound Target Range ($):", 0.0, 500.0, st.session_state.a_price_range, step=5.0, key="a_price_range")
        leaders_rating_range = st.sidebar.slider("Rating Target Range (⭐):", 1.0, 5.0, st.session_state.a_rating_range, step=0.1, key="a_rating_range")
       
        # Part 3: Specific Parameters
        item_limit = st.sidebar.slider("Number of Products to Show:", 5, 30, int(st.session_state.a_limit), key="a_limit")


        # Part 4: Axis & Chart Configurations
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📊 Display Configurations")
        sort_opts = ['love', 'number_of_reviews', 'price', 'rating', 'vfm_score']
        ranking_var = st.sidebar.selectbox("Sort Assortments Based On:", sort_opts, index=sort_opts.index(st.session_state.a_sort), key="a_sort")
       
        area_x_options = ['name', 'brand', 'category']
        area_x_axis = st.sidebar.selectbox("Select Area X-Axis Category:", options=area_x_options, index=area_x_options.index(st.session_state.a_x_axis), key="a_x_axis")
       
        area_y_options = ['love', 'number_of_reviews', 'price', 'rating', 'vfm_score']
        area_y_axis = st.sidebar.selectbox("Select Area Y-Axis Metric:", options=area_y_options, index=area_y_options.index(st.session_state.a_y_axis), key="a_y_axis")


    elif tab_selection == "💎 Cosmetics Explorer":
        st.sidebar.markdown("### 💎 Explorer Custom Controls")
        if st.sidebar.button("🔄 Reset filters for this tab", use_container_width=True, key="reset_explorer"):
            st.session_state.exp_cats = defaults["exp_cats"]
            st.session_state.exp_brands = defaults["exp_brands"]
            st.session_state.exp_search = defaults["exp_search"]
            st.session_state.exp_x = defaults["exp_x"]
            st.session_state.exp_y = defaults["exp_y"]
            st.session_state.exp_chart = defaults["exp_chart"]
            st.session_state.exp_rating = defaults["exp_rating"]
            st.session_state.exp_love = defaults["exp_love"]
            st.session_state.exp_price = defaults["exp_price"]
            st.rerun()


        # Part 1: Scope Filters (Brand & Category)
        brand_opts_explorer = df['brand'].dropna().unique().tolist()
        explorer_brands = st.sidebar.multiselect("Base Catalog Brands (Multi):", brand_opts_explorer, default=st.session_state.exp_brands, key="exp_brands")
       
        cat_opts_explorer = df['category'].dropna().unique().tolist()
        explorer_categories = st.sidebar.multiselect("Base Catalog Categories (Multi):", cat_opts_explorer, default=st.session_state.exp_cats, key="exp_cats")
       
        # Part 2: Range Sliders (Price & Rating)
        explorer_price_range = st.sidebar.slider("Budget Bound Target Range ($):", 5.0, 500.0, st.session_state.exp_price, step=5.0, key="exp_price")
        explorer_rating_range = st.sidebar.slider("Satisfaction Target Range (⭐):", 1.0, 5.0, st.session_state.exp_rating, step=0.1, key="exp_rating")
       
        # Part 3: Specific Parameters
        explorer_love_range = st.sidebar.slider("Customer Love Index Range:", 0, 1000000, st.session_state.exp_love, step=500, key="exp_love")
        search_kw = st.sidebar.text_input("Formula or Name Keyword search:", value=st.session_state.exp_search, key="exp_search")
       
        # Part 4: Axis & Chart Configurations
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📊 Axis & Chart Settings")
        x_opts = ['brand', 'category', 'rating', 'vfm_score']
        exp_x_val = st.session_state.exp_x if st.session_state.exp_x in x_opts else "brand"
        x_axis_var = st.sidebar.selectbox("X-Axis Selector:", x_opts, index=x_opts.index(exp_x_val), key="exp_x")
       
        y_opts = ['love', 'price', 'number_of_reviews', 'rating', 'vfm_score']
        exp_y_val = st.session_state.exp_y if st.session_state.exp_y in y_opts else "love"
        y_axis_var = st.sidebar.selectbox("Y-Axis Selector:", y_opts, index=y_opts.index(exp_y_val), key="exp_y")
       
        chart_opts = ['Treemap', 'Bar', 'Scatter']
        exp_chart_val = st.session_state.exp_chart if st.session_state.exp_chart in chart_opts else "Treemap"
        chart_type_sel = st.sidebar.selectbox("Chart Type Selector:", chart_opts, index=chart_opts.index(exp_chart_val), key="exp_chart")


    st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
    if st.sidebar.button("⬅️ Back to Start Screen", use_container_width=True):
        st.session_state.started = False
        st.rerun()




    # -------------------------------------------------------------
    # TAB 1: EXECUTIVE HOME
    # -------------------------------------------------------------
    if tab_selection == "🏠 Executive Home":
        # KPI widgets Row
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.markdown(f"<div class='stat-box'><div class='stat-val'>{df.shape[0]:,}</div><div class='stat-lbl'>Catalog Assortments</div></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='stat-box'><div class='stat-val'>{df['brand'].nunique()}</div><div class='stat-lbl'>Unique Brands</div></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='stat-box'><div class='stat-val'>${df['price'].mean():.2f}</div><div class='stat-lbl'>Average Price</div></div>", unsafe_allow_html=True)
        with c4: st.markdown(f"<div class='stat-box'><div class='stat-val'>{df['rating'].mean():.2f}⭐</div><div class='stat-lbl'>Satisfaction Score</div></div>", unsafe_allow_html=True)


        st.markdown("<br>", unsafe_allow_html=True)
       
        # Restored 2 cards with bold headers and clean, non-bold description blocks
        col_home_txt1, col_home_txt2 = st.columns(2)
        with col_home_txt1:
            st.markdown("""
            <div class='premium-card' style='height: 100%; border-right: 4.5px solid #E91E63; margin-bottom: 0px;'>
                <h3 style='margin-top: 0; color: #111827; font-size: 1.35rem;'>✨ Strategic Hub Operating Instructions</h3>
                <p style='color: #4A5568; line-height: 1.75; font-size: 0.95rem;'>
                    Welcome to the Sephora Corporate Decision Support Portal. This interface is structured to prioritize high-fidelity customizable visual layouts. The control settings on the left sidebar automatically adapt to your chosen category tab, providing an intuitive, clean, and professional workspace.
                </p>
                <p style='color: #4A5568; line-height: 1.75; font-size: 0.95rem; margin-top: 10px;'>
                    Active Functional Modules:
                </p>
                <ul style='color: #4A5568; line-height: 1.6; padding-left: 20px; font-size: 0.92rem;'>
                    <li><b>Strategy Sandbox:</b> Evaluate channelling trends across pricing, consumer ratings, and catalog love counts.</li>
                    <li><b>Price Distributions:</b> Map continuous density spectrums to discover active market segment gaps.</li>
                    <li><b>Assortment Leaders:</b> View leading items and trace audience affection concentration curves.</li>
                    <li><b>Cosmetics Explorer:</b> Enjoy analytical freedom to isolate specific brands and filter product dimensions.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
           
        with col_home_txt2:
            st.markdown("""
            <div class='premium-card' style='height: 100%; border-left: 5px solid #B71C1C; margin-bottom: 0px;'>
                <h3 style='margin-top: 0; color: #111827; font-size: 1.35rem;'>🎯 Core Strategic Objectives</h3>
                <p style='color: #4A5568; line-height: 1.6; font-size: 0.95rem; margin-bottom: 12px;'>
                    Which critical consumer benchmarks do we analyze across this dataset?
                </p>
                <ul style='font-size: 0.92rem; line-height: 1.7; color: #4A5568; padding-left: 20px; margin-bottom: 0;'>
                    <li style='margin-bottom: 8px;'><b>Optimal Price Thresholds:</b> Determining retail boundaries that optimize revenue margins while preserving high volume conversions.</li>
                    <li style='margin-bottom: 8px;'><b>Satisfaction Projections:</b> Checking if high catalog popularity ratings map directly to customer review volumes.</li>
                    <li style='margin-bottom: 8px;'><b>Catalog Assortment Footprints:</b> Evaluating retail diversity metrics across Makeup, Skincare, Fragrances, and Tools.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)


        st.markdown("<br>", unsafe_allow_html=True)
       
        # Primary Dataset Explorer Workspace
        st.markdown("### 📋 Primary Dataset Explorer Workspace")
       
        # Expander table filters
        with st.expander("🛠️ Advanced Table Filtering Options (Click to Expand)", expanded=True):
            col_filt_1, col_filt_2, col_filt_3 = st.columns(3)
            with col_filt_1:
                home_brands_filter = st.multiselect(
                    "Filter Brand (Select Multiple):",
                    options=df['brand'].dropna().unique().tolist(),
                    placeholder="All Brands (Leave empty)"
                )
               
                size_keyword = st.text_input("Filter Product Size Keyword:", placeholder="e.g. 1.7 oz, 50 ml, travel")
               
            with col_filt_2:
                home_categories_filter = st.multiselect(
                    "Filter Category (Select Multiple):",
                    options=df['category'].dropna().unique().tolist(),
                    placeholder="All Categories (Leave empty)"
                )
               
                rows_selection = st.selectbox(
                    "Max Rows to Preview:",
                    options=[10, 25, 50, 100, 250],
                    index=1
                )
               
            with col_filt_3:
                home_price_range = st.slider(
                    "Price Filter Boundary ($):",
                    min_value=0.0,
                    max_value=500.0,
                    value=(0.0, 500.0),
                    step=5.0
                )
               
                home_rating_range = st.slider(
                    "Rating Filter Boundary (⭐):",
                    min_value=1.0,
                    max_value=5.0,
                    value=(1.0, 5.0),
                    step=0.1
                )


        # Execute filtration
        preview_df = df.copy()
        if home_brands_filter:
            preview_df = preview_df[preview_df['brand'].isin(home_brands_filter)]
        if home_categories_filter:
            preview_df = preview_df[preview_df['category'].isin(home_categories_filter)]
        if size_keyword:
            size_cols = [c for c in df.columns if 'size' in c.lower()]
            if size_cols:
                preview_df = preview_df[preview_df[size_cols[0]].astype(str).str.lower().str.contains(size_keyword.lower(), na=False)]
            else:
                preview_df = preview_df[preview_df['name'].astype(str).str.lower().str.contains(size_keyword.lower(), na=False)]
               
        preview_df = preview_df[
            (preview_df['price'] >= home_price_range[0]) &
            (preview_df['price'] <= home_price_range[1])
        ]
        preview_df = preview_df[
            (preview_df['rating'] >= home_rating_range[0]) &
            (preview_df['rating'] <= home_rating_range[1])
        ]
       
        # ADDED UNIFIED LIVE INSIGHTS BANNER
        st.success(f"📈 **Live Workspace Insights:** Found **{preview_df.shape[0]}** matching listings.")
        st.dataframe(preview_df.head(rows_selection), use_container_width=True)




    # -------------------------------------------------------------
    # TAB 2: STRATEGY SANDBOX
    # -------------------------------------------------------------
    elif tab_selection == "🔮 Strategy Sandbox":
        st.markdown("<span class='badge'>INTERACTIVE EXPERIMENT</span>", unsafe_allow_html=True)
        st.markdown("<h2>Dynamic Performance & Customer Loyalty Sandbox</h2>", unsafe_allow_html=True)
       
        # Apply scope filters
        filtered_sandbox = df[
            (df['price'] >= sandbox_price_range[0]) &
            (df['price'] <= sandbox_price_range[1])
        ]
        if sandbox_brands:
            filtered_sandbox = filtered_sandbox[filtered_sandbox['brand'].isin(sandbox_brands)]
        if sandbox_categories:
            filtered_sandbox = filtered_sandbox[filtered_sandbox['category'].isin(sandbox_categories)]
           
        filtered_sandbox = filtered_sandbox[
            (filtered_sandbox['rating'] >= sandbox_rating_range[0]) &
            (filtered_sandbox['rating'] <= sandbox_rating_range[1])
        ]
        filtered_sandbox = filtered_sandbox[filtered_sandbox['number_of_reviews'] >= sandbox_min_reviews]
           
        col_plot1, col_plot2 = st.columns(2)
        with col_plot1:
            st.markdown(f"<h4>Density Heatmap: Correlation Analysis (Sephora High Contrast)</h4>", unsafe_allow_html=True)
           
            x_title = sandbox_x_axis.replace('_', ' ').title()
            y_title = sandbox_y_axis.replace('_', ' ').title()
           
            fig_density = px.density_heatmap(
                filtered_sandbox, x=sandbox_x_axis, y=sandbox_y_axis,
                marginal_x="histogram", marginal_y="histogram",
                labels={sandbox_x_axis: x_title, sandbox_y_axis: y_title},
                color_continuous_scale=HIGH_CONTRAST_BURGUNDY,
                template="simple_white"
            )
           
            # Apply crimson tone specifically to marginal histogram traces to avoid dim/pale layout
            fig_density.update_traces(marker_color='#C2185B', selector=dict(type='histogram'))
           
            fig_density.update_layout(
                paper_bgcolor='rgba(255,255,255,1)',
                plot_bgcolor='rgba(255,255,255,1)',
                font_family="Plus Jakarta Sans", margin=dict(l=10, r=10, t=30, b=10)
            )
            st.plotly_chart(fig_density, use_container_width=True)
           
        with col_plot2:
            st.markdown(f"<h4>Distribution: Product Satisfaction Star Ratings</h4>", unsafe_allow_html=True)
            fig_hist = px.histogram(
                filtered_sandbox, x=sandbox_x_axis,
                color_discrete_sequence=[SEPHORA_COLORS[3]],
                template="simple_white", opacity=0.85,
                labels={sandbox_x_axis: x_title}
            )
               
            fig_hist.update_layout(
                paper_bgcolor='rgba(255,255,255,1)',
                plot_bgcolor='rgba(255,255,255,1)',
                font_family="Plus Jakarta Sans", margin=dict(l=10, r=10, t=30, b=10)
            )
            st.plotly_chart(fig_hist, use_container_width=True)
           
        # LIVE INSIGHTS BANNER
        st.success(f"📈 **Live Sandbox Insights:** Found **{filtered_sandbox.shape[0]}** matching listings.")


        # Restored description card - Bold heading and light paragraph
        col_desc_sandbox, col_img_sandbox = st.columns([2, 1])
        with col_desc_sandbox:
            st.markdown("""
            <div class='premium-card' style='margin-bottom: 0px; height: 100%; border-left: 5px solid #C2185B;'>
                <h4 style='color: #E91E63; font-weight: 700;'>📝 Sandbox Strategic Diagnostic Analysis</h4>
                <p style='color: #4A5568; line-height:1.75; font-size: 0.95rem;'>
                    This interactive sandbox workspace illustrates how a single unified filter panel can control multiple data-driven angles. By restricting catalog assets to specified brands and categories, analysts can instantly study customer loyalty clusters (Scatter Heatmap) alongside satisfaction distribution levels (Histogram).
                </p>
                <p style='color: #4A5568; line-height:1.75; font-size: 0.95rem; margin-top: 10px;'>
                    Leveraging these connected visual summaries, brand managers can readily map <i>"sweet spots"</i> where high star rankings converge with fair retail pricing structures. This provides instant diagnostic support for portfolio expansion strategies.
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
        st.markdown("<span class='badge'>PRICING STRUCTURE MATRIX</span>", unsafe_allow_html=True)
        st.markdown("<h2>Custom Lollipop Distribution & Pricing Analytics Matrix</h2>", unsafe_allow_html=True)
       
        # Apply multiselect filters
        density_df = df[
            (df['price'] >= density_price_range[0]) &
            (df['price'] <= density_price_range[1])
        ]
        if density_brands:
            density_df = density_df[density_df['brand'].isin(density_brands)]
        if density_categories:
            density_df = density_df[density_df['category'].isin(density_categories)]
        density_df = density_df[
            (density_df['rating'] >= density_rating_range[0]) &
            (density_df['rating'] <= density_rating_range[1])
        ]
       
        if not density_df.empty:
            lollipop_data = density_df.groupby(density_x_axis)[density_y_axis].mean().reset_index()
            lollipop_data = lollipop_data.sort_values(by=density_y_axis, ascending=False).head(35)
           
            fig_lollipop = go.Figure()
           
            for i, row in lollipop_data.iterrows():
                fig_lollipop.add_shape(
                    type="line",
                    x0=row[density_x_axis], y0=0,
                    x1=row[density_x_axis], y1=row[density_y_axis],
                    line=dict(
                        color="#FF4D6D",
                        width=2.5
                    )
                )
           
            fig_lollipop.add_trace(go.Scatter(
                x=lollipop_data[density_x_axis],
                y=lollipop_data[density_y_axis],
                mode='markers',
                marker=dict(
                    color='#800F2F',
                    size=13,
                    line=dict(
                        color='#3D001B',
                        width=1.5
                    )
                ),
                name=density_y_axis.replace('_', ' ').title(),
                hoverinfo='text',
                text=[f"Segment ({density_x_axis.upper()}): {r[density_x_axis]}<br>Average {density_y_axis.replace('_', ' ').title()}: {r[density_y_axis]:.2f}" for _, r in lollipop_data.iterrows()]
            ))
           
            fig_lollipop.update_layout(
                title=f"Lollipop Analysis: Average {density_y_axis.replace('_', ' ').title()} by {density_x_axis.replace('_', ' ').title()}",
                xaxis_title=density_x_axis.replace('_', ' ').title(),
                yaxis_title=f"Average {density_y_axis.replace('_', ' ').title()}",
                paper_bgcolor='rgba(255,255,255,1)',
                plot_bgcolor='rgba(255,255,255,1)',
                font_family="Plus Jakarta Sans",
                font_color="#111827",
                margin=dict(l=10, r=10, t=50, b=10)
            )
           
            st.plotly_chart(fig_lollipop, use_container_width=True)
           
            # ADDED UNIFIED LIVE INSIGHTS BANNER
            st.success(f"📈 **Live Density Insights:** Found **{density_df.shape[0]}** matching listings.")
        else:
            st.warning("⚠️ No products match the current filter selection.")


        # Restored description card - Bold heading and light paragraph
        col_desc_densities, col_img_densities = st.columns([2, 1])
        with col_desc_densities:
            st.markdown(f"""
            <div class='premium-card' style='margin-bottom: 0px; height: 100%; border-left: 5px solid #C2185B;'>
                <h4 style='color: #B71C1C; font-weight: 700;'>📝 Pricing Segment Density Analysis</h4>
                <p style='color: #4A5568; line-height:1.75; font-size: 0.95rem;'>
                    This visual lollipop chart maps the continuous distribution density of Sephora's inventory.
                    By grouping catalog offerings based on targeted brand and category inputs, the resulting metrics pinpoint where the brand concentrates its primary market assets.
                </p>
                <p style='color: #4A5568; line-height:1.75; font-size: 0.95rem; margin-top: 10px;'>
                    Typically, high-density pricing clusters at the lower tier process mass market customer acquisitions, while high-end specialty lines carry significant retail margins.
                    Tracking these segments helps discover underserved areas in the beauty marketplace.
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
        if leaders_categories:
            area_df = area_df[area_df['category'].isin(leaders_categories)]
        if leaders_brands:
            area_df = area_df[area_df['brand'].isin(leaders_brands)]
       
        # Apply range parameters
        area_df = area_df[
            (area_df['price'] >= leaders_price_range[0]) &
            (area_df['price'] <= leaders_price_range[1])
        ]
        area_df = area_df[
            (area_df['rating'] >= leaders_rating_range[0]) &
            (area_df['rating'] <= leaders_rating_range[1])
        ]
           
        area_plot_data = area_df.sort_values(by=ranking_var, ascending=False).head(item_limit)
       
        if not area_plot_data.empty:
            fig_area = px.area(
                area_plot_data, x=area_x_axis, y=area_y_axis,
                color_discrete_sequence=[SEPHORA_COLORS[3]], template="simple_white",
                labels={area_x_axis: area_x_axis.replace('_', ' ').title(), area_y_axis: area_y_axis.replace('_', ' ').title()}
            )
            fig_area.update_layout(
                xaxis={'categoryorder':'total descending'},
                paper_bgcolor='rgba(255,255,255,1)',
                plot_bgcolor='rgba(255,255,255,1)',
                font_family="Plus Jakarta Sans", font_color="#2D3748",
                margin=dict(l=10, r=10, t=20, b=10)
            )
            st.plotly_chart(fig_area, use_container_width=True)
           
            # ADDED UNIFIED LIVE INSIGHTS BANNER
            st.success(f"📈 **Live Leader Insights:** Found **{area_df.shape[0]}** matching listings.")
        else:
            st.warning("⚠️ No products match the selected parameters in this segment.")


        # Restored description card - Bold heading and light paragraph
        col_desc_leaders, col_img_leaders = st.columns([2, 1])
        with col_desc_leaders:
            st.markdown(f"""
            <div class='premium-card' style='margin-bottom: 0px; height: 100%; border-right: 5px solid #C2185B;'>
                <h4 style='color: #E91E63; font-weight: 700;'>📝 Cumulative Assortment Area Trend Analysis</h4>
                <p style='color: #4A5568; line-height:1.75; font-size: 0.95rem;'>
                    This cumulative area visualization charts leading marketplace listings ranked by your selected priority variable.
                    The steep curves demonstrate standard <b>Power Law concentration</b> in beauty retail, where a small set of 'Hero Products' carries the vast majority of consumer engagement.
                </p>
                <p style='color: #4A5568; line-height:1.75; font-size: 0.95rem; margin-top: 10px;'>
                    Large review counts and high emotional attachment indexes point to strong viral retention.
                    Tracking these curves helps portfolio coordinators identify central products that act as natural gateways driving organic traffic to other catalog options.
                </p>
            </div>
            """, unsafe_allow_html=True)
        with col_img_leaders:
            st.image(
                "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?auto=format&fit=crop&w=600&q=80",
                caption="Professional Sephora Brush Collection",
                use_container_width=True
            )




    # -------------------------------------------------------------
    # TAB 5: COSMETICS EXPLORER
    # -------------------------------------------------------------
    elif tab_selection == "💎 Cosmetics Explorer":
        st.markdown("<span class='badge'>EXPLORATIVE ENGINE</span>", unsafe_allow_html=True)
        st.markdown("<h2>💎 Cosmetics Multidimensional Strategy Explorer</h2>", unsafe_allow_html=True)
       
        exp_df = df.copy()
        if explorer_categories:
            exp_df = exp_df[exp_df['category'].isin(explorer_categories)]
        if explorer_brands:
            exp_df = exp_df[exp_df['brand'].isin(explorer_brands)]
           
        exp_df = exp_df[
            (exp_df['rating'] >= explorer_rating_range[0]) &
            (exp_df['rating'] <= explorer_rating_range[1])
        ]
        exp_df = exp_df[
            (exp_df['price'] >= explorer_price_range[0]) &
            (exp_df['price'] <= explorer_price_range[1])
        ]
        exp_df = exp_df[
            (exp_df['love'] >= explorer_love_range[0]) &
            (exp_df['love'] <= explorer_love_range[1])
        ]
           
        if search_kw:
            search_clean = search_kw.lower()
            mask_brand = exp_df['brand'].astype(str).str.lower().str.contains(search_clean)
            mask_name = exp_df['name'].astype(str).str.lower().str.contains(search_clean)
           
            if 'ingredients' in exp_df.columns:
                mask_ing = exp_df['ingredients'].astype(str).str.lower().str.contains(search_clean)
                combined_mask = mask_brand | mask_name | mask_ing
            else:
                combined_mask = mask_brand | mask_name
               
            exp_df = exp_df[combined_mask]


        if not exp_df.empty:
            chart_data = exp_df.groupby(x_axis_var)[y_axis_var].mean().reset_index()
            chart_data = chart_data.sort_values(by=y_axis_var, ascending=False).head(30)


            if chart_type_sel == 'Treemap':
                fig_custom = px.treemap(
                    chart_data, path=[x_axis_var], values=y_axis_var,
                    color=y_axis_var, color_continuous_scale=HIGH_CONTRAST_BURGUNDY
                )
            elif chart_type_sel == 'Bar':
                fig_custom = px.bar(
                    chart_data, x=x_axis_var, y=y_axis_var,
                    color=y_axis_var, color_continuous_scale=HIGH_CONTRAST_BURGUNDY,
                    template="simple_white"
                )
            else:
                fig_custom = px.scatter(
                    exp_df.head(250), x=x_axis_var, y=y_axis_var, color='category',
                    color_discrete_sequence=SEPHORA_COLORS, template="simple_white"
                )


            fig_custom.update_layout(
                paper_bgcolor='rgba(255,255,255,1)',
                plot_bgcolor='rgba(255,255,255,1)',
                font_family="Plus Jakarta Sans", font_color="#2D3748",
                margin=dict(l=10, r=10, t=30, b=10)
            )
            st.plotly_chart(fig_custom, use_container_width=True)


            # HARMONIZED LIVE INSIGHTS BANNER
            st.success(f"📈 **Live Explorer Insights:** Found **{exp_df.shape[0]}** matching listings.")
        else:
            st.warning("⚠️ No products matching your criteria are present in our dataset.")


        # Restored description card - Bold heading and light paragraph
        st.markdown(f"""
        <div class='premium-card' style='margin-bottom: 0px;'>
            <h4 style='color: #E91E63; font-weight: 700;'>📝 Multidimensional Explorer Strategic Projections</h4>
            <p style='color: #4A5568; line-height:1.75; font-size: 0.95rem;'>
                <b>Advanced Strategy Modeling:</b> By offering customizable coordinates, this portal bridges the gap between raw datasets and executive planning.
                For example, setting the X-Axis to 'brand' and the Y-Axis to 'price' while isolating active components like 'glycol' or 'organic' immediately reveals which premium labels successfully leverage ingredient-focused marketing to justify higher pricing margins on the store floor.
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
       
        # ADDED UNIFIED LIVE INSIGHTS BANNER FOR COMPLETENESS
        st.success("📈 **Live Database Insights:** Project directory active, verified, and compiled.")


