import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="MUBAS Blast Designer", page_icon="🏗️", layout="wide")

# ---------------- SESSION STATE ----------------
if 'history' not in st.session_state:
    st.session_state.history = []

# Default values
default_values = {
    "d_mm": 90.0,
    "h_total": 9.0,
    "ucs": 45.0,
    "pf_fixed": 1.0,
    "rho_anfo": 825.0
}

# Reset function
def reset_inputs():
    for key, value in default_values.items():
        st.session_state[key] = value

# PDF generator
def create_pdf(data):
    doc = SimpleDocTemplate("blast_report.pdf")
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("Blast Design Report", styles['Title']))
    content.append(Spacer(1, 12))

    for key, value in data.items():
        content.append(Paragraph(f"{key}: {value}", styles['Normal']))
        content.append(Spacer(1, 8))

    doc.build(content)

# ---------------- SIDEBAR FORM ----------------
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/5/5a/Malawi_University_of_Business_and_Applied_Sciences_logo.png", use_container_width=True)
    st.title("Mining Engineering")

    with st.form("input_form"):
        st.subheader("🔧 Input Parameters")

        d_mm = st.number_input("Hole Diameter (mm)", 32.0, 400.0, key="d_mm")
        h_total = st.number_input("Hole Depth (m)", 1.0, key="h_total")
        ucs = st.number_input("Rock Strength UCS (MPa)", 30.0, 400.0, key="ucs")
        pf_fixed = st.number_input("Target PF (kg/m³)", 0.1, 2.0, step=0.1, key="pf_fixed")
        rho_anfo = st.number_input("ANFO Density (kg/m³)", key="rho_anfo")

        col1, col2 = st.columns(2)
        submit = col1.form_submit_button("🚀 Calculate")
        reset = col2.form_submit_button("🗑️ Reset", on_click=reset_inputs)

# ---------------- MAIN APP ----------------
st.title("🏗️ Blast Planner App")
st.subheader("Malawi University of Business and Applied Sciences")

if submit:
    # -------- CALCULATIONS --------
    d_m = d_mm / 1000
    kb = 25
    ks = 1.25

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
        df = pd.DataFrame({
            "Parameter": ["Burden", "Spacing", "Stemming", "Charged Length", "Volume"],
            "Value": [
                f"{burden:.2f} m",
                f"{spacing:.2f} m",
                f"{stemming:.2f} m",
                f"{lc:.2f} m",
                f"{volume:.2f} m³"
            ]
        })
        st.table(df)

    with col2:
        st.markdown("### 🧨 Explosives")
        st.metric("Charge per Hole", f"{theoretical_charge:.2f} kg")
        st.metric("Actual PF", f"{actual_pf:.2f} kg/m³")

        if stemming > (0.4 * h_total):
            st.warning("⚠️ Stemming too high!")
        elif abs(actual_pf - pf_fixed) > 0.2:
            st.error("❌ Powder Factor mismatch")
        else:
            st.success("✅ Design OK")

    # -------- FRAGMENTATION --------
    st.divider()
    st.subheader("📈 Fragmentation Curve")

    x = np.linspace(1, 1000, 200)
    n = 1.2
    x50 = 350

    passing = 100 * (1 - np.exp(-0.693 * (x / x50)**n))

    chart_df = pd.DataFrame({
        "Size (mm)": x,
        "Passing (%)": passing
    }).set_index("Size (mm)")

    st.line_chart(chart_df)

    st.caption("Rosin-Rammler distribution (Kuz-Ram approximation)")

    # -------- SAVE HISTORY --------
    entry = {
        "Time": datetime.now().strftime("%H:%M:%S"),
        "Dia (mm)": d_mm,
        "UCS": ucs,
        "Target PF": pf_fixed,
        "Actual PF": round(actual_pf, 2)
    }

    st.session_state.history.insert(0, entry)
    st.success("✅ Saved to history")

    # -------- PDF REPORT --------
    report_data = {
        "Hole Diameter (mm)": d_mm,
        "Hole Depth (m)": h_total,
        "Burden (m)": round(burden, 2),
        "Spacing (m)": round(spacing, 2),
        "Stemming (m)": round(stemming, 2),
        "Charge (kg)": round(theoretical_charge, 2),
        "Powder Factor": round(actual_pf, 2)
    }

    if st.button("📄 Generate PDF Report"):
        create_pdf(report_data)

        with open("blast_report.pdf", "rb") as f:
            st.download_button("⬇️ Download Report", f, file_name="blast_report.pdf")

# -------- HISTORY --------
st.subheader("📜 Calculation History")

if st.session_state.history:
    st.table(pd.DataFrame(st.session_state.history))
else:
    st.info("No calculations yet.")
