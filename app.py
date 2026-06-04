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


# Khởi tạo Session State để theo dõi phiên làm việc
if 'started' not in st.session_state:
    st.session_state.started = False


# Khai báo các giá trị mặc định cho Session State để tránh xung đột khi nhấn Reset
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


# Nạp các cấu hình mặc định vào hệ thống state
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val


# Hàm mã hóa ảnh sang Base64 để hiển thị làm nền mượt mà
def get_image_base64(file_name):
    try:
        if os.path.exists(file_name):
            with open(file_name, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode()
    except Exception:
        pass
    return ""


# Tải ảnh nền trực tiếp từ tệp cục bộ
sephora_bg_base64 = get_image_base64("image_238c12.jpg")
if not sephora_bg_base64:
    sephora_bg_base64 = get_image_base64("image_f68b1e.jpg")


# CSS tạo dựng kiểu dáng: Tích hợp hiệu ứng chuyển động mượt mà, màu sắc đậm đà rõ nét
css_style = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght=300;400;500;600;700;800&display=swap');


* {
    font-family: 'Plus Jakarta Sans', sans-serif;
}


/* Hiệu ứng chuyển động mượt mà */
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


/* Màu nền của ứng dụng - đậm đà và tương phản sắc nét hơn */
.stApp {
    background-color: #F3F4F6;
    color: #111827;
}


/* Sidebar Pastel Pink Elegance */
section[data-testid="stSidebar"] {
    background-color: #FFE5EC !important;
    border-right: 1px solid #FFCCD5;
}


/* Thẻ Glassmorphic Card cao cấp - viền đậm và bóng đổ rõ nét */
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


/* Tiêu đề lớn dải màu Sephora */
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


/* Các chỉ số KPI (Metric Widgets) */
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
    font-weight: 800;
    color: #C2185B;
}
.stat-lbl {
    font-size: 0.75rem;
    color: #374151;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 3px;
}


/* Thiết kế nút bấm khởi động */
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
    background-color: #FFE5EC;
    color: #C2185B;
    padding: 6px 16px;
    border-radius: 50px;
    font-weight: 800;
    font-size: 0.8rem;
    display: inline-block;
    margin-bottom: 12px;
    border: 1px solid #FFA2B6;
}


/* Ẩn nhãn radio điều hướng mặc định */
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


/* Định dạng thanh thực đơn ngang giống Google Chrome Tabs */
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
    font-weight: 700 !important;
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


