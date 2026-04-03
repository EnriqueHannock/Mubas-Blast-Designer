import streamlit as st
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from datetime import datetime
import io
import zipfile
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, Image as RLImage, PageBreak
)

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(page_title="MUBAS | Blast Designer", page_icon="💥", layout="wide")

# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Barlow+Condensed:wght@400;600;700;800&family=Barlow:wght@300;400;500&display=swap');
html, body, [class*="css"] { font-family: 'Barlow', sans-serif; }
.stApp { background-color: #f5efe6; color: #2c1a0e; }
[data-testid="stSidebar"] { background-color: #2c1a0e; border-right: 1px solid #4a2e1a; }
[data-testid="stSidebar"] * { color: #c9a882 !important; font-family: 'Barlow', sans-serif; }
.main-title { font-family:'Barlow Condensed',sans-serif; font-weight:800; font-size:2.6rem;
    letter-spacing:0.04em; text-transform:uppercase; color:#2c1a0e; line-height:1.1; margin:0; }
.main-subtitle { font-family:'DM Mono',monospace; font-weight:300; font-size:0.78rem;
    letter-spacing:0.12em; text-transform:uppercase; color:#7a4a28; margin-top:4px; }
.section-label { font-family:'Barlow Condensed',sans-serif; font-weight:700; font-size:0.65rem;
    letter-spacing:0.2em; text-transform:uppercase; color:#7a4a28;
    border-bottom:1px solid #d4b896; padding-bottom:6px; margin-bottom:14px; }
label, .stNumberInput label, .stCheckbox label {
    font-family:'Barlow',sans-serif !important; font-size:0.8rem !important;
    font-weight:500 !important; color:#6b4226 !important;
    letter-spacing:0.02em !important; text-transform:uppercase !important; }
input[type="number"], input[type="text"] {
    background-color:#fdf6ee !important; border:1px solid #c9a882 !important;
    border-radius:4px !important; color:#2c1a0e !important;
    font-family:'DM Mono',monospace !important; font-size:0.9rem !important; }
input[type="number"]:focus { border-color:#7a4a28 !important; box-shadow:0 0 0 2px rgba(122,74,40,0.15) !important; }
[data-testid="stForm"] { background-color:#fdf6ee; border:1px solid #d4b896; border-radius:6px; padding:24px; }
[data-testid="stFormSubmitButton"] button {
    background-color:#7a4a28 !important; color:#fdf6ee !important;
    font-family:'Barlow Condensed',sans-serif !important; font-weight:700 !important;
    font-size:1rem !important; letter-spacing:0.15em !important;
    text-transform:uppercase !important; border:none !important;
    border-radius:4px !important; padding:12px 24px !important; }
[data-testid="stFormSubmitButton"] button:hover { background-color:#5c3318 !important; }
[data-testid="stMetric"] { background-color:#fdf6ee; border:1px solid #d4b896;
    border-left:3px solid #7a4a28; border-radius:4px; padding:16px 20px !important; }
[data-testid="stMetricLabel"] { font-family:'DM Mono',monospace !important; font-size:0.65rem !important;
    letter-spacing:0.15em !important; text-transform:uppercase !important; color:#a07850 !important; }
[data-testid="stMetricValue"] { font-family:'Barlow Condensed',sans-serif !important; font-weight:700 !important;
    font-size:1.6rem !important; color:#2c1a0e !important; }
.stAlert { background-color:#fdf6ee !important; border:1px solid #d4b896 !important;
    border-radius:4px !important; color:#6b4226 !important;
    font-family:'Barlow',sans-serif !important; font-size:0.85rem !important; }
hr { border-color:#d4b896 !important; }
.sidebar-heading { font-family:'Barlow Condensed',sans-serif; font-weight:700; font-size:0.65rem;
    letter-spacing:0.2em; text-transform:uppercase; color:#e8c99a; margin-bottom:10px; }
.team-member { font-family:'Barlow',sans-serif; font-size:0.82rem; color:#a07850;
    padding:4px 0; border-bottom:1px solid #4a2e1a; }
.team-group { font-family:'DM Mono',monospace; font-size:0.7rem; color:#e8c99a;
    letter-spacing:0.08em; margin-bottom:8px; }
[data-testid="stCheckbox"] span { font-family:'Barlow',sans-serif !important;
    font-size:0.8rem !important; color:#6b4226 !important; }
.col-header { font-family:'Barlow Condensed',sans-serif; font-weight:700; font-size:0.62rem;
    letter-spacing:0.22em; text-transform:uppercase; color:#7a4a28;
    padding-bottom:8px; border-bottom:1px solid #d4b896; margin-bottom:16px; }
.stDownloadButton button { background-color:#7a4a28 !important; color:#fdf6ee !important;
    font-family:'Barlow Condensed',sans-serif !important; font-weight:700 !important;
    font-size:0.85rem !important; letter-spacing:0.12em !important;
    text-transform:uppercase !important; border:none !important; border-radius:4px !important; }
.stDownloadButton button:hover { background-color:#5c3318 !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# COLOUR PALETTE (matplotlib)
# ─────────────────────────────────────────────
SAND   = "#f5efe6"
CREAM  = "#fdf6ee"
BROWN  = "#7a4a28"
DBROWN = "#2c1a0e"
TAN    = "#d4b896"
MBROWN = "#a07850"
LBROWN = "#c9a882"


def _ax(ax, title=""):
    ax.set_facecolor(CREAM)
    ax.figure.patch.set_facecolor(CREAM)
    for sp in ax.spines.values():
        sp.set_color(TAN)
    ax.tick_params(colors=MBROWN, labelsize=8)
    ax.xaxis.label.set_color(BROWN)
    ax.yaxis.label.set_color(BROWN)
    if title:
        ax.set_title(title, color=DBROWN, fontsize=10, fontweight="bold", pad=8)
    ax.grid(color=TAN, linestyle="--", linewidth=0.5, alpha=0.6)


# ─────────────────────────────────────────────
# BLAST CALCULATIONS
# ─────────────────────────────────────────────
def calc(d_mm, h_bench, ucs, rho_anfo, pf_target, subdrill, use_decking, deck_stemming):
    d = d_mm / 1000.0

    # Burden (Langefors-Kihlstrom simplified)
    B = round(max(0.5, 0.012 * (d_mm / 10) * np.sqrt(rho_anfo / ucs) * d_mm / 25.4 * 0.3048), 2)
    S = round(1.15 * B, 2)
    T = round(max(0.3, 0.7 * B), 2)
    L = round(h_bench + subdrill, 2)

    if use_decking and deck_stemming > 0:
        available = max(0.1, L - T - deck_stemming)
        cl_bot = round(available * 0.55, 2)
        cl_top = round(available * 0.45, 2)
        cl_tot = round(cl_bot + cl_top, 2)
    else:
        cl_tot = round(max(0.1, L - T), 2)
        cl_bot = cl_tot
        cl_top = 0.0

    Q   = round(rho_anfo * np.pi * (d / 2) ** 2 * cl_tot, 2)
    V   = round(B * S * h_bench, 2)
    pf  = round(Q / V if V > 0 else 0, 3)
    sd  = round(1.0 / (B * S) if B * S > 0 else 0, 3)
    A   = max(1, 10 - ucs / 50)
    x50 = round(A * (V / max(Q, 0.01)) ** 0.8 * max(Q, 0.01) ** (1/6) * (115/100) ** (19/30), 2)

    return dict(
        B=B, S=S, T=T, subdrill=subdrill, L=L,
        cl_bot=cl_bot, cl_top=cl_top, cl_tot=cl_tot,
        Q=Q, V=V, pf=pf, sd=sd, x50=x50,
        mode="Decked" if (use_decking and deck_stemming > 0) else "Continuous",
        deck_stemming=deck_stemming if use_decking else 0.0,
        d_mm=d_mm, h_bench=h_bench, ucs=ucs, rho_anfo=rho_anfo,
    )


# ─────────────────────────────────────────────
# FIGURES
# ─────────────────────────────────────────────
def fig_profile(r):
    fig, ax = plt.subplots(figsize=(3.2, 6.5))
    _ax(ax, "Hole Profile")
    L, T, h = r["L"], r["T"], r["h_bench"]
    cl_bot, cl_top = r["cl_bot"], r["cl_top"]
    deck = r["deck_stemming"]
    sub  = r["subdrill"]
    w    = 0.38

    ax.axhline(0,   color=MBROWN, lw=1, ls="--", alpha=0.7, label="Bench Top")
    ax.axhline(-h,  color=MBROWN, lw=1, ls=":",  alpha=0.7, label="Bench Floor")

    # Stemming
    ax.barh(-T/2, w, height=T, left=-w/2, color=TAN,   alpha=0.9, edgecolor=BROWN, lw=0.5, label="Stemming")

    if r["mode"] == "Decked" and cl_top > 0:
        y0 = T
        ax.barh(-(y0 + cl_top/2),           w, height=cl_top, left=-w/2, color=BROWN,  alpha=0.85, edgecolor=DBROWN, lw=0.5, label="Top Charge")
        ax.barh(-(y0 + cl_top + deck/2),     w, height=deck,   left=-w/2, color=LBROWN, alpha=0.7,  edgecolor=TAN,    lw=0.4, label="Mid Stemming")
        ax.barh(-(y0 + cl_top + deck + cl_bot/2), w, height=cl_bot, left=-w/2, color=DBROWN, alpha=0.9, edgecolor=DBROWN, lw=0.5, label="Bottom Charge")
    else:
        ax.barh(-(T + cl_bot/2), w, height=cl_bot, left=-w/2, color=DBROWN, alpha=0.9, edgecolor=DBROWN, lw=0.5, label="Charge")

    if sub > 0:
        ax.barh(-L + sub/2, w, height=sub, left=-w/2, color=SAND, alpha=0.7, edgecolor=TAN, lw=0.4, label="Subdrill")

    ax.set_xlim(-0.55, 0.55)
    ax.set_ylim(-L - 0.3, 0.6)
    ticks = np.arange(0, -(L+0.1), -1)
    ax.set_yticks(ticks)
    ax.set_yticklabels([f"{abs(v):.0f} m" for v in ticks], fontsize=7)
    ax.set_xticks([])
    ax.legend(loc="lower right", fontsize=6, framealpha=0.8, facecolor=CREAM, edgecolor=TAN)
    fig.tight_layout()
    return fig


def fig_pattern(r):
    fig, ax = plt.subplots(figsize=(5, 4))
    _ax(ax, "Blast Hole Pattern")
    B, S = r["B"], r["S"]
    rows, cols = 4, 5
    for row in range(rows):
        for col in range(cols):
            x = col * S + (row % 2) * (S / 2)
            y = row * B
            ax.plot(x, y, "o", ms=10, color=BROWN, mec=DBROWN, mew=0.8)
    ax.set_xlabel("Spacing direction (m)", fontsize=9)
    ax.set_ylabel("Burden direction (m)", fontsize=9)
    ax.set_aspect("equal")
    ax.annotate("", xy=(S, 0.15), xytext=(0, 0.15), arrowprops=dict(arrowstyle="<->", color=MBROWN, lw=1.2))
    ax.text(S/2, 0.32, f"S = {S} m", ha="center", fontsize=8, color=BROWN)
    ax.annotate("", xy=(S*4.8, B), xytext=(S*4.8, 0), arrowprops=dict(arrowstyle="<->", color=MBROWN, lw=1.2))
    ax.text(S*4.92, B/2, f"B = {B} m", ha="left", fontsize=8, color=BROWN)
    fig.tight_layout()
    return fig


def fig_pf_sensitivity(r):
    fig, ax = plt.subplots(figsize=(5, 4))
    _ax(ax, "Powder Factor vs Hole Diameter")
    diams = np.linspace(50, 250, 60)
    pfs   = [calc(d, r["h_bench"], r["ucs"], r["rho_anfo"], 1.0,
                  r["subdrill"], r["mode"]=="Decked", r["deck_stemming"])["pf"] for d in diams]
    ax.plot(diams, pfs, color=BROWN, lw=2)
    ax.axvline(r["d_mm"], color=DBROWN, ls="--", lw=1.2, alpha=0.8)
    ax.axhline(r["pf"],   color=MBROWN, ls=":",  lw=1.0, alpha=0.8)
    ax.scatter([r["d_mm"]], [r["pf"]], color=DBROWN, s=60, zorder=5)
    ax.set_xlabel("Hole Diameter (mm)", fontsize=9)
    ax.set_ylabel("Powder Factor (kg/m³)", fontsize=9)
    fig.tight_layout()
    return fig


def fig_fragmentation(r):
    fig, ax = plt.subplots(figsize=(5, 4))
    _ax(ax, "Fragmentation Prediction (Kuz-Ram)")
    pfs  = np.linspace(0.3, 2.5, 60)
    V    = r["V"]
    A    = max(1, 10 - r["ucs"] / 50)
    x50s = []
    for pf in pfs:
        Q = max(pf * V, 0.01)
        x50s.append(A * (V/Q)**0.8 * Q**(1/6) * (115/100)**(19/30))
    ax.plot(pfs, x50s, color=BROWN, lw=2, label="Predicted x50")
    ax.axvline(r["pf"],  color=DBROWN, ls="--", lw=1.2, alpha=0.8, label="Current PF")
    ax.axhline(r["x50"], color=MBROWN, ls=":",  lw=1.0, alpha=0.8, label=f"x50 = {r['x50']} mm")
    ax.scatter([r["pf"]], [r["x50"]], color=DBROWN, s=60, zorder=5)
    ax.set_xlabel("Powder Factor (kg/m³)", fontsize=9)
    ax.set_ylabel("Mean Fragment Size x50 (mm)", fontsize=9)
    ax.legend(fontsize=7.5, facecolor=CREAM, edgecolor=TAN)
    fig.tight_layout()
    return fig


def fig_distribution(r):
    fig, ax = plt.subplots(figsize=(4.5, 3.8))
    _ax(ax, "Explosive Distribution per Hole")
    if r["mode"] == "Decked":
        zones  = ["Bottom\nCharge", "Mid\nStemming", "Top\nCharge", "Stemming"]
        vals   = [r["cl_bot"], r["deck_stemming"], r["cl_top"], r["T"]]
        clrs   = [DBROWN, LBROWN, BROWN, TAN]
    else:
        zones  = ["Charge", "Stemming"]
        vals   = [r["cl_tot"], r["T"]]
        clrs   = [DBROWN, TAN]
    bars = ax.bar(zones, vals, color=clrs, edgecolor=DBROWN, lw=0.6, width=0.5)
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.04,
                f"{v:.2f} m", ha="center", va="bottom", fontsize=8, color=BROWN)
    ax.set_ylabel("Length (m)", fontsize=9)
    ax.set_ylim(0, max(vals) * 1.3)
    fig.tight_layout()
    return fig


def fig_to_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    buf.seek(0)
    return buf.read()


# ─────────────────────────────────────────────
# PDF GENERATION
# ─────────────────────────────────────────────
C_SAND   = colors.HexColor("#f5efe6")
C_CREAM  = colors.HexColor("#fdf6ee")
C_BROWN  = colors.HexColor("#7a4a28")
C_DBROWN = colors.HexColor("#2c1a0e")
C_TAN    = colors.HexColor("#d4b896")
C_MBROWN = colors.HexColor("#a07850")


def build_pdf(r, figs_bytes, fig_labels):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)

    title_s  = ParagraphStyle("T",  fontName="Helvetica-Bold",   fontSize=18, textColor=C_DBROWN, alignment=TA_CENTER, spaceAfter=3)
    sub_s    = ParagraphStyle("S",  fontName="Helvetica",         fontSize=9,  textColor=C_MBROWN, alignment=TA_CENTER, spaceAfter=2)
    h2_s     = ParagraphStyle("H2", fontName="Helvetica-Bold",   fontSize=12, textColor=C_BROWN,  spaceBefore=12, spaceAfter=4)
    body_s   = ParagraphStyle("B",  fontName="Helvetica",         fontSize=9,  textColor=C_DBROWN, leading=14)
    small_s  = ParagraphStyle("Sm", fontName="Helvetica",         fontSize=8,  textColor=C_MBROWN, alignment=TA_CENTER)
    cap_s    = ParagraphStyle("C",  fontName="Helvetica-Oblique", fontSize=8,  textColor=C_MBROWN, alignment=TA_CENTER, spaceAfter=6)

    ts_header = TableStyle([
        ("BACKGROUND",     (0,0), (-1,0),   C_BROWN),
        ("TEXTCOLOR",      (0,0), (-1,0),   colors.white),
        ("FONTNAME",       (0,0), (-1,0),   "Helvetica-Bold"),
        ("FONTSIZE",       (0,0), (-1,-1),  9),
        ("ROWBACKGROUNDS", (0,1), (-1,-1),  [C_CREAM, C_SAND]),
        ("GRID",           (0,0), (-1,-1),  0.4, C_TAN),
        ("TOPPADDING",     (0,0), (-1,-1),  4),
        ("BOTTOMPADDING",  (0,0), (-1,-1),  4),
        ("TEXTCOLOR",      (0,1), (-1,-1),  C_DBROWN),
    ])

    story = []

    # ── Cover / header
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph("MUBAS Production Blast Planner", title_s))
    story.append(Paragraph("Malawi University of Business and Applied Sciences", sub_s))
    story.append(Paragraph("Department of Mining and Mineral Processing Engineering", sub_s))
    story.append(Spacer(1, 0.2*cm))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_BROWN))
    story.append(Spacer(1, 0.1*cm))
    story.append(Paragraph(f"Report Generated: {datetime.now().strftime('%d %B %Y, %H:%M')}", small_s))
    story.append(Paragraph("Group 4 — BMEN 5  |  Enrique Hannock · Saidi Ibrahim · Promise Magola", small_s))
    story.append(HRFlowable(width="100%", thickness=0.5, color=C_TAN))
    story.append(Spacer(1, 0.4*cm))

    # ── 1. Inputs
    story.append(Paragraph("1. Design Inputs", h2_s))
    story.append(HRFlowable(width="100%", thickness=0.5, color=C_TAN))
    story.append(Spacer(1, 0.2*cm))
    inp_rows = [
        ["Parameter", "Value", "Unit"],
        ["Hole Diameter",           str(r["d_mm"]),          "mm"],
        ["Bench Height",            str(r["h_bench"]),        "m"],
        ["Rock Strength (UCS)",     str(r["ucs"]),            "MPa"],
        ["ANFO Density",            str(r["rho_anfo"]),       "kg/m³"],
        ["Subdrill",                str(r["subdrill"]),       "m"],
        ["Charging Mode",           r["mode"],                "—"],
        ["Mid-Deck Stemming",       str(r["deck_stemming"]), "m"],
    ]
    t1 = Table(inp_rows, colWidths=[7*cm, 5*cm, 4*cm])
    t1.setStyle(ts_header)
    story.append(t1)
    story.append(Spacer(1, 0.5*cm))

    # ── 2. Calculated Results
    story.append(Paragraph("2. Calculated Design Parameters", h2_s))
    story.append(HRFlowable(width="100%", thickness=0.5, color=C_TAN))
    story.append(Spacer(1, 0.2*cm))
    out_rows = [
        ["Parameter", "Value", "Unit"],
        ["Burden B",                    str(r["B"]),      "m"],
        ["Spacing S",                   str(r["S"]),      "m"],
        ["Stemming T",                  str(r["T"]),      "m"],
        ["Hole Depth L",                str(r["L"]),      "m"],
        ["Total Charge Length",         str(r["cl_tot"]), "m"],
        ["Bottom Charge Length",        str(r["cl_bot"]), "m"],
        ["Top Charge Length",           str(r["cl_top"]), "m"],
        ["Explosive per Hole",          str(r["Q"]),      "kg"],
        ["Rock Volume per Hole",        str(r["V"]),      "m³"],
        ["Actual Powder Factor",        str(r["pf"]),     "kg/m³"],
        ["Specific Drilling",           str(r["sd"]),     "m/m³"],
        ["Mean Fragment Size (x50)",    str(r["x50"]),    "mm"],
    ]
    t2 = Table(out_rows, colWidths=[8*cm, 4*cm, 4*cm])
    t2.setStyle(ts_header)
    story.append(t2)
    story.append(Spacer(1, 0.5*cm))

    # ── 3. Interpretation
    story.append(Paragraph("3. Engineering Interpretation", h2_s))
    story.append(HRFlowable(width="100%", thickness=0.5, color=C_TAN))
    story.append(Spacer(1, 0.2*cm))
    pf_tag  = "optimal" if 0.6 <= r["pf"] <= 1.4 else ("high — consider reducing charge" if r["pf"] > 1.4 else "low — consider increasing charge")
    frg_tag = "fine" if r["x50"] < 200 else ("acceptable" if r["x50"] < 500 else "coarse — review design")
    txt = (
        f"Burden <b>{r['B']} m</b> and spacing <b>{r['S']} m</b> were derived using the "
        f"Langefors-Kihlstrom method. The actual powder factor of <b>{r['pf']} kg/m³</b> is {pf_tag}. "
        f"Kuz-Ram fragmentation modelling gives a mean fragment size (x50) of <b>{r['x50']} mm</b>, "
        f"classified as {frg_tag}. Charging mode is <b>{r['mode']}</b>."
        + (f" Deck stemming of <b>{r['deck_stemming']} m</b> is applied for energy distribution." if r["mode"] == "Decked" else "")
        + (f" Subdrill of <b>{r['subdrill']} m</b> is included." if r["subdrill"] > 0 else "")
    )
    story.append(Paragraph(txt, body_s))
    story.append(Spacer(1, 0.4*cm))

    # ── 4. Charts
    story.append(PageBreak())
    story.append(Paragraph("4. Design Charts", h2_s))
    story.append(HRFlowable(width="100%", thickness=0.5, color=C_TAN))
    story.append(Spacer(1, 0.3*cm))

    iw = 7.6*cm
    ih = 5.8*cm

    # Profile (tall) + pattern side by side
    profile_img = RLImage(io.BytesIO(figs_bytes[0]), width=4.2*cm, height=8.5*cm)
    pattern_img = RLImage(io.BytesIO(figs_bytes[1]), width=iw,     height=ih)

    row0 = Table(
        [[profile_img, pattern_img],
         [Paragraph("Fig 1: " + fig_labels[0], cap_s), Paragraph("Fig 2: " + fig_labels[1], cap_s)]],
        colWidths=[5*cm, iw + 0.5*cm]
    )
    row0.setStyle(TableStyle([("ALIGN",(0,0),(-1,-1),"CENTER"),("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
    story.append(row0)
    story.append(Spacer(1, 0.3*cm))

    # Remaining in pairs
    rest = list(zip(figs_bytes[2:], fig_labels[2:]))
    for i in range(0, len(rest), 2):
        cells_img = []
        cells_cap = []
        for j in range(2):
            if i + j < len(rest):
                fb, lbl = rest[i + j]
                cells_img.append(RLImage(io.BytesIO(fb), width=iw, height=ih))
                cells_cap.append(Paragraph(f"Fig {i+j+3}: {lbl}", cap_s))
            else:
                cells_img.append(Paragraph("", cap_s))
                cells_cap.append(Paragraph("", cap_s))
        row = Table([cells_img, cells_cap], colWidths=[iw + 0.5*cm, iw + 0.5*cm])
        row.setStyle(TableStyle([("ALIGN",(0,0),(-1,-1),"CENTER"),("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
        story.append(row)
        story.append(Spacer(1, 0.2*cm))

    # Footer
    story.append(Spacer(1, 0.5*cm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=C_TAN))
    story.append(Paragraph(
        "Results are based on empirical blast design formulae (Langefors-Kihlstrom, Kuz-Ram). "
        "Always verify designs with a qualified blasting engineer.",
        ParagraphStyle("Ft", fontName="Helvetica-Oblique", fontSize=7.5,
                       textColor=C_MBROWN, alignment=TA_CENTER, spaceBefore=4)
    ))

    doc.build(story)
    buf.seek(0)
    return buf.read()


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        '<img src="https://www.mubas.ac.mw/wp-content/uploads/2021/06/mubas-logo.png" '
        'style="width:100%;max-width:160px;display:block;margin:0 auto 14px auto;'
        'background:#fff;border-radius:4px;padding:6px;">',
        unsafe_allow_html=True
    )
    st.markdown('<div class="sidebar-heading">Control Panel</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<div class="sidebar-heading">Project Team</div>', unsafe_allow_html=True)
    st.markdown('<div class="team-group">Group 4 — BMEN 5</div>', unsafe_allow_html=True)
    for name in ["Enrique Hannock", "Saidi Ibrahim", "Promise Magola"]:
        st.markdown(f'<div class="team-member">{name}</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(
        '<div style="font-family:\'DM Mono\',monospace;font-size:0.65rem;'
        'color:#6b4226;letter-spacing:0.1em;text-transform:uppercase;">'
        'Innovate. Create. Generate.</div>',
        unsafe_allow_html=True
    )


# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown('<div class="main-title">Production Blast Planner</div>', unsafe_allow_html=True)
st.markdown('<div class="main-subtitle">Malawi University of Business and Applied Sciences</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")


# ─────────────────────────────────────────────
# INPUT FORM
# ─────────────────────────────────────────────
st.markdown('<div class="section-label">Engineering Design Inputs</div>', unsafe_allow_html=True)

with st.form("blast_form"):
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown('<div class="col-header">Geometry & Rock</div>', unsafe_allow_html=True)
        d_mm    = st.number_input("Hole Diameter (mm)",      32.0,  400.0, value=90.0,  step=5.0)
        h_bench = st.number_input("Bench Height (m)",         1.0,   50.0, value=9.0,   step=0.5)
        ucs     = st.number_input("Rock Strength UCS (MPa)", 30.0,  400.0, value=45.0,  step=10.0)

    with c2:
        st.markdown('<div class="col-header">Explosives</div>', unsafe_allow_html=True)
        rho_anfo  = st.number_input("ANFO Density (kg/m³)",          value=825.0, min_value=100.0, step=25.0)
        pf_target = st.number_input("Target Powder Factor (kg/m³)",  0.1, 2.0, value=1.0, step=0.1)
        st.markdown("<br>", unsafe_allow_html=True)
        use_subdrill = st.checkbox("Enable Subdrill (optional)")
        subdrill_val = 0.0
        if use_subdrill:
            subdrill_val = st.number_input("Subdrill Depth (m)", 0.0, 5.0, value=0.5, step=0.1)

    with c3:
        st.markdown('<div class="col-header">Advanced Charging</div>', unsafe_allow_html=True)
        use_decking = st.checkbox("Apply Deck Charging (optional)")
        deck_stemming = 0.0
        if use_decking:
            deck_stemming = st.number_input("Mid-Deck Stemming (m)", 0.0, 5.0, value=1.5, step=0.1)
        st.markdown("<br>" * 5, unsafe_allow_html=True)
        submit = st.form_submit_button("Generate Design Report", use_container_width=True)


# ─────────────────────────────────────────────
# RESULTS
# ─────────────────────────────────────────────
if submit:
    r = calc(d_mm, h_bench, ucs, rho_anfo, pf_target,
             subdrill_val, use_decking, deck_stemming)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")

    # ── Key metrics
    st.markdown('<div class="section-label">Design Output — Key Parameters</div>', unsafe_allow_html=True)
    m1, m2, m3, m4, m5, m6 = st.columns(6)
    m1.metric("Burden",         f"{r['B']} m")
    m2.metric("Spacing",        f"{r['S']} m")
    m3.metric("Stemming",       f"{r['T']} m")
    m4.metric("Hole Depth",     f"{r['L']} m")
    m5.metric("Powder Factor",  f"{r['pf']} kg/m³")
    m6.metric("Fragment x50",   f"{r['x50']} mm")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Full results table (outputs only)
    with st.expander("Full Parameter Table", expanded=True):
        tbl = pd.DataFrame([
            {"Parameter": "Burden B",               "Value": r["B"],      "Unit": "m"},
            {"Parameter": "Spacing S",              "Value": r["S"],      "Unit": "m"},
            {"Parameter": "Stemming T",             "Value": r["T"],      "Unit": "m"},
            {"Parameter": "Subdrill",               "Value": r["subdrill"],"Unit": "m"},
            {"Parameter": "Hole Depth L",           "Value": r["L"],      "Unit": "m"},
            {"Parameter": "Total Charge Length",    "Value": r["cl_tot"], "Unit": "m"},
            {"Parameter": "Bottom Charge Length",   "Value": r["cl_bot"], "Unit": "m"},
            {"Parameter": "Top Charge Length",      "Value": r["cl_top"], "Unit": "m"},
            {"Parameter": "Explosive per Hole",     "Value": r["Q"],      "Unit": "kg"},
            {"Parameter": "Rock Volume per Hole",   "Value": r["V"],      "Unit": "m³"},
            {"Parameter": "Actual Powder Factor",   "Value": r["pf"],     "Unit": "kg/m³"},
            {"Parameter": "Specific Drilling",      "Value": r["sd"],     "Unit": "m/m³"},
            {"Parameter": "Mean Fragment x50",      "Value": r["x50"],    "Unit": "mm"},
            {"Parameter": "Charging Mode",          "Value": r["mode"],   "Unit": "—"},
        ])
        st.dataframe(tbl, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ── Charts
    st.markdown('<div class="section-label">Design Charts</div>', unsafe_allow_html=True)

    f1 = fig_profile(r)
    f2 = fig_pattern(r)
    f3 = fig_pf_sensitivity(r)
    f4 = fig_fragmentation(r)
    f5 = fig_distribution(r)

    fig_labels = [
        "Hole Profile",
        "Blast Hole Pattern",
        "Powder Factor vs Hole Diameter",
        "Fragmentation Prediction (Kuz-Ram)",
        "Explosive Distribution per Hole",
    ]

    rc1, rc2, rc3 = st.columns([1.1, 2, 2])
    with rc1:
        st.pyplot(f1, use_container_width=True)
        st.caption("Hole Profile")
    with rc2:
        st.pyplot(f2, use_container_width=True)
        st.caption("Blast Hole Pattern")
    with rc3:
        st.pyplot(f5, use_container_width=True)
        st.caption("Explosive Distribution per Hole")

    rd1, rd2 = st.columns(2)
    with rd1:
        st.pyplot(f3, use_container_width=True)
        st.caption("Powder Factor Sensitivity")
    with rd2:
        st.pyplot(f4, use_container_width=True)
        st.caption("Fragmentation Prediction (Kuz-Ram)")

    # ── Downloads
    st.markdown("---")
    st.markdown('<div class="section-label">Download Options</div>', unsafe_allow_html=True)

    figs_bytes = [fig_to_bytes(f) for f in [f1, f2, f3, f4, f5]]

    pdf_bytes = build_pdf(r, figs_bytes, fig_labels)

    csv_df = pd.DataFrame([
        {"Parameter": "Burden B",             "Value": r["B"],       "Unit": "m"},
        {"Parameter": "Spacing S",            "Value": r["S"],       "Unit": "m"},
        {"Parameter": "Stemming T",           "Value": r["T"],       "Unit": "m"},
        {"Parameter": "Subdrill",             "Value": r["subdrill"],"Unit": "m"},
        {"Parameter": "Hole Depth L",         "Value": r["L"],       "Unit": "m"},
        {"Parameter": "Total Charge Length",  "Value": r["cl_tot"],  "Unit": "m"},
        {"Parameter": "Bottom Charge Length", "Value": r["cl_bot"],  "Unit": "m"},
        {"Parameter": "Top Charge Length",    "Value": r["cl_top"],  "Unit": "m"},
        {"Parameter": "Explosive per Hole",   "Value": r["Q"],       "Unit": "kg"},
        {"Parameter": "Rock Volume per Hole", "Value": r["V"],       "Unit": "m³"},
        {"Parameter": "Actual Powder Factor", "Value": r["pf"],      "Unit": "kg/m³"},
        {"Parameter": "Specific Drilling",    "Value": r["sd"],      "Unit": "m/m³"},
        {"Parameter": "Mean Fragment x50",    "Value": r["x50"],     "Unit": "mm"},
        {"Parameter": "Charging Mode",        "Value": r["mode"],    "Unit": "—"},
        # inputs also captured in CSV summary
        {"Parameter": "INPUT: Hole Diameter", "Value": r["d_mm"],    "Unit": "mm"},
        {"Parameter": "INPUT: Bench Height",  "Value": r["h_bench"], "Unit": "m"},
        {"Parameter": "INPUT: UCS",           "Value": r["ucs"],     "Unit": "MPa"},
        {"Parameter": "INPUT: ANFO Density",  "Value": r["rho_anfo"],"Unit": "kg/m³"},
    ])
    csv_io = io.StringIO()
    csv_df.to_csv(csv_io, index=False)

    zip_io = io.BytesIO()
    with zipfile.ZipFile(zip_io, "w") as zf:
        for fb, lbl in zip(figs_bytes, fig_labels):
            zf.writestr(lbl.replace(" ", "_").replace("(","").replace(")","") + ".png", fb)
    zip_io.seek(0)

    ts = datetime.now().strftime("%Y%m%d_%H%M")
    dl1, dl2, dl3 = st.columns(3)

    with dl1:
        st.download_button(
            label="Download PDF Report",
            data=pdf_bytes,
            file_name=f"MUBAS_Blast_Report_{ts}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
    with dl2:
        st.download_button(
            label="Download Results CSV",
            data=csv_io.getvalue(),
            file_name=f"MUBAS_Blast_Results_{ts}.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with dl3:
        st.download_button(
            label="Download Charts ZIP",
            data=zip_io.getvalue(),
            file_name=f"MUBAS_Blast_Charts_{ts}.zip",
            mime="application/zip",
            use_container_width=True,
        )

    plt.close("all")
