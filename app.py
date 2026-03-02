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

# --- KONFIGURASI DASAR ---
st.set_page_config(page_title="ElectroNoob-less Architect", layout="wide")

# --- NAVIGASI MULTI-PAGE ---
page = st.sidebar.radio("Navigasi Sistem", 
    ["🏠 Dashboard Utama", "☀️ Modul Surya", "🌬️ Modul Angin & Reducer", "🧲 Desain AFG (N52)", "🔋 Manajemen Baterai"])

# --- SHARED STATE (INPUT BEBAN UTAMA) ---
st.sidebar.markdown("---")
st.sidebar.header("🎯 Target Sistem")
load_watt = st.sidebar.number_input("Total Beban (Watt)", min_value=1.0, value=200.0)
daily_hours = st.sidebar.number_input("Jam Pakai/Hari", min_value=1, max_value=24, value=12)
sys_volt = st.sidebar.selectbox("Voltase Sistem (V)", [12, 24, 48])

# Hitungan Dasar Otonomi (5 Hari)
daily_energy_wh = load_watt * daily_hours
total_storage_needed_wh = daily_energy_wh * 5 

# --- 1. DASHBOARD UTAMA ---
if page == "🏠 Dashboard Utama":
    st.header("📊 Ringkasan Arsitektur Sistem")
    st.info("Sistem ini dirancang untuk ketahanan 5 hari tanpa input energi (Otonomi Penuh).")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Energi Harian", f"{daily_energy_wh} Wh")
        st.metric("Target Cadangan (5 Hari)", f"{total_storage_needed_wh / 1000:.2f} kWh")
    
    with col2:
        st.metric("Arus Sistem Puncak", f"{load_watt / sys_volt:.2f} A")
        st.write("**Status Kelayakan:**")
        if (load_watt / sys_volt) > 50:
            st.error("Arus terlalu tinggi untuk kabel standar. Disarankan naik ke 24V/48V.")
        else:
            st.success("Arus dalam batas aman untuk komponen standar.")

# --- 2. MODUL SURYA ---
elif page == "☀️ Modul Surya":
    st.header("☀️ Kalkulasi Panel Surya")
    sun_hours = st.number_input("Rata-rata Jam Matahari Terik", value=4.0)
    panel_watt = st.number_input("Kapasitas Per Panel (Wp)", value=100)
    
    # Logic: Panel harus bisa mengisi beban harian dalam waktu matahari terik
    required_panel_watt = daily_energy_wh / (sun_hours * 0.7) # 0.7 efisiensi sistem
    num_panels = math.ceil(required_panel_watt / panel_watt)
    
    st.subheader("Hasil Rekomendasi")
    st.write(f"Untuk menutup beban {daily_energy_wh} Wh/hari, Anda membutuhkan:")
    st.metric("Total Kapasitas Surya", f"{required_panel_watt:.1f} Wp")
    st.metric("Jumlah Panel", f"{num_panels} Unit (@{panel_watt}Wp)")

# --- 3. MODUL ANGIN & REDUCER ---
elif page == "🌬️ Modul Angin & Reducer":
    st.header("🌬️ Mekanis Turbin & Reducer")
    v_wind = st.number_input("Kecepatan Angin (m/s)", value=5.0)
    r_turbine = st.number_input("Jari-jari Bilah (m)", value=1.0)
    
    # Betz Limit & Efficiency
    p_wind = 0.5 * 1.225 * (math.pi * r_turbine**2) * v_wind**3 * 0.3 # 0.3 efisiensi nyata
    
    st.subheader("Gearbox / Reducer")
    pulley_ratio = st.number_input("Rasio Pulley (1:X)", value=3.0)
    rpm_turbine = (v_wind * 60) / (2 * math.pi * r_turbine) # Estimasi RPM dasar
    rpm_gen = rpm_turbine * pulley_ratio
    
    st.metric("Potensi Daya Angin", f"{p_wind:.1f} Watt")
    st.metric("RPM Generator (Output Reducer)", f"{int(rpm_gen)} RPM")
    
    if pulley_ratio > 5:
        st.warning("⚠️ Rasio terlalu tinggi dapat menyebabkan beban awal (cogging) terlalu berat.")

# --- 4. DESAIN AFG (N52) ---
elif page == "🧲 Desain AFG (N52)":
    st.header("🧲 Generator Axial Flux (N52)")
    st.write("Parameter magnet dikunci pada N52 (1.4 Tesla).")
    
    rpm_input = st.number_input("RPM Operasional (dari Reducer)", value=300)
    
    # Faraday Law: V = B * A * omega * N
    # Kita balik untuk cari N (Lilitan)
    b_field = 1.4
    area_coil = 0.0025 # m^2
    omega = (2 * math.pi * rpm_input) / 60
    
    if omega > 0:
        n_turns = math.ceil(sys_volt / (b_field * area_coil * omega))
    else:
        n_turns = 0
        
    st.metric("Jumlah Lilitan Per Koil", f"{n_turns} Lilitan")
    
    current_sys = load_watt / sys_volt
    wire_size = math.sqrt(current_sys / 5.0) # 5A/mm2 density
    st.metric("Rekomendasi Diameter Kawat", f"{wire_size:.2f} mm")

# --- 5. MANAJEMEN BATERAI ---
elif page == "🔋 Manajemen Baterai":
    st.header("🔋 Sistem Penyimpanan (5 Hari Otonom)")
    dod = st.slider("Depth of Discharge (%)", 10, 90, 80)
    
    capacity_ah = (total_storage_needed_wh) / (sys_volt * (dod/100))
    
    st.subheader("Spesifikasi Bank Baterai")
    st.metric("Total Kapasitas Dibutuhkan", f"{int(capacity_ah)} Ah")
    st.write(f"Kapasitas ini menjamin sistem menyala selama **5 hari** tanpa pengisian.")
    
    if capacity_ah > 1000:
        st.error("Kapasitas terlalu besar untuk baterai tunggal. Gunakan bank baterai paralel.")

st.sidebar.markdown("---")
st.sidebar.caption("ElectroNoob-less v2.0 | Engineering Mode")
