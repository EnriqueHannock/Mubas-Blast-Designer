import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io

# --- 1. PAGE CONFIGURATION ---
# Using the Excavator URL as the browser tab icon
excavator_url = "https://cdn-icons-png.flaticon.com"
mubas_logo_url = "https://www.mubas.ac.mw"

st.set_page_config(
    page_title="MUBAS Blast Designer", 
    page_icon=excavator_url, 
    layout="wide"
)

# --- 2. SESSION STATE FOR HISTORY ---
if 'history' not in st.session_state:
    st.session_state.history = []

# --- 3. PDF GENERATOR FUNCTION ---
def create_pdf(data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    content = [
        Paragraph("MUBAS Blast Design Report", styles['Title']),
        Spacer(1, 12),
        Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']),
        Spacer(1, 12)
    ]
    for key, value in data.items():
        content.append(Paragraph(f"<b>{key}</b>: {value}", styles['Normal']))
        content.append(Spacer(1, 8))
    doc.build(content)
    buffer.seek(0)
    return buffer

# --- 4. HEADER SECTION (LOGOS & WELCOME) ---
col_logo, col_excavator, col_welcome = st.columns([1, 1, 4])

with col_logo:
    st.image(mubas_logo_url, width=110)

with col_excavator:
    st.image(excavator_url, width=110)

with col_welcome:
    st.title("MUBAS Blast Planner")
    st.info("Welcome to the Production Blast Designer. Adjust your parameters below for standard or decked charging models. Innovate. Create. Generate.")

# --- 5. GROUP MEMBERS (TOP GRID) ---
st.markdown("#### Project Team: Group 4 (BMEN 5)")
tm1, tm2, tm3 = st.columns(3)
tm1.write("Enrique Hannock")
tm2.write("Saidi Ibrahim")
tm3.write("Promise Magola")

st.divider()

# --- 6. INPUT SECTION (LANDING PAGE GRID) ---
st.markdown("### Design Inputs")
with st.form("input_form"):
    col_in1, col_in2, col_in3 = st.columns(3)
    
    with col_in1:
        d_mm = st.number_input("Hole Diameter (mm)", 32.0, 400.0, value=90.0, step=5.0)
        h_bench = st.number_input("Bench Height (m)", 1.0, 50.0, value=9.0, step=0.5)
        ucs = st.number_input("Rock Strength UCS (MPa)", 30.0, 400.0, value=45.0, step=10.0)
    
    with col_in2:
        rho_anfo = st.number_input("ANFO Density (kg/m³)", value=825.0, step=25.0)
        pf_target = st.number_input("Target Powder Factor (kg/m³)", 0.1, 2.0, value=1.0, step=0.1)
        st.write("---")
        use_subdrill = st.checkbox("Include Subdrill?")
        subdrill_val = st.number_input("Subdrill Depth (m)", 0.0, 5.0, value=0.5, step=0.1) if use_subdrill else 0.0
        
    with col_in3:
        st.write("Advanced Charging")
        use_decking = st.checkbox("Use Deck Charging? (2 Decks)")
        deck_stemming = st.number_input("Mid-Deck Stemming (m)", 0.5, 5.0, value=1.5, step=0.1) if use_decking else 0.0
        st.write("") 
        submit = st.form_submit_button("Run Calculation & Predict")

# --- 7. MAIN LOGIC & CALCULATIONS ---
if submit:
    # Engineering Math
    d_m = d_mm / 1000
    kb, ks = 25, 1.25 
    burden = kb * d_m
    spacing = ks * burden
    primary_stemming = 0.7 * burden
    total_depth = h_bench + subdrill_val
    
    if use_decking:
        available_charge_len = total_depth - primary_stemming - deck_stemming
        lc = max(available_charge_len, 0.0)
        style = "2-Deck Column"
    else:
        lc = total_depth - primary_stemming
        style = "Single Column"

    volume = burden * spacing * h_bench 
    charge_weight = (np.pi * (d_m**2) / 4) * rho_anfo * lc
    actual_pf = charge_weight / volume

    # Results Table
    st.markdown("### Calculated Outcomes")
    res_df = pd.DataFrame({
        "Parameter": ["Burden (B)", "Spacing (S)", "Primary Stemming (T)", "Total Depth", "Charge Style", "Total Charge"],
        "Value": [f"{burden:.2f} m", f"{spacing:.2f} m", f"{primary_stemming:.2f} m", f"{total_depth:.2f} m", style, f"{charge_weight:.2f} kg"]
    })
    st.table(res_df)

    # PF Tolerance Check
    st.markdown("### Powder Factor Validation")
    tolerance = 0.05
    diff = abs(actual_pf - pf_target)
    if diff <= tolerance:
        st.success(f"PF Match: Actual ({actual_pf:.2f}) is within tolerance of Target ({pf_target:.2f})")
    else:
        st.error(f"PF Mismatch: Actual ({actual_pf:.2f}) deviates from Target ({pf_target:.2f})")

    # Fragmentation Curve
    st.divider()
    st.subheader("Fragmentation Prediction (20-600mm)")
    x_sizes = np.linspace(1, 1000, 100)
    x50 = 380 * (ucs/45)**0.5 
    n_val = 1.2 if use_decking else 1.0 
    passing = 100 * (1 - np.exp(-0.693 * (x_sizes / x50)**n_val))
    st.line_chart(pd.DataFrame({"Size (mm)": x_sizes, "Passing (%)": passing}).set_index("Size (mm)"))

    # PDF Report Generation
    report_data = {
        "Diameter (mm)": d_mm,
        "Total Depth (m)": f"{total_depth:.2f}",
        "Burden (m)": f"{burden:.2f}",
        "Spacing (m)": f"{spacing:.2f}",
        "Charge (kg)": f"{charge_weight:.2f}",
        "Charging Style": style
    }
    pdf_file = create_pdf(report_data)
    st.download_button("Download Design Report", data=pdf_file, file_name=f"Blast_Report_{datetime.now().strftime('%H%M')}.pdf")

    # Save to History
    st.session_state.history.insert(0, {
        "Time": datetime.now().strftime("%H:%M"),
        "Dia": d_mm,
        "Style": style,
        "Subdrill": subdrill_val,
        "Actual PF": round(actual_pf, 2)
    })

# --- 8. HISTORY SECTION ---
st.divider()
st.subheader("Calculation History")
if st.session_state.history:
    st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)
    if st.button("Clear History"):
        st.session_state.history = []
        st.rerun()
else:
    st.info("Please enter parameters and click 'Run Calculation'.")
