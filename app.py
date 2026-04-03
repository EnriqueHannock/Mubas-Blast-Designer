import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import io

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="MUBAS | Blast Designer", 
    page_icon="💥", 
    layout="wide"
)

# --- CUSTOM CSS FOR STYLING ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    h1 {
        color: #1E3A8A;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 800;
    }
    h3 {
        color: #1E40AF;
        border-bottom: 2px solid #1E40AF;
        padding-bottom: 5px;
    }
    .team-box {
        font-size: 0.9rem;
        color: #64748b;
        font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR NAVIGATION & TEAM ---
with st.sidebar:
    st.image("https://www.flaticon.com/free-icon/excavator_4738992", width=80)
    st.markdown("# CONTROL PANEL")
    st.markdown("---")
    
    st.markdown("### PROJECT TEAM")
    st.markdown("""
    <div class="team-box">
    <b>Group 4 (BMEN 5)</b><br>
    • Enrique Hannock<br>
    • Saidi Ibrahim<br>
    • Promise Magola
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.info("Innovate. Create. Generate.")

# --- 3. HEADER SECTION ---
col_title, col_logo = st.columns([4, 1])

with col_title:
    st.title("MUBAS Production Blast Planner")
    st.markdown("**Malawi University of Business and Applied Sciences**")
    st.caption(f"System Date: {datetime.now().strftime('%d %B %Y')}")

with col_logo:
    # Placeholder for the MUBAS logo from your code
    st.image("https://placeholder.com", use_container_width=True)

st.divider()

# --- 4. MAIN INPUT GRID ---
st.markdown("### 🛠️ Engineering Design Inputs")

with st.form("input_form"):
    # Create three distinct visual zones
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**GEOMETRY & ROCK**")
        d_mm = st.number_input("Hole Diameter (mm)", 32.0, 400.0, value=90.0, step=5.0)
        h_bench = st.number_input("Bench Height (m)", 1.0, 50.0, value=9.0, step=0.5)
        ucs = st.number_input("Rock Strength UCS (MPa)", 30.0, 400.0, value=45.0, step=10.0)
    
    with col2:
        st.markdown("**EXPLOSIVES**")
        rho_anfo = st.number_input("ANFO Density (kg/m³)", value=825.0, step=25.0)
        pf_target = st.number_input("Target Powder Factor (kg/m³)", 0.1, 2.0, value=1.0, step=0.1)
        
        st.markdown("---")
        use_subdrill = st.checkbox("Enable Subdrill")
        if use_subdrill:
            subdrill_val = st.number_input("Subdrill Depth (m)", 0.0, 5.0, value=0.5, step=0.1)
        else:
            subdrill_val = 0.0
        
    with col3:
        st.markdown("**ADVANCED CHARGING**")
        use_decking = st.checkbox("Apply Deck Charging (2 Decks)")
        if use_decking:
            deck_stemming = st.number_input("Mid-Deck Stemming (m)", 0.5, 5.0, value=1.5, step=0.1)
        else:
            deck_stemming = 0.0
            
        st.markdown("<br>" * 2, unsafe_allow_html=True) # Spacer
        submit = st.form_submit_button("GENERATE DESIGN REPORT", use_container_width=True)

# --- 5. RESULTS AREA ---
if submit:
    st.success("Calculations Complete. Viewing Optimized Blast Model...")
    
    res1, res2, res3 = st.columns(3)
    res1.metric("Hole Diameter", f"{d_mm} mm")
    res2.metric("Total Depth", f"{h_bench + subdrill_val} m")
    res3.metric("Charging Style", "Decked" if use_decking else "Continuous")
    
    # Placeholder for the rest of your logic (Graphs, CSVs, etc)
    st.info("Detailed parameters and PDF download would generate here.")
