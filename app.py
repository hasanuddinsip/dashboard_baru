import streamlit as st
import pandas as pd

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="Dashboard Pegawai Badau",
    page_icon="📊",
    layout="wide"
)

# =========================
# BACA DATA
# =========================
FILE_EXCEL = "DATA PEG BADAU SETELAH AGUSTUS 2026.xlsx"

try:
    df = pd.read_excel(FILE_EXCEL)
except Exception as e:
    st.error(f"Gagal membaca file Excel: {e}")
    st.stop()

# =========================
# JUDUL
# =========================
st.title("📊 Dashboard Pegawai Badau")
st.caption("Dashboard SDM berbasis Streamlit")

# =========================
# FILTER
# =========================
st.sidebar.header("Filter")

if "UraianJabatan" in df.columns:
    daftar_jabatan = sorted(df["UraianJabatan"].dropna().unique())
    jabatan_pilih = st.sidebar.multiselect(
        "Pilih Jabatan",
        daftar_jabatan,
        default=daftar_jabatan
    )

    df = df[df["UraianJabatan"].isin(jabatan_pilih)]

# =========================
# KPI
# =========================
total_pegawai = len(df)

jumlah_pangkat = (
    df["UraianPangkat"].nunique()
    if "UraianPangkat" in df.columns
    else 0
)

jumlah_jabatan = (
    df["UraianJabatan"].nunique()
    if "UraianJabatan" in df.columns
    else 0
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "👥 Total Pegawai",
    total_pegawai
)

col2.metric(
    "🎖 Jumlah Pangkat",
    jumlah_pangkat
)

col3.metric(
    "💼 Jumlah Jabatan",
    jumlah_jabatan
)

st.divider()

# =========================
# GRAFIK
# =========================
kiri, kanan = st.columns(2)

with kiri:
    st.subheader("Distribusi Pangkat")

    if "UraianPangkat" in df.columns:
        pangkat = df["UraianPangkat"].value_counts()
        st.bar_chart(pangkat)

with kanan:
    st.subheader("Distribusi Jabatan")

    if "UraianJabatan" in df.columns:
        jabatan = df["UraianJabatan"].value_counts()
        st.bar_chart(jabatan)

st.divider()

# =========================
# PENCARIAN PEGAWAI
# =========================
st.subheader("🔍 Cari Pegawai")

keyword = st.text_input(
    "Masukkan nama pegawai"
)

if keyword:
    hasil = df[
        df["NmPegawai"]
        .astype(str)
        .str.contains(keyword,
                      case=False,
                      na=False)
    ]

    st.write(
        f"Ditemukan {len(hasil)} pegawai"
    )

    st.dataframe(
        hasil,
        use_container_width=True
    )

st.divider()

# =========================
# AI SEDERHANA GRATIS
# =========================
st.subheader("🤖 AI Pegawai")

pertanyaan = st.text_input(
    "Contoh: berapa jumlah pegawai?"
)

if pertanyaan:

    q = pertanyaan.lower()

    if "jumlah pegawai" in q:
        st.success(
            f"Jumlah pegawai saat ini adalah {len(df)} orang."
        )

    elif "pegawai tertua" in q:

        if "Unnamed: 4" in df.columns:

            st.info(
                "Silakan cek kolom umur (Unnamed: 4) pada tabel."
            )

    elif "pangkat terbanyak" in q:

        top = (
            df["UraianPangkat"]
            .value_counts()
            .idxmax()
        )

        jml = (
            df["UraianPangkat"]
            .value_counts()
            .max()
        )

        st.success(
            f"Pangkat terbanyak adalah {top} sebanyak {jml} pegawai."
        )

    elif "jabatan terbanyak" in q:

        top = (
            df["UraianJabatan"]
            .value_counts()
            .idxmax()
        )

        jml = (
            df["UraianJabatan"]
            .value_counts()
            .max()
        )

        st.success(
            f"Jabatan terbanyak adalah {top} sebanyak {jml} pegawai."
        )

    else:

        st.warning(
            "Pertanyaan belum dikenali. Coba:\n"
            "- berapa jumlah pegawai\n"
            "- pangkat terbanyak\n"
            "- jabatan terbanyak"
        )

st.divider()

# =========================
# DATA LENGKAP
# =========================
st.subheader("📋 Data Pegawai")

st.dataframe(
    df,
    use_container_width=True,
    height=500
)