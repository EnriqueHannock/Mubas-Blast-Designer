import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import io

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="MUBAS | Blast Designer",
    page_icon="💥",
    layout="wide"
)

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Barlow+Condensed:wght@400;600;700;800&family=Barlow:wght@300;400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Barlow', sans-serif;
    }

    .stApp {
        background-color: #f5efe6;
        color: #2c1a0e;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #2c1a0e;
        border-right: 1px solid #4a2e1a;
    }

    [data-testid="stSidebar"] * {
        color: #c9a882 !important;
        font-family: 'Barlow', sans-serif;
    }

    /* Main title */
    .main-title {
        font-family: 'Barlow Condensed', sans-serif;
        font-weight: 800;
        font-size: 2.6rem;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        color: #2c1a0e;
        line-height: 1.1;
        margin: 0;
    }

    .main-subtitle {
        font-family: 'DM Mono', monospace;
        font-weight: 300;
        font-size: 0.78rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #7a4a28;
        margin-top: 4px;
    }

    .date-line {
        font-family: 'DM Mono', monospace;
        font-size: 0.7rem;
        color: #a07850;
        letter-spacing: 0.08em;
        margin-top: 2px;
    }

    /* Section headings */
    .section-label {
        font-family: 'Barlow Condensed', sans-serif;
        font-weight: 700;
        font-size: 0.65rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: #7a4a28;
        border-bottom: 1px solid #d4b896;
        padding-bottom: 6px;
        margin-bottom: 14px;
    }

    /* Input labels */
    label, .stNumberInput label, .stCheckbox label {
        font-family: 'Barlow', sans-serif !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        color: #6b4226 !important;
        letter-spacing: 0.02em !important;
        text-transform: uppercase !important;
    }

    /* Input fields */
    input[type="number"], input[type="text"] {
        background-color: #fdf6ee !important;
        border: 1px solid #c9a882 !important;
        border-radius: 4px !important;
        color: #2c1a0e !important;
        font-family: 'DM Mono', monospace !important;
        font-size: 0.9rem !important;
    }

    input[type="number"]:focus {
        border-color: #7a4a28 !important;
        box-shadow: 0 0 0 2px rgba(122,74,40,0.15) !important;
    }

    /* Form container */
    [data-testid="stForm"] {
        background-color: #fdf6ee;
        border: 1px solid #d4b896;
        border-radius: 6px;
        padding: 24px;
    }

    /* Submit button */
    [data-testid="stFormSubmitButton"] button {
        background-color: #7a4a28 !important;
        color: #fdf6ee !important;
        font-family: 'Barlow Condensed', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        letter-spacing: 0.15em !important;
        text-transform: uppercase !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 12px 24px !important;
        transition: background-color 0.2s ease;
    }

    [data-testid="stFormSubmitButton"] button:hover {
        background-color: #5c3318 !important;
    }

    /* Metrics */
    [data-testid="stMetric"] {
        background-color: #fdf6ee;
        border: 1px solid #d4b896;
        border-left: 3px solid #7a4a28;
        border-radius: 4px;
        padding: 16px 20px !important;
    }

    [data-testid="stMetricLabel"] {
        font-family: 'DM Mono', monospace !important;
        font-size: 0.65rem !important;
        letter-spacing: 0.15em !important;
        text-transform: uppercase !important;
        color: #a07850 !important;
    }

    [data-testid="stMetricValue"] {
        font-family: 'Barlow Condensed', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.6rem !important;
        color: #2c1a0e !important;
    }

    /* Info / success boxes */
    .stAlert {
        background-color: #fdf6ee !important;
        border: 1px solid #d4b896 !important;
        border-radius: 4px !important;
        color: #6b4226 !important;
        font-family: 'Barlow', sans-serif !important;
        font-size: 0.85rem !important;
    }

    /* Divider */
    hr {
        border-color: #d4b896 !important;
    }

    /* Sidebar labels */
    .sidebar-heading {
        font-family: 'Barlow Condensed', sans-serif;
        font-weight: 700;
        font-size: 0.65rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: #e8c99a;
        margin-bottom: 10px;
    }

    .team-member {
        font-family: 'Barlow', sans-serif;
        font-size: 0.82rem;
        color: #a07850;
        padding: 4px 0;
        border-bottom: 1px solid #4a2e1a;
    }

    .team-group {
        font-family: 'DM Mono', monospace;
        font-size: 0.7rem;
        color: #e8c99a;
        letter-spacing: 0.08em;
        margin-bottom: 8px;
    }

    /* Checkbox */
    [data-testid="stCheckbox"] span {
        font-family: 'Barlow', sans-serif !important;
        font-size: 0.8rem !important;
        color: #6b4226 !important;
    }

    /* Column headers in form */
    .col-header {
        font-family: 'Barlow Condensed', sans-serif;
        font-weight: 700;
        font-size: 0.62rem;
        letter-spacing: 0.22em;
        text-transform: uppercase;
        color: #7a4a28;
        padding-bottom: 8px;
        border-bottom: 1px solid #d4b896;
        margin-bottom: 16px;
    }

    .result-header {
        font-family: 'Barlow Condensed', sans-serif;
        font-weight: 700;
        font-size: 0.65rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: #a07850;
        margin: 24px 0 14px 0;
    }

    </style>
