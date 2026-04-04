"""
app.py — Prototype Prediksi Dropout Siswa
Jaya Jaya Institut | Streamlit
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

/* Card section */
.card {
    background: white;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 16px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.07);
    border-left: 4px solid #3182CE;
}
.card.green { border-left-color: #276749; }
.card.amber { border-left-color: #D69E2E; }

.card-title {
    font-size: 1rem; font-weight: 700;
    color: #1A365D; margin-bottom: 14px;
    display: flex; align-items: center; gap: 8px;
}

/* Label input lebih besar dan jelas */
label, .stNumberInput label, .stSelectbox label, .stSlider label {
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    color: #2D3748 !important;
}

/* Hint text di bawah input */
.hint {
    font-size: 0.75rem;
    color: #A0AEC0;
    margin-top: -8px;
    margin-bottom: 8px;
}

/* Hasil prediksi */
.result-card {
    border-radius: 12px; padding: 20px 24px;
    margin: 8px 0; text-align: center;
}
.result-card.dropout  { background: #FFF5F5; border: 2px solid #FC8181; }
.result-card.graduate { background: #F0FFF4; border: 2px solid #68D391; }
.result-card.enrolled { background: #FFFBEB; border: 2px solid #F6AD55; }
.result-label { font-size: 1.3rem; font-weight: 800; margin-bottom: 4px; }
.result-sub   { font-size: 0.85rem; color: #718096; }

.kpi {
    background: white; border-radius: 10px;
    padding: 14px 16px; border-left: 4px solid #3182CE;
    box-shadow: 0 1px 3px rgba(0,0,0,.05);
}
.kpi.red   { border-left-color: #C53030; }
.kpi.green { border-left-color: #276749; }
.kpi.amber { border-left-color: #D69E2E; }
.kpi-lbl { font-size:.7rem; font-weight:700; color:#718096; text-transform:uppercase; }
.kpi-val { font-size:1.5rem; font-weight:800; color:#1A202C; }
.kpi-sub { font-size:.72rem; color:#A0AEC0; }

.ibox { border-radius:8px; padding:11px 15px; margin:8px 0; font-size:.86rem; }
.ibox.info   { background:#EBF8FF; border:1px solid #90CDF4; color:#1A365D; }
.ibox.danger { background:#FFF5F5; border:1px solid #FEB2B2; color:#63171B; }
.ibox.warn   { background:#FFFBEB; border:1px solid #F6E05E; color:#744210; }
.ibox.green  { background:#F0FFF4; border:1px solid #9AE6B4; color:#1C4532; }

.divider { height:2px; background:linear-gradient(90deg,#3182CE,#90CDF4,transparent);
           border:none; margin:16px 0 20px 0; }

/* Step indicator */
.step-badge {
    display: inline-flex; align-items: center; justify-content: center;
    width: 24px; height: 24px; border-radius: 50%;
    background: #3182CE; color: white;
    font-size: 0.75rem; font-weight: 700;
    margin-right: 8px; flex-shrink: 0;
}
</style>
""", unsafe_allow_html=True)


# ── Load model ─────────────────────────────────────────────────
@st.cache_resource
def load_model():
    md = "model"
    files = ["model.joblib","scaler.joblib","label_encoder.joblib","feature_names.joblib"]
    if not all(os.path.exists(f"{md}/{f}") for f in files):
        return None, None, None, None
    return (
        joblib.load(f"{md}/model.joblib"),
        joblib.load(f"{md}/scaler.joblib"),
        joblib.load(f"{md}/label_encoder.joblib"),
        joblib.load(f"{md}/feature_names.joblib"),
    )

model, scaler, le, feature_names = load_model()

def kpi(label, val, sub="", cls=""):
    return (f'<div class="kpi {cls}"><div class="kpi-lbl">{label}</div>'
            f'<div class="kpi-val">{val}</div><div class="kpi-sub">{sub}</div></div>')

def ibox(text, kind="info"):
    icons = {"info":"ℹ️","danger":"🔴","warn":"⚠️","green":"✅"}
    st.markdown(f'<div class="ibox {kind}">{icons[kind]} {text}</div>', unsafe_allow_html=True)

