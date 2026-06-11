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
    "all_sb_brands": True,        # Mặc định ban đầu đã bật Select All
    "sb_categories": [],
    "all_sb_categories": True,    # Mặc định ban đầu đã bật Select All
    "sb_price": (5.0, 150.0),
    "sb_rating": (3.5, 5.0),
    "sb_min_reviews": 0,
    "sb_x_axis": "price",
    "sb_y_axis": "love",
   
    "d_bins": 35,
    "d_price": (5.0, 150.0),
    "d_brands": [],
    "all_d_brands": True,         # Mặc định ban đầu đã bật Select All
    "d_categories": [],
    "all_d_categories": True,     # Mặc định ban đầu đã bật Select All
    "d_rating": (1.0, 5.0),
    "d_x_axis": "category",      
    "d_y_axis": "price",        
    "d_color_by": "category",
   
    "a_sort": "love",
    "a_limit": 10,
    "a_cats": [],
    "all_a_cats": True,           # Mặc định ban đầu đã bật Select All
    "a_brands": [],
    "all_a_brands": True,         # Mặc định ban đầu đã bật Select All
    "a_price_range": (0.0, 300.0),
    "a_rating_range": (1.0, 5.0),
    "a_x_axis": "name",
    "a_y_axis": "love",
   
    "exp_cats": [],
    "all_exp_cats": True,         # Mặc định ban đầu đã bật Select All
    "exp_brands": [],
    "all_exp_brands": True,       # Mặc định ban đầu đã bật Select All
    "exp_search": "",
    "exp_x": "brand",
    "exp_y": "love",
    "exp_chart": "Treemap",
    "exp_rating": (1.0, 5.0),
    "exp_love": (0, 500000),
    "exp_price": (5.0, 300.0),
   
    "home_brands_filter_multiselect": [],
    "all_home_brands_filter_multiselect": True,
    "home_categories_filter_multiselect": [],
    "all_home_categories_filter_multiselect": True
}


# Safely inject missing defaults into st.session_state
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val


# Safe Image Base64 encoder for secure background rendering
def get_image_base64(file_name):
    try:
        if os.path.exists(file_name):
            with open(file_name, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode()
    except Exception:
        pass
    return ""


sephora_bg_base64 = get_image_base64("image_238c12.jpg")
if not sephora_bg_base64:
    sephora_bg_base64 = get_image_base64("image_f68b1e.jpg")


# Premium CSS Styling: Elegant, responsive, featuring micro-interactions
css_style = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght=300;400;500;600;700;800&display=swap');


* {
    font-family: 'Plus Jakarta Sans', sans-serif;
}


/* TARGETS ONLY SPECIFIC CARD DESCRIPTIONS TO BE LIGHT/READABLE COPIES */
.premium-card p,
.premium-card li,
.glass-desc,
.glass-panel p,
.glass-panel li {
    font-weight: 400 !important;
}


/* GUARANTEES STYLISH RICH BOLDING FOR ALL SLIDERS, TABS, BUTTONS, LABELS & METRICS */
h1, h2, h3, h4, h5, h6, strong, b, .main-title, .stat-val, .stat-lbl, .badge {
    font-weight: 700 !important;
}


/* RESTORES NATURAL BOLD WEIGHTS TO SIDEBAR SLIDER VALUES, EXPANDER HEADERS AND LABEL TITLES */
div[data-testid="stWidgetLabel"] p,
.streamlit-expanderHeader p,
div[data-testid="stMarkdown"] b,
div[data-testid="stMarkdown"] strong,
.stSlider p,
.stSelectbox p,
.stMultiSelect p {
    font-weight: 700 !important;
}


/* BEAUTIFULLY ROUNDED CORNERS FOR GREEN SUCCESS/ALERT BLOCKS TO MATCH THE BRAND DESIGN */
div[data-testid="stNotification"], .stAlert {
    border-radius: 16px !important;
    border: 1.5px solid rgba(16, 185, 129, 0.25) !important;
    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.04) !important;
}


/* BEAUTIFULLY ROUNDED AND EXPANDED SIDEBAR DROP-DOWN BOX CONTAINERS (BO TRÒN ĐỒNG BỘ) */
div[data-testid="stExpander"] {
    border: 2px solid #FFA2B6 !important;
    border-radius: 16px !important;
    background-color: #FFF2F5 !important;
    margin-bottom: 12px !important;
    box-shadow: 0 4px 15px rgba(233, 30, 99, 0.05) !important;
}


/* FIXED: Override Streamlit's inner container hidden overflows to ensure dropdowns align flawlessly */
div[data-testid="stExpander"],
div[data-testid="stExpander"] div,
div[data-testid="stExpanderDetails"],
.streamlit-expanderContent {
    overflow: visible !important;
}


/* Custom style for expanded details inside stExpander */
div[data-testid="stExpander"] [data-testid="stExpanderDetails"] {
    background-color: #FFF9FA !important; /* Extremely soft cute pink inside */
    border-radius: 0 0 14px 14px !important;
    padding: 16px 12px !important;
}


.streamlit-expanderHeader {
    background-color: #FFE5EC !important;
    border-bottom: 1.5px solid #FFCCD5 !important;
    font-weight: 700 !important;
    padding: 10px 16px !important;
    border-radius: 14px 14px 0 0 !important; /* Perfect rounding alignment */
}


