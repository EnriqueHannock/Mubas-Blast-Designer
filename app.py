import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io

# 1. Page Setup
st.set_page_config(page_title="MUBAS Blast Designer", page_icon="🏗️", layout="wide")

# 2. Session State for History
if 'history' not in st.session_state:
    st.session_state.history = []

# --- PDF Generator Function ---
def create_pdf(data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    content = [Paragraph("MUBAS Blast Design Report", styles['Title']), Spacer(1, 12)]
    for key, value in data.items():
        content.append(Paragraph(f"<b>{key}</b>: {value}", styles['Normal']))
        content.append(Spacer(1, 8))
    doc.build(content)
    buffer.seek(0)
    return buffer

# --- SIDEBAR ---
with st.sidebar:
    # Reliable Logo Link
    st.image("https://www.mubas.ac.mw", use_container_width=True)
    st.title("Mining Engineering")
    
    with st.form("input_form"):
        st.subheader("🔧 Design Parameters")
        d_mm = st.number_input("Hole Diameter (mm)", 32.0, 400.0, value=90.0, step=5.0)
        h_total = st.number_input("Hole Depth (m)", 1.0, 50.0, value=9.0, step=0.5)
        ucs = st.number_input("Rock Strength UCS (MPa)", 30.0, 400.0, value=45.0, step=10.0)
        pf_target = st.number_input("Target PF (kg/m³)", 0.1, 2.0, value=1.0, step=0.1)
        rho_anfo = st.number_input("ANFO Density (kg/m³)", value=825.0)
        submit = st.form_submit_button("🚀 Calculate & Predict")

    with st.expander("👥 Group 4 Members"):
        st.write("Enrique Hannock, Saidi Ibrahim, Promise Magola")

# --- MAIN INTERFACE ---
st.title("🏗️ Blast Planner App")
st.subheader("Malawi University of Business and Applied Sciences")

if submit:
    # 1. CALCULATIONS
    d_m = d_mm / 1000
    kb, ks = 25, 1.25
    burden = kb * d_m
    spacing = ks * burden
    stemming = 0.7 * burden
    lc = h_total - stemming
    volume = burden * spacing * h_total
    charge_weight = (np.pi * (d_m**2) / 4) * rho_anfo * lc
    actual_pf = charge_weight / volume

    # 2. DISPLAY METRICS
    col1, col2, col3 = st.columns(3)
    col1.metric("Burden (B)", f"{burden:.2f} m")
    col2.metric("Spacing (S)", f"{spacing:.2f} m")
    col3.metric("Actual PF", f"{actual_pf:.2f} kg/m³")

    # 3. GEOMETRY TABLE & SUMMARY
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown("### 📊 Blast Geometry")
        df = pd.DataFrame({
            "Parameter": ["Stemming (T)", "Charge Length (Lc)", "Volume/Hole", "Charge/Hole"],
            "Value": [f"{stemming:.2f} m", f"{lc:.2f} m", f"{volume:.2f} m³", f"{charge_weight:.2f} kg"]
        })
        st.table(df)
        
        # PDF Download
        report_data = {"Dia": d_mm, "Burden": f"{burden:.2f}m", "Spacing": f"{spacing:.2f}m", "PF": f"{actual_pf:.2f}"}
        pdf_file = create_pdf(report_data)
        st.download_button("📄 Download PDF Report", data=pdf_file, file_name="blast_report.pdf")

    with c2:
        st.markdown("### 📍 Pattern Visualization")
        fig, ax = plt.subplots(figsize=(4,3))
        ax.scatter([0, spacing, 0, spacing], [0, 0, burden, burden], color='red', s=100, label='Holes')
        ax.scatter(spacing/2, burden/2, color='blue', marker='x', s=100, label='Dummy')
        ax.set_title("Drill Grid (3.0x2.5 concept)")
        st.pyplot(fig)

    # 4. PREDICTION GRAPH (Fragmentation)
    st.divider()
    st.subheader("📈 Predicted Fragmentation (20-600mm)")
    x_sizes = np.linspace(1, 1000, 100)
    x50 = 350 * (ucs/45)**0.5 # Dynamic X50 based on UCS
    n_uniformity = 1.3
    passing = 100 * (1 - np.exp(-0.693 * (x_sizes / x50)**n_uniformity))
    
    chart_data = pd.DataFrame({"Size (mm)": x_sizes, "Passing (%)": passing}).set_index("Size (mm)")
    st.line_chart(chart_data)
    
    # Target success logic
    p600 = 100 * (1 - np.exp(-0.693 * (600 / x50)**n_uniformity))
    p20 = 100 * (1 - np.exp(-0.693 * (20 / x50)**n_uniformity))
    st.write(f"**Target Success:** {p600-p20:.1f}% of rock fits the 20-600mm range.")

    # 5. SAVE TO HISTORY
    st.session_state.history.insert(0, {"Time": datetime.now().strftime("%H:%M"), "Dia": d_mm, "UCS": ucs, "PF": round(actual_pf, 2)})

# --- HISTORY SECTION (Always visible) ---
st.divider()
st.subheader("📜 Calculation History")
if st.session_state.history:
    st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)
    if st.button("🗑️ Clear"):
        st.session_state.history = []
        st.rerun()
else:
    st.info("Fill the sidebar and click 'Calculate' to see results.")