def hint(text):
    st.markdown(f'<div class="hint">{text}</div>', unsafe_allow_html=True)


# ── Header ─────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding: 24px 0 8px'>
    <div style='font-size:2.4rem'>🎓</div>
    <div style='font-size:1.5rem; font-weight:800; color:#1A365D;'>
        Prediksi Risiko Dropout Siswa
    </div>
    <div style='font-size:0.88rem; color:#718096; margin-top:4px;'>
        Jaya Jaya Institut — Sistem Deteksi Dini
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

if model is None:
    st.error("⚠️ Model belum tersedia. Jalankan **notebook.ipynb** terlebih dahulu.")
    st.stop()

st.markdown(f"""
<div class="ibox info">
    ℹ️ Isi semua data di bawah, lalu klik tombol <b>Prediksi</b> untuk mengetahui
    apakah siswa berisiko dropout. Model: <b>Random Forest</b> ({len(feature_names)} fitur).
</div>
""", unsafe_allow_html=True)
st.markdown("")


# ══════════════════════════════════════════════════════════════
# FORM
# ══════════════════════════════════════════════════════════════
with st.form("prediction_form"):

    # ── STEP 1: Semester 1 ──────────────────────────────────
    st.markdown("""
    <div class="card">
        <div class="card-title">
            <span class="step-badge">1</span>
            Performa Akademik Semester 1
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        sem1_enrolled = st.number_input(
            "Berapa mata kuliah yang diambil?",
            min_value=0, max_value=30, value=6,
            help="Jumlah total MK yang didaftarkan di Semester 1")
        hint("Contoh: 6 mata kuliah")

        sem1_grade = st.number_input(
            "Nilai rata-rata Semester 1",
            min_value=0.0, max_value=20.0, value=12.0, step=0.5,
            help="Rata-rata nilai akhir semua MK di Semester 1 (skala 0–20)")
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
            help="Total jumlah ujian atau evaluasi yang diikuti di Semester 1")
        hint("Contoh: 6 evaluasi")

    # ── STEP 2: Semester 2 ──────────────────────────────────
    st.markdown("""
    <div class="card">
        <div class="card-title">
            <span class="step-badge">2</span>
            Performa Akademik Semester 2
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        sem2_enrolled = st.number_input(
            "Berapa mata kuliah yang diambil?",
            min_value=0, max_value=30, value=6,
            help="Jumlah total MK yang didaftarkan di Semester 2",
            key="sem2_enrolled")
        hint("Contoh: 6 mata kuliah")

        sem2_grade = st.number_input(
            "Nilai rata-rata Semester 2",
            min_value=0.0, max_value=20.0, value=11.0, step=0.5,
            help="Rata-rata nilai akhir semua MK di Semester 2 (skala 0–20)",
            key="sem2_grade")
        hint("Skala 0–20. Contoh: 11.0")

    with c2:
        sem2_approved = st.number_input(
            "Berapa mata kuliah yang lulus?",
            min_value=0, max_value=30, value=4,
            help="Jumlah MK yang berhasil lulus di Semester 2",
            key="sem2_approved")
        hint("Harus ≤ jumlah MK yang diambil")

        sem2_evaluations = st.number_input(
            "Jumlah evaluasi/ujian Semester 2",
            min_value=0, max_value=50, value=6,
            help="Total jumlah ujian atau evaluasi yang diikuti di Semester 2",
            key="sem2_eval")
        hint("Contoh: 6 evaluasi")

    # ── STEP 3: Data Lainnya ────────────────────────────────
    st.markdown("""
    <div class="card amber">
        <div class="card-title">
            <span class="step-badge" style="background:#D69E2E">3</span>
            Data Pribadi & Keuangan
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        age = st.number_input(
            "Usia saat mendaftar",
            min_value=16, max_value=70, value=20,
            help="Usia siswa saat pertama mendaftar ke institusi")
        hint("Tahun. Contoh: 20")

    with c2:
        admission_grade = st.number_input(
            "Nilai seleksi masuk",
            min_value=0.0, max_value=200.0, value=127.0, step=1.0,
            help="Nilai yang diperoleh saat seleksi masuk perguruan tinggi (skala 0–200)")
        hint("Skala 0–200. Contoh: 127")

    with c3:
        prev_qual_grade = st.number_input(
            "Nilai ijazah sebelumnya",
            min_value=0.0, max_value=200.0, value=120.0, step=1.0,
            help="Nilai dari kualifikasi pendidikan sebelumnya (skala 0–200)")
        hint("Skala 0–200. Contoh: 120")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        tuition = st.selectbox(
            "Apakah SPP sudah lunas?",
            options=[1, 0],
            format_func=lambda x: "Ya, sudah lunas" if x == 1 else "Belum lunas",
            help="Status pembayaran SPP/uang kuliah semester ini")
    with c2:
        scholarship = st.selectbox(
            "Penerima beasiswa?",
            options=[0, 1],
            format_func=lambda x: "Ya, penerima beasiswa" if x == 1 else "Tidak",
            help="Apakah siswa saat ini menerima beasiswa?")
    with c3:
        debtor = st.selectbox(
            "Apakah memiliki hutang?",
            options=[0, 1],
            format_func=lambda x: "Ya, ada hutang" if x == 1 else "Tidak ada hutang",
            help="Apakah siswa memiliki kewajiban pembayaran yang tertunggak?")
    with c4:
        course = st.number_input(
            "Kode program studi",
            min_value=1, max_value=9999, value=171,
            help="Kode numerik program studi siswa. Contoh: 171 = Animation & Multimedia")
        hint("Contoh: 171, 9003, 9147")

    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button(
        "Prediksi",
        type="primary",
        use_container_width=True,
    )


# ══════════════════════════════════════════════════════════════
# VALIDASI & HASIL
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

    # Feature Engineering
    sem1_approval_rate = sem1_approved / max(sem1_enrolled, 1)
    sem2_approval_rate = sem2_approved / max(sem2_enrolled, 1)
    total_approved     = sem1_approved + sem2_approved
    avg_grade          = (sem1_grade + sem2_grade) / 2
    grade_diff         = sem2_grade - sem1_grade
    total_evaluations  = sem1_evaluations + sem2_evaluations

    feature_map = {
        "Sem2_approval_rate":                 sem2_approval_rate,
        "Total_approved":                     total_approved,
        "Sem1_approval_rate":                 sem1_approval_rate,
        "Curricular_units_2nd_sem_approved":  sem2_approved,
        "Curricular_units_2nd_sem_grade":     sem2_grade,
        "Avg_grade":                          avg_grade,
        "Curricular_units_1st_sem_grade":     sem1_grade,
        "Curricular_units_1st_sem_approved":  sem1_approved,
        "Admission_grade":                    admission_grade,
        "Previous_qualification_grade":       prev_qual_grade,
        "Tuition_fees_up_to_date":            tuition,
        "Age_at_enrollment":                  age,
        "Grade_diff":                         grade_diff,
        "Course":                             course,
        "Total_evaluations":                  total_evaluations,
    }

    X_in  = pd.DataFrame([[feature_map.get(f, 0) for f in feature_names]],
                          columns=feature_names)
    X_sc  = scaler.transform(X_in)
    pred  = model.predict(X_sc)[0]
    proba = model.predict_proba(X_sc)[0]
    result = le.inverse_transform([pred])[0]

    classes   = list(le.classes_)
    prob_dict = dict(zip(classes, proba))
    dropout_p = prob_dict.get("Dropout", 0)

    # ── Hasil Utama ────────────────────────────────────────────
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown("### Hasil Prediksi")

    status_config = {
        "Dropout":  ("dropout",  "🔴 Berisiko Dropout",    "#C53030", "red"),
        "Graduate": ("graduate", "🟢 Diprediksi Lulus",     "#276749", "green"),
        "Enrolled": ("enrolled", "🟡 Masih Aktif Kuliah",  "#D69E2E", "amber"),
    }
    cls, label_txt, color, kpi_cls = status_config.get(
        result, ("enrolled", result, "#2B6CB0", ""))

    st.markdown(f"""
    <div class="result-card {cls}">
        <div class="result-label" style="color:{color}">{label_txt}</div>
        <div class="result-sub">Probabilitas Dropout: <b>{dropout_p:.1%}</b></div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI breakdown ──────────────────────────────────────────
    risk_lbl = ("Tinggi"   if dropout_p >= 0.6
                else "Sedang" if dropout_p >= 0.35
                else "Rendah")
    risk_cls = "red" if dropout_p >= 0.6 else "amber" if dropout_p >= 0.35 else "green"

    st.markdown("")
    c1, c2, c3 = st.columns(3)
    c1.markdown(kpi("Prediksi Status", result, "", kpi_cls), unsafe_allow_html=True)
    c2.markdown(kpi("Probabilitas Dropout", f"{dropout_p:.1%}", "", risk_cls),
                unsafe_allow_html=True)
    c3.markdown(kpi("Tingkat Risiko", risk_lbl, "", risk_cls), unsafe_allow_html=True)

    # ── Gauge ──────────────────────────────────────────────────
    gc  = "#C53030" if dropout_p >= 0.6 else "#D69E2E" if dropout_p >= 0.35 else "#276749"
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=dropout_p * 100,
        number={"suffix": "%", "font": {"size": 32, "color": gc}},
        title={"text": "Probabilitas Dropout", "font": {"size": 13, "color": "#1A365D"}},
        gauge={
            "axis":    {"range": [0, 100]},
            "bar":     {"color": gc, "thickness": 0.25},
            "bgcolor": "white",
            "steps": [
                {"range": [0,  35], "color": "#C6F6D5"},
                {"range": [35, 60], "color": "#FEFCBF"},
                {"range": [60, 100],"color": "#FED7D7"},
            ],
            "threshold": {"line": {"color": "#374151", "width": 3},
                          "thickness": 0.75, "value": 50}
        }
    ))
    fig.update_layout(height=260, paper_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # ── Probabilitas semua kelas ───────────────────────────────
    st.markdown("**Probabilitas per Status:**")
    clr_map = {"Dropout":"red","Enrolled":"amber","Graduate":"green"}
    c1, c2, c3 = st.columns(3)
    for cls_name, col in zip(classes, [c1, c2, c3]):
        p = prob_dict.get(cls_name, 0)
        col.markdown(kpi(cls_name, f"{p:.1%}", "", clr_map.get(cls_name, "")),
                     unsafe_allow_html=True)

    # ── Rekomendasi ────────────────────────────────────────────
    st.markdown("")
    if result == "Dropout":
        ibox("<b>Siswa ini diprediksi berisiko DROPOUT.</b> Segera lakukan intervensi: "
             "bimbingan akademik intensif, cek status keuangan, dan konseling.", "danger")
    elif result == "Graduate":
        ibox("<b>Siswa ini diprediksi akan LULUS.</b> "
             "Performa akademik dan finansial mendukung kelulusan.", "green")
    else:
        ibox("<b>Siswa ini masih AKTIF KULIAH.</b> "
             "Pantau perkembangan nilai di semester berikutnya.", "warn")

    # ── Faktor risiko teridentifikasi ──────────────────────────
    risks = []
    if sem1_approval_rate < 0.5:
        risks.append("Kurang dari 50% mata kuliah Semester 1 lulus")
    if sem2_approval_rate < 0.5:
        risks.append("Kurang dari 50% mata kuliah Semester 2 lulus")
    if avg_grade < 10:
        risks.append("Nilai rata-rata kedua semester di bawah 10")
    if grade_diff < -3:
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
                f'<div style="background:#FFF5F5;border-radius:7px;padding:8px 14px;'
                f'margin:4px 0;font-size:.86rem;color:#63171B;border-left:3px solid #FC8181;">'
                f'⚠️ {r}</div>', unsafe_allow_html=True)