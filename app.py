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
excavator_url = "https://www.flaticon.com/free-icon/excavator_4738992"
mubas_logo_url = "data:image/png;base64,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"
st.set_page_config(
    page_title="MUBAS Blast Designer", 
    page_icon=excavator_url, 
    layout="wide"
)
st.info("MALAWI UNIVERVESITY OF BUSINESS AND APPLIED SCIENCES")
st.info("Innovate. Create. Generate.")
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
    st.info("Welcome to the Production Blast Designer.")
    st.info("Adjust your parameters below for standard or decked charging models.")

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
