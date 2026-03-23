import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="MUBAS Blast Designer", page_icon="🏗️", layout="wide")

# ---------------- SESSION STATE ----------------
if 'history' not in st.session_state:
    st.session_state.history = []

# Default values for reset
if 'd_mm' not in st.session_state: st.session_state.d_mm = 90.0
if 'h_total' not in st.session_state: st.session_state.h_total = 9.0
if 'ucs' not in st.session_state: st.session_state.ucs = 45.0
if 'pf_fixed' not in st.session_state: st.session_state.pf_fixed = 1.0
if 'rho_anfo' not in st.session_state: st.session_state.rho_anfo = 825.0

# PDF generator function
def create_pdf(data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("MUBAS Blast Design Report", styles['Title']))
    content.append(Spacer(1, 12))
    content.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    content.append(Spacer(1, 12))

    for key, value in data.items():
        content.append(Paragraph(f"<b>{key}</b>: {value}", styles['Normal']))
        content.append(Spacer(1, 8))

    doc.build(content)
    buffer.seek(0)
    return buffer

# ---------------- SIDEBAR ----------------
with st.sidebar:
    # Official MUBAS Logo Link
    st.image("https://www.mubas.ac.mw", use_container_width=True)
    st.title("Mining Engineering")
    
    with st.form("input_form"):
        st.subheader("🔧 Input Parameters")
        
        # Increments: 5 for Dia, 10 for UCS, 0.1 for PF
        d_mm = st.number_input("Hole Diameter (mm)", 32.0, 400.0, step=5.0, key="d_mm")
        h_total = st.number_input("Hole Depth (m)", 1.0, 50.0, step=0.5, key="h_total")
        ucs = st.number_input("Rock Strength UCS (MPa)", 30.0, 400.0, step=10.0, key="ucs")
        pf_fixed = st.number_input("Target PF (kg/m³)", 0.1, 2.0, step=0.1, key="pf_fixed")
        rho_anfo = st.number_input("ANFO Density (kg/m³)", key="rho_anfo")

        submit = st.form_submit_button("🚀 Calculate")

    with st.expander("👥 Group 4 Members"):
        st.write("Enrique Hannock, Saidi Ibrahim, Promise Magola")

# ---------------- MAIN APP ----------------
st.title("🏗️ Blast Planner App")
st.subheader("Malawi University of Business and Applied Sciences")

if submit:
    # -------- CALCULATIONS --------
    d_m = d_mm / 1000
    kb, ks = 25, 1.25
    burden = kb * d_m
    spacing = ks * burden
    stemming = 0.7 * burden
    lc = h_total - stemming
    volume = burden * spacing * h_total
    theoretical_charge = (np.pi * (d_m**2) / 4) * rho_anfo * lc
    actual_pf = theoretical_charge / volume

    # -------- RESULTS DISPLAY --------
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 📊 Blast Geometry")
        results_df = pd.DataFrame({
            "Parameter": ["Burden (B)", "Spacing (S)", "Stemming (T)", "Charged Length (Lc)", "Volume"],
            "Value": [f"{burden:.2f} m", f"{spacing:.2f} m", f"{stemming:.2f} m", f"{lc:.2f} m", f"{volume:.2f} m³"]
        })
        st.table(results_df)

    with col2:
        st.markdown("### 🧨 Explosives")
        st.metric("Charge per Hole", f"{theoretical_charge:.2f} kg")
        st.metric("Actual PF", f"{actual_pf:.2f} kg/m³")

        if stemming > (0.4 * h_total):
            st.warning("⚠️ Stemming too high!")
        if abs(actual_pf - pf_fixed) > 0.2:
            st.error("❌ Powder Factor mismatch")
        else:
            st.success("✅ Design OK")

    # -------- SAVE HISTORY --------
    entry = {
        "Time": datetime.now().strftime("%H:%M:%S"),
        "Dia (mm)": d_mm,
        "UCS": ucs,
        "Target PF": pf_fixed,
        "Actual PF": round(actual_pf, 2)
    }
    st.session_state.history.insert(0, entry)

    # -------- PDF REPORT --------
    st.divider()
    st.subheader("📄 Generate Report")
    report_data = {
        "Hole Diameter (mm)": f"{d_mm}",
        "Hole Depth (m)": f"{h_total}",
        "Burden (m)": f"{burden:.2f}",
        "Spacing (m)": f"{spacing:.2f}",
        "Stemming (m)": f"{stemming:.2f}",
        "Charge (kg)": f"{theoretical_charge:.2f}",
        "Powder Factor": f"{actual_pf:.2f}"
    }
    
    pdf_file = create_pdf(report_data)
    st.download_button(
        label="⬇️ Download PDF Report",
        data=pdf_file,
        file_name=f"Blast_Report_{datetime.now().strftime('%H%M%S')}.pdf",
        mime="application/pdf"
    )

    # -------- FRAGMENTATION --------
    st.divider()
    st.subheader("📈 Fragmentation Curve (20-600mm Target)")
    x = np.linspace(1, 1000, 200)
    n, x50 = 1.2, 350
    passing = 100 * (1 - np.exp(-0.693 * (x / x50)**n))
    chart_df = pd.DataFrame({"Size (mm)": x, "Passing (%)": passing}).set_index("Size (mm)")
    st.line_chart(chart_df)

# -------- HISTORY --------
st.divider()
st.subheader("📜 Calculation History")
if st.session_state.history:
    st.table(pd.DataFrame(st.session_state.history))
    if st.button("🗑️ Clear History"):
        st.session_state.history = []
        st.rerun()
else:
    st.info("No calculations performed yet.")
