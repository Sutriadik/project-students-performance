"""
dashboard.py — Business Dashboard Student Dropout
Jaya Jaya Institut | Stakeholder View
streamlit run dashboard.py
"""

import warnings
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Student Dashboard — Jaya Jaya Institut",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Colour palette ────────────────────────────────────────────
C_RED   = "#C53030"
C_GREEN = "#276749"
C_BLUE  = "#2B6CB0"
C_AMB   = "#D69E2E"
C_LRED  = "#FC8181"
C_LGRN  = "#68D391"
C_LBLUE = "#63B3ED"
C_LAMB  = "#F6AD55"

STATUS_COLORS = {
    "Dropout":  C_LRED,
    "Enrolled": C_LBLUE,
    "Graduate": C_LGRN,
}

# ── CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
html, body, [class*="css"], .stApp {
    background-color: #F7FAFC !important;
    color: #1A202C !important;
    font-family: 'Segoe UI', sans-serif;
}
#MainMenu, footer, header { visibility: hidden; }

[data-testid="stSidebar"] {
    background-color: #EBF8FF !important;
    border-right: 1px solid #BEE3F8;
}
[data-testid="stSidebar"] * { color: #1A365D !important; }

.kpi {
    background: white; border-radius: 10px; padding: 16px 18px;
    border-left: 4px solid #3182CE;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    margin-bottom: 6px;
}
.kpi.red   { border-left-color: #C53030; }
.kpi.green { border-left-color: #276749; }
.kpi.amber { border-left-color: #D69E2E; }
.kpi.blue  { border-left-color: #2B6CB0; }
.kpi-lbl { font-size:.71rem; font-weight:700; color:#718096;
           text-transform:uppercase; letter-spacing:.06em; }
.kpi-val { font-size:1.75rem; font-weight:800; color:#1A202C; line-height:1.2; }
.kpi-sub { font-size:.74rem; color:#A0AEC0; margin-top:2px; }

.sec { font-size:.95rem; font-weight:700; color:#1A365D;
       border-left:4px solid #3182CE; padding-left:10px;
       margin:22px 0 12px 0; }

.ibox { border-radius:8px; padding:11px 15px; margin:8px 0; font-size:.86rem; }
.ibox.info   { background:#EBF8FF; border:1px solid #90CDF4; color:#1A365D; }
.ibox.danger { background:#FFF5F5; border:1px solid #FEB2B2; color:#63171B; }
.ibox.warn   { background:#FFFBEB; border:1px solid #F6E05E; color:#744210; }

.ptitle { font-size:1.55rem; font-weight:800; color:#1A365D; margin-bottom:2px; }
.psub   { font-size:.88rem; color:#718096; margin-bottom:14px; }
.divider { height:2px;
           background:linear-gradient(90deg,#3182CE,#90CDF4,transparent);
           border:none; margin:12px 0 18px 0; }

.stTabs [data-baseweb="tab-list"] {
    background: white; border-radius: 8px; padding: 4px; gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 6px; font-weight: 600; color: #4A5568;
}
.stTabs [aria-selected="true"] {
    background: #EBF8FF !important; color: #1A365D !important;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────
def kpi(label, val, sub="", cls="blue"):
    return (f'<div class="kpi {cls}"><div class="kpi-lbl">{label}</div>'
            f'<div class="kpi-val">{val}</div>'
            f'<div class="kpi-sub">{sub}</div></div>')

def sec(title, icon=""):
    st.markdown(f'<div class="sec">{icon} {title}</div>', unsafe_allow_html=True)

def ibox(text, kind="info"):
    icons = {"info": "ℹ️", "danger": "🔴", "warn": "⚠️"}
    st.markdown(f'<div class="ibox {kind}">{icons[kind]} {text}</div>',
                unsafe_allow_html=True)

def pchart(fig, h=340):
    fig.update_layout(
        height=h,
        font=dict(family="Segoe UI", size=11, color="#2D3748"),
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(t=46, b=10, l=8, r=8),
        title_font=dict(size=13, color="#1A365D"),
    )
    fig.update_xaxes(showgrid=True, gridcolor="#EDF2F7", zeroline=False,
                     tickfont=dict(size=10), title_font=dict(size=11))
    fig.update_yaxes(showgrid=True, gridcolor="#EDF2F7", zeroline=False,
                     tickfont=dict(size=10), title_font=dict(size=11))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# ── Load data ─────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv('data.csv', delimiter=';')
    # Normalise column names: spaces → underscores
    df.columns = [c.strip().replace(' ', '_').replace('(', '').replace(')', '')
                  .replace("'", "") for c in df.columns]
    return df

df = load_data()

# Kolom key (sudah di-normalise)
COL_STATUS      = "Target"           if "Target" in df.columns else "Status"
COL_GENDER      = "Gender"
COL_SCHOLAR     = "Scholarship_holder"
COL_TUITION     = "Tuition_fees_up_to_date"
COL_DEBTOR      = "Debtor"
COL_AGE         = "Age_at_enrollment"
COL_ADMISSION   = "Admission_grade"
COL_COURSE      = "Course"
COL_DAYTIME     = "Daytimeevening_attendance"
COL_G1_APPROVED = "Curricular_units_1st_sem_approved"
COL_G2_APPROVED = "Curricular_units_2nd_sem_approved"
COL_G1_GRADE    = "Curricular_units_1st_sem_grade"
COL_G2_GRADE    = "Curricular_units_2nd_sem_grade"
COL_DISPLACED   = "Displaced"
COL_INTL        = "International"

# Status labels
STATUS_ORDER = ["Dropout", "Enrolled", "Graduate"]


# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:10px 0 16px'>
        <div style='font-size:2rem'>🎓</div>
        <div style='font-size:1rem;font-weight:700;color:#1A365D'>Student Analytics</div>
        <div style='font-size:.74rem;color:#4A5568'>Jaya Jaya Institut · Monitoring</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.caption("**Filter Data**")

    status_filter = st.multiselect(
        "Status Siswa",
        options=STATUS_ORDER,
        default=STATUS_ORDER,
    )
    gender_filter = st.multiselect(
        "Gender",
        options=[0, 1],
        default=[0, 1],
        format_func=lambda x: "Laki-laki" if x == 1 else "Perempuan",
    )
    scholar_filter = st.multiselect(
        "Penerima Beasiswa",
        options=[0, 1],
        default=[0, 1],
        format_func=lambda x: "Ya" if x == 1 else "Tidak",
    )

    st.markdown("---")
    st.caption(f"**Dataset:** {len(df):,} siswa terdaftar")

# Apply filter
dff = df[
    (df[COL_STATUS].isin(status_filter)) &
    (df[COL_GENDER].isin(gender_filter)) &
    (df[COL_SCHOLAR].isin(scholar_filter))
].copy()


# ══════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════
st.markdown('<div class="ptitle">🎓 Student Performance Dashboard</div>',
            unsafe_allow_html=True)
st.markdown(
    '<div class="psub">Business Intelligence — Jaya Jaya Institut | '
    f'Menampilkan <b>{len(dff):,}</b> dari {len(df):,} siswa</div>',
    unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# VISUALISASI 1 — KPI OVERVIEW
# ══════════════════════════════════════════════════════════════
total      = len(dff)
dropout_n  = int((dff[COL_STATUS] == "Dropout").sum())
graduate_n = int((dff[COL_STATUS] == "Graduate").sum())
enrolled_n = int((dff[COL_STATUS] == "Enrolled").sum())
dropout_rt = dropout_n / total * 100 if total else 0
graduate_rt= graduate_n / total * 100 if total else 0

avg_g1 = dff[COL_G1_GRADE].replace(0, np.nan).mean()
avg_g2 = dff[COL_G2_GRADE].replace(0, np.nan).mean()

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.markdown(kpi("Total Siswa",     f"{total:,}",      "Data terpilih"), unsafe_allow_html=True)
c2.markdown(kpi("Dropout",         f"{dropout_n:,}",  f"{dropout_rt:.1f}% dari total", "red"), unsafe_allow_html=True)
c3.markdown(kpi("Graduate",        f"{graduate_n:,}", f"{graduate_rt:.1f}% dari total", "green"), unsafe_allow_html=True)
c4.markdown(kpi("Masih Enrolled",  f"{enrolled_n:,}", f"{enrolled_n/total*100:.1f}%",  "amber"), unsafe_allow_html=True)
c5.markdown(kpi("Avg Nilai Sem 1", f"{avg_g1:.1f}" if not np.isnan(avg_g1) else "—", "Skala 0–20", "blue"), unsafe_allow_html=True)
c6.markdown(kpi("Avg Nilai Sem 2", f"{avg_g2:.1f}" if not np.isnan(avg_g2) else "—", "Skala 0–20", "blue"), unsafe_allow_html=True)

if dropout_rt > 30:
    ibox(f"<b>⚠️ Perhatian:</b> Dropout rate <b>{dropout_rt:.1f}%</b> tergolong tinggi. "
         f"Hampir 1 dari 3 siswa tidak menyelesaikan pendidikannya.", "danger")
st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# VISUALISASI 2 & 3 — DISTRIBUSI STATUS & DROPOUT PER COURSE
# ══════════════════════════════════════════════════════════════
sec("Distribusi Status & Dropout per Program Studi", "📊")
c1, c2 = st.columns([1, 1.6])

with c1:
    counts = dff[COL_STATUS].value_counts().reindex(STATUS_ORDER, fill_value=0)
    fig = go.Figure(go.Pie(
        values=counts.values,
        labels=counts.index,
        marker=dict(
            colors=[STATUS_COLORS.get(s, "#CBD5E0") for s in counts.index],
            line=dict(color="white", width=2)),
        hole=0.55,
        textinfo="percent+label",
        textfont_size=11,
        hovertemplate="<b>%{label}</b><br>%{value} siswa (%{percent})<extra></extra>",
    ))
    fig.add_annotation(
        text=f"<b>{total:,}</b><br><span style='font-size:10px'>Siswa</span>",
        x=0.5, y=0.5, showarrow=False, font=dict(size=13, color="#1A202C"))
    fig.update_layout(
        title="<b>Distribusi Status Siswa</b>",
        showlegend=True,
        legend=dict(orientation="h", y=-0.1),
        paper_bgcolor="white")
    pchart(fig, 320)

with c2:
    # Dropout rate per course — top 10
    course_stat = (dff.groupby(COL_COURSE)[COL_STATUS]
                   .value_counts(normalize=True).unstack(fill_value=0) * 100)
    course_total = dff[COL_COURSE].value_counts().rename("Total")
    if "Dropout" in course_stat.columns:
        course_dropout = (course_stat["Dropout"]
                          .rename("DropoutRate")
                          .reset_index()
                          .merge(course_total.reset_index(), on=COL_COURSE)
                          .query("Total >= 50")      # min 50 siswa agar valid
                          .sort_values("DropoutRate", ascending=True)
                          .tail(10))
        course_dropout["Course_lbl"] = "Course " + course_dropout[COL_COURSE].astype(str)
        fig = px.bar(
            course_dropout, x="DropoutRate", y="Course_lbl",
            orientation="h",
            color="DropoutRate", color_continuous_scale="RdYlGn_r",
            text="DropoutRate",
            custom_data=["Total"],
        )
        fig.update_traces(
            texttemplate="<b>%{text:.1f}%</b>", textposition="outside",
            hovertemplate="<b>%{y}</b><br>Dropout Rate: %{x:.1f}%<br>"
                          "Total Siswa: %{customdata[0]}<extra></extra>")
        fig.update_coloraxes(showscale=False)
        fig.update_xaxes(title_text="Dropout Rate (%)",
                         range=[0, course_dropout["DropoutRate"].max() * 1.3])
        fig.update_yaxes(title_text="")
        fig.update_layout(title="<b>Top 10 Program Studi: Dropout Rate Tertinggi</b>",
                          paper_bgcolor="white")
        pchart(fig, 320)

ibox("Program studi dengan dropout rate tertinggi membutuhkan evaluasi kurikulum dan "
     "dukungan akademik yang lebih intensif.", "warn")


# ══════════════════════════════════════════════════════════════
# VISUALISASI 4 & 5 — PERFORMA AKADEMIK SEMESTER 1 & 2
# ══════════════════════════════════════════════════════════════
sec("Performa Akademik: Nilai & Mata Kuliah Lulus", "📚")
c1, c2 = st.columns(2)

with c1:
    # Nilai rata-rata sem 1 & 2 per status
    fig = go.Figure()
    for status, clr in STATUS_COLORS.items():
        sub = dff[dff[COL_STATUS] == status]
        for col, sem in [(COL_G1_GRADE, "Sem 1"), (COL_G2_GRADE, "Sem 2")]:
            vals = sub[col].replace(0, np.nan).dropna()
            if not vals.empty:
                fig.add_trace(go.Box(
                    y=vals, name=f"{status} — {sem}",
                    marker_color=clr,
                    boxmean=True,
                    opacity=0.85 if "2" in sem else 0.55,
                    hovertemplate=f"<b>{status} {sem}</b><br>Nilai: %{{y:.1f}}<extra></extra>"))
    fig.update_yaxes(title_text="Nilai Rata-rata (0–20)")
    fig.update_layout(
        title="<b>Distribusi Nilai: Sem 1 & 2 per Status</b>",
        showlegend=True,
        legend=dict(orientation="h", y=-0.3, font_size=9),
        paper_bgcolor="white")
    pchart(fig, 360)

with c2:
    # Rata-rata mata kuliah lulus per status
    mk_data = []
    for status in STATUS_ORDER:
        sub = dff[dff[COL_STATUS] == status]
        mk_data.append({
            "Status": status,
            "Sem 1": sub[COL_G1_APPROVED].mean(),
            "Sem 2": sub[COL_G2_APPROVED].mean(),
        })
    mk_df = pd.DataFrame(mk_data)

    fig = go.Figure()
    for sem, clr in [("Sem 1", C_LBLUE), ("Sem 2", C_LGRN)]:
        fig.add_trace(go.Bar(
            name=sem, x=mk_df["Status"], y=mk_df[sem],
            marker_color=clr, text=mk_df[sem].round(1),
            texttemplate="<b>%{text:.1f}</b>", textposition="outside",
            hovertemplate=f"<b>%{{x}}</b> — {sem}<br>Rata-rata: %{{y:.2f}} MK<extra></extra>"))
    fig.update_layout(barmode="group",
                      title="<b>Rata-rata Mata Kuliah Lulus per Status</b>",
                      showlegend=True, paper_bgcolor="white")
    fig.update_yaxes(title_text="Jumlah MK Lulus (rata-rata)")
    fig.update_xaxes(title_text="")
    pchart(fig, 360)

ibox("Siswa dropout rata-rata lulus sangat sedikit mata kuliah di kedua semester. "
     "Ini adalah sinyal peringatan dini paling akurat yang dapat dimonitor setiap semester.", "danger")


# ══════════════════════════════════════════════════════════════
# VISUALISASI 6 — FAKTOR KEUANGAN
# ══════════════════════════════════════════════════════════════
sec("Faktor Keuangan terhadap Status Siswa", "💰")
c1, c2, c3 = st.columns(3)

def stacked_bar(col, labels_map, title, ax):
    ct = (pd.crosstab(dff[col], dff[COL_STATUS], normalize="index") * 100)
    ct = ct.reindex(columns=STATUS_ORDER, fill_value=0)
    ct.index = ct.index.map(labels_map)
    fig = go.Figure()
    for status, clr in STATUS_COLORS.items():
        if status in ct.columns:
            fig.add_trace(go.Bar(
                name=status, x=ct.index, y=ct[status],
                marker_color=clr,
                text=ct[status].round(1),
                texttemplate="%{text:.0f}%", textposition="inside",
                hovertemplate=f"<b>%{{x}}</b><br>{status}: %{{y:.1f}}%<extra></extra>"))
    fig.update_layout(barmode="stack", title=f"<b>{title}</b>",
                      showlegend=False, paper_bgcolor="white")
    fig.update_yaxes(title_text="Proporsi (%)", range=[0, 105])
    fig.update_xaxes(title_text="")
    return fig

with c1:
    pchart(stacked_bar(COL_TUITION, {0: "Belum Lunas", 1: "Lunas"},
                       "Status SPP vs Outcomes", c1), 300)
with c2:
    pchart(stacked_bar(COL_SCHOLAR, {0: "Non-Beasiswa", 1: "Beasiswa"},
                       "Status Beasiswa vs Outcomes", c2), 300)
with c3:
    pchart(stacked_bar(COL_DEBTOR, {0: "Tidak", 1: "Ya"},
                       "Status Hutang vs Outcomes", c3), 300)

ibox("Siswa yang SPP-nya belum lunas dan memiliki hutang menunjukkan dropout rate "
     "yang jauh lebih tinggi. Program bantuan keuangan proaktif dapat mencegah dropout.", "danger")


# ══════════════════════════════════════════════════════════════
# VISUALISASI 7 — DISTRIBUSI USIA & NILAI MASUK
# ══════════════════════════════════════════════════════════════
sec("Profil Demografi: Usia Pendaftaran & Nilai Masuk", "👥")
c1, c2 = st.columns(2)

with c1:
    fig = go.Figure()
    for status, clr in STATUS_COLORS.items():
        sub = dff[dff[COL_STATUS] == status][COL_AGE]
        fig.add_trace(go.Histogram(
            x=sub, name=status, marker_color=clr,
            opacity=0.70, nbinsx=20,
            hovertemplate=f"<b>{status}</b><br>Usia: %{{x}}<br>Jumlah: %{{y}}<extra></extra>"))
        fig.add_vline(x=sub.median(), line_dash="dash", line_color=clr, line_width=1.5,
                      annotation_text=f"  {status} Med={sub.median():.0f}",
                      annotation_font=dict(size=9, color=clr))
    fig.update_layout(barmode="overlay", title="<b>Distribusi Usia saat Mendaftar</b>",
                      showlegend=True, paper_bgcolor="white")
    fig.update_xaxes(title_text="Usia (tahun)")
    fig.update_yaxes(title_text="Jumlah Siswa")
    pchart(fig, 340)

with c2:
    fig = go.Figure()
    for status, clr in STATUS_COLORS.items():
        sub = dff[dff[COL_STATUS] == status][COL_ADMISSION]
        fig.add_trace(go.Violin(
            y=sub, name=status,
            marker_color=clr, fillcolor=clr,
            opacity=0.7, box_visible=True, meanline_visible=True,
            hovertemplate=f"<b>{status}</b><br>Nilai Masuk: %{{y:.1f}}<extra></extra>"))
    fig.update_layout(title="<b>Distribusi Nilai Masuk per Status</b>",
                      showlegend=False, paper_bgcolor="white")
    fig.update_yaxes(title_text="Nilai Masuk (0–200)")
    pchart(fig, 340)


# ══════════════════════════════════════════════════════════════
# VISUALISASI 8 — GENDER & KEHADIRAN
# ══════════════════════════════════════════════════════════════
sec("Analisis Gender & Pola Kehadiran", "🔍")
c1, c2 = st.columns(2)

with c1:
    gen = (pd.crosstab(dff[COL_GENDER], dff[COL_STATUS], normalize="index") * 100)
    gen = gen.reindex(columns=STATUS_ORDER, fill_value=0)
    gen.index = gen.index.map({0: "Perempuan", 1: "Laki-laki"})
    fig = go.Figure()
    for status, clr in STATUS_COLORS.items():
        if status in gen.columns:
            fig.add_trace(go.Bar(
                name=status, x=gen.index, y=gen[status],
                marker_color=clr,
                text=gen[status].round(1),
                texttemplate="%{text:.0f}%", textposition="inside",
                hovertemplate=f"<b>%{{x}}</b><br>{status}: %{{y:.1f}}%<extra></extra>"))
    fig.update_layout(barmode="stack",
                      title="<b>Gender vs Status Siswa (%)</b>",
                      showlegend=True,
                      legend=dict(orientation="h", y=1.1),
                      paper_bgcolor="white")
    fig.update_yaxes(title_text="Proporsi (%)")
    pchart(fig, 320)

with c2:
    if COL_DAYTIME in dff.columns:
        att = (pd.crosstab(dff[COL_DAYTIME], dff[COL_STATUS], normalize="index") * 100)
        att = att.reindex(columns=STATUS_ORDER, fill_value=0)
        att.index = att.index.map({0: "Malam", 1: "Pagi/Siang"})
        fig = go.Figure()
        for status, clr in STATUS_COLORS.items():
            if status in att.columns:
                fig.add_trace(go.Bar(
                    name=status, x=att.index, y=att[status],
                    marker_color=clr,
                    text=att[status].round(1),
                    texttemplate="%{text:.0f}%", textposition="inside",
                    hovertemplate=f"<b>%{{x}}</b><br>{status}: %{{y:.1f}}%<extra></extra>"))
        fig.update_layout(barmode="stack",
                          title="<b>Jadwal Kehadiran vs Status Siswa (%)</b>",
                          showlegend=True,
                          legend=dict(orientation="h", y=1.1),
                          paper_bgcolor="white")
        fig.update_yaxes(title_text="Proporsi (%)")
        pchart(fig, 320)


# ══════════════════════════════════════════════════════════════
# VISUALISASI 9 — FAKTOR RISIKO DROPOUT
# ══════════════════════════════════════════════════════════════
sec("Faktor Risiko Dropout: Dropout Rate per Kondisi", "⚠️")

ibox("Dropout rate aktual untuk setiap kondisi faktor risiko. "
     "Bar merah = kondisi yang mendorong dropout di atas rata-rata (baseline).", "warn")

baseline = dff[COL_STATUS].eq("Dropout").mean() * 100

risk_data = []
risk_defs = [
    (COL_TUITION,  0, "SPP Belum Lunas"),
    (COL_DEBTOR,   1, "Memiliki Hutang"),
    (COL_SCHOLAR,  0, "Tidak Penerima Beasiswa"),
    (COL_DISPLACED,1, "Displaced (Pindahan)"),
    (COL_INTL,     1, "Mahasiswa Internasional"),
]
for col, val, label in risk_defs:
    if col and col in dff.columns:
        sub = dff[dff[col] == val]
        if len(sub) > 10:
            risk_data.append({"Faktor": label,
                               "Rate": round(sub[COL_STATUS].eq("Dropout").mean()*100, 1),
                               "n": len(sub)})
if COL_G1_GRADE in dff.columns:
    sub = dff[dff[COL_G1_GRADE].between(0.01, 9.99)]
    risk_data.append({"Faktor": "Nilai Sem 1 < 10",
                       "Rate": round(sub[COL_STATUS].eq("Dropout").mean()*100, 1),
                       "n": len(sub)})
if COL_G1_APPROVED in dff.columns:
    sub = dff[dff[COL_G1_APPROVED] == 0]
    risk_data.append({"Faktor": "MK Lulus Sem 1 = 0",
                       "Rate": round(sub[COL_STATUS].eq("Dropout").mean()*100, 1),
                       "n": len(sub)})
risk_data.append({"Faktor": "📊 Rata-rata (Baseline)",
                   "Rate": round(baseline, 1), "n": len(dff)})

risk_df = pd.DataFrame(risk_data).sort_values("Rate", ascending=True)
clrs    = ["#C53030" if r > baseline else "#3182CE" for r in risk_df["Rate"]]

fig = go.Figure(go.Bar(
    x=risk_df["Rate"], y=risk_df["Faktor"],
    orientation="h", marker_color=clrs,
    text=[f"{v:.1f}%  (n={n:,})" for v, n in zip(risk_df["Rate"], risk_df["n"])],
    textposition="outside", textfont=dict(size=10),
    hovertemplate="<b>%{y}</b><br>Dropout Rate: %{x:.1f}%<extra></extra>",
))
fig.add_vline(x=baseline, line_dash="dash", line_color="#374151", line_width=1.5,
              annotation_text=f"  Baseline {baseline:.1f}%",
              annotation_font=dict(size=10, color="#374151"))
fig.update_xaxes(title_text="Dropout Rate (%)",
                 range=[0, risk_df["Rate"].max() * 1.3])
fig.update_yaxes(title_text="")
fig.update_layout(title="<b>Dropout Rate per Kondisi Faktor Risiko</b>",
                  showlegend=False, paper_bgcolor="white")
pchart(fig, 420)

ibox("Faktor berwarna <b>merah</b> memiliki dropout rate di atas baseline — "
     "prioritas untuk intervensi segera.", "danger")


# ══════════════════════════════════════════════════════════════
# VISUALISASI 10 — CRITICAL ACADEMIC WARNING
# ══════════════════════════════════════════════════════════════
sec("Critical Academic Warning: Siswa dengan Success Rate < 50%", "🚨")

ibox("Success Rate = proporsi mata kuliah yang lulus dibanding yang diambil. "
     "Siswa di bawah 50% di Sem 1 atau Sem 2 dikategorikan dalam zona merah.", "warn")

dff_warn = dff.copy()
dff_warn["sr1"] = np.where(
    dff_warn[COL_G1_APPROVED].add(1) > 0,
    dff_warn[COL_G1_APPROVED] / dff_warn[COL_G1_APPROVED].add(dff_warn.get(
        "Curricular_units_1st_sem_enrolled", dff_warn[COL_G1_APPROVED]
    ).clip(lower=1)),
    0
)
# Cara sederhana: gunakan approved / (approved + failed_proxy)
# Proxy: jika enrolled tersedia
enrolled_1 = "Curricular_units_1st_sem_enrolled"
enrolled_2 = "Curricular_units_2nd_sem_enrolled"

if enrolled_1 in dff.columns:
    dff_warn["sr1"] = np.where(
        dff_warn[enrolled_1] > 0,
        dff_warn[COL_G1_APPROVED] / dff_warn[enrolled_1],
        0)
else:
    dff_warn["sr1"] = np.where(
        dff_warn[COL_G1_APPROVED] > 0, 1.0, 0.0)

if enrolled_2 in dff.columns:
    dff_warn["sr2"] = np.where(
        dff_warn[enrolled_2] > 0,
        dff_warn[COL_G2_APPROVED] / dff_warn[enrolled_2],
        0)
else:
    dff_warn["sr2"] = np.where(
        dff_warn[COL_G2_APPROVED] > 0, 1.0, 0.0)

THRESHOLD = 0.5
low_sr1 = dff_warn[dff_warn["sr1"] < THRESHOLD]
low_sr2 = dff_warn[dff_warn["sr2"] < THRESHOLD]
low_both = dff_warn[(dff_warn["sr1"] < THRESHOLD) & (dff_warn["sr2"] < THRESHOLD)]

total_w = len(dff_warn)
c1, c2, c3 = st.columns(3)
c1.markdown(kpi("SR Sem 1 < 50%",
                f"{len(low_sr1):,}",
                f"{len(low_sr1)/total_w*100:.1f}% dari total", "red"),
            unsafe_allow_html=True)
c2.markdown(kpi("SR Sem 2 < 50%",
                f"{len(low_sr2):,}",
                f"{len(low_sr2)/total_w*100:.1f}% dari total", "red"),
            unsafe_allow_html=True)
c3.markdown(kpi("SR Rendah di Kedua Sem",
                f"{len(low_both):,}",
                f"{len(low_both)/total_w*100:.1f}% dari total — zona kritis", "red"),
            unsafe_allow_html=True)

st.markdown("")

# Chart: dropout rate di tiap zona SR
c1, c2 = st.columns(2)
with c1:
    bins_sr = [0, 0.25, 0.5, 0.75, 1.01]
    lbl_sr  = ["0–25%", "26–50%", "51–75%", "76–100%"]
    dff_warn["SR1_bin"] = pd.cut(dff_warn["sr1"], bins=bins_sr, labels=lbl_sr, right=True)
    sr1_stat = (dff_warn.groupby("SR1_bin", observed=True)[COL_STATUS]
                .value_counts(normalize=True).unstack(fill_value=0) * 100)
    sr1_stat = sr1_stat.reindex(columns=STATUS_ORDER, fill_value=0).reset_index()

    fig = go.Figure()
    for status, clr in STATUS_COLORS.items():
        if status in sr1_stat.columns:
            fig.add_trace(go.Bar(
                name=status, x=sr1_stat["SR1_bin"].astype(str), y=sr1_stat[status],
                marker_color=clr,
                text=sr1_stat[status].round(0),
                texttemplate="%{text:.0f}%", textposition="inside",
                hovertemplate=f"<b>SR Sem 1: %{{x}}</b><br>{status}: %{{y:.1f}}%<extra></extra>"))
    fig.update_layout(barmode="stack", paper_bgcolor="white",
                      title="<b>Status Siswa per Zona Success Rate Sem 1</b>",
                      showlegend=True, legend=dict(orientation="h", y=1.1))
    fig.update_xaxes(title_text="Success Rate Semester 1")
    fig.update_yaxes(title_text="Proporsi (%)", range=[0, 108])
    pchart(fig, 340)

with c2:
    dff_warn["SR2_bin"] = pd.cut(dff_warn["sr2"], bins=bins_sr, labels=lbl_sr, right=True)
    sr2_stat = (dff_warn.groupby("SR2_bin", observed=True)[COL_STATUS]
                .value_counts(normalize=True).unstack(fill_value=0) * 100)
    sr2_stat = sr2_stat.reindex(columns=STATUS_ORDER, fill_value=0).reset_index()

    fig = go.Figure()
    for status, clr in STATUS_COLORS.items():
        if status in sr2_stat.columns:
            fig.add_trace(go.Bar(
                name=status, x=sr2_stat["SR2_bin"].astype(str), y=sr2_stat[status],
                marker_color=clr,
                text=sr2_stat[status].round(0),
                texttemplate="%{text:.0f}%", textposition="inside",
                hovertemplate=f"<b>SR Sem 2: %{{x}}</b><br>{status}: %{{y:.1f}}%<extra></extra>"))
    fig.update_layout(barmode="stack", paper_bgcolor="white",
                      title="<b>Status Siswa per Zona Success Rate Sem 2</b>",
                      showlegend=True, legend=dict(orientation="h", y=1.1))
    fig.update_xaxes(title_text="Success Rate Semester 2")
    fig.update_yaxes(title_text="Proporsi (%)", range=[0, 108])
    pchart(fig, 340)

ibox(f"Terdapat <b>{len(low_both):,} siswa</b> ({len(low_both)/total_w*100:.1f}%) dengan success rate rendah "
     f"di kedua semester sekaligus — kelompok ini harus menjadi prioritas program bimbingan intensif.", "danger")


# ══════════════════════════════════════════════════════════════
# FEATURE IMPORTANCE
# ══════════════════════════════════════════════════════════════
sec("Feature Importance: Faktor Penentu Dropout", "🔑")

ibox("Feature importance dihitung menggunakan Random Forest Classifier. "
     "Semakin tinggi nilainya, semakin besar pengaruh fitur tersebut dalam memprediksi dropout.", "info")

from sklearn.ensemble import RandomForestClassifier as _RFC

_df_fi = dff.copy()
_df_fi["_target"] = (_df_fi[COL_STATUS] == "Dropout").astype(int)

_feat_cols = [c for c in [
    COL_G1_APPROVED, COL_G2_APPROVED,
    COL_G1_GRADE, COL_G2_GRADE,
    COL_ADMISSION, COL_AGE,
    COL_TUITION, COL_SCHOLAR, COL_DEBTOR,
    COL_DISPLACED, COL_INTL, COL_DAYTIME,
] if c and c in _df_fi.columns]

_feat_label_map = {
    COL_G1_APPROVED: "MK Lulus Sem 1",
    COL_G2_APPROVED: "MK Lulus Sem 2",
    COL_G1_GRADE:    "Nilai Rata-rata Sem 1",
    COL_G2_GRADE:    "Nilai Rata-rata Sem 2",
    COL_ADMISSION:   "Nilai Masuk",
    COL_AGE:         "Usia saat Mendaftar",
    COL_TUITION:     "SPP Lunas",
    COL_SCHOLAR:     "Penerima Beasiswa",
    COL_DEBTOR:      "Memiliki Hutang",
    COL_DISPLACED:   "Displaced",
    COL_INTL:        "Internasional",
    COL_DAYTIME:     "Jadwal Pagi/Siang",
}

_X = _df_fi[_feat_cols].fillna(0)
_y = _df_fi["_target"]
_rf = _RFC(n_estimators=100, max_depth=8, random_state=42, n_jobs=-1)
_rf.fit(_X, _y)

_fi_df = pd.DataFrame({
    "Fitur":      [_feat_label_map.get(c, c) for c in _feat_cols],
    "Importance": _rf.feature_importances_,
}).sort_values("Importance", ascending=True)

_threshold_fi = _fi_df["Importance"].quantile(0.6)
_clrs_fi = ["#C53030" if v >= _threshold_fi else "#3182CE"
            for v in _fi_df["Importance"]]

fig = go.Figure(go.Bar(
    x=_fi_df["Importance"],
    y=_fi_df["Fitur"],
    orientation="h",
    marker_color=_clrs_fi,
    text=[f"{v:.4f}" for v in _fi_df["Importance"]],
    textposition="outside",
    textfont=dict(size=10),
    hovertemplate="<b>%{y}</b><br>Importance: %{x:.4f}<extra></extra>",
))
fig.update_xaxes(title_text="Importance Score",
                 range=[0, _fi_df["Importance"].max() * 1.3])
fig.update_yaxes(title_text="")
fig.update_layout(
    title="<b>Feature Importance — Random Forest (Top Predictors of Dropout)</b>",
    showlegend=False, paper_bgcolor="white")
pchart(fig, 420)

ibox("Fitur berwarna <b>merah</b> adalah prediktor terkuat dropout. "
     "Nilai & kelulusan MK di semester 1 dan 2 secara konsisten menjadi faktor paling menentukan.", "danger")


# ══════════════════════════════════════════════════════════════
# VISUALISASI 11 — TREN DROPOUT vs GRADUATE PER APPROVAL RATE
# ══════════════════════════════════════════════════════════════
sec("Tren Performa: Dropout vs Graduate berdasarkan Progression Akademik", "📉")

ibox("Visualisasi ini mensimulasikan tren kelulusan berdasarkan tingkat kelulusan mata kuliah "
     "(Approval Rate) sebagai proxy perkembangan akademik siswa dari Sem 1 ke Sem 2.", "info")

c1, c2 = st.columns(2)

with c1:
    # Bin approval rate sem 1 → dropout rate per bin
    dff_trend = dff.copy()
    dff_trend["sem1_rate"] = (
        dff_trend[COL_G1_APPROVED] /
        dff_trend[COL_G1_APPROVED].add(1).clip(lower=1)
    )
    # Gunakan approved langsung sebagai bins
    bins   = [0, 1, 2, 3, 4, 5, 6, 10, 30]
    labels_b = ["0","1","2","3","4","5","6–9","10+"]
    dff_trend["MK_Lulus_Sem1_Bin"] = pd.cut(
        dff_trend[COL_G1_APPROVED], bins=bins, labels=labels_b, right=True)

    trend1 = (dff_trend.groupby("MK_Lulus_Sem1_Bin")[COL_STATUS]
              .value_counts(normalize=True).unstack(fill_value=0) * 100)
    trend1 = trend1.reindex(columns=STATUS_ORDER, fill_value=0).reset_index()

    fig = go.Figure()
    for status, clr in STATUS_COLORS.items():
        if status in trend1.columns:
            fig.add_trace(go.Scatter(
                x=trend1["MK_Lulus_Sem1_Bin"].astype(str),
                y=trend1[status],
                mode="lines+markers",
                name=status,
                line=dict(color=clr, width=2.5),
                marker=dict(size=7, color=clr),
                hovertemplate=(f"<b>{status}</b><br>"
                               f"MK Lulus Sem 1: %{{x}}<br>"
                               f"Proporsi: %{{y:.1f}}%<extra></extra>"),
            ))
    fig.update_xaxes(title_text="Jumlah MK Lulus Semester 1")
    fig.update_yaxes(title_text="Proporsi Siswa (%)", range=[0, 105])
    fig.update_layout(
        title="<b>Tren Status vs MK Lulus Semester 1</b>",
        showlegend=True,
        legend=dict(orientation="h", y=1.12),
        paper_bgcolor="white")
    pchart(fig, 360)

with c2:
    # Sem 2
    dff_trend["MK_Lulus_Sem2_Bin"] = pd.cut(
        dff_trend[COL_G2_APPROVED], bins=bins, labels=labels_b, right=True)

    trend2 = (dff_trend.groupby("MK_Lulus_Sem2_Bin")[COL_STATUS]
              .value_counts(normalize=True).unstack(fill_value=0) * 100)
    trend2 = trend2.reindex(columns=STATUS_ORDER, fill_value=0).reset_index()

    fig = go.Figure()
    for status, clr in STATUS_COLORS.items():
        if status in trend2.columns:
            fig.add_trace(go.Scatter(
                x=trend2["MK_Lulus_Sem2_Bin"].astype(str),
                y=trend2[status],
                mode="lines+markers",
                name=status,
                line=dict(color=clr, width=2.5),
                marker=dict(size=7, color=clr),
                hovertemplate=(f"<b>{status}</b><br>"
                               f"MK Lulus Sem 2: %{{x}}<br>"
                               f"Proporsi: %{{y:.1f}}%<extra></extra>"),
            ))
    fig.update_xaxes(title_text="Jumlah MK Lulus Semester 2")
    fig.update_yaxes(title_text="Proporsi Siswa (%)", range=[0, 105])
    fig.update_layout(
        title="<b>Tren Status vs MK Lulus Semester 2</b>",
        showlegend=True,
        legend=dict(orientation="h", y=1.12),
        paper_bgcolor="white")
    pchart(fig, 360)

ibox("Semakin banyak mata kuliah yang lulus, proporsi Graduate meningkat tajam sementara "
     "Dropout menurun drastis. Siswa dengan 0 MK lulus di Sem 1 hampir pasti Dropout.", "danger")


# ══════════════════════════════════════════════════════════════
# VISUALISASI 12 — DEMOGRAFI: USIA & MARITAL STATUS vs STATUS
# ══════════════════════════════════════════════════════════════
sec("Demografi Siswa: Usia & Status Pernikahan vs Outcome", "🧑‍🎓")

COL_MARITAL = next((c for c in dff.columns if "marital" in c.lower()), None)

c1, c2 = st.columns(2)

with c1:
    # Usia dibagi kelompok
    dff_age = dff.copy()
    age_bins   = [0, 18, 21, 25, 30, 40, 100]
    age_labels = ["≤18", "19–21", "22–25", "26–30", "31–40", "41+"]
    dff_age["AgeGroup"] = pd.cut(
        dff_age[COL_AGE], bins=age_bins, labels=age_labels, right=True)

    age_stat = (dff_age.groupby("AgeGroup")[COL_STATUS]
                .value_counts(normalize=True).unstack(fill_value=0) * 100)
    age_stat = age_stat.reindex(columns=STATUS_ORDER, fill_value=0).reset_index()

    fig = go.Figure()
    for status, clr in STATUS_COLORS.items():
        if status in age_stat.columns:
            fig.add_trace(go.Bar(
                name=status,
                x=age_stat["AgeGroup"].astype(str),
                y=age_stat[status],
                marker_color=clr,
                text=age_stat[status].round(0),
                texttemplate="%{text:.0f}%",
                textposition="inside",
                hovertemplate=(f"<b>Usia %{{x}}</b><br>"
                               f"{status}: %{{y:.1f}}%<extra></extra>"),
            ))
    fig.update_layout(
        barmode="stack",
        title="<b>Kelompok Usia vs Status Siswa (%)</b>",
        showlegend=True,
        legend=dict(orientation="h", y=1.1),
        paper_bgcolor="white")
    fig.update_xaxes(title_text="Kelompok Usia saat Mendaftar")
    fig.update_yaxes(title_text="Proporsi (%)", range=[0, 108])
    pchart(fig, 360)

with c2:
    if COL_MARITAL:
        marital_map = {
            1: "Single",
            2: "Menikah",
            3: "Janda/Duda",
            4: "Cerai",
            5: "5 - Facto Union",
            6: "Pisah Legal",
        }
        dff_marital = dff.copy()
        dff_marital["Marital_lbl"] = dff_marital[COL_MARITAL].map(marital_map).fillna("Lainnya")

        # Filter hanya yang cukup banyak
        valid_marital = (dff_marital["Marital_lbl"]
                         .value_counts()[lambda x: x >= 20].index.tolist())
        dff_marital   = dff_marital[dff_marital["Marital_lbl"].isin(valid_marital)]

        mar_stat = (dff_marital.groupby("Marital_lbl")[COL_STATUS]
                    .value_counts(normalize=True).unstack(fill_value=0) * 100)
        mar_stat = mar_stat.reindex(columns=STATUS_ORDER, fill_value=0).reset_index()
        mar_stat = mar_stat.sort_values("Dropout", ascending=False)

        fig = go.Figure()
        for status, clr in STATUS_COLORS.items():
            if status in mar_stat.columns:
                fig.add_trace(go.Bar(
                    name=status,
                    x=mar_stat["Marital_lbl"],
                    y=mar_stat[status],
                    marker_color=clr,
                    text=mar_stat[status].round(0),
                    texttemplate="%{text:.0f}%",
                    textposition="inside",
                    hovertemplate=(f"<b>%{{x}}</b><br>"
                                   f"{status}: %{{y:.1f}}%<extra></extra>"),
                ))
        fig.update_layout(
            barmode="stack",
            title="<b>Status Pernikahan vs Status Siswa (%)</b>",
            showlegend=True,
            legend=dict(orientation="h", y=1.1),
            paper_bgcolor="white")
        fig.update_xaxes(title_text="Status Pernikahan")
        fig.update_yaxes(title_text="Proporsi (%)", range=[0, 108])
        pchart(fig, 360)
    else:
        st.info("Kolom Marital Status tidak ditemukan dalam dataset.")

ibox("Siswa yang mendaftar di usia lebih tua (31+) cenderung memiliki dropout rate lebih tinggi. "
     "Siswa single memiliki proporsi terbesar namun juga tingkat kelulusan yang beragam.", "warn")


# ══════════════════════════════════════════════════════════════
# VISUALISASI — DROPOUT RATE PER NATIONALITY
# ══════════════════════════════════════════════════════════════
sec("Dropout Rate per Asal Negara (Nationality)", "🌍")

COL_NATION = next((c for c in dff.columns if "nacional" in c.lower() or "nation" in c.lower()), None)
NATION_MAP = {
    1:"Portugal", 2:"Jerman", 6:"Spanyol", 11:"Italia", 13:"Belanda",
    14:"Inggris", 17:"Lithuania", 21:"Angola", 22:"Tanjung Hijau",
    24:"Guinea", 25:"Mozambik", 26:"São Tomé", 32:"Turki", 41:"Brasil",
    62:"Rumania", 100:"Moldova", 101:"Meksiko", 103:"Ukraina",
    105:"Rusia", 108:"Kuba", 109:"Kolombia",
}

if COL_NATION:
    dff_nat = dff.copy()
    dff_nat["Nationality_lbl"] = dff_nat[COL_NATION].map(NATION_MAP).fillna("Lainnya")

    nat_cnt  = dff_nat["Nationality_lbl"].value_counts()
    valid    = nat_cnt[nat_cnt >= 10].index
    nat_stat = (dff_nat[dff_nat["Nationality_lbl"].isin(valid)]
                .groupby("Nationality_lbl")[COL_STATUS]
                .value_counts(normalize=True).unstack(fill_value=0) * 100)
    nat_stat = nat_stat.reindex(columns=STATUS_ORDER, fill_value=0)

    if "Dropout" in nat_stat.columns:
        _base = dff[COL_STATUS].eq("Dropout").mean() * 100
        nat_plot = (nat_stat[["Dropout"]]
                    .rename(columns={"Dropout": "Rate"})
                    .reset_index()
                    .sort_values("Rate", ascending=True))
        nat_plot["n"] = nat_plot["Nationality_lbl"].map(nat_cnt).fillna(0).astype(int)
        clrs_nat = ["#C53030" if r > _base else "#3182CE" for r in nat_plot["Rate"]]

        fig = go.Figure(go.Bar(
            x=nat_plot["Rate"], y=nat_plot["Nationality_lbl"],
            orientation="h", marker_color=clrs_nat,
            text=[f"{v:.1f}%  (n={n:,})" for v, n in zip(nat_plot["Rate"], nat_plot["n"])],
            textposition="outside", textfont=dict(size=10),
            hovertemplate="<b>%{y}</b><br>Dropout Rate: %{x:.1f}%<extra></extra>",
        ))
        fig.add_vline(x=_base, line_dash="dash", line_color="#374151", line_width=1.5,
                      annotation_text=f"  Baseline {_base:.1f}%",
                      annotation_font=dict(size=10, color="#374151"))
        fig.update_xaxes(title_text="Dropout Rate (%)",
                         range=[0, nat_plot["Rate"].max() * 1.3])
        fig.update_yaxes(title_text="")
        fig.update_layout(
            title="<b>Dropout Rate per Negara Asal Siswa</b>",
            showlegend=False, paper_bgcolor="white")
        pchart(fig, max(360, len(nat_plot) * 32))

    ibox("Bar <b>merah</b> = dropout rate di atas baseline. Siswa internasional dari beberapa "
         "negara tertentu menunjukkan risiko dropout lebih tinggi dan mungkin membutuhkan "
         "dukungan adaptasi tambahan.", "info")
else:
    st.info("Kolom Nationality tidak ditemukan dalam dataset.")


# Footer
st.markdown("---")
st.caption("📊 Jaya Jaya Institut — Student Performance Dashboard · Data Science Project · sutriadik24")