""", unsafe_allow_html=True)


# --- SIDEBAR ---
with st.sidebar:
    st.markdown('<div class="sidebar-heading">Control Panel</div>', unsafe_allow_html=True)
    st.markdown("---")

    st.markdown('<div class="sidebar-heading">Project Team</div>', unsafe_allow_html=True)
    st.markdown('<div class="team-group">Group 4 — BMEN 5</div>', unsafe_allow_html=True)
    for name in ["Enrique Hannock", "Saidi Ibrahim", "Promise Magola"]:
        st.markdown(f'<div class="team-member">{name}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(
        '<div style="font-family: \'DM Mono\', monospace; font-size: 0.65rem; '
        'color: #6b4226; letter-spacing: 0.1em; text-transform: uppercase;">'
        'Innovate. Create. Generate.</div>',
        unsafe_allow_html=True
    )


# --- HEADER ---
col_title, col_spacer = st.columns([5, 1])
with col_title:
    st.markdown('<div class="main-title">Production Blast Planner</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-subtitle">Malawi University of Business and Applied Sciences</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="date-line">{datetime.now().strftime("%d %B %Y")}</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")


# --- INPUTS ---
st.markdown('<div class="section-label">Engineering Design Inputs</div>', unsafe_allow_html=True)

with st.form("input_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="col-header">Geometry & Rock</div>', unsafe_allow_html=True)
        d_mm = st.number_input("Hole Diameter (mm)", 32.0, 400.0, value=90.0, step=5.0)
        h_bench = st.number_input("Bench Height (m)", 1.0, 50.0, value=9.0, step=0.5)
        ucs = st.number_input("Rock Strength UCS (MPa)", 30.0, 400.0, value=45.0, step=10.0)

    with col2:
        st.markdown('<div class="col-header">Explosives</div>', unsafe_allow_html=True)
        rho_anfo = st.number_input("ANFO Density (kg/m³)", value=825.0, step=25.0)
        pf_target = st.number_input("Target Powder Factor (kg/m³)", 0.1, 2.0, value=1.0, step=0.1)
        st.markdown("<br>", unsafe_allow_html=True)
        use_subdrill = st.checkbox("Enable Subdrill")
        if use_subdrill:
            subdrill_val = st.number_input("Subdrill Depth (m)", 0.0, 5.0, value=0.5, step=0.1)
        else:
            subdrill_val = 0.0

    with col3:
        st.markdown('<div class="col-header">Advanced Charging</div>', unsafe_allow_html=True)
        use_decking = st.checkbox("Apply Deck Charging (2 Decks)")
        if use_decking:
            deck_stemming = st.number_input("Mid-Deck Stemming (m)", 0.5, 5.0, value=1.5, step=0.1)
        else:
            deck_stemming = 0.0

        st.markdown("<br>" * 4, unsafe_allow_html=True)
        submit = st.form_submit_button("Generate Design Report", use_container_width=True)


# --- RESULTS ---
if submit:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<div class="section-label">Design Output</div>', unsafe_allow_html=True)

    res1, res2, res3 = st.columns(3)
    res1.metric("Hole Diameter", f"{d_mm} mm")
    res2.metric("Total Depth", f"{h_bench + subdrill_val:.1f} m")
    res3.metric("Charging Mode", "Decked" if use_decking else "Continuous")

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("Detailed parameters and PDF download will generate here once computation logic is connected.")
