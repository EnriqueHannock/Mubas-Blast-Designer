import streamlit as st
import numpy as np
import pandas as pd

# Page Config & Icons
st.set_page_config(page_title="MUBAS Blast Designer", page_icon="🏗️", layout="wide")

# --- SIDEBAR: LOGO & TEAM ---
# Using the official MUBAS logo URL for guaranteed display
logo_url = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAP4AAACUCAMAAACEJ2RfAAAA/1BMVEX////t15kbgcQkIFwAAFLm5ezl0ZaTiHkAAFQAAFYAADzW1t334J3z3JsrJVurm4HNzNgAfMYAAE8ahsojKGMAAEI4Nmkea6qjo7QhHVu3poZQT3i/rYeCgJtSSmWSkadfUmW0rpdyoLyrp5MfX5xkmr4AADjWwpEAAEkAeccWFFrOu44Adsj39vlJQWT/6KCsuKohRYCgkX6NgHdsYm16b3EiO3U9icHAv8x3dpJfXYJkW2s5NFyEeHWZr7NMj77VzJ9GRHBoZ4UAACy7vqr/8qQAGGUMP4EAIWgADmYiUo4OM3M5JU4HS43/8YiKqrTFxqMAbMwAY88fAE0kDU/wfQMrAAANGElEQVR4nO2ce3OiShqHg0qjkQYlioCtZN2YVlrFgES8X9a5bGbPmt3J9/8s+zaoMZkz548zpyoly68yRpu2ah7eOxqurlKlSpUqVapUqVKlSpUqVapUqVKlSpUqVapUqX5PffEX1f9ogl9S6R/Xv6L7+/CjCX5JRc3McpmOY2Ydx4lewHPTMQ/Lh7Xs6Wi0aB6emqWPJvgllWL8QsDIIL+gVhZeFggp+HTgAOcCUTKLqQse9bQIWVERHWmJwvcFPMtZMonwKc1LGPCzjuRSAcWoeerSQoS8cC2KBk6S8BfIDfLsDF+I8dEswH6egxYQEvhm07RQYaA2k4bv6/R38AMf+dz6zgCrru5wYkkOCnknWc5PkRpQ4Qd8zBCLDF0I5JEbpQFTp2h0yH3JwWdEtdAP+DI94nt4LkdhAI5AhVEuWfhIJdT7ER/NRoLHTZ0ngidbhQgZ+KmeqNj3UcDcgB7xtVf8W6QqHB/cQKBgfTO78HOBEBSShT8jbpOyuO7jBUOcGWJftbDPE15WsBQiF0x4psqBKsy0JOEv6MyjcxZZ35lRhDxuXccXECI89p0mWhR8OUr9TYaomjUThO8MgnlzlB3NooSmzfxRhGc2F0EQNTjmAH4PFnq86gfzxBQ+pwDK5wr5PH+MlMsdnuRzOViO194cjhcd07ls/KKjjDzpT8obOfqF4+uKitGfFPYK9eJHE/ySOL4s/EnJaj7B+Bi//f3/hY8oRee/k46PZfnczkQZUXiN2UwhZ+uw6bgtSfjYJQuJnXmCpTUZxydN7QwfS77vHbYlCB9TnwmyL73yW7kjfu4V3wV2Kliqmyx8jFRELYtYHv4j/E8jhgTiUWbJicKXF8RiMmLMR3+AL6sWUVVXZtYoWfjYHyGZeURiivtz/E8KWxBGGPUknCh82UJsxIjk01v0U3zZ8oQFClSPIilZ1pdViRGrafmyO5J/ho8kV/ZV2lQtVU0WPiY88XlNn0PiH/Bj+gUSkN8MiEUoS5bzC5TAT+B7RJDpSFVVz3rFz6uRRtD9MmsRwMkgNDmFD0O0Y0GlMoLEThhywccxnIT8Cd+H49hVBb6BQSTQKPSRkAR8i6qEUGxB1yNQrFIVSQJlTCDnzg8OjzxquR6SwQeIJViSH5Ak4KtolMspFpOowASPYKz6RKVQ31/xVYnyWg9hQmfIQiigXi6XD1Ai8F0WDAoDpEJcE4+ngZEsy8gPXp1/oSIYdTwIEplY/oISNHCaEnUTgQ8DnNXUoZP3YbRFMPgxjo3OMz+0QtiiskwRJAFVxbQ5opAfkoHPG5qAuhLhkw9igAWTLrZyt2S3XO6sqO5jRmREoskf+S7yLZyUzC8DNLMQNH68ARB8mGrA2aHu3/5t1eu1/34L+JhasMmPGyIPTgQBz0gKPmIqExDh+DJhTJUp2Jvjt8vlVoQvEwqxj1SBtztQJ6Ba0MQ4P4OyJketDPdxF6wLA+1bfItiT5AZ4ReAkAqzIbwlGanPpapFwZN5WrMkQukI8b7mLX7AaIAI8/guxB2GqCwZ+NDFUJ7ZIelD/wNtDzS9o/f43sKbMYtSCtsQ30rB/InApxD4PPsBl4QgyUFn69N3sS8IKkz5cBRLcCiaeKhHk4Ev8Swe+T+LLvwIiMrCO3wYDFxf5qeJe77KhwIpIfgetPuEcN+Hzgbw3Si/v7M+kHtwlqDzhxeMIAQhkwh8Ps9AUgMseeFB0yMdL3e8wxc8DK0RuABGC5Uxy0pI4UOW6hHe6UFpJ8z18e/jY0+Gc8RnXaQiFQIlIfgRG4OGVvZwPNTKP8S+LLvUghCRfd4lUZycyx3xtT3e9LkSpr6LF8x/3/YgLwgWgjzC4AJR4UsaPuZdP2R/ZkEbpAaefI4vqzNAdhf8uhAMPJaQNOtjC+Y9Pu3LEvATmHXf4NOmSl0/+myPMRk6ANkFqUn5eoNs8ZSPuFFd4nl+0xVYbmAte72lNc8z7KrSbZZGn4BgSJJI8ppKQSs4CcHH0UQXp3ycnwVZMPi8EKDdDgW5W14Ums1Fx4rjRJKRpCjNuZlNDD6EPYkTmhsEn2Siu4JaKMw9aV4oqDwkRvInlnMPSRJZn9CCf90vKfiEoqjlhadzT8ZsjjHyTS2fz5mewBsiCbqdXPQ9F9WD3M/mnx8ezYvH3zhehM8Yv4oPg4yf/6ww2lQgu2NrNhjMCMw5mN46BAWFBQw9noUwmxW+1e4qFWd62fhiPe8dPJrxK72LwufH2t3nz18etQCqoAvdTnR9Q/n69PWf354+awTdLojV/OdTJvPw8KRtxY8m+CWJE82PCx+yAsUsfH2q3WRuQJmn3JwgzK/8Cmz0+TFavKl9y98OZgP9691NJlOrPVUbF47f6AQcHiOqzs3HpwxgxQLUrM+8hQoHvt4dF28eTOSySo1vu8k8VO3L/jPGvlEdIRkjJkEqu3uFj+ievpojb6RXvpyt1/7lykK9Fj9/rBofDfCLCjtNgshC+fpQO0EOjyfgtxl1afO3N2elYjH128E/Ks5l/xEnr3zZIFC+PR3gy61yZvzvTKYd842oy2a1+EhmvIIHiInpl3jl5k678LoX5T7nG3j9wcDl/aqbee6Ol/HLp0ANnuID7eVyOWxlyje1k5tcfOYDGdVvtaNzr8rwb79f7uFZecyj+8vnL3GcL5do2RKWw3H5CA++r1166F9dlRTz7oTfWq32693zernKtNrlCDE6WB4OV7t2Zj1ePr+mxrvv9cv+Nj+X2Kg+nJDamV0LfHwPVm6PMyf8cms37u1aGdTrDpfd4+aHzoWXvUiheTR/udxboefWfphZr1vd8qv1OXp3uRrvAF3oHX3fVC4973OJk85DFM/l1r69a7darWVm2d6Nufcf8Z/bXcgF5TGcIKF7Mv7k4hMfV5iNzd9dPu+HrRvAb69Wu/162D3gd5fr1qoda7V+7sXGd5TLT3xc0Pg+RsmfF3a0LoP11+txZjU+On93vxsetBzuhr2oJXzsTBIQ+VyhnouLew+y2/i5tdyt1uN275T6yvt2GSIfxBvCYeT9T0lI+wfZmsnNzzFXCJx/hdqZ1v6U+sqtNZS9Mo8PoYd46r+pvTj2R/+v/zJB9qvUDm1f+3k3fI5YXwtfd7dvrzO97n/Weyh+vB3KatuEuD5Xqa49xt0cpDnQsPsGP7NedvfCcImHvTbm/UDl8rv9NwqV7wf+1RIy3DvrQ9uDIDEsy/9dP3Pff/yekKx/kuEc+HsCQqfafmp6e+vlul1GezcT0Sco8A8yKi+VKPjH6+dV+R0+t39bwK3nPad/ySaOvl+qOzH/eAkDz3t8sH+v3er24LxUXpx6GCai4Tupv1UaG9N54fWve7T9OX40EvBH0zH1yrbeTBS/oRRL+lZ3vt9lzvUGPxpyXxzT7juGqCfJ//vbibit98N69uXxj/Cfvpsb46pvD4rGIDFNX2R8Ixv2xRDs/3L3M/wapHwwvNgXtUZx0/jo//RfJnFrF7d1sb/dTuu69v2xdnZB64APj08vml6fTqbTYr8xD8NBEqb9SIZeMjpAUwKF26xmHi/8nvBvMneQ8adGke/oXxW1SbHeSEjbW5zapWldvOrHsnXzpXIXnYAD/k2m9vBiZifFw46rfkMJw3kyzA+8YHzjqmTHMuqOon2vcA+I8Dm82THNin1UeFXqTIrbZFztKW2MsL4pnvDhBBiNTQdOwF0G8DN3AO9MDMN4PQ4zopkQ8/ftTWhXjXeBXLI3nY758FR5fHSq5tZ4b+iwsy1NLvzj7Ugl3Qh1MH5onCvsl4yt03nJOh1lAvBvjxp9caLB2y5/7us3pmHjGoxvNM7Fm7piaG8c3Y76+3dH+2B+eN+Ff7njik/6Rmjymy8d71gc5fbDDYj7djXKb/2z9Ui8V+hw81948RO3EMNvvqUghobdmEy2k4ZdvDLu7b5oNOAVvDTC4tm+sFMPbf3CzR+aRni68xaQN7bTTVYDOZ2cWbcnna1dr3Q0hy+Zen07MY6zrrit2uH8sj/nEuuTcNuxxX4xJle063tN2dR1s9pxTCermErWMU2t6uj1jZK/v9eyGzgHdlgS+4amh7Z2yebvG1kj1MzNFHp9xdGq1x3oa/lMI4pFQ6+appmFH02xi2K0Wgy32jWcmIq+qU/rWc0OB5f8Eb+YnYS6ltOq1ev76zz0vsAY2jD4wGgTikZ0N16z0xAhx8PS1DaKV/2isTWr99fVKrxPC+3O5Q6+fRvS/pQnNaPEM3sxnNQ3lei+5I6jbIshv1l5xxDtw5qZnW+2RolXgJLBE+QW+sXpxZpf1KYl7tbFEmT7yUZXwNXNw83Xs6azFcNOHqqC7ZzWTJ4P9M0WqkD0TlGcVC+19e1v/1G9P+n6Ghz6XB0tvqBlmJ23Bw635j++zbxQ8/fDsPRThSHkvmqnA+iQ4f5gZxhedO37uSCuueqXXdtTpUqVKlWqVKlSpUqVKlWqVKlSpUqVKlWqVB+l/wHuQhGMfKxdCAAAAABJRU5ErkJggg=="
st.sidebar.image(logo_url, use_container_width=True)
st.sidebar.title("Mining Department")
st.sidebar.subheader("Mining Engineering")
# --- CUSTOM CSS FOR PROFESSIONAL UI ---

with st.sidebar.expander("👥 Group 4 Members"):
    st.write("1. **Enrique Hannock**")
    st.write("2. **Saidi Ibrahim**")
    st.write("3. **Promise Magola**")
    st.caption("BMEN 5")

st.sidebar.divider()

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
ucs = st.sidebar.number_input("Rock Strength (UCS) [MPa]", min_value=30.0, max_value=400.0, value=45.0)
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
st.subheader("Malawi University Of Business and Applied Sciences")

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