/* Ẩn dấu radio tròn mặc định */
div[role="radiogroup"] [data-testid="stRadioSquare"] {
    display: none !important;
}
</style>
"""
st.markdown(css_style, unsafe_allow_html=True)


# --- 2. THE BRAND COLOR PALETTE (GRADIENT PINK-TO-RED SEPHORA) ---
SEPHORA_COLORS = ["#F48FB1", "#F06292", "#EC407A", "#E91E63", "#EF5350", "#E53935", "#B71C1C"]


# Phổ màu siêu đậm đà, độ tương phản cao, làm sâu sắc dải hồng và đỏ mận, loại bỏ hiện tượng nhạt nhòa
HIGH_CONTRAST_BURGUNDY = [
    "#FFB3C1",  # Hồng nhạt rõ ràng
    "#FF4D6D",  # Hồng san hô đậm
    "#E0115F",  # Hồng Ruby sang trọng
    "#C2185B",  # Hồng mận Sephora
    "#A01A40",  # Đỏ Crimson sẫm
    "#700C25",  # Đỏ mận chín
    "#3D001B"   # Đỏ đen Burgundy vương giả
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
    st.sidebar.markdown("<div style='text-align: center; padding: 10px 0;'><h2 style='color: #E91E63; font-weight: 800; margin-bottom: 0;'>SEPHORA PRODUCT ANALYSIS</h2><p style='color: #880E4F; font-size: 0.8rem; letter-spacing: 2px; font-weight: 700;'>DECISION ENGINE</p></div>", unsafe_allow_html=True)
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


    # --- 6. UNIFIED & SYNCHRONIZED SIDEBAR FILTER LAYOUT FOR PERFECT CONSISTENCY ---
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


        # Synchronized Order Part 1: Scope Filters (Brand & Category)
        brand_opt = df['brand'].value_counts().head(50).index.tolist()
        sandbox_brands = st.sidebar.multiselect("Filter Brand Segments (Multi):", options=brand_opt, default=st.session_state.sb_brands, key="sb_brands")
       
        cat_opt_sandbox = df['category'].dropna().unique().tolist()
        sandbox_categories = st.sidebar.multiselect("Filter Product Categories (Multi):", options=cat_opt_sandbox, default=st.session_state.sb_categories, key="sb_categories")
       
        # Synchronized Order Part 2: Range Sliders (Price & Rating)
        sandbox_price_range = st.sidebar.slider("Price Target Range ($):", 5.0, 400.0, st.session_state.sb_price, key="sb_price")
        sandbox_rating_range = st.sidebar.slider("Rating Target Range (⭐):", 1.0, 5.0, st.session_state.sb_rating, step=0.1, key="sb_rating")
       
        # Synchronized Order Part 3: Specific Parameters
        sandbox_min_reviews = st.sidebar.number_input("Minimum Reviews Count:", min_value=0, max_value=5000, value=int(st.session_state.sb_min_reviews), step=10, key="sb_min_reviews")


        # Synchronized Order Part 4: Axis & Chart Configurations
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


        # Synchronized Order Part 1: Scope Filters (Brand & Category)
        brand_opt_density = df['brand'].value_counts().head(40).index.tolist()
        density_brands = st.sidebar.multiselect("Select Brand Segments (Multi):", brand_opt_density, default=st.session_state.d_brands, key="d_brands")
       
        cat_opt_density = df['category'].dropna().unique().tolist()
        density_categories = st.sidebar.multiselect("Select Product Categories (Multi):", cat_opt_density, default=st.session_state.d_categories, key="d_categories")
       
        # Synchronized Order Part 2: Range Sliders (Price & Rating)
        density_price_range = st.sidebar.slider("Retail Price Limits ($):", 5.0, 500.0, st.session_state.d_price, step=5.0, key="d_price")
        density_rating_range = st.sidebar.slider("Satisfaction Rating Range (⭐):", 1.0, 5.0, st.session_state.d_rating, step=0.1, key="d_rating")
       
        # Synchronized Order Part 3: Specific Parameters
        bin_count = st.sidebar.slider("Adjust Bins (Granularity):", 10, 100, int(st.session_state.d_bins), key="d_bins")


        # Synchronized Order Part 4: Axis & Chart Configurations
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


        # Synchronized Order Part 1: Scope Filters (Brand & Category)
        brand_opts_leaders = df['brand'].value_counts().head(50).index.tolist()
        leaders_brands = st.sidebar.multiselect("Select Brand Targets (Multi):", brand_opts_leaders, default=st.session_state.a_brands, key="a_brands")
       
        cat_opts = df['category'].value_counts().head(30).index.tolist()
        leaders_categories = st.sidebar.multiselect("Select Category Sectors (Multi):", cat_opts, default=st.session_state.a_cats, key="a_cats")
       
        # Synchronized Order Part 2: Range Sliders (Price & Rating)
        leaders_price_range = st.sidebar.slider("Price Bound Target Range ($):", 0.0, 500.0, st.session_state.a_price_range, step=5.0, key="a_price_range")
        leaders_rating_range = st.sidebar.slider("Rating Target Range (⭐):", 1.0, 5.0, st.session_state.a_rating_range, step=0.1, key="a_rating_range")
       
        # Synchronized Order Part 3: Specific Parameters
        item_limit = st.sidebar.slider("Number of Products to Show:", 5, 30, int(st.session_state.a_limit), key="a_limit")


        # Synchronized Order Part 4: Axis & Chart Configurations
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


        # Synchronized Order Part 1: Scope Filters (Brand & Category)
        brand_opts_explorer = df['brand'].dropna().unique().tolist()
        explorer_brands = st.sidebar.multiselect("Base Catalog Brands (Multi):", brand_opts_explorer, default=st.session_state.exp_brands, key="exp_brands")
       
        cat_opts_explorer = df['category'].dropna().unique().tolist()
        explorer_categories = st.sidebar.multiselect("Base Catalog Categories (Multi):", cat_opts_explorer, default=st.session_state.exp_cats, key="exp_cats")
       
        # Synchronized Order Part 2: Range Sliders (Price & Rating)
        explorer_price_range = st.sidebar.slider("Budget Bound Target Range ($):", 5.0, 500.0, st.session_state.exp_price, step=5.0, key="exp_price")
        explorer_rating_range = st.sidebar.slider("Satisfaction Target Range (⭐):", 1.0, 5.0, st.session_state.exp_rating, step=0.1, key="exp_rating")
       
        # Synchronized Order Part 3: Specific Parameters
        explorer_love_range = st.sidebar.slider("Customer Love Index Range:", 0, 1000000, st.session_state.exp_love, step=500, key="exp_love")
        search_kw = st.sidebar.text_input("Formula or Name Keyword search:", value=st.session_state.exp_search, key="exp_search")
       
        # Synchronized Order Part 4: Axis & Chart Configurations
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
    # TAB 1: EXECUTIVE HOME (KHÔI PHỤC HOÀN TOÀN HAI KHUNG HỘP CHỈ DẪN VÀ MỤC TIÊU - image_3390ff.png)
    # -------------------------------------------------------------
    if tab_selection == "🏠 Executive Home":
        # Khối chỉ số KPI tổng quan
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.markdown(f"<div class='stat-box'><div class='stat-val'>{df.shape[0]:,}</div><div class='stat-lbl'>Catalog Assortments</div></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='stat-box'><div class='stat-val'>{df['brand'].nunique()}</div><div class='stat-lbl'>Unique Brands</div></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='stat-box'><div class='stat-val'>${df['price'].mean():.2f}</div><div class='stat-lbl'>Average Price</div></div>", unsafe_allow_html=True)
        with c4: st.markdown(f"<div class='stat-box'><div class='stat-val'>{df['rating'].mean():.2f}⭐</div><div class='stat-lbl'>Satisfaction Score</div></div>", unsafe_allow_html=True)


        st.markdown("<br>", unsafe_allow_html=True)
       
        # Khôi phục hoàn toàn 2 khung hộp đẹp mắt ở trang đầu (Hình image_3390ff.png)
        col_home_txt1, col_home_txt2 = st.columns(2)
        with col_home_txt1:
            st.markdown("""
            <div class='premium-card' style='height: 100%; border: 1.5px solid #FF85A2; border-radius: 20px; padding: 25px;'>
                <h3 style='margin-top: 0; color: #111827; font-size: 1.35rem;'>✨ Strategic Hub Operating Instructions</h3>
                <p style='color: #4A5568; line-height: 1.75; font-size: 0.92rem;'>
                    Welcome to the <b>Sephora Corporate Decision Support Portal</b>. This space has been carefully optimized to avoid unnecessary whitespace, offering lightning-fast database loads and high-fidelity layouts.
                </p>
                <p style='color: #111827; font-weight: 700; font-size: 0.92rem; margin-top: 15px; margin-bottom: 8px;'>Active Functional Modules:</p>
                <ul style='color: #4A5568; line-height: 1.7; padding-left: 20px; font-size: 0.9rem;'>
                    <li style='margin-bottom: 6px;'><b>Strategy Sandbox:</b> Explores cross-metric behaviors (Price, Reviews, Sentiment) under targeted brand standards.</li>
                    <li style='margin-bottom: 6px;'><b>Price Distributions:</b> Charts continuous price levels to pinpoint pricing gaps and margin strategies.</li>
                    <li style='margin-bottom: 6px;'><b>Assortment Leaders:</b> Displays rapid market power drops and lists viral products driven by community engagement.</li>
                    <li style='margin-bottom: 6px;'><b>Cosmetics Explorer (Dynamic):</b> Gives you complete analytical freedom to search ingredients, filter categories, and map bespoke multi-axis projections.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
           
        with col_home_txt2:
            st.markdown("""
            <div class='premium-card' style='height: 100%; border: 1.5px solid #E91E63; border-radius: 20px; padding: 25px;'>
                <h3 style='margin-top: 0; color: #111827; font-size: 1.35rem;'>🎯 Strategic Objectives</h3>
                <p style='color: #4A5568; line-height: 1.6; font-weight: 600; margin-bottom: 12px; font-size: 0.92rem;'>
                    What key insights do we explore from this dataset?
                </p>
                <ul style='font-size: 0.9rem; line-height: 1.7; color: #4A5568; padding-left: 20px; margin-bottom: 0;'>
                    <li style='margin-bottom: 10px;'><b>Pricing Sweet Spots:</b> Finding perfect value targets that balance brand prestige and volume sales.</li>
                    <li style='margin-bottom: 10px;'><b>Love Index vs Rating Frequencies:</b> Investigating whether social loyalty translates directly into higher rating stars.</li>
                    <li style='margin-bottom: 10px;'><b>Assortment Strength:</b> Benchmarking market footprints across sectors like Makeup, Skincare, Fragrances, and Tools.</li>
                    <li style='margin-bottom: 10px;'><b>Value for Money Index:</b> Uncovering the best consumer-voted returns per dollar spent.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)


        st.markdown("<br>", unsafe_allow_html=True)
       
        # Không gian làm việc dữ liệu (Data Workspace) chiếm 100% chiều rộng để mang lại tốc độ phản hồi cực cao
        st.markdown("### 📋 Primary Dataset Explorer Workspace")
       
        # Bảng lọc dữ liệu chi tiết
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


        # Lọc dữ liệu theo các tiêu chí đã chọn
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
       
        st.markdown(f"**Showing {min(rows_selection, preview_df.shape[0])} of {preview_df.shape[0]} filtered products:**")
        st.dataframe(preview_df.head(rows_selection), use_container_width=True)




    # -------------------------------------------------------------
    # TAB 2: STRATEGY SANDBOX (ĐỒNG BỘ HOÀN HẢO MÀU SẮC CHO DENSITY HEATMAP - SỬA LỖI HÌNH image_3390bd.png và image_338dd8.png)
    # -------------------------------------------------------------
    elif tab_selection == "🔮 Strategy Sandbox":
        st.markdown("<span class='badge'>INTERACTIVE EXPERIMENT</span>", unsafe_allow_html=True)
        st.markdown("<h2>Dynamic Performance & Customer Loyalty Sandbox</h2>", unsafe_allow_html=True)
       
        # Áp dụng bộ lọc đa chọn từ thanh bên
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
            # SỬA LỖI HÌNH image_338dd8.png: Gom trực tiếp tiêu đề vào thẻ premium-card đơn để tránh lỗi rỗng trắng
            st.markdown("<div class='premium-card' style='padding: 15px; margin-bottom: 12px;'><h4>Density Heatmap: Correlation Analysis</h4></div>", unsafe_allow_html=True)
           
            x_title = sandbox_x_axis.replace('_', ' ').title()
            y_title = sandbox_y_axis.replace('_', ' ').title()
           
            # Khởi tạo đồ thị mật độ nhiệt 2 chiều đồng bộ trực tiếp gam màu Sephora
            fig_density = px.density_heatmap(
                filtered_sandbox, x=sandbox_x_axis, y=sandbox_y_axis,
                marginal_x="histogram", marginal_y="histogram",
                labels={sandbox_x_axis: x_title, sandbox_y_axis: y_title},
                color_continuous_scale=HIGH_CONTRAST_BURGUNDY,  # Đồng bộ dải màu đỏ mận mộc mạc cao cấp
                template="simple_white"
            )
           
            # SỬA LỖI HÌNH image_3390bd.png: Thay đổi màu của marginal histogram thành hồng/đỏ mận đậm đà sắc nét
            fig_density.update_traces(marker_color='#C2185B', selector=dict(type='histogram'))
           
            fig_density.update_layout(
                paper_bgcolor='rgba(255,255,255,1)',
                plot_bgcolor='rgba(255,255,255,1)',
                font_family="Plus Jakarta Sans", margin=dict(l=10, r=10, t=30, b=10)
            )
            st.plotly_chart(fig_density, use_container_width=True)
           
        with col_plot2:
            st.markdown("<div class='premium-card' style='padding: 15px; margin-bottom: 12px;'><h4>Distribution: Product Satisfaction Star Ratings</h4></div>", unsafe_allow_html=True)
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
           
        st.success(f"📈 **Live Sandbox Insights:** Found **{filtered_sandbox.shape[0]}** matching listings.")


        # KHÔI PHỤC TIẾNG VIỆT BẢN CŨ GỐC CHO PHẦN MÔ TẢ (Hình image_338d9b.png)
        col_desc_sandbox, col_img_sandbox = st.columns([2, 1])
        with col_desc_sandbox:
            st.markdown("""
            <div class='premium-card' style='margin-bottom: 0px; height: 100%;'>
                <h4 style='color: #E91E63; font-weight: 700;'>💡 Sandbox Multidimensional Insights</h4>
                <p style='color: #4A5568; line-height:1.7; font-size: 0.92rem;'>
                    <b>1. Density Heatmap & Value Correlation: The left density heatmap (Sephora High Contrast) illustrates the correlation between product price and customer "Love" engagement. The data is most densely concentrated in the budget-friendly segment under $50, where customer interaction peaks, and gradually thins out as prices increase. 
                </p>
                <p style='color: #4A5568; line-height:1.7; font-size: 0.92rem;'>
                    <b>2. Product Satisfaction & Price Distribution: The right bar chart displays the frequency of product listings across various price points relative to star ratings. The volume peaks sharply (with counts approaching 600) within the $20 to $40 price range, highlighting this as the most dominant and highly-reviewed pricing sweet spot. 
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
    # TAB 3: CUSTOMIZABLE PRICE DENSITIES (LOLLIPOP CHART OVERHAUL & VIETNAMESE DESCRIPTIONS)
    # -------------------------------------------------------------
    elif tab_selection == "📊 Customizable Price Densities":
        st.markdown("<span class='badge'>PRICING STRUCTURE MATRIX</span>", unsafe_allow_html=True)
        st.markdown("<h2>Custom Lollipop Distribution & Pricing Analytics Matrix</h2>", unsafe_allow_html=True)
       
        # Áp dụng bộ lọc đa chọn từ thanh bên
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
       
        # "Đập đi xây lại" hoàn toàn thành biểu đồ Lollipop (Kẹo mút) tuyệt đẹp
        if not density_df.empty:
            lollipop_data = density_df.groupby(density_x_axis)[density_y_axis].mean().reset_index()
            # Sắp xếp giảm dần để đồ thị kẹo mút trông có cấu trúc chiến lược cao
            lollipop_data = lollipop_data.sort_values(by=density_y_axis, ascending=False).head(35)
           
            fig_lollipop = go.Figure()
           
            # Vẽ các thanh "thân kẹo mút" (sticks)
            for i, row in lollipop_data.iterrows():
                fig_lollipop.add_shape(
                    type="line",
                    x0=row[density_x_axis], y0=0,
                    x1=row[density_x_axis], y1=row[density_y_axis],
                    line=dict(
                        color="#FF4D6D", # Màu hồng mận đậm đà
                        width=2.5
                    )
                )
           
            # Vẽ "đầu kẹo mút" (markers) rực rỡ và sắc nét
            fig_lollipop.add_trace(go.Scatter(
                x=lollipop_data[density_x_axis],
                y=lollipop_data[density_y_axis],
                mode='markers',
                marker=dict(
                    color='#800F2F', # Đỏ Burgundy đậm sắc sảo
                    size=13,
                    line=dict(
                        color='#3D001B', # Viền đen mận tương phản cực cao
                        width=1.5
                    )
                ),
                name=density_y_axis.replace('_', ' ').title(),
                hoverinfo='text',
                text=[f"Phân loại ({density_x_axis.upper()}): {r[density_x_axis]}<br>Trung bình {density_y_axis.replace('_', ' ').title()}: {r[density_y_axis]:.2f}" for _, r in lollipop_data.iterrows()]
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
        else:
            st.warning("⚠️ Không tìm thấy sản phẩm nào khớp với bộ lọc dữ liệu hiện tại.")


        # KHÔI PHỤC TIẾNG VIỆT GỐC BẢN CŨ CHO TAB 3
        col_desc_densities, col_img_densities = st.columns([2, 1])
        with col_desc_densities:
            st.markdown(f"""
            <div class='premium-card' style='margin-bottom: 0px; height: 100%; border-left: 5px solid #C2185B;'>
                <h4 style='color: #B71C1C; font-weight: 700;'>🍭 Lollipop Pricing & Metric Distribution Analytics</h4>
                <p style='color: #4A5568; line-height:1.7;'>
                    <b>High-End Premium Categories: The chart highlights that "High Tech Tools" commands the highest average price point, peaking at approximately $130, closely followed by specialized treatments like "Hair Thinning & Hair Loss" and "Hair Straighteners & Flat Irons" hovering around $120. 
                </p>
                <p style='color: #E91E63; font-weight: 600; margin-top: 10px;'>
                     Currently aggregating data from {density_df.shape[0]} qualified products to establish precise category baseline trends. 
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
    # TAB 4: FLEXIBLE AREA TREND LEADERS (TIẾNG VIỆT BẢN CŨ)
    # -------------------------------------------------------------
    elif tab_selection == "📈 Flexible Area Trend Leaders":
        st.markdown("<span class='badge'>ASSORTMENT POWER</span>", unsafe_allow_html=True)
        st.markdown("<h2>Category Leaders and Market Concentration Curves</h2>", unsafe_allow_html=True)
       
        area_df = df.copy()
        if leaders_categories:
            area_df = area_df[area_df['category'].isin(leaders_categories)]
        if leaders_brands:
            area_df = area_df[area_df['brand'].isin(leaders_brands)]
       
        # Lọc theo thanh kéo khoảng giá 2 đầu
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
            # Biểu đồ diện tích lũy tiến hỗ trợ tự chọn trục X và Y để tăng khả năng phân tích đa chiều
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


        # KHÔI PHỤC TIẾNG VIỆT GỐC BẢN CŨ CHO TAB 4
        col_desc_leaders, col_img_leaders = st.columns([2, 1])
        with col_desc_leaders:
            st.markdown(f"""
            <div class='premium-card' style='margin-bottom: 0px; height: 100%;'>
                <h4 style='color: #E91E63; font-weight: 700;'>⭐ Power Law Dynamics in Modern Cosmetics</h4>
                <p style='color: #4A5568; line-height:1.7;'>
                    The area chart has been optimized to allow for the structuring of the horizontal axis (e.g., Product Name, Brand, Category) and the correlation of the vertical axis (e.g., Love Score, Price, Star Ratings). This supports the team's strategic reports in easily identifying the "Leading Product" that represents the Sephora customer segment.
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
    # TAB 5: COSMETICS EXPLORER (TIẾNG VIỆT BẢN CŨ)
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


            # Sử dụng phổ màu HIGH_CONTRAST_BURGUNDY phân biệt rõ ràng không chồng chéo
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


            st.success(f"🎯 **Explorer Execution Matrix:** Identified **{exp_df.shape[0]}** matching assortments.")
        else:
            st.warning("⚠️ No products matching your criteria are present in our dataset.")


         # KHÔI PHỤC TIẾNG VIỆT GỐC BẢN CŨ CHO TAB 5
        col_desc_densities, col_img_densities = st.columns([2, 1])
        with col_desc_densities:
            st.markdown(f"""
            <div class='premium-card' style='margin-bottom: 0px; height: 100%; border-left: 5px solid #C2185B;'>
                <h4 style='color: #B71C1C; font-weight: 700;'>📊 Enhanced Multidimensional Strategy Insights</h4>
                <p style='color: #4A5568; line-height:1.7;'>
                     <b>Brand Engagement Powerhouses: The treemap segments brands by total engagement volume. "stila" and "Buxom" clearly dominate the market footprint, coated in the deepest burgundy shades to signal peak customer "Love" accumulations (with stila pushing past 140k). 
                </p>
                <p style='color: #4A5568; line-height:1.7; font-size: 0.92rem;'>
                    <b>Mid-Tier Market Density: Mainstream brands such as "Urban Decay", "Anastasia Beverly Hills", "HUDA BEAUTY", and "Too Faced" represent massive structural blocks with strong, consistent pink-to-red tone distribution. 
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



