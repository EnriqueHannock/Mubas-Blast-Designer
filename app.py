import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io

# 1. Page Configuration
st.set_page_config(page_title="MUBAS Blast Designer", page_icon="🏗️", layout="wide")

# 2. Session State for History
if 'history' not in st.session_state:
    st.session_state.history = []

# --- PDF Generator Function ---
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

# --- HEADER SECTION (LOGO & WELCOME) ---
col_logo, col_welcome = st.columns([1, 4])
with col_logo:
    st.image("https://www.mubas.ac.mw", width=140)

with col_welcome:
    st.title("🏗️ MUBAS Blast Planner")
    st.info("👋 **Welcome to the Deterministic Empirical Blast Designer.** Enter your drill parameters below to generate a high-precision fragmentation model. *Innovate. Create. Generate.*")

# --- GROUP MEMBERS (TOP GRID) ---
st.markdown("#### 👥 Project Team: Group 4 (BMEN 5)")
tm1, tm2, tm3 = st.columns(3)
tm1.write("👤 **Enrique Hannock**")
tm2.write("👤 **Saidi Ibrahim**")
tm3.write("👤 **Promise Magola**")

st.divider()

# --- INPUT SECTION (LANDING PAGE GRID) ---
st.markdown("### 📥 Design Inputs 🛠️")
with st.form("input_form"):
    col_in1, col_in2, col_in3 = st.columns(3)
    
    with col_in1:
        # Step=5.0 for Diameter
        d_mm = st.number_input("Hole Diameter (mm)", 32.0, 400.0, value=90.0, step=5.0)
        h_total = st.number_input("Hole Depth (m)", 1.0, 50.0, value=9.0, step=0.5)
    
    with col_in2:
        # Step=10.0 for UCS
        ucs = st.number_input("Rock Strength UCS (MPa)", 30.0, 400.0, value=45.0, step=10.0)
        rho_anfo = st.number_input("ANFO Density (kg/m³)", value=825.0, step=25.0)
        
    with col_in3:
        # Step=0.1 for PF
        pf_target = st.number_input("Target PF (kg/m³)", 0.1, 2.0, value=1.0, step=0.1)
        st.write("") # Spacer
        submit = st.form_submit_button("🚀 Run Calculation & Predict")

# --- MAIN LOGIC & CALCULATIONS ---
if submit:
    # 1. Engineering Math
    d_m = d_mm / 1000
    kb, ks = 25, 1.25 # Konya Constants
    burden = kb * d_m
    spacing = ks * burden
    stemming = 0.7 * burden
    lc = h_total - stemming
    volume = burden * spacing * h_total
    charge_weight = (np.pi * (d_m**2) / 4) * rho_anfo * lc
    actual_pf = charge_weight / volume

    # 2. Results Table
    st.markdown("### 📊 Calculated Outcomes")
    res_df = pd.DataFrame({
        "Parameter": ["Burden (B)", "Spacing (S)", "Stemming (T)", "Charge Length (Lc)", "Volume/Hole", "Charge/Hole"],
        "Value": [f"{burden:.2f} m", f"{spacing:.2f} m", f"{stemming:.2f} m", f"{lc:.2f} m", f"{volume:.2f} m³", f"{charge_weight:.2f} kg"]
    })
    st.table(res_df)

    # 3. PF Tolerance Check
    st.markdown("### 🧨 Powder Factor Validation")
    tolerance = 0.05
    diff = abs(actual_pf - pf_target)
    if diff <= tolerance:
        st.success(f"✅ PF Match: Actual ({actual_pf:.2f}) is within tolerance of Target ({pf_target:.2f})")
    else:
        st.error(f"❌ PF Mismatch: Actual ({actual_pf:.2f}) deviates from Target ({pf_target:.2f})")

    # 4. Fragmentation Curve
    st.divider()
    st.subheader("📈 Fragmentation Prediction (20-600mm Range)")
    x_sizes = np.linspace(1, 1000, 100)
    x50 = 350 * (ucs/45)**0.5 # Dynamic X50
    n_val = 1.3
    passing = 100 * (1 - np.exp(-0.693 * (x_sizes / x50)**n_val))
    st.line_chart(pd.DataFrame({"Size (mm)": x_sizes, "Passing (%)": passing}).set_index("Size (mm)"))

    # 5. Pattern Visualization (Below Curve)
    st.subheader("📍 Pattern Visualization")
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.scatter([0, spacing, 0, spacing], [0, 0, burden, burden], color='red', s=200, label='Primary Holes')
    ax.scatter(spacing/2, burden/2, color='blue', marker='x', s=200, label='Dummy Relief')
    ax.set_xlabel("Spacing (m)")
    ax.set_ylabel("Burden (m)")
    ax.legend()
    st.pyplot(fig)

    # 6. PDF Report Generation
    report_data = {
        "Diameter (mm)": d_mm,
        "Burden (m)": f"{burden:.2f}",
        "Spacing (m)": f"{spacing:.2f}",
        "Actual PF": f"{actual_pf:.2f}"
    }
    pdf_file = create_pdf(report_data)
    st.download_button("📄 Download Design Report", data=pdf_file, file_name=f"Blast_Report_{datetime.now().strftime('%H%M')}.pdf")

    # 7. Save to History
    st.session_state.history.insert(0, {
        "Time": datetime.now().strftime("%H:%M"),
        "Dia": d_mm,
        "UCS": ucs,
        "Actual PF": round(actual_pf, 2)
    })

# --- HISTORY SECTION ---
st.divider()
st.subheader("📜 Calculation History")
if st.session_state.history:
    st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)
    if st.button("🗑️ Clear History"):
        st.session_state.history = []
        st.rerun()
else:
    st.info("👋 Welcome! Please enter your blast parameters above and click 'Run Calculation' to begin.")
