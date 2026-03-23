import streamlit as st

# --- SCHOOL LOGO & HEADER ---
# This uses the official MUBAS logo URL
logo_url = "https://www.mubas.ac.mw"

# Display logo in the sidebar
st.sidebar.image(# Replace your current logo code with this one line
st.sidebar.image("https://www.mubas.ac.mw", use_container_width=True)
st.sidebar.markdown("### **MUBAS Blast Designer**")
st.sidebar.caption("The Home of Innovation: Innovate. Create. Generate.")

import streamlit as st
import numpy as np
import pandas as pd

# Page Config & Icons
st.set_page_config(page_title="MUBAS Blast Designer", page_icon="🏗️", layout="wide")

# --- CUSTOM CSS FOR PROFESSIONAL UI ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    .reportview-container .main .block-container { padding-top: 2rem; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: INPUT PARAMETERS ---
st.sidebar.header("📥 Design Inputs")
st.sidebar.info("DRILLING AND BLASTING DESIGNING")

d_mm = st.sidebar.number_input("Hole Diameter (D) [mm]", min_value=32.0, max_value=400.0, value=90.0)
h_total = st.sidebar.number_input("Total Hole Depth (H) [m]", min_value=1.0, value=9.0)
ucs = st.sidebar.number_input("Rock Strength (UCS) [MPa]", min_value=5.0, max_value=400.0, value=45.0)
pf_fixed = st.sidebar.number_input("Target Powder Factor [kg/m³]", min_value=0.1, max_value=2.0, value=1.0, step=0.1)
rho_anfo = st.sidebar.number_input("ANFO Density [kg/m³]", value=825.0)

# --- BACKEND: ENGINEERING CALCULATIONS ---
# 1. Unit Conversion
d_m = d_mm / 1000

# 2. Burden (Konya Constant KB between 20-30)
kb = 25 
burden = kb * d_m

# 3. Spacing (KS between 1.15-1.4)
ks = 1.25
spacing = ks * burden

# 4. Stemming (T = 0.7B)
stemming = 0.7 * burden

# 5. Charged Length & Volume
lc = h_total - stemming
volume = burden * spacing * h_total
theoretical_charge = (np.pi * (d_m**2) / 4) * rho_anfo * lc
actual_pf = theoretical_charge / volume

# --- FRONTEND: DASHBOARD ---
st.title("🏗️ Blast Planner App")
st.subheader("Group 4 (Malawi University Of Business and Applied Sciences)")
# --- GROUP MEMBERS SECTION ---
st.sidebar.divider() # Adds a line in the sidebar
with st.sidebar.expander("👥 Project Team Members"):
    st.write("**MUBAS Engineering - Group 4**")
    st.write("1. **Said**")
    st.write("2. **Enrique**")
    st.write("3. **Promise**")
    st.caption("Conceptual Development & Optimization")

# --- FOOTER BOX AT THE BOTTOM OF MAIN PAGE ---
st.markdown("---")
with st.container():
    col_a, col_b = st.columns([1, 4])
    with col_a:
        st.image("https://img.icons8.com") # A generic group icon
    with col_b:
        st.subheader("Project Identification")
        st.info("""
        **Course:** Mining Engineering - Blast Design  
        **Institution:** Malawi University of Business and Applied Sciences (MUBAS)  
        **Team:** Group 4 (Said, Enrique, Promise)
        """)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📊 Calculated Blast Geometry")
    res_df = pd.DataFrame({
        "Parameter": ["Burden (B)", "Spacing (S)", "Stemming (T)", "Charged Length (Lc)", "Volume per Hole"],
        "Value": [f"{burden:.2f} m", f"{spacing:.2f} m", f"{stemming:.2f} m", f"{lc:.2f} m", f"{volume:.2f} m³"],
        "Icon": ["📏", "↔️", "🪵", "🧨", "🧊"]
    })
    st.table(res_df)

with col2:
    st.markdown("### 🧨 Explosives Check")
    st.metric("Charge per Hole", f"{theoretical_charge:.2f} Kg")
    st.metric("Actual Powder Factor", f"{actual_pf:.2f} kg/m³")
    
    # Validation Alerts
    if stemming > (0.4 * h_total):
        st.warning("⚠️ Warning: Stemming exceeds 40% of hole depth!")
    if abs(actual_pf - pf_fixed) > 0.2:
        st.error(f"❌ PF Mismatch: Actual ({actual_pf:.2f}) vs Target ({pf_fixed:.2f})")
    else:
        st.success("✅ Powder Factor within tolerance.")

# --- VISUALIZATION: DUMMY HOLE IMPACT ---
st.divider()
st.markdown("### 📈 Predicted Fragmentation (<600mm Target)")
# (Kuz-Ram Sim)
x = np.linspace(0, 1000, 100)
n_val = 1.2 # Uniformity
x50 = 350 # Mean size
passing = 100 * (1 - np.exp(-0.693 * (x / x50)**n_val))

chart_data = pd.DataFrame({"Size (mm)": x, "Passing (%)": passing}).set_index("Size (mm)")
st.line_chart(chart_data)
st.caption("Figure: Expected Rosin-Rammler distribution for selected design.")
