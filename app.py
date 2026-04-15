"""
app.py — Prototype Prediksi Dropout Siswa
Jaya Jaya Institut | Binary: Dropout vs Graduate
streamlit run app.py
"""

import os, joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Prediksi Dropout — Jaya Jaya Institut",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
html, body, [class*="css"], .stApp {
    background-color: #F7FAFC !important;
    color: #1A202C !important;
    font-family: 'Segoe UI', sans-serif;
}
#MainMenu, footer, header { visibility: hidden; }
.step-badge {
    display:inline-flex; align-items:center; justify-content:center;
    width:24px; height:24px; border-radius:50%;
    background:#3182CE; color:white;
    font-size:.75rem; font-weight:700; margin-right:8px;
}
.card-title { font-size:1rem; font-weight:700; color:#1A365D;
              margin-bottom:14px; }
.hint { font-size:.75rem; color:#A0AEC0; margin-top:-8px; margin-bottom:8px; }
.kpi { background:white; border-radius:10px; padding:14px 16px;
       border-left:4px solid #3182CE;
       box-shadow:0 1px 3px rgba(0,0,0,.05); }
.kpi.red   { border-left-color:#C53030; }
.kpi.green { border-left-color:#276749; }
.kpi.amber { border-left-color:#D69E2E; }
.kpi-lbl { font-size:.7rem; font-weight:700; color:#718096; text-transform:uppercase; }
.kpi-val { font-size:1.5rem; font-weight:800; color:#1A202C; }
.kpi-sub { font-size:.72rem; color:#A0AEC0; }
.ibox { border-radius:8px; padding:11px 15px; margin:8px 0; font-size:.86rem; }
.ibox.info   { background:#EBF8FF; border:1px solid #90CDF4; color:#1A365D; }
.ibox.danger { background:#FFF5F5; border:1px solid #FEB2B2; color:#63171B; }
.ibox.warn   { background:#FFFBEB; border:1px solid #F6E05E; color:#744210; }
.ibox.green  { background:#F0FFF4; border:1px solid #9AE6B4; color:#1C4532; }
.divider { height:2px;
           background:linear-gradient(90deg,#3182CE,#90CDF4,transparent);
           border:none; margin:16px 0 20px 0; }
.result-box { border-radius:12px; padding:20px; text-align:center; margin:10px 0; }
.result-box.dropout  { background:#FFF5F5; border:2px solid #FC8181; }
.result-box.graduate { background:#F0FFF4; border:2px solid #68D391; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ────────────────────────────────────────────────────
def kpi(label, val, sub="", cls=""):
    return (f'<div class="kpi {cls}"><div class="kpi-lbl">{label}</div>'
            f'<div class="kpi-val">{val}</div><div class="kpi-sub">{sub}</div></div>')

def ibox(text, kind="info"):
    icons = {"info":"ℹ️","danger":"🔴","warn":"⚠️","green":"✅"}
    st.markdown(f'<div class="ibox {kind}">{icons[kind]} {text}</div>',
                unsafe_allow_html=True)

def hint(text):
    st.markdown(f'<div class="hint">{text}</div>', unsafe_allow_html=True)


# ── Load model ──────────────────────────────────────────────────
@st.cache_resource
def load_model():
    md    = "model"
    files = ["model.joblib","scaler.joblib",
             "label_encoder.joblib","feature_names.joblib"]
    if not all(os.path.exists(f"{md}/{f}") for f in files):
        return None, None, None, None
    return (
        joblib.load(f"{md}/model.joblib"),
        joblib.load(f"{md}/scaler.joblib"),
        joblib.load(f"{md}/label_encoder.joblib"),
        joblib.load(f"{md}/feature_names.joblib"),
    )

model, scaler, le, feature_names = load_model()


# ── Header ──────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center;padding:24px 0 8px'>
    <div style='font-size:2.4rem'>🎓</div>
    <div style='font-size:1.5rem;font-weight:800;color:#1A365D;'>
        Prediksi Risiko Dropout Siswa
    </div>
    <div style='font-size:.88rem;color:#718096;margin-top:4px;'>
        Jaya Jaya Institut — Sistem Deteksi Dini
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

if model is None:
    st.error("⚠️ Model belum tersedia. Jalankan **notebook.ipynb** terlebih dahulu.")
    st.stop()

# Tampilkan kelas yang diprediksi
classes = list(le.classes_)
st.markdown(f"""
<div class="ibox info">
    ℹ️ Model: <b>Random Forest</b> | Fitur: <b>{len(feature_names)}</b> |
    Prediksi: <b>{' vs '.join(classes)}</b>
</div>
""", unsafe_allow_html=True)
st.markdown("")


# ══════════════════════════════════════════════════════════════
# FORM INPUT
# ══════════════════════════════════════════════════════════════
with st.form("prediction_form"):

    # STEP 1
    st.markdown(
        '<div class="card-title">'
        '<span class="step-badge">1</span>'
        'Performa Akademik Semester 1</div>',
        unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        sem1_enrolled = st.number_input(
            "Berapa mata kuliah yang diambil?",
            min_value=0, max_value=30, value=6,
            help="Jumlah MK yang didaftarkan di Semester 1 (0–30)")
        hint("Contoh: 6 mata kuliah")
        sem1_grade = st.number_input(
            "Nilai rata-rata Semester 1",
            min_value=0.0, max_value=20.0, value=12.0, step=0.5,
            help="Rata-rata nilai akhir Semester 1, skala 0–20")
        hint("Skala 0–20. Contoh: 12.5")
    with c2:
        sem1_approved = st.number_input(
            "Berapa mata kuliah yang lulus?",
            min_value=0, max_value=30, value=5,
            help="Jumlah MK yang berhasil lulus di Semester 1")
        hint("Harus ≤ jumlah MK yang diambil")
        sem1_evaluations = st.number_input(
            "Jumlah evaluasi/ujian Semester 1",
            min_value=0, max_value=50, value=6,
            help="Total ujian/evaluasi yang diikuti di Semester 1")
        hint("Contoh: 6 evaluasi")

    st.markdown("---")

    # STEP 2
    st.markdown(
        '<div class="card-title">'
        '<span class="step-badge">2</span>'
        'Performa Akademik Semester 2</div>',
        unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        sem2_enrolled = st.number_input(
            "Berapa mata kuliah yang diambil?",
            min_value=0, max_value=30, value=6,
            help="Jumlah MK yang didaftarkan di Semester 2",
            key="s2e")
        hint("Contoh: 6 mata kuliah")
        sem2_grade = st.number_input(
            "Nilai rata-rata Semester 2",
            min_value=0.0, max_value=20.0, value=11.0, step=0.5,
            help="Rata-rata nilai akhir Semester 2, skala 0–20",
            key="s2g")
        hint("Skala 0–20. Contoh: 11.0")
    with c2:
        sem2_approved = st.number_input(
            "Berapa mata kuliah yang lulus?",
            min_value=0, max_value=30, value=4,
            help="Jumlah MK yang berhasil lulus di Semester 2",
            key="s2a")
        hint("Harus ≤ jumlah MK yang diambil")
        sem2_evaluations = st.number_input(
            "Jumlah evaluasi/ujian Semester 2",
            min_value=0, max_value=50, value=6,
            help="Total ujian/evaluasi yang diikuti di Semester 2",
            key="s2ev")
        hint("Contoh: 6 evaluasi")

    st.markdown("---")

    # STEP 3
    st.markdown(
        '<div class="card-title">'
        '<span class="step-badge" style="background:#D69E2E">3</span>'
        'Data Pribadi & Keuangan</div>',
        unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        age = st.number_input(
            "Usia saat mendaftar",
            min_value=16, max_value=70, value=20,
            help="Usia siswa saat pertama mendaftar")
        hint("Tahun. Contoh: 20")
    with c2:
        admission_grade = st.number_input(
            "Nilai seleksi masuk",
            min_value=0.0, max_value=200.0, value=127.0, step=1.0,
            help="Nilai seleksi masuk, skala 0–200")
        hint("Skala 0–200. Contoh: 127")
    with c3:
        prev_qual_grade = st.number_input(
            "Nilai ijazah sebelumnya",
            min_value=0.0, max_value=200.0, value=120.0, step=1.0,
            help="Nilai dari kualifikasi pendidikan sebelumnya, skala 0–200")
        hint("Skala 0–200. Contoh: 120")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        tuition = st.selectbox(
            "SPP sudah lunas?", [1, 0],
            format_func=lambda x: "Ya, lunas" if x==1 else "Belum lunas",
            help="Status pembayaran SPP semester ini")
    with c2:
        scholarship = st.selectbox(
            "Penerima beasiswa?", [0, 1],
            format_func=lambda x: "Ya" if x==1 else "Tidak",
            help="Apakah siswa menerima beasiswa?")
    with c3:
        debtor = st.selectbox(
            "Memiliki hutang?", [0, 1],
            format_func=lambda x: "Ya" if x==1 else "Tidak",
            help="Apakah ada kewajiban pembayaran yang tertunggak?")
    with c4:
        course = st.number_input(
            "Kode program studi",
            min_value=1, max_value=9999, value=171,
            help="Kode numerik program studi. Contoh: 171 = Animation & Multimedia")
        hint("Contoh: 171, 9003")

    st.markdown("")
    submitted = st.form_submit_button(
        "Prediksi",
        type="primary",
        use_container_width=True,
    )


# ══════════════════════════════════════════════════════════════
# VALIDASI & PREDIKSI
# ══════════════════════════════════════════════════════════════
if submitted:
    errors = []
    if sem1_approved > sem1_enrolled:
        errors.append("MK Lulus Sem 1 tidak boleh melebihi MK Diambil Sem 1.")
    if sem2_approved > sem2_enrolled:
        errors.append("MK Lulus Sem 2 tidak boleh melebihi MK Diambil Sem 2.")
    if errors:
        for e in errors:
            st.error(f"❌ {e}")
        st.stop()

    # Feature Engineering (identik dengan notebook)
    sem1_ar = sem1_approved / max(sem1_enrolled, 1)
    sem2_ar = sem2_approved / max(sem2_enrolled, 1)
    total_ap = sem1_approved + sem2_approved
    avg_gr   = (sem1_grade + sem2_grade) / 2
    gr_diff  = sem2_grade - sem1_grade
    total_ev = sem1_evaluations + sem2_evaluations

    feat_map = {
        "Sem2_approval_rate":                sem2_ar,
        "Total_approved":                    total_ap,
        "Sem1_approval_rate":                sem1_ar,
        "Curricular_units_2nd_sem_approved": sem2_approved,
        "Curricular_units_2nd_sem_grade":    sem2_grade,
        "Avg_grade":                         avg_gr,
        "Curricular_units_1st_sem_grade":    sem1_grade,
        "Curricular_units_1st_sem_approved": sem1_approved,
        "Admission_grade":                   admission_grade,
        "Previous_qualification_grade":      prev_qual_grade,
        "Tuition_fees_up_to_date":           tuition,
        "Age_at_enrollment":                 age,
        "Grade_diff":                        gr_diff,
        "Course":                            course,
        "Total_evaluations":                 total_ev,
    }

    X_in   = pd.DataFrame([[feat_map.get(f, 0) for f in feature_names]],
                           columns=feature_names)
    X_sc   = scaler.transform(X_in)
    pred   = model.predict(X_sc)[0]
    proba  = model.predict_proba(X_sc)[0]
    result = le.inverse_transform([pred])[0]

    prob_dict  = dict(zip(classes, proba))
    dropout_p  = prob_dict.get("Dropout",  0)
    graduate_p = prob_dict.get("Graduate", 0)

    # ── Hasil ──────────────────────────────────────────────────
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown("### Hasil Prediksi")

    is_dropout = result == "Dropout"
    box_cls    = "dropout"  if is_dropout else "graduate"
    result_lbl = "🔴 Berisiko Dropout" if is_dropout else "🟢 Diprediksi Lulus (Graduate)"
    result_clr = "#C53030"  if is_dropout else "#276749"

    st.markdown(
        f'<div class="result-box {box_cls}">'
        f'<div style="font-size:1.3rem;font-weight:800;color:{result_clr};">{result_lbl}</div>'
        f'<div style="font-size:.88rem;color:#718096;margin-top:4px;">'
        f'Probabilitas Dropout: <b>{dropout_p:.1%}</b> | Graduate: <b>{graduate_p:.1%}</b>'
        f'</div></div>',
        unsafe_allow_html=True)

    # KPI
    risk_lbl = ("Tinggi"   if dropout_p >= 0.6
                else "Sedang" if dropout_p >= 0.35
                else "Rendah")
    risk_cls = "red" if dropout_p >= 0.6 else "amber" if dropout_p >= 0.35 else "green"

    st.markdown("")
    c1, c2, c3 = st.columns(3)
    c1.markdown(kpi("Prediksi Status", result, "",
                    "red" if is_dropout else "green"), unsafe_allow_html=True)
    c2.markdown(kpi("Probabilitas Dropout", f"{dropout_p:.1%}",
                    "", risk_cls), unsafe_allow_html=True)
    c3.markdown(kpi("Tingkat Risiko", risk_lbl, "", risk_cls),
                unsafe_allow_html=True)

    # Gauge
    gc  = "#C53030" if dropout_p >= 0.6 else "#D69E2E" if dropout_p >= 0.35 else "#276749"
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=dropout_p * 100,
        number={"suffix":"%","font":{"size":32,"color":gc}},
        title={"text":"Probabilitas Dropout","font":{"size":13,"color":"#1A365D"}},
        gauge={
            "axis":    {"range":[0,100]},
            "bar":     {"color":gc,"thickness":0.25},
            "bgcolor": "white",
            "steps":   [
                {"range":[0,35],  "color":"#C6F6D5"},
                {"range":[35,60], "color":"#FEFCBF"},
                {"range":[60,100],"color":"#FED7D7"},
            ],
            "threshold":{"line":{"color":"#374151","width":3},
                         "thickness":0.75,"value":50},
        }
    ))
    fig.update_layout(height=260, paper_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True,
                    config={"displayModeBar":False})

    # Probabilitas 2 kelas
    st.markdown("**Probabilitas per Kelas:**")
    c1, c2 = st.columns(2)
    c1.markdown(kpi("Dropout",  f"{dropout_p:.1%}",  "", "red"),   unsafe_allow_html=True)
    c2.markdown(kpi("Graduate", f"{graduate_p:.1%}", "", "green"),  unsafe_allow_html=True)

    # Rekomendasi
    st.markdown("")
    if is_dropout:
        ibox("<b>Siswa ini diprediksi berisiko DROPOUT.</b> "
             "Rekomendasikan bimbingan akademik intensif, cek status keuangan, dan konseling.",
             "danger")
    else:
        ibox("<b>Siswa ini diprediksi akan LULUS (Graduate).</b> "
             "Performa akademik dan finansial mendukung kelulusan.", "green")

    # Faktor risiko
    risks = []
    if sem1_ar < 0.5:
        risks.append("Kurang dari 50% MK Semester 1 lulus")
    if sem2_ar < 0.5:
        risks.append("Kurang dari 50% MK Semester 2 lulus")
    if avg_gr < 10:
        risks.append("Nilai rata-rata kedua semester di bawah 10")
    if gr_diff < -3:
        risks.append("Nilai turun signifikan dari Sem 1 ke Sem 2")
    if tuition == 0:
        risks.append("SPP belum lunas")
    if debtor == 1:
        risks.append("Memiliki hutang kepada institusi")
    if age > 30:
        risks.append("Mendaftar di usia lebih dari 30 tahun")

    if risks:
        st.markdown("**Faktor risiko yang teridentifikasi:**")
        for r in risks:
            st.markdown(
                f'<div style="background:#FFF5F5;border-radius:7px;'
                f'padding:8px 14px;margin:4px 0;font-size:.86rem;'
                f'color:#63171B;border-left:3px solid #FC8181;">⚠️ {r}</div>',
                unsafe_allow_html=True)