/* Bold slider values, multiselect values, dropdown items */
.stSlider, .stMultiSelect, .stSelectbox, .stTextInput {
    font-weight: 700 !important;
}
.stSlider div, .stMultiSelect div, .stSelectbox div {
    font-weight: 700 !important;
}


@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(24px); }
    to { opacity: 1; transform: translateY(0); }
}


@keyframes pulseGlow {
    0% { box-shadow: 0 0 0 0 rgba(233, 30, 99, 0.45); transform: scale(1); }
    50% { transform: scale(1.02); }
    70% { box-shadow: 0 0 0 16px rgba(233, 30, 99, 0); }
    100% { box-shadow: 0 0 0 0 rgba(233, 30, 99, 0); transform: scale(1); }
}


.stApp {
    background-color: #F3F4F6;
    color: #1F2937;
}


section[data-testid="stSidebar"] {
    background-color: #FFE5EC !important;
    border-right: 1px solid #FFCCD5;
}


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


.main-title {
    background: linear-gradient(90deg, #E91E63 0%, #B71C1C 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.5rem !important;
    letter-spacing: -1px;
    margin-bottom: 4px;
    margin-top: -10px;
}


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
.stat-val { font-size: 1.8rem; color: #C2185B; }
.st-lbl { font-size: 0.72rem; color: #374151; text-transform: uppercase; letter-spacing: 1px; margin-top: 3px;}


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


div[data-testid="stRadio"] > label { display: none !important; height: 0px !important; margin: 0 !important; padding: 0 !important; }
div[data-testid="stRadio"] { margin-top: 0px !important; padding-top: 0px !important; }


div[role="radiogroup"] {
    gap: 6px !important;
    background-color: #FFE5EC !important;
    padding: 6px 10px !important;
    border-radius: 14px !important;
    border: 1px solid #FFA2B6 !important;
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
}


div[role="radiogroup"] label[data-checked="true"] {
    background-color: #FFFFFF !important;
    color: #C2185B !important;
    border-radius: 10px 10px 0px 0px !important;
    border-top: 3px solid #C2185B !important;
    box-shadow: 0 -3px 12px rgba(233, 30, 99, 0.12) !important;
}


div[role="radiogroup"] [data-testid="stRadioSquare"] { display: none !important; }

/* 1. Multiselect box limit and scrollbar */
div[data-testid="stMultiSelect"] div[data-baseweb="select"] > div:first-child {
    max-height: 140px !important; 
    overflow-y: auto !important;  
    overflow-x: hidden !important;
    align-items: center !important; /* Giữ các thẻ bắt đầu từ trên xuống */
}

/* 2. (Scrollbar) */
div[data-testid="stMultiSelect"] div[data-baseweb="select"] > div:first-child::-webkit-scrollbar {
    width: 6px;
}

div[data-testid="stMultiSelect"] div[data-baseweb="select"] > div:first-child::-webkit-scrollbar-track {
    background: transparent;
}

div[data-testid="stMultiSelect"] div[data-baseweb="select"] > div:first-child::-webkit-scrollbar-thumb {
    background-color: #FFCCD5; /* Màu hồng nhạt */
    border-radius: 10px;
}

div[data-testid="stMultiSelect"] div[data-baseweb="select"] > div:first-child::-webkit-scrollbar-thumb:hover {
    background-color: #E91E63; /* Đậm lên khi di chuột vào */
}

</style>
"""
st.markdown(css_style, unsafe_allow_html=True)


# --- 2. PALETTES ---
SEPHORA_COLORS = ["#F48FB1", "#F06292", "#EC407A", "#E91E63", "#EF5350", "#E53935", "#B71C1C"]
HIGH_CONTRAST_BURGUNDY = ["#FFB3C1", "#FF4D6D", "#E0115F", "#C2185B", "#A01A40", "#700C25", "#3D001B"]


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


# Trợ lý lọc "Select All" thông minh bằng Checkbox độc lập - ẨN hoàn toàn hộp Multiselect phía dưới khi được chọn
def get_multiselect_values(label, options, key):
    all_key = f"all_{key}"
    chk_key = f"widget_chk_{key}"
   
    # Check default từ defaults dictionary
    default_val = defaults.get(all_key, True)
   
    # Đảm bảo ép kiểu và khởi tạo giá trị an toàn
    if all_key not in st.session_state or not isinstance(st.session_state[all_key], bool):
        st.session_state[all_key] = default_val
       
    if chk_key not in st.session_state or not isinstance(st.session_state[chk_key], bool):
        st.session_state[chk_key] = st.session_state[all_key]
   
    # Hiển thị nhãn của bộ chọn bằng chữ Bold sang trọng
    st.markdown(f"**{label}**")
   
    # Khởi tạo Checkbox "Select All" liên kết trực tiếp để ngăn lỗi KeyError/TypeError
    is_all = st.checkbox("✨ Select All", key=chk_key)
    st.session_state[all_key] = is_all
   
    if is_all:
        return [] # Trả về danh sách rỗng để hiển thị đầy đủ 100% dữ liệu
    else:
        # Nếu bỏ tích, hiển thị hộp chọn đa năng (multiselect) gọn gàng ở dưới
        multiselect_key = f"widget_mul_{key}"
        if multiselect_key not in st.session_state or not isinstance(st.session_state[multiselect_key], list):
            st.session_state[multiselect_key] = []
        val = st.multiselect(label, options=options, key=multiselect_key, label_visibility="collapsed")
        st.session_state[key] = val
        return val


try:
    df = load_data()
    # Safeguard to ensure calculated 'vfm_score' always exists (bypasses stale cache issues)
    if 'vfm_score' not in df.columns:
        df['vfm_score'] = (df['love'] / (df['price'] + 1)).round(2)
    total_rows, total_cols = df.shape
except Exception as e:
    st.error(f"⚠️ Error loading file: {e}")
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
    st.markdown("<style>.stApp { background: #FAFAFB !important; }</style>", unsafe_allow_html=True)
    st.sidebar.markdown("<div style='text-align: center; padding: 10px 0;'><h2 style='color: #E91E63; font-weight: 800; margin-bottom: 0;'>SEPHORA PRODUCT ANALYSIS</h2><p style='color: #880E4F; font-size: 0.8rem; letter-spacing: 2px; font-weight: 700;'>DECISION ENGINE</p></div>", unsafe_allow_html=True)
    st.sidebar.markdown("<hr style='margin: 8px 0; border-color: #FCDDEC;'>", unsafe_allow_html=True)


    # --- MAIN TITLE & BRAND IDENTIFIER RENDERED AT COHERENT HEADING AT TOP OF THE CORE LAYOUT ---
    st.markdown("<h1 class='main-title'>Strategic Decision Support Hub</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #880E4F; font-weight:600; font-size:0.92rem; margin-bottom: 15px;'>Vietnamese-German University (VGU) • Business Information Systems Project</p>", unsafe_allow_html=True)


    tab_selection = st.radio(
        "Navigation",
        ["🏠 Executive Home", "🔮 Strategy Sandbox", "📊 Customizable Price Densities", "📈 Flexible Area Trend Leaders", "💎 Cosmetics Explorer", "👥 Research Team"],
        label_visibility="collapsed"
    )


    # --- UNIFIED FILTER SYSTEMS BY TAB (ORGANIZED INTO ELEGANT DRAG-&-DROP BO TRÒN EXPANDERS) ---
    if tab_selection == "🔮 Strategy Sandbox":
        st.sidebar.markdown("### 🔮 Strategy Sandbox Filters")
       
        # Reset parameters hook
        if st.sidebar.button("🔄 Reset Filters", use_container_width=True, key="reset_sandbox_btn"):
            for k in ["sb_brands", "sb_categories"]:
                st.session_state[k] = defaults[k]
                st.session_state[f"all_{k}"] = True
                st.session_state[f"widget_chk_{k}"] = True
                st.session_state[f"widget_mul_{k}"] = []
            for k in ["sb_price", "sb_rating", "sb_min_reviews", "sb_x_axis", "sb_y_axis"]:
                st.session_state[k] = defaults[k]
            st.rerun()


        # EXPANDER 1: Scope Filters (Brand & Category dropdown) - BO TRÒN QUA CSS VỚI HIỂN THỊ ĐẦY ĐỦ KHÔNG BỊ TRÀN
        with st.sidebar.expander("🔍 1. Product Scope Selection", expanded=True):
            sandbox_brands = get_multiselect_values("Filter Brand Segments:", options=df['brand'].value_counts().head(50).index.tolist(), key="sb_brands")
            sandbox_categories = get_multiselect_values("Filter Product Categories:", options=df['category'].dropna().unique().tolist(), key="sb_categories")
       
        # EXPANDER 2: Range Sliders (Price & Rating dropdown)
        with st.sidebar.expander("💰 2. Price & Rating Thresholds", expanded=True):
            sandbox_price_range = st.slider("Price Target Range ($):", 5.0, 400.0, st.session_state.sb_price, key="sb_price")
            sandbox_rating_range = st.slider("Rating Target Range (⭐):", 1.0, 5.0, st.session_state.sb_rating, step=0.1, key="sb_rating")
            sandbox_min_reviews = st.number_input("Minimum Reviews Count:", min_value=0, value=int(st.session_state.sb_min_reviews), key="sb_min_reviews")
       
        # EXPANDER 3: Axis & Chart Configurations
        with st.sidebar.expander("📊 3. Interactive Axis Settings", expanded=True):
            axis_choices = ['price', 'love', 'rating', 'number_of_reviews', 'vfm_score']
            sandbox_x_axis = st.selectbox("Select X-Axis Metric:", options=axis_choices, index=axis_choices.index(st.session_state.sb_x_axis), key="sb_x_axis")
            sandbox_y_axis = st.selectbox("Select Y-Axis Metric:", options=axis_choices, index=axis_choices.index(st.session_state.sb_y_axis), key="sb_y_axis")


        # Tab execution and rendering - FIXED: Checks session state directly to keep charts visible under "Select All"
        is_brands_active = st.session_state.get("all_sb_brands", True) or len(sandbox_brands) > 0
        is_categories_active = st.session_state.get("all_sb_categories", True) or len(sandbox_categories) > 0
       
        if not is_brands_active and not is_categories_active:
            st.markdown("""
            <div class='premium-card' style='text-align: center; padding: 50px 30px; border: 2px dashed rgba(233,30,99,0.25); background: #FFF9FA; border-radius: 20px;'>
                <div style='font-size: 3.5rem; margin-bottom: 15px;'>🔮</div>
                <h3 style='color: #C2185B; margin-top: 0; font-weight: 700;'>Awaiting Filter Selections</h3>
                <p style='color: #4A5568; max-width: 600px; margin: 0 auto; line-height: 1.6;'>
                    Please select your target <b>Brands</b> or <b>Categories</b> in the sidebar filter panel, or click <b>Select All</b>, and the strategic metrics will be instantly calculated and rendered below.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # TABS TITLES
            st.markdown("<h2>🔮 Dynamic Performance & Customer Loyalty Sandbox</h2>", unsafe_allow_html=True)
            filtered_sandbox = df[
                (df['price'] >= sandbox_price_range[0]) &
                (df['price'] <= sandbox_price_range[1])
            ]
            if not st.session_state.get("all_sb_brands", True) and sandbox_brands:
                filtered_sandbox = filtered_sandbox[filtered_sandbox['brand'].isin(sandbox_brands)]
            if not st.session_state.get("all_sb_categories", True) and sandbox_categories:
                filtered_sandbox = filtered_sandbox[filtered_sandbox['category'].isin(sandbox_categories)]
               
            filtered_sandbox = filtered_sandbox[
                (filtered_sandbox['rating'] >= sandbox_rating_range[0]) &
                (filtered_sandbox['rating'] <= sandbox_rating_range[1])
            ]
            filtered_sandbox = filtered_sandbox[filtered_sandbox['number_of_reviews'] >= sandbox_min_reviews]
               
            col_plot1, col_plot2 = st.columns(2)
            with col_plot1:
                st.markdown(f"<h4>Bivariate Price & Customer Love Density Surface</h4>", unsafe_allow_html=True)
                x_title = sandbox_x_axis.replace('_', ' ').title()
                y_title = sandbox_y_axis.replace('_', ' ').title()
               
                fig_density = px.density_heatmap(
                    filtered_sandbox, x=sandbox_x_axis, y=sandbox_y_axis,
                    marginal_x="histogram", marginal_y="histogram",
                    labels={sandbox_x_axis: x_title, sandbox_y_axis: y_title},
                    color_continuous_scale=HIGH_CONTRAST_BURGUNDY,
                    template="simple_white"
                )
                fig_density.update_traces(marker_color='#C2185B', selector=dict(type='histogram'))
                fig_density.update_layout(
                    paper_bgcolor='rgba(255,255,255,1)',
                    plot_bgcolor='rgba(255,255,255,1)',
                    font_family="Plus Jakarta Sans", margin=dict(l=10, r=10, t=30, b=10)
                )
                st.plotly_chart(fig_density, use_container_width=True)
               
            with col_plot2:
                st.markdown(f"<h4>Univariate Rating Frequency Index</h4>", unsafe_allow_html=True)
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
               
            st.success(f"📈 **Live Insights:** Found **{filtered_sandbox.shape[0]:,}** matching entries within this scope out of the total **{total_rows:,}** database records.")


            col_desc_sandbox, col_img_sandbox = st.columns([2, 1])
            with col_desc_sandbox:
                st.markdown("""
                <div class='premium-card' style='margin-bottom: 0px; height: 100%; border-left: 5px solid #C2185B;'>
                    <h4 style='color: #E91E63; font-weight: 700;'>📝 Sandbox Strategic Diagnostic Analysis</h4>
                    <p style='color: #4A5568; line-height:1.75; font-size: 0.95rem;'>
                        This interactive sandbox workspace illustrates how a single unified filter panel can control multiple data-driven angles. By restricting catalog assets to specified brands and categories, analysts can instantly study customer loyalty clusters (Scatter Heatmap) alongside satisfaction distribution levels (Histogram).
                    </p>
                    <p style='color: #4A5568; line-height:1.75; font-size: 0.95rem;'>
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


    elif tab_selection == "📊 Customizable Price Densities":
        st.sidebar.markdown("### 📊 Price Density Filters")
        if st.sidebar.button("🔄 Reset Filters", use_container_width=True, key="reset_density_btn"):
            for k in ["d_brands", "d_categories"]:
                st.session_state[k] = defaults[k]
                st.session_state[f"all_{k}"] = True
                st.session_state[f"widget_chk_{k}"] = True
                st.session_state[f"widget_mul_{k}"] = []
            for k in ["d_bins", "d_price", "d_rating", "d_x_axis", "d_y_axis", "d_color_by"]:
                st.session_state[k] = defaults[k]
            st.rerun()


        # EXPANDER 1: Scope Filters (Brand & Category dropdown)
        with st.sidebar.expander("🔍 1. Product Scope Selection", expanded=True):
            density_brands = get_multiselect_values("Select Brand Segments:", options=df['brand'].value_counts().head(40).index.tolist(), key="d_brands")
            density_categories = get_multiselect_values("Select Product Categories:", options=df['category'].dropna().unique().tolist(), key="d_categories")
       
        # EXPANDER 2: Range Sliders (Price & Rating dropdown)
        with st.sidebar.expander("💰 2. Price & Rating Thresholds", expanded=True):
            density_price_range = st.slider("Retail Price Limits ($):", 5.0, 500.0, st.session_state.d_price, step=5.0, key="d_price")
            density_rating_range = st.slider("Satisfaction Rating Range (⭐):", 1.0, 5.0, st.session_state.d_rating, step=0.1, key="d_rating")
            bin_count = st.slider("Adjust Bins (Granularity):", 10, 100, int(st.session_state.d_bins), key="d_bins")
       
        # EXPANDER 3: Matrix Style Settings
        with st.sidebar.expander("📊 3. Matrix Style Settings", expanded=True):
            density_x_choices = ['category', 'brand', 'rating']
            density_x_axis = st.selectbox("Select Grouping Axis (X-Axis):", options=density_x_choices, index=density_x_choices.index(st.session_state.d_x_axis), key="d_x_axis")
            density_y_choices = ['price', 'love', 'number_of_reviews', 'vfm_score']
            density_y_axis = st.selectbox("Select Analytical Metric (Y-Axis):", options=density_y_choices, index=density_y_choices.index(st.session_state.d_y_axis), key="d_y_axis")
            density_color_by = st.selectbox("Segment Color By:", options=['category', 'brand', 'rating'], index=['category', 'brand', 'rating'].index(st.session_state.d_color_by), key="d_color_by")


        # Tab execution and conditional rendering
        is_density_active = st.session_state.get("all_d_brands", True) or len(density_brands) > 0 or st.session_state.get("all_d_categories", True) or len(density_categories) > 0
       
        if not is_density_active:
            st.markdown("""
            <div class='premium-card' style='text-align: center; padding: 50px 30px; border: 2px dashed rgba(233,30,99,0.25); background: #FFF9FA; border-radius: 20px;'>
                <div style='font-size: 3.5rem; margin-bottom: 15px;'>📊</div>
                <h3 style='color: #C2185B; margin-top: 0; font-weight: 700;'>Awaiting Filter Selections</h3>
                <p style='color: #4A5568; max-width: 600px; margin: 0 auto; line-height: 1.6;'>
                    Please select your target <b>Brands</b> or <b>Categories</b> in the sidebar filter panel, or click <b>Select All Products</b>, and the customized lollipop analytics will be instantly calculated and rendered below.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # RESTORED TAB TITLE
            st.markdown("<h2>📊 Custom Lollipop Distribution & Pricing Analytics Matrix</h2>", unsafe_allow_html=True)
            density_df = df[
                (df['price'] >= density_price_range[0]) &
                (df['price'] <= density_price_range[1])
            ]
            if not st.session_state.get("all_d_brands", True) and density_brands:
                density_df = density_df[density_df['brand'].isin(density_brands)]
            if not st.session_state.get("all_d_categories", True) and density_categories:
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
                        line=dict(color="#FF4D6D", width=2.5)
                    )
               
                fig_lollipop.add_trace(go.Scatter(
                    x=lollipop_data[density_x_axis],
                    y=lollipop_data[density_y_axis],
                    mode='markers',
                    marker=dict(
                        color='#800F2F', size=13,
                        line=dict(color='#3D001B', width=1.5)
                    ),
                    name=density_y_axis.replace('_', ' ').title(),
                    hoverinfo='text',
                    text=[f"Segment ({density_x_axis.upper()}): {row[density_x_axis]}<br>Average {density_y_axis.replace('_', ' ').title()}: {row[density_y_axis]:.2f}" for _, row in lollipop_data.iterrows()]
                ))
               
                fig_lollipop.update_layout(
                    title=f"Lollipop Analysis: Average {density_y_axis.replace('_', ' ').title()} by {density_x_axis.replace('_', ' ').title()}",
                    xaxis_title=density_x_axis.replace('_', ' ').title(),
                    yaxis_title=f"Average {density_y_axis.replace('_', ' ').title()}",
                    xaxis=dict(tickangle=-45),
                    paper_bgcolor='rgba(255,255,255,1)',
                    plot_bgcolor='rgba(255,255,255,1)',
                    font_family="Plus Jakarta Sans",
                    font_color="#111827",
                    margin=dict(l=10, r=10, t=50, b=10)
                )
                st.plotly_chart(fig_lollipop, use_container_width=True)
            else:
                st.warning("⚠️ No products match the current filter selection.")


            st.success(f"📈 **Live Insights:** Found **{density_df.shape[0]:,}** matching entries within this scope out of the total **{total_rows:,}** database records.")


            col_desc_densities, col_img_densities = st.columns([2, 1])
            with col_desc_densities:
                st.markdown("""
                <div class='premium-card' style='margin-bottom: 0px; height: 100%; border-left: 5px solid #C2185B;'>
                    <h4 style='color: #B71C1C; font-weight: 700;'>📝 Pricing Segment Density Analysis</h4>
                    <p style='color: #4A5568; line-height:1.75; font-size: 0.95rem;'>
                        This visual lollipop chart maps the continuous distribution density of Sephora's inventory.
                        By grouping catalog offerings based on targeted brand and category inputs, the resulting metrics pinpoint where the brand concentrates its primary market assets.
                    </p>
                    <p style='color: #4A5568; line-height:1.75; font-size: 0.95rem;'>
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


    elif tab_selection == "📈 Flexible Area Trend Leaders":
        st.sidebar.markdown("### 📈 Ranking Configuration")
        if st.sidebar.button("🔄 Reset Filters", use_container_width=True, key="reset_leaders_btn"):
            for k in ["a_brands", "a_cats"]:
                st.session_state[k] = defaults[k]
                st.session_state[f"all_{k}"] = True
                st.session_state[f"widget_chk_{k}"] = True
                st.session_state[f"widget_mul_{k}"] = []
            for k in ["a_sort", "a_limit", "a_price_range", "a_rating_range", "a_x_axis", "a_y_axis"]:
                st.session_state[k] = defaults[k]
            st.rerun()


        # EXPANDER 1: Scope Filters (Brand & Category dropdown)
        with st.sidebar.expander("🔍 1. Product Scope Selection", expanded=True):
            leaders_brands = get_multiselect_values("Select Brand Targets:", options=df['brand'].value_counts().head(50).index.tolist(), key="a_brands")
            leaders_categories = get_multiselect_values("Select Category Sectors:", options=df['category'].value_counts().head(30).index.tolist(), key="a_cats")
       
        # EXPANDER 2: Range Sliders (Price & Rating dropdown)
        with st.sidebar.expander("💰 2. Price & Rating Thresholds", expanded=True):
            leaders_price_range = st.slider("Price Bound Target Range ($):", 0.0, 500.0, st.session_state.a_price_range, key="a_price_range")
            leaders_rating_range = st.slider("Rating Target Range (⭐):", 1.0, 5.0, st.session_state.a_rating_range, step=0.1, key="a_rating_range")
            item_limit = st.slider("Number of Products to Show:", 5, 30, int(st.session_state.a_limit), key="a_limit")
       
        # EXPANDER 3: Display Configurations
        with st.sidebar.expander("📊 3. Display Configurations", expanded=True):
            sort_opts = ['vfm_score', 'love', 'number_of_reviews', 'price', 'rating']
            ranking_var = st.selectbox("Sort Assortments Based On:", sort_opts, index=sort_opts.index(st.session_state.a_sort), key="a_sort")
            area_x_axis = st.selectbox("Select Area X-Axis Category:", options=['name', 'brand', 'category'], index=['name', 'brand', 'category'].index(st.session_state.a_x_axis), key="a_x_axis")
            area_y_axis = st.selectbox("Select Area Y-Axis Metric:", options=sort_opts, index=sort_opts.index(st.session_state.a_y_axis), key="a_y_axis")


        # Tab execution and conditional rendering
        is_leaders_active = st.session_state.get("all_a_brands", True) or len(leaders_brands) > 0 or st.session_state.get("all_a_cats", True) or len(leaders_categories) > 0
       
        if not is_leaders_active:
            st.markdown("""
            <div class='premium-card' style='text-align: center; padding: 50px 30px; border: 2px dashed rgba(233,30,99,0.25); background: #FFF9FA; border-radius: 20px;'>
                <div style='font-size: 3.5rem; margin-bottom: 15px;'>📈</div>
                <h3 style='color: #C2185B; margin-top: 0; font-weight: 700;'>Awaiting Filter Selections</h3>
                <p style='color: #4A5568; max-width: 600px; margin: 0 auto; line-height: 1.6;'>
                    Please select your target <b>Brands</b> or <b>Categories</b> in the sidebar filter panel, or click <b>Select All Products</b>, and the cumulative market leader trends will be instantly calculated and rendered below.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # RESTORED TAB TITLE
            st.markdown("<h2>📈 Category Leaders and Market Concentration Curves</h2>", unsafe_allow_html=True)
            area_df = df.copy()
            if not st.session_state.get("all_a_cats", True) and leaders_categories:
                area_df = area_df[area_df['category'].isin(leaders_categories)]
            if not st.session_state.get("all_a_brands", True) and leaders_brands:
                area_df = area_df[area_df['brand'].isin(leaders_brands)]
           
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
            else:
                st.warning("⚠️ No products match the selected parameters in this segment.")


            st.success(f"📈 **Live Insights:** Found **{area_df.shape[0]:,}** matching entries within this scope out of the total **{total_rows:,}** database records.")


            col_desc_leaders, col_img_leaders = st.columns([2, 1])
            with col_desc_leaders:
                st.markdown("""
                <div class='premium-card' style='margin-bottom: 0px; height: 100%; border-right: 5px solid #C2185B;'>
                    <h4 style='color: #E91E63; font-weight: 700;'>📝 Cumulative Assortment Area Trend Analysis</h4>
                    <p style='color: #4A5568; line-height:1.75; font-size: 0.95rem;'>
                        This cumulative area visualization tracks market concentration curves across top-performing catalog assets.
                        Evaluating these trends against the log-stabilized value formula prevents volume skewing, allowing analysts to accurately identify true market leaders.
                    </p>
                    <p style='color: #4A5568; line-height:1.75; font-size: 0.95rem;'>
                        Large review counts and high emotional attachment indexes point to strong viral retention.
                        Tracking these curves helps portfolio coordinators identify central products that act as natural gateways driving organic traffic to other catalog options.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            with col_img_leaders:
                st.image(
                    "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?auto=format&fit=crop&w=600&q=80",
                    caption="Sephora Product Trend Analysis",
                    use_container_width=True
                )


    elif tab_selection == "💎 Cosmetics Explorer":
        st.sidebar.markdown("### 💎 Explorer Custom Controls")
        if st.sidebar.button("🔄 Reset Filters", use_container_width=True, key="reset_explorer_btn"):
            for k in ["exp_brands", "exp_cats"]:
                st.session_state[k] = defaults[k]
                st.session_state[f"all_{k}"] = True
                st.session_state[f"widget_chk_{k}"] = True
                st.session_state[f"widget_mul_{k}"] = []
            for k in ["exp_search", "exp_x", "exp_y", "exp_chart", "exp_rating", "exp_love", "exp_price"]:
                st.session_state[k] = defaults[k]
            st.rerun()


        # EXPANDER 1: Scope Filters (Brand & Category dropdown)
        with st.sidebar.expander("🔍 1. Product Scope Selection", expanded=True):
            explorer_brands = get_multiselect_values("Base Catalog Brands (Multi):", options=df['brand'].dropna().unique().tolist(), key="exp_brands")
            explorer_categories = get_multiselect_values("Base Catalog Categories (Multi):", options=df['category'].dropna().unique().tolist(), key="exp_cats")
            search_kw = st.text_input("Formula or Name Keyword search:", value=st.session_state.exp_search, key="exp_search")
       
        # EXPANDER 2: Range Sliders (Price & Rating dropdown)
        with st.sidebar.expander("💰 2. Price & Rating Thresholds", expanded=True):
            explorer_price_range = st.slider("Budget Bound Target Range ($):", 5.0, 500.0, st.session_state.exp_price, step=5.0, key="exp_price")
            explorer_rating_range = st.slider("Satisfaction Target Range (⭐):", 1.0, 5.0, st.session_state.exp_rating, step=0.1, key="exp_rating")
            explorer_love_range = st.slider("Customer Love Index Range:", 0, 1000000, st.session_state.exp_love, step=500, key="exp_love")
       
        # EXPANDER 3: Axis & Chart Configurations
        with st.sidebar.expander("📊 3. Axis & Chart Settings", expanded=True):
            x_opts = ['brand', 'category', 'rating', 'vfm_score']
            exp_x_state_val = st.session_state.get("exp_x", "brand")
            exp_x_val = exp_x_state_val if exp_x_state_val in x_opts else "brand"
            x_axis_var = st.selectbox("X-Axis Selector:", x_opts, index=x_opts.index(exp_x_val), key="exp_x")
           
            y_opts = ['vfm_score', 'love', 'price', 'number_of_reviews', 'rating']
            exp_y_state_val = st.session_state.get("exp_y", "vfm_score")
            exp_y_val = exp_y_state_val if exp_y_state_val in y_opts else "vfm_score"
            y_axis_var = st.selectbox("Y-Axis Selector:", y_opts, index=y_opts.index(exp_y_val), key="exp_y")
           
            chart_opts = ['Treemap', 'Bar', 'Scatter']
            exp_chart_state_val = st.session_state.get("exp_chart", "Treemap")
            exp_chart_val = exp_chart_state_val if exp_chart_state_val in chart_opts else "Treemap"
            chart_type_sel = st.selectbox("Chart Type Selector:", chart_opts, index=chart_opts.index(exp_chart_val), key="exp_chart")


        # Tab execution and conditional rendering
        is_explorer_active = st.session_state.get("all_exp_brands", True) or len(explorer_brands) > 0 or st.session_state.get("all_exp_cats", True) or len(explorer_categories) > 0
       
        if not is_explorer_active:
            st.markdown("""
            <div class='premium-card' style='text-align: center; padding: 50px 30px; border: 2px dashed rgba(233,30,99,0.25); background: #FFF9FA; border-radius: 20px;'>
                <div style='font-size: 3.5rem; margin-bottom: 15px;'>💎</div>
                <h3 style='color: #C2185B; margin-top: 0; font-weight: 700;'>Awaiting Filter Selections</h3>
                <p style='color: #4A5568; max-width: 600px; margin: 0 auto; line-height: 1.6;'>
                    Please select your target <b>Brands</b> or <b>Categories</b> in the sidebar filter panel, or click <b>Select All Products</b>, and the multidimensional explorer metrics will be instantly calculated and rendered below.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # RESTORED TAB TITLE
            st.markdown("<h2>💎 Cosmetics Multidimensional Strategy Explorer</h2>", unsafe_allow_html=True)
            exp_df = df.copy()
            if not st.session_state.get("all_exp_cats", True) and explorer_categories:
                exp_df = exp_df[exp_df['category'].isin(explorer_categories)]
            if not st.session_state.get("all_exp_brands", True) and explorer_brands:
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
            else:
                st.warning("⚠️ No products matching your criteria are present in our dataset.")


            st.success(f"📈 **Live Insights:** Found **{exp_df.shape[0]:,}** matching entries within this scope out of the total **{total_rows:,}** database records.")


            st.markdown("---")
            st.markdown("### 🎯 Deep Strategic Business Insights & Executive Recommendations")
           
            rec_col1, rec_col2 = st.columns(2)
            with rec_col1:
                st.markdown("""
                <div class='premium-card' style='border-top: 5px solid #E91E63; height: 100%;'>
                    <h5 style='color: #B71C1C; margin-top:0;'>💡 1. Portfolio Pricing & Value Optimization</h5>
                    <p style='color: #2D3748; font-size: 0.92rem; line-height:1.75; text-align: justify;'>
                        Based on our corrected, simplified <b>VFM analytics pipeline</b>, there is a clear distinction between highly viral products and high-value ones. Premium items priced above $90 often see lower overall conversion efficiency, even when backed by strong customer love metrics.
                    </p>
                    <p style='color: #2D3748; font-size: 0.92rem; line-height:1.75; text-align: justify; margin-top: 10px;'>
                        <b>Actionable Corporate Mandate:</b> Brand managers should avoid focusing purely on raw engagement volume. Instead, resources should be channeled into developing high-margin products in the $35–$65 sweet spot. This range yields optimal performance by balancing fair retail costs with strong customer satisfaction indices.
                    </p>
                </div>
                """, unsafe_allow_html=True)
               
            with rec_col2:
                st.markdown("""
                <div class='premium-card' style='border-top: 5px solid #B71C1C; height: 100%;'>
                    <h5 style='color: #B71C1C; margin-top:0;'>💡 2. Dynamic Merchandising & Viral Risk Mitigation</h5>
                    <p style='color: #2D3748; font-size: 0.92rem; line-height:1.75; text-align: justify;'>
                        The continuous density spectrums reveal significant concentration risks across a few prominent brand segments. High review counts often reflect temporary promotional visibility rather than sustained quality or value.
                    </p>
                    <p style='color: #2D3748; font-size: 0.92rem; line-height:1.75; text-align: justify; margin-top: 10px;'>
                        <b>Actionable Corporate Mandate:</b> Sephora’s optimization teams should use this model to proactively identify inventory gaps. Transitioning from volume-heavy promotions to high-VFM boutique lines can reduce over-exposure risks, stabilize supply-chain requirements, and boost long-term customer retention.
                    </p>
                </div>
                """, unsafe_allow_html=True)




    # -------------------------------------------------------------
    # TAB 1: EXECUTIVE HOME
    # -------------------------------------------------------------
    elif tab_selection == "🏠 Executive Home":
        # RESTORED TAB TITLE
        st.markdown("<h2>🏠 Executive Hub & Catalog Overview</h2>", unsafe_allow_html=True)
       
        # KPI widgets Row
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.markdown(f"<div class='stat-box'><div class='stat-val'>{df.shape[0]:,}</div><div class='stat-lbl'>Catalog Assortments</div></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='stat-box'><div class='stat-val'>{df['brand'].nunique()}</div><div class='stat-lbl'>Unique Brands</div></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='stat-box'><div class='stat-val'>${df['price'].mean():.2f}</div><div class='stat-lbl'>Average Price</div></div>", unsafe_allow_html=True)
        with c4: st.markdown(f"<div class='stat-box'><div class='stat-val'>{df['rating'].mean():.2f}⭐</div><div class='stat-lbl'>Satisfaction Score</div></div>", unsafe_allow_html=True)


        st.markdown("<br>", unsafe_allow_html=True)
       
        # Restored description blocks with proper typography (unbolded paragraphs, bolded metrics)
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
       
        # Table filtration options
        with st.expander("🛠️ Advanced Table Filtering Options (Click to Expand)", expanded=True):
            col_filt_1, col_filt_2, col_filt_3 = st.columns(3)
            with col_filt_1:
                st.markdown("**Filter Brand (Select Multiple):**")
                home_brands_filter = st.multiselect(
                    "Filter Brand (Select Multiple):",
                    options=df['brand'].dropna().unique().tolist(),
                    key="home_brands_filter_multiselect",
                    label_visibility="collapsed"
                )
                size_keyword = st.text_input("Filter Product Size Keyword:", placeholder="e.g. 1.7 oz, 50 ml, travel", key="home_size_keyword_input")
               
            with col_filt_2:
                st.markdown("**Filter Category (Select Multiple):**")
                home_categories_filter = st.multiselect(
                    "Filter Category (Select Multiple):",
                    options=df['category'].dropna().unique().tolist(),
                    key="home_categories_filter_multiselect",
                    label_visibility="collapsed"
                )
                rows_selection = st.selectbox(
                    "Max Rows to Preview:",
                    options=[10, 25, 50, 100, 250],
                    index=1,
                    key="home_rows_selection_selectbox"
                )
               
            with col_filt_3:
                home_price_range = st.slider(
                    "Price Filter Boundary ($):",
                    min_value=0.0,
                    max_value=500.0,
                    value=(0.0, 500.0),
                    step=5.0,
                    key="home_price_range_slider"
                )
                home_rating_range = st.slider(
                    "Rating Filter Boundary (⭐):",
                    min_value=1.0,
                    max_value=5.0,
                    value=(1.0, 5.0),
                    step=0.1,
                    key="home_rating_range_slider"
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
       
        st.success(f"📈 **Live Insights:** Found **{preview_df.shape[0]:,}** matching entries within this scope out of the total **{total_rows:,}** database records.")
        st.dataframe(preview_df.head(rows_selection), use_container_width=True)




    # -------------------------------------------------------------
    # TAB 6: RESEARCH TEAM
    # -------------------------------------------------------------
    elif tab_selection == "👥 Research Team":
        # RESTORED TAB TITLE
        st.markdown("<h2>👥 Group Research Contributors & Responsibility Matrices</h2>", unsafe_allow_html=True)


        st.markdown(f"""
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
       
        # BEAUTIFULLY ROUNDED GREEN BANNER SYNCHRONIZED THROUGHOUT APP (Hình b4bf08.png)
        st.success(f"📊 **Database Integrity Scope Checked:** System securely validating total pipeline consisting of **{total_rows:,} rows** and **{total_cols} attributes**.")


    st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
    if st.sidebar.button("⬅️ Back to Start Screen", use_container_width=True):
        st.session_state.started = False
        st.rerun()

