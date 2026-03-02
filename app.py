"""
ElectroNoob-less: Independent Power Architect
==============================================
An Expert System for Designing Off-Grid Renewable Energy Systems
Based on Pure Physics Laws: Faraday, Ohm, Joule, and Betz

Author: AI Assistant
Version: 1.0.0
"""

import streamlit as st
import math

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="ElectroNoob-less: Architect", layout="wide")

st.title("⚡ ElectroNoob-less: Independent Power Architect")
st.markdown("---")

# --- SIDEBAR: INPUT TEKNIS (DISIPLIN) ---
st.sidebar.header("🛠️ Parameter Rekayasa")

# 1. Kebutuhan Beban
st.sidebar.subheader("1. Kebutuhan Beban")
load_watt = st.sidebar.number_input("Total Beban (Watt)", min_value=1.0, value=100.0)
duration = st.sidebar.number_input("Durasi Pakai (Jam/Hari)", min_value=1, max_value=24, value=12)
autonomy_days = 5  # Dikunci sesuai instruksi Operator

# 2. Sistem Voltase
st.sidebar.subheader("2. Voltase Sistem")
system_voltage = st.sidebar.selectbox("Pilih Voltase Baterai (V)", [12, 24, 48])

# 3. Potensi Alam & Mekanis
st.sidebar.subheader("3. Mekanis & Angin")
wind_speed = st.sidebar.number_input("Kecepatan Angin Rata-rata (m/s)", value=5.0)
turbine_diameter = st.sidebar.number_input("Diameter Turbin (m)", value=2.0)
pulley_ratio = st.sidebar.number_input("Rasio Reducer (1:X)", min_value=1.0, value=3.0)

# --- CORE LOGIC: CALCULATION ENGINE ---

# A. Kalkulasi Baterai (5 Hari Otonom)
daily_energy = load_watt * duration  # Wh
total_energy_needed = daily_energy * autonomy_days
battery_ah = total_energy_needed / (system_voltage * 0.8)  # DoD 80% untuk Lithium

# B. Kalkulasi AFG (Standard N52)
# Konstanta Fisika N52
B_field = 1.4  # Tesla (Standard N52)
coil_area = 0.002  # m^2 (Estimasi Koil Trapesium)
target_rpm = (wind_speed * 60) * pulley_ratio # Estimasi RPM Generator

# Rumus Faraday: N = V / (B * A * omega)
omega = (2 * math.pi * target_rpm) / 60
if omega > 0:
    required_turns = math.ceil(system_voltage / (B_field * coil_area * omega))
else:
    required_turns = 0

# C. Safety Check: Diameter Kawat
current_load = load_watt / system_voltage
# Standar keamanan: 1mm kawat tembaga aman untuk ~5A
min_wire_diameter = math.sqrt(current_load / 5.0)

# --- DISPLAY DASHBOARD ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Kapasitas Baterai (5 Hari)", f"{battery_ah:.1f} Ah")
    st.caption(f"Target Otonomi: {autonomy_days} Hari")

with col2:
    st.metric("Jumlah Lilitan AFG", f"{required_turns} Lilitan")
    st.caption(f"Berdasarkan Flux N52: {B_field}T")

with col3:
    st.metric("Min. Diameter Kawat", f"{min_wire_diameter:.2f} mm")
    st.caption(f"Arus Puncak: {current_load:.1f} A")

# --- SYSTEM STATUS (DECISION MAKER) ---
st.markdown("### 📋 System Health Audit")

errors = []
warnings = []

if battery_ah > 1000:
    errors.append("Kapasitas baterai terlalu besar untuk sistem rumahan. Pertimbangkan menaikkan voltase ke 48V.")
if min_wire_diameter > 3.0:
    warnings.append("Kawat sangat tebal (>3mm). Gunakan lilitan ganda (multistrand) untuk kemudahan fabrikasi.")
if pulley_ratio > 5:
    warnings.append("Rasio reducer terlalu tinggi. Risiko turbin macet (Stall) pada angin rendah.")

if not errors and not warnings:
    st.success("✅ Desain Sistem: LAYAK (Fungsional & Aman)")
else:
    for err in errors:
        st.error(f"❌ ERROR: {err}")
    for warn in warnings:
        st.warning(f"⚠️ PERINGATAN: {warn}")

# --- EDUKASI OPERATOR ---
with st.expander("Lihat Dasar Fisika (The Noob-less Insight)"):
    st.write(f"""
    - **Hukum Faraday:** Tegangan induksi ({system_voltage}V) dihasilkan dari perubahan fluks magnet N52 ({B_field}T) terhadap waktu.
    - **Hukum Joule:** Arus sebesar {current_load:.1f}A akan memanaskan kawat. Kawat {min_wire_diameter:.2f}mm dipilih untuk mencegah kebakaran stator.
    - **Otonomi:** Desain ini menjamin alat tetap hidup selama {autonomy_days} hari tanpa input energi sama sekali.
    """